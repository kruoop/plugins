# Generate a take for every paragraph (or only the ids given) with the approved BBN voice: one seed, one pace for the whole VO.
#   python3 gen.py [p03 p07 ...]          (run from the episode folder; new take = next free letter: p03-1_b.wav ...)
import glob, json, os, string, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.environ.get('BBN_KIT') or json.load(open(os.path.expanduser('~/.codex/skills/bbn-voice-clone/assets/kit-location.json')))['kit']  # this Mac's kit
CLONE = os.environ.get('BBN_CLONE', os.path.expanduser('~/.codex/skills/bbn-voice-clone/scripts/clone.py'))
PROFILE = os.environ.get('PROFILE', os.path.join(HERE, '..', 'assets', 'profile.json'))
PACE = os.environ.get('PACE', '1.0')  # EP5 v6; 1.1 is clearer but slower — never mix paces inside one VO
os.makedirs('vo/takes', exist_ok=True)
ids = sys.argv[1:] or sorted(os.path.basename(f)[:-6] for f in glob.glob('vo/text/*-1.txt'))
for i in ids:
    have = glob.glob(f'vo/takes/{i}-1_?.wav')
    out = f'vo/takes/{i}-1_{string.ascii_lowercase[len(have)]}.wav'
    r = subprocess.run([f'{KIT}/.venv/bin/python', CLONE, '--kit', KIT, '--profile', PROFILE, '--text-file', f'vo/text/{i}-1.txt',
                        '--output', out, '--pace', PACE], capture_output=True, text=True)
    print(i, out if r.returncode == 0 else 'FAILED ' + r.stderr.strip().splitlines()[-1], flush=True)
