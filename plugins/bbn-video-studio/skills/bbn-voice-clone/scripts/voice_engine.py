"""Read long Thai text in short phrases, with one shared voice reference."""
import json
import difflib
import hashlib
import math
import os
import re
import subprocess
import shutil
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from mlx_audio.tts.models.omnivoice.duration import RuleDurationEstimator
from pythainlp import word_tokenize
from voice_quality import ThaiChecker, analyze_phrase, clean_breaths, normalized, remove_intervals, silence_cuts



def lower_pitch_file(source: Path, target: Path, pitch_semitones: float) -> None:
    info = sf.info(source)
    ratio = 2 ** (pitch_semitones / 12)
    subprocess.run([
        shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(source),
        '-af', f'asetrate={info.samplerate * ratio:.8f},aresample={info.samplerate},atempo={1 / ratio:.8f},apad,atrim=end_sample={info.frames}',
        '-c:a', 'pcm_s16le', str(target),
    ], check=True, capture_output=True, timeout=300)


def split_text(text: str, max_weight: float = float('inf')) -> list[str]:
    estimator = RuleDurationEstimator()
    chunks = []
    for paragraph in text.splitlines():
        buffer = ''
        for token in word_tokenize(paragraph, engine='newmm', keep_whitespace=True):
            if len(token) > 120 or estimator.calculate_total_weight(token) > max_weight:
                raise ValueError('คำหรือรหัสยาวเกินช่วงอ่าน กรุณาเว้นวรรคหรือเขียนเป็นคำอ่าน')
            candidate = buffer + token
            if buffer.strip() and (len(candidate) > 120 or estimator.calculate_total_weight(candidate) > max_weight):
                chunks.append(buffer.strip())
                buffer = ''
            buffer += token
            if token in ('.', '!', '?', '。', '！', '？') and buffer.strip():
                chunks.append(buffer.strip())
                buffer = ''
        if buffer.strip():
            chunks.append(buffer.strip())
    return chunks


def phrase_pauses(text: str, chunks: list[str], settings: dict) -> list[float]:
    pauses = []
    cursor = 0
    for index, chunk in enumerate(chunks):
        start = text.find(chunk, cursor)
        if start < 0:
            raise ValueError('Phrase does not match source text')
        separator = text[cursor:start]
        if index == 0:
            pause = 0.0
        elif re.search(r'\n\s*\n', separator):
            pause = settings['pause_paragraph']
        elif chunk.startswith(('ข่าวแรก', 'ข่าวที่', 'นี่คือสรุป')):
            pause = settings['pause_topic']
        elif '\n' in separator or chunks[index - 1].endswith(('ครับ', 'ค่ะ', 'คะ', '.', '!', '?', '。')):
            pause = settings['pause_sentence']
        else:
            pause = settings['pause_phrase']
        pauses.append(pause * settings['pause_scale'])
        cursor = start + len(chunk)
    return pauses


def repair_chunks(text, analysis, seconds_per_weight):
    estimator = RuleDurationEstimator()
    prefix = ''
    expected, heard = normalized(text), analysis.get('cleaned_text', '')
    opcodes = difflib.SequenceMatcher(None, expected, heard, autojunk=False).get_opcodes()
    if len(text) >= 20 and opcodes and opcodes[0][0] == 'delete' and opcodes[0][1] == 0 and opcodes[0][2] >= 4:
        missing = opcodes[0][2]
        boundary = 0
        for token in word_tokenize(text, engine='newmm', keep_whitespace=True):
            boundary += len(token)
            if len(normalized(text[:boundary])) >= missing:
                break
        if boundary < 12:
            boundary = text.find(' ', boundary) if ' ' in text[boundary:] else len(text)
        prefix, text = text[:boundary].strip(), text[boundary:].strip()
    fragments = re.split(r'\s+', text) if text else []
    children = [prefix] if prefix else []
    for fragment in fragments:
        if fragment == 'ๆ' and children:
            children[-1] += ' ๆ'
            continue
        try:
            pieces = split_text(fragment, max_weight=3.2 / seconds_per_weight)
        except ValueError:
            pieces = [fragment]
        for piece in pieces:
            if children and children[-1] != prefix and estimator.calculate_total_weight(piece) * seconds_per_weight < 1.4:
                children[-1] += ' ' + piece
            else:
                children.append(piece)
    return children or [text]


