# Soften the hard stop at the end of an English loanword (e.g. Desktop → "ท็อป" that sounds too clipped).
# Finds every occurrence with Whisper word timestamps, then fades the last FADE s of the word's final voiced
# stretch (qsin curve) and ramps back in over 8 ms. Timing is unchanged, so vo.timing.json stays valid.
# Owner-approved for Desktop (2026-10-26, "E": TTS spelling เดสท็อป + 0.08 s soft tail).
#   HF_HUB_OFFLINE=1 python soften_word.py IN.wav OUT.wav [--match desk] [--fade 0.08]
import argparse, re, numpy as np, soundfile as sf, librosa, mlx_whisper

ap = argparse.ArgumentParser()
ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--match', default=r'desk\s*top|เดส.{0,3}ท็?อ[ปบ]|ด.ส.{0,4}ท็?อ[ปบ]',
                help='regex over the joined Whisper text (Thai comes back one character per "word")')
ap.add_argument('--fade', type=float, default=0.08)
a = ap.parse_args()

y, sr = sf.read(a.inp, always_2d=True)
mono = y.mean(axis=1)
y16 = librosa.resample(mono, orig_sr=sr, target_sr=16000)
r = mlx_whisper.transcribe(y16.astype(np.float32), path_or_hf_repo='mlx-community/whisper-large-v3-turbo',
                           language='th', word_timestamps=True)
toks = [w for s in r['segments'] for w in s.get('words', [])]
text, owner = '', []                                          # joined text + which token owns each character
for i, w in enumerate(toks):
    text += w['word'].lower(); owner += [i] * len(w['word'])
words = []
for m in re.finditer(a.match, text):
    t0, t1 = toks[owner[m.start()]], toks[owner[m.end() - 1]]
    words.append({'word': m.group(0), 'start': t0['start'], 'end': t1['end']})

hop = int(.005 * sr)
gain = np.ones(len(mono))
for w in words:
    s0, s1 = int(w['start'] * sr), min(len(mono), int((w['end'] + .25) * sr))
    rms = librosa.feature.rms(y=mono[s0:s1], frame_length=int(.02 * sr), hop_length=hop)[0]
    quiet = rms < .10 * rms.max()                              # vowel offset = start of the first >=30 ms gap after
    run, need = 0, int(.03 * sr / hop)                          # Whisper's word end (it lands just before the last
    k0 = max(0, int((w['end'] - w['start'] - .05) * sr / hop))   # vowel ends; skips the desk|top closure);
    for k in range(k0, len(quiet)):                             # never reaches into the next word
        run = run + 1 if quiet[k] else 0
        if run == need: break
    e = s0 + int((k - need + 1) * hop + .01 * sr)
    f = int(a.fade * sr); back = int(.008 * sr)
    f0 = e - int(.030 * sr)                                     # start just before the vowel offset: the fade covers
    gain[f0:f0 + f] = np.cos(np.linspace(0, np.pi / 2, f))      # the hard stop after it (qsin-style), as in "E"
    gain[f0 + f:f0 + f + back] = np.linspace(0, 1, back)
    print(f"{w['word'].strip():12s} {w['start']:7.2f}-{w['end']:6.2f}s  softened {f0 / sr:.3f}-{(f0 + f) / sr:.3f}s")
sf.write(a.out, y * gain[:, None], sr, subtype='PCM_16' if sf.info(a.inp).subtype == 'PCM_16' else sf.info(a.inp).subtype)
print(f'{len(words)} word(s) softened -> {a.out}')
