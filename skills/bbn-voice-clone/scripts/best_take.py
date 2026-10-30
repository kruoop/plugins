"""One WAV per script line, best take kept: for video narration where each line is placed on its own.

Each line is generated, breath-cleaned and checked by the Thai ASR. A take is accepted when the check passes and the
voice did not add a particle the script does not have (ครับ, นะครับ, เนี่ย, ค่ะ, น่ะ — the clone picks them up from
the reference's speaking style). Otherwise the next seed is tried; after the last seed the closest take is kept and
reported for listening. Same text + same seed always gives the same take, so a retake needs a new seed.

  <PYTHON> best_take.py --text-file lines.txt --out-dir DIR [--seeds 42,7,11,23] [--kit KIT]
  <PYTHON> best_take.py ... --engine voxcpm --voxcpm-python ~/.venvs/bbn-video-studio/bin/python

lines.txt: one clip per line, `id|ข้อความ` or just `ข้อความ` (ids become line-001, line-002, ...).
Writes DIR/<id>.wav, every take under DIR/takes/ (OmniVoice takes keep their engine .json), and DIR/report.json.
"""
import argparse
import json
import re
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import soundfile as sf

from clone import load_kit
from voice_engine import synthesize, validate_settings
from voice_quality import ThaiChecker, analyze_phrase, clean_breaths, normalized

PARTICLES = ('นะครับ', 'ครับ', 'เนี่ย', 'ค่ะ', 'คะ', 'น่ะ', 'เอ่อ')

# VoxCPM2 (Apache-2.0) clones timbre from the reference only. Its prompt/continuation mode was tried and leaked the
# reference's own words ("ซึ่งในวันนี้นะครับ…") and garbled short lines, so it is not offered.
VOXCPM = r'''
import json, os, sys
os.environ.setdefault('VOXCPM_MPS_DTYPE', 'float32')
import soundfile as sf, torch
from voxcpm import VoxCPM
jobs = json.load(open(sys.argv[1]))
model = VoxCPM.from_pretrained(os.environ.get('VOXCPM_MODEL', 'openbmb/VoxCPM2'), load_denoiser=False, optimize=False)
for job in jobs:
    torch.manual_seed(job['seed'])
    audio = model.generate(text=job['text'], reference_wav_path=job['reference'], cfg_value=2.0,
                           inference_timesteps=10, normalize=False, denoise=False, retry_badcase=True, max_len=4096)
    sf.write(job['out'], audio, model.tts_model.sample_rate, subtype='PCM_16')
    print('DONE', job['out'], flush=True)
'''


def read_lines(path):
    rows = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line:
            continue
        key, sep, text = line.partition('|')
        rows.append((key.strip(), text.strip()) if sep else (f'line-{len(rows) + 1:03d}', line))
    ids = [key for key, _ in rows]
    if len(set(ids)) != len(ids) or any(not key.replace('-', '').replace('_', '').isalnum() for key in ids):
        raise SystemExit('ids must be unique and use letters, digits, - or _')
    return rows


def added_particles(text, heard):
    found, script, rest = [], normalized(text), normalized(heard)
    for word in PARTICLES:  # longest first, so นะครับ is not also counted as ครับ
        if rest.count(word) > script.count(word):
            found.append(word)
            rest = rest.replace(word, '')
    return found


def too_long(text, seconds):
    """A take far longer than its text can be spoken has run on (VoxCPM2 sometimes loops a word for seconds)."""
    return seconds > len(normalized(text)) / 6 + 1.5


LOOP = re.compile(r'(\S{2,}?)(?:\s*\1){2,}')


def strip_asr_loop(transcript):
    """Whisper-style ASR can loop on a word after an English term ("cross.md สินค้า สินค้า สินค้า …") although the
    audio has ended. Cut where one chunk of text repeats three times in a row; script lines never do that
    (ๆ means two). Word timestamps are syllable pieces, so the word list is cut at the same character count."""
    text = transcript.get('text', '')
    match = LOOP.search(text)
    if not match:
        return transcript
    keep = len(re.sub(r'\s', '', text[:match.start()]))
    kept, count = [], 0
    for word in (w for segment in transcript.get('segments', []) for w in segment.get('words', [])):
        count += len(re.sub(r'\s', '', word['word']))
        if count > keep:
            break
        kept.append(word)
    return {'text': text[:match.start()].rstrip(), 'segments': [{'words': kept}]}


def without_terms(text, transcript, ignore):
    """English terms written in Thai for the voice (คล็อดดอตเอ็มดี) come back from the ASR in Latin letters
    (cross.md, cloud.md …). Leave both sides out of the comparison so a correct take is not rejected."""
    for term in ignore:
        text = text.replace(term, ' ')
    words = [w for segment in transcript.get('segments', []) for w in segment.get('words', [])
             if not re.fullmatch(r'[\sA-Za-z0-9._\-]+', w['word'])]
    return ' '.join(text.split()), {'text': ''.join(w['word'] for w in words), 'segments': [{'words': words}]}