def synthesize(reference: str, reference_text: str, text: str, output: str, model_path: Path, settings: dict,
               breath_cleanup: bool = True, drop_lead_filler: bool = True) -> None:
    import mlx.core as mx
    from mlx_audio.tts.models.omnivoice.utils import create_voice_clone_prompt
    from mlx_audio.tts.utils import load_model

    validate_settings(settings)
    if not text.strip() or len(text) > 5000:
        raise ValueError("Use 1-5000 characters")
    estimator = RuleDurationEstimator()
    mx.set_cache_limit(256 * 1024 * 1024)
    reference_duration = sf.info(reference).duration
    reference_weight = estimator.calculate_total_weight(reference_text)
    if reference_weight <= 0 or not 2 <= reference_duration <= 8.01:
        raise ValueError('Invalid prepared reference or transcript')
    # shortcut: estimate pace from reference phonetic weights; difficult names may need Thai spelling.
    seconds_per_weight = reference_duration / reference_weight * settings['pace_factor']
    chunks = split_text(text, max_weight=10 / seconds_per_weight)
    if not chunks:
        raise ValueError('Empty script')
    pauses = phrase_pauses(text, chunks, settings)
    checker = ThaiChecker(model_path.parent / 'typhoon-asr')
    model = None
    ref_tokens = None
    destination = Path(output)
    parts = destination.with_suffix('')
    parts.mkdir(exist_ok=True)
    reference_hash = hashlib.sha256(Path(reference).read_bytes()).hexdigest()
    temporary = destination.with_suffix('.tmp.wav')
    shifted = destination.with_suffix('.pitch.wav')
    manifest = []
    quality_details = []

    def generate_part(chunk, label, seed):
        nonlocal model, ref_tokens
        duration = math.ceil(max(1.2, estimator.calculate_total_weight(chunk) * seconds_per_weight) * 25) / 25
        weights = model_path / 'model.safetensors'
        identity = f'{model_path.resolve()}:{weights.stat().st_size}:{weights.stat().st_mtime_ns}'
        fingerprint = hashlib.sha256(f'{identity}|{reference_hash}|{reference_text}|{chunk}|{duration}|{settings["steps"]}|{settings["guidance"]}|{seed}'.encode()).hexdigest()[:12]
        part = parts / f'{label}-{fingerprint}.wav'
        if part.exists():
            audio, sample_rate = sf.read(part, dtype='float32')
        else:
            if model is None:
                model = load_model(model_path)
                ref_tokens = create_voice_clone_prompt(reference, tokenizer=model.audio_tokenizer, max_duration_s=8)
            mx.random.seed(seed)
            result = next(model.generate(text=chunk, language='th', ref_tokens=ref_tokens,
                          ref_text=reference_text, duration_s=duration, num_steps=settings['steps'],
                          guidance_scale=settings['guidance']))
            audio = np.asarray(result.audio, dtype=np.float32).squeeze().copy()
            sample_rate = result.sample_rate
        if sample_rate != 24000 or audio.ndim != 1 or not len(audio) or not np.isfinite(audio).all() or np.max(np.abs(audio)) <= .001:
            raise RuntimeError(f'Invalid generated audio at phrase {label}')
        if not part.exists():
            sf.write(part, audio, sample_rate, subtype='FLOAT')
        return audio, duration

    try:
        with sf.SoundFile(temporary, 'w', samplerate=24000, channels=1, subtype='PCM_16') as joined:
            for index, chunk in enumerate(chunks):
                audio, duration = generate_part(chunk, f'{index:03d}', settings['seed'])
                breath = None
                if breath_cleanup:  # before ASR: a word cut by mistake is then caught as missing and repaired
                    audio, breath = clean_breaths(audio, 24000, drop_lead_filler)
                print(f'PHRASE {index + 1}/{len(chunks)}', flush=True)
                print(f'VERIFY {index + 1}/{len(chunks)}', flush=True)
                original_check = analyze_phrase(chunk, checker(audio, 24000), len(audio) / 24000)
                check = original_check
                cleaned = remove_intervals(audio, 24000, check['cuts'])
                detail = {'text': chunk, 'initial': original_check, 'repairs': [], 'selected': 'initial', 'breath': breath}
                if check['needs_repair']:
                    print(f'REPAIR {index + 1}/{len(chunks)}', flush=True)
                    repaired, checks = [], []
                    children = repair_chunks(chunk, check, seconds_per_weight)
                    for child_index, child in enumerate(children):
                        candidate, _ = generate_part(child, f'{index:03d}-repair{child_index}', settings['seed'] + 1 if len(children) == 1 else settings['seed'])
                        if breath_cleanup:  # no lead cut here: a repair often restores exactly that first word
                            candidate, _ = clean_breaths(candidate, 24000, drop_lead=False)
                        child_check = analyze_phrase(child, checker(candidate, 24000), len(candidate) / 24000)
                        checks.append(child_check)
                        repaired.extend([remove_intervals(candidate, 24000, child_check['cuts']), np.zeros(1920, dtype=np.float32)])
                    detail['repairs'] = [{'text': child, **row} for child, row in zip(children, checks)]
                    if checks and (all(not row['needs_repair'] for row in checks) or np.mean([row['score'] for row in checks]) < check['score']):
                        cleaned = np.concatenate(repaired[:-1])
                        check = {'needs_repair': any(row['needs_repair'] for row in checks),
                                 'flags': [flag for row in checks for flag in row['flags']],
                                 'cuts': [cut for row in checks for cut in row['cuts']]}
                        detail['selected'] = 'repair'
                detail['needs_review'] = check['needs_repair']
                detail['flags'] = check['flags']
                quality_details.append(detail)
                audio = cleaned
                fade = min(120, len(audio) // 2)
                audio[:fade] *= np.linspace(0, 1, fade)
                audio[-fade:] *= np.linspace(1, 0, fade)
                if pauses[index]:
                    joined.write(np.zeros(round(pauses[index] * 24000), dtype=np.float32))
                start = joined.tell() / 24000
                joined.write(audio)
                manifest.append({'text':chunk, 'start':start, 'end':joined.tell() / 24000, 'duration_control':duration, 'pause_before':pauses[index]})
                mx.clear_cache()
        model = None
        ref_tokens = None
        mx.clear_cache()
        print('CLEANUP ตัดคำแทรก คำซ้ำ และเดดแอร์', flush=True)
        lower_pitch_file(temporary, shifted, settings['pitch_semitones'])
        audio, sample_rate = sf.read(shifted, dtype='float32')
        scan = subprocess.run([shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg', '-hide_banner', '-nostdin', '-i', str(shifted), '-af', 'silencedetect=noise=-45dB:d=0.15', '-f', 'null', '-'], check=True, capture_output=True, text=True, timeout=300)
        quiet = silence_cuts(scan.stderr, len(audio) / sample_rate)
        sf.write(shifted, remove_intervals(audio, sample_rate, quiet), sample_rate, subtype='PCM_16')
        for row in manifest:
            for key in ('start', 'end'):
                before = row[key]
                row['before_silence_trim_' + key] = before
                row[key] = before - sum(max(0, min(before, cut['end']) - cut['start']) for cut in quiet)
        flags = [f'ช่วง {i + 1}: {flag}' for i, row in enumerate(quality_details) for flag in row['flags']]
        quality = {'status': 'needs_review' if flags else 'passed', 'flags': flags, 'details': quality_details,
                   'silence_cuts': quiet, 'repair_round_limit': 1, 'human_listening': False,
                   'breath_cleanup': breath_cleanup, 'drop_lead_filler': breath_cleanup and drop_lead_filler}
        os.replace(shifted, destination)
        destination.with_suffix('.json').write_text(json.dumps({'chunks':manifest, 'sample_rate':24000, 'duration':sf.info(destination).duration, 'settings':settings, 'quality':quality},ensure_ascii=False,indent=2))
    finally:
        temporary.unlink(missing_ok=True)
        shifted.unlink(missing_ok=True)


def validate_settings(settings: dict) -> None:
    bounds = {'steps':(4,64),'guidance':(0,5),'seed':(0,2147483647),'pace_factor':(.7,1.15),'pitch_semitones':(-2,2),'pause_phrase':(0,2),'pause_sentence':(0,2),'pause_topic':(0,3),'pause_paragraph':(0,3),'pause_scale':(.5,1.5)}
    if set(settings) != set(bounds):
        raise ValueError('Settings have missing or unknown keys')
    for key,(low,high) in bounds.items():
        value=settings[key]
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not low<=value<=high:
            raise ValueError(f'Invalid {key}: expected {low}..{high}')
    if not isinstance(settings['steps'],int) or not isinstance(settings['seed'],int):
        raise ValueError('steps and seed must be integers')
