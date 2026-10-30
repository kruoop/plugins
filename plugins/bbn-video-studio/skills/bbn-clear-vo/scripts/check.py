# Per-line clarity: Whisper (no hints) on every chunk of each paragraph's latest take vs the TTS text.
#   HF_HUB_OFFLINE=1 ~/.venvs/blender-explainer/bin/python check.py [vo/takes]
# Score = Thai letters only, tone marks ignored. English names come back in Latin and digits as numerals -> low score
# there is a false alarm; read the "got" text. Garbled Thai, a dropped word, or a wrong number is real.
import difflib, glob, json, os, re, sys, numpy as np, soundfile as sf, mlx_whisper
d = sys.argv[1] if len(sys.argv) > 1 else 'vo/takes'
thai = lambda s: ''.join(c for c in s if 'ก' <= c <= '๛' and c not in 'ๆ่้๊๋์')
ids = [l.strip()[1:-1] for l in open('vo/script_asm.txt', encoding='utf-8') if l.startswith('[')]
for i in ids:
    f = sorted(glob.glob(f'{d}/{i}-1_?.wav'))[-1]
    y, sr = sf.read(f)
    for c in json.load(open(f[:-4] + '.json'))['chunks']:
        sf.write('/tmp/_check.wav', np.concatenate([np.zeros(sr // 4), y[int(c['start'] * sr):int(c['end'] * sr)], np.zeros(sr // 4)]), sr)
        got = mlx_whisper.transcribe('/tmp/_check.wav', path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='th')['text'].strip()
        r = difflib.SequenceMatcher(None, thai(c['text']), thai(got), autojunk=False).ratio()
        flag = '  ' if r >= .97 else '~ ' if re.search(r'[A-Za-z0-9]', got) else '??'  # ~ = names/digits in Latin: read it yourself
        print(f"{flag} {r:.2f} {os.path.basename(f)[:-4]:8s} {c['text']}\n                 -> {got}", flush=True)