def verdict(text, audio, sample_rate, checker, ignore=()):
    seconds = len(audio) / sample_rate
    transcript = strip_asr_loop(checker(audio, sample_rate))
    heard = transcript['text']
    if ignore:
        text, transcript = without_terms(text, transcript, ignore)
    check = analyze_phrase(text, transcript, seconds)
    check['heard'] = heard
    extra = added_particles(text, check['heard'])
    flags = check['flags'] + (['ยาวผิดปกติ (พูดวนต่อท้าย)'] if too_long(text, seconds) else [])
    return {'passed': not check['needs_repair'] and not extra and not too_long(text, seconds), 'flags': flags,
            'added': extra, 'score': check['score'] + (1 if too_long(text, seconds) else 0), 'heard': check['heard']}


def omnivoice_take(kit, profile, settings, text, seed, out, lead):
    synthesize(str(kit / profile['reference']), profile['reference_text'], text, str(out),
               kit / profile['model']['path'], {**settings, 'seed': seed}, drop_lead_filler=lead)


def voxcpm_takes(python, reference, jobs):
    with tempfile.TemporaryDirectory() as tmp:
        spec, code = Path(tmp) / 'jobs.json', Path(tmp) / 'gen.py'
        spec.write_text(json.dumps([{**job, 'reference': str(reference)} for job in jobs], ensure_ascii=False))
        code.write_text(VOXCPM)
        subprocess.run([str(python), str(code), str(spec)], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--kit', type=Path)
    parser.add_argument('--profile', type=Path)
    parser.add_argument('--text-file', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--seeds', default='42,7,11,23')
    parser.add_argument('--engine', choices=('omnivoice', 'voxcpm'), default='omnivoice')
    parser.add_argument('--voxcpm-python', type=Path, help='A Python with voxcpm installed (engine voxcpm)')
    parser.add_argument('--keep-lead', action='store_true', help='Do not drop a sound+inhale at a line start')
    parser.add_argument('--ignore', action='append', default=[], metavar='THAI_SPELLING',
                        help='A Thai-spelled English term the ASR writes in Latin letters (repeatable), e.g. คล็อดดอตเอ็มดี')
    args = parser.parse_args()
    seeds = [int(seed) for seed in args.seeds.split(',')]
    rows = read_lines(args.text_file)
    kit, profile = load_kit(args.kit, args.profile)
    settings = dict(profile['settings'])
    validate_settings(settings)
    if args.engine == 'voxcpm' and not (args.voxcpm_python and args.voxcpm_python.exists()):
        parser.error('--engine voxcpm needs --voxcpm-python pointing to a Python with voxcpm installed')
    takes_dir = args.out_dir / 'takes'
    takes_dir.mkdir(parents=True, exist_ok=True)
    os.environ['HF_HUB_OFFLINE'] = '1' if args.engine == 'omnivoice' else os.environ.get('HF_HUB_OFFLINE', '0')
    checker = ThaiChecker((kit / profile['model']['path']).parent / 'typhoon-asr')
    # OmniVoice already drops a leading filler+inhale; VoxCPM2 has no such habit, so its starts are kept.
    lead = not args.keep_lead and args.engine == 'omnivoice'
    results = {key: [] for key, _ in rows}
    pending = list(rows)
    for seed in seeds:
        if not pending:
            break
        if args.engine == 'voxcpm':
            jobs = [{'text': text, 'seed': seed, 'out': str(takes_dir / f'{key}_s{seed}.raw.wav')}
                    for key, text in pending if not (takes_dir / f'{key}_s{seed}.wav').exists()]
            if jobs:
                voxcpm_takes(args.voxcpm_python, kit / profile['reference'], jobs)
        still = []
        for key, text in pending:
            out = takes_dir / f'{key}_s{seed}.wav'
            if args.engine == 'omnivoice':
                if not out.exists():
                    omnivoice_take(kit, profile, settings, text, seed, out, lead)
                audio, sample_rate = sf.read(out, dtype='float32')
            else:
                raw = out.with_suffix('.raw.wav')
                if not out.exists():
                    audio, sample_rate = sf.read(raw, dtype='float32')
                    audio, _ = clean_breaths(audio if audio.ndim == 1 else audio.mean(1), sample_rate, drop_lead=lead)
                    sf.write(out, audio, sample_rate, subtype='PCM_16')
                    raw.unlink(missing_ok=True)
                audio, sample_rate = sf.read(out, dtype='float32')
            result = {'seed': seed, 'file': str(out), **verdict(text, audio, sample_rate, checker, args.ignore)}
            results[key].append(result)
            print(f"{key:12} seed {seed:<6} {'ok' if result['passed'] else 'retry'} "
                  f"score {result['score']:.2f} {' '.join(result['added'])} | {result['heard']}", flush=True)
            if not result['passed']:
                still.append((key, text))
        pending = still
    report = {}
    for key, text in rows:
        # score is the ASR mismatch (lower = closer to the script)
        best = next((r for r in results[key] if r['passed']), None) or min(results[key], key=lambda r: r['score'] + .2 * len(r['added']))
        shutil.copyfile(best['file'], args.out_dir / f'{key}.wav')
        report[key] = {'text': text, 'chosen': best, 'tried': results[key], 'needs_listening': not best['passed']}
    (args.out_dir / 'report.json').write_text(json.dumps({'engine': args.engine, 'lines': report}, ensure_ascii=False, indent=2))
    review = [key for key, row in report.items() if row['needs_listening']]
    print('ต้องฟังทวน: ' + ', '.join(review) if review else 'ผ่านทุกบรรทัด (ยังไม่ใช่การฟังด้วยหู)')
    print((args.out_dir / 'report.json').resolve())


if __name__ == '__main__':
    main()
