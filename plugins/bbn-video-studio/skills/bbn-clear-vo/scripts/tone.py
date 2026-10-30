# Pitch contour of given syllables in a VO, to check Thai tones Whisper can't hear.
# Finds each target via Whisper char timestamps, prints F0 (semitones vs the speaker median) at 5 points.
#   HF_HUB_OFFLINE=1 ~/.venvs/blender-explainer/bin/python vo/tone.py vo.wav ซี ว่า ต่อ
import sys, numpy as np, soundfile as sf, librosa, mlx_whisper
f, targets = sys.argv[1], sys.argv[2:]
y, sr = sf.read(f); y = y if y.ndim == 1 else y.mean(1)
f0, v, _ = librosa.pyin(y, fmin=60, fmax=320, sr=sr, frame_length=2048, hop_length=sr // 200)
med = np.nanmedian(f0[v])
r = mlx_whisper.transcribe(f, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='th', word_timestamps=True,
                           initial_prompt=None)
chars, ts = '', []
for s in r['segments']:
    for w in s['words']:
        cs = w['word']; d = (w['end'] - w['start']) / max(1, len(cs))
        for k, c in enumerate(cs): chars += c; ts.append((w['start'] + d * k, w['start'] + d * (k + 1)))
print('transcript:', chars)
for t in targets:
    i = chars.find(t)
    while i >= 0:
        a, b = ts[i][0], ts[i + len(t) - 1][1]
        if t in ('ซี',) and chars[i - 1:i] in ('ม', 'บ'): pass
        seg = f0[int(a * 200):int(b * 200) + 1]; vv = v[int(a * 200):int(b * 200) + 1]
        st = 12 * np.log2(seg[vv] / med) if vv.any() else np.array([])
        pts = ' '.join(f'{x:+.1f}' for x in st[np.linspace(0, len(st) - 1, 5).astype(int)]) if len(st) >= 3 else 'n/a'
        print(f"{t:4s} {a:6.2f}-{b:5.2f}s  ctx '{chars[max(0, i - 6):i + len(t) + 6]}'  F0 st: {pts}")
        i = chars.find(t, i + 1)
