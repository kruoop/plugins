"""One command for the latest approved BBN narration (EP9 VO v1, 2026-10-16).

Script in the user's format (one phrase per line, blank line between thoughts, "-" syllable hints) -> finished VO:
lexicon spellings (TTS text only) -> one take per paragraph (profile_latest, seed 42, pace 1.0) -> Whisper clarity
check -> breath/filler cleanup, gaps .12/.26 s, x1.16 tempo, room tone.  Reuses the bbn-clear-vo scripts unchanged.

  python3 speak.py SCRIPT.txt OUT.wav [--work DIR]

Writes OUT.wav (48 kHz stereo), OUT.timing.json and OUT.check.txt (lines Whisper heard differently: read them
before sending; see bbn-clear-vo SKILL.md section 3 for fixes). The work folder keeps vo/text and vo/takes so a single
paragraph can be fixed and re-assembled (gen.py <id> then assemble.py).
"""
import argparse, os, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLEAR = Path(os.environ.get('BBN_CLEAR', Path.home() / '.claude/skills/bbn-clear-vo/scripts'))
PY_ASR = Path(os.environ.get('BBN_PY_ASR') or next((p for p in (Path.home() / '.venvs/blender-explainer/bin/python',
                                                     Path.home() / '.venvs/bbn-video-studio/bin/python') if p.exists()),
                                                    Path.home() / '.venvs/blender-explainer/bin/python'))          # librosa + mlx_whisper for check/assemble
FFMPEG_BIN = Path(os.environ.get('BBN_FFMPEG_BIN') or (Path.home() / '.local/share/bbn-ai-cut/bin' if (Path.home() / '.local/share/bbn-ai-cut/bin').exists()
                  else Path(shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg').parent))              # ffmpeg/ffprobe


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('script', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--work', type=Path, help='keep the takes here (default: a temp folder)')
    a = ap.parse_args()
    out = a.output.resolve()
    if out.exists():
        ap.error('Output exists; choose a new filename to preserve it')
    for need in (CLEAR / 'prep.py', PY_ASR):
        if not need.exists():
            sys.exit(f'missing {need} (bbn-clear-vo skill / ~/.venvs/blender-explainer)')
    work = (a.work or Path(tempfile.mkdtemp(prefix='bbn-vo-'))).resolve()
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy(a.script, work / 'script.txt')
    env = {**os.environ, 'BBN_CLONE': str(HERE / 'clone.py'), 'PATH': f'{FFMPEG_BIN}:{os.environ["PATH"]}', 'HF_HUB_OFFLINE': '1',
           'PROFILE': str(HERE.parent / 'assets/profile_latest.json'), 'PACE': '1.0'}
    run = lambda *cmd: subprocess.run([str(c) for c in cmd], cwd=work, env=env, check=True, capture_output=True, text=True).stdout
    print(run(sys.executable, CLEAR / 'prep.py', 'script.txt'), end='')
    gen = run(sys.executable, CLEAR / 'gen.py')
    print(gen, end='')
    if 'FAILED' in gen:
        sys.exit('a paragraph failed to generate; see above')
    check = run(PY_ASR, CLEAR / 'check.py')
    run(PY_ASR, CLEAR / 'assemble.py', 'vo/takes')
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(work / 'vo.wav', out)
    shutil.copy(work / 'vo.timing.json', out.with_suffix('.timing.json'))
    out.with_suffix('.check.txt').write_text(check, encoding='utf-8')
    flagged = [l for l in check.splitlines() if l.startswith('??')]
    print(out)
    print(f'work folder: {work}')
    print(f'{len(flagged)} line(s) Whisper heard differently -> {out.with_suffix(".check.txt")}')


if __name__ == '__main__':
    main()
