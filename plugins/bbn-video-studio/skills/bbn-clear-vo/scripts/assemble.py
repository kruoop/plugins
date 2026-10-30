# Join the paragraph takes into one VO: split at the engine's chunk times, strip breaths/fillers, lay out with the approved gaps, speed up.
# Run from the episode folder -> ./vo.wav + ./vo.timing.json. Defaults = EP5 v6 (approved 2026-10-16).
#   $PY assemble.py vo/takes        (each paragraph's latest take: <id>-1_a, _b, ...; order from vo/script_asm.txt)
import glob, json, os, re, subprocess, sys, tempfile
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath('vo/takes')
ids, sec, n = [], None, 0
for raw in open(os.environ.get('SCRIPT', 'vo/script_asm.txt'), encoding='utf-8'):
    s = raw.strip()
    if m := re.fullmatch(r'\[(\w+)\]', s):
        sec, n = m.group(1).lower(), 0
    elif s:
        n += 1
        ids.append(f'{sec}-{n}')
GAP = {}  # tight: a 45 s short has no pauses
LEAD, SEC_GAP, LINE_GAP, TAIL = 0.15, float(os.environ.get('SEC_GAP', .26)), float(os.environ.get('LINE_GAP', .12)), 0.6  # EP4 v6: one seed, one pace, sentence-level splits only  # speaking rhythm kept; gaps are clean silence
SR = 48000
TEMPO = float(os.environ.get('TEMPO', '1.16'))  # pitch-kept speed-up (ffmpeg atempo); target total 45–50 s
BEAT = float(os.environ.get('BEAT', .30))  # EP5: pause after 'ตัวที่ N <name>' so each item lands
PAUSE_MAX, PAUSE_TO = 0.40, 0.28  # inner silences longer than this shrink to PAUSE_TO seconds


def tighten(y):
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), 'same'))[::hop]
    quiet = rms < 0.05 * rms.max()
    keep, i = np.ones(len(y), bool), 0
    while i < len(quiet):
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        if (j - i) * hop > PAUSE_MAX * SR and i > 0 and j < len(quiet):
            cut = (j - i) * hop - int(PAUSE_TO * SR)
            a = i * hop + int(PAUSE_TO * SR / 2)
            keep[a:a + cut] = False
        i = j + 1
    return y[keep]


def debreath(y):
    """Silence breaths without changing timing: quiet-ish stretches (< 12 % of peak RMS) lasting >= 150 ms.
    Shorter dips are consonants (ส ฟ ช ห) and are left alone."""
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), 'same'))[::hop]
    low = rms < 0.12 * rms.max()
    g = np.ones(len(y))
    i = 0
    while i < len(low):
        j = i
        while j < len(low) and low[j]:
            j += 1
        if j - i >= 15:
            a, b = i * hop + int(0.015 * SR), min(len(y), j * hop - int(0.015 * SR))
            if b > a:
                f = int(0.025 * SR)
                g[a:b] = 0
                g[max(0, a - f):a] = np.minimum(g[max(0, a - f):a], np.linspace(1, 0, a - max(0, a - f)))
                g[b:b + f] = np.minimum(g[b:b + f], np.linspace(0, 1, len(g[b:b + f])))
        i = j + 1
    return y * g


def unvoiced_islands(y):
    """Silence short sound islands with no voicing (breaths, lip noise) that sit between silences: < 0.35 s and
    < 20 % voiced frames (librosa pyin) and quieter than 35 % of peak. Breaths measured 0 % voiced at 13-16 % level;
    pyin misses voicing on some short loud words (EP3 "ด็อทส์" 0.78, "ใช้" 0.62), so loudness keeps them."""
    import librosa
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), 'same'))[::hop]
    sil = rms < 0.02 * rms.max()
    _, voiced, _ = librosa.pyin(y, fmin=70, fmax=400, sr=SR, frame_length=2048, hop_length=hop)
    n, i, g = min(len(sil), len(voiced)), 0, np.ones(len(y))
    while i < n:
        if sil[i]:
            i += 1
            continue
        j = i
        while j < n and not sil[j:j + 4].all():
            j += 1
        if (j - i) < 35 and voiced[i:j].mean() < 0.2 and rms[i:j].max() < 0.35 * rms.max():
            a, b = i * hop, min(len(y), j * hop)
            g[a:b] = 0
        i = j
    f = int(0.025 * SR)
    g = np.convolve(g, np.ones(f) / f, 'same')  # 25 ms fades
    return y * g


def inhales(y):
    """Silence inhales: unvoiced, < 20 % of peak RMS, >= 150 ms, spectral centroid < 5.5 kHz (breaths ~4.5 kHz;
    ส/ฟ/ช fricatives sit at 7-8 kHz). Then drop leading/trailing silence this leaves."""
    import librosa
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), 'same'))[::hop]
    rms /= rms.max()
    _, voiced, _ = librosa.pyin(y, fmin=70, fmax=400, sr=SR, frame_length=2048, hop_length=hop)
    cen = librosa.feature.spectral_centroid(y=y, sr=SR, n_fft=1024, hop_length=hop)[0]
    n = min(len(rms), len(voiced), len(cen))
    m = (~voiced[:n]) & (rms[:n] > 0.015) & (rms[:n] < 0.20)
    g, i = np.ones(len(y)), 0
    while i < n:
        j = i
        while j < n and m[j]:
            j += 1
        if j - i >= 15 and np.median(cen[i:j]) < 5500:
            g[i * hop:j * hop] = 0
        i = j + 1
    f = int(0.025 * SR)
    y = y * np.convolve(g, np.ones(f) / f, 'same')
    nz = np.flatnonzero(np.abs(y) > 1e-4)
    return y[max(0, nz[0] - int(0.01 * SR)):nz[-1] + int(0.03 * SR)]


def voiced_blips(y, max_len=18, max_lvl=.25):
    """Silence isolated hesitation blips ("เออ"): islands < 0.18 s, quieter than 25 % of peak RMS, with >= 120 ms of
    silence on both sides. Running words are never isolated like that."""
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), 'same'))[::hop]
    top = rms.max()
    sil = rms < 0.03 * top
    g, i, n = np.ones(len(y)), 0, len(sil)
    while i < n:
        if sil[i]:
            i += 1
            continue
        j = i
        while j < n and not sil[j]:
            j += 1
        a0 = i
        while a0 > 0 and sil[a0 - 1]:
            a0 -= 1
        b0 = j
        while b0 < n and sil[b0]:
            b0 += 1
        if (j - i) < max_len and rms[i:j].max() < max_lvl * top and i - a0 >= 12 and b0 - j >= 12 and a0 > 0 and b0 < n:
            g[i * hop:j * hop] = 0
        i = j
    f = int(0.02 * SR)
    return y * np.convolve(g, np.ones(f) / f, 'same')


def edges(y):
    """Cut leading/trailing breath: keep from 120 ms before the first voiced frame to 80 ms after the last."""
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), 'same'))[::hop]
    v = np.flatnonzero(rms > 0.2 * rms.max())
    a = max(0, v[0] - 12)
    while a < v[0] and rms[a] < 0.04 * rms.max():
        a += 1
    b = min(len(rms), v[-1] + 8)  # 80 ms tail: Thai finals are unreleased, anything longer is an exhale
    if len(rms) < 160:  # a short phrase (e.g. "พ้อมต์ของเรา") is all word: only trim the tail
        return y[a * hop:b * hop]
    # generated lead-in ("อือ"/breath) before the first word: within the first 0.5 s, a stretch quieter than 60 % of
    # the clip's peak followed by a near-silent dip (>= 30 ms) -> start after the dip
    top = rms.max()
    for k in range(a + 1, min(len(rms) - 3, a + 50)):
        if (rms[k:k + 3] < 0.05 * top).all():
            d = k
            while d < len(rms) and rms[d] < 0.05 * top:
                d += 1
            if rms[a:k].max() < 0.6 * top:
                a = max(a, d - 2)
            break
    # blip + breath before the first sustained word (no clean silence between them): start at the word
    loud = rms > .25 * top
    L = next((k for k in range(a, min(len(rms) - 15, a + 80)) if loud[k:k + 15].all()), None)
    if L is not None:
        k = L - 1
        while k > a and rms[k] < .2 * top:
            k -= 1
        blip = rms[a:k + 1]
        if L - 1 - k >= 10 and (blip > .2 * top).sum() < 15 and blip.max() < .5 * top:  # short, quiet blip only — never a real word
            a = L - 3
    return y[a * hop:b * hop]


def speed(y):
    with tempfile.TemporaryDirectory() as d:
        sf.write(f'{d}/a.wav', y, SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{d}/a.wav', '-af', f'atempo={TEMPO}', f'{d}/b.wav'], check=True)
        return sf.read(f'{d}/b.wav')[0]

clips = []
for i in ids:
    y, sr = sf.read(sorted(glob.glob(os.path.join(CLIPS, f'{i}_?.wav')))[-1], always_2d=True)
    y = y.mean(1)
    if sr != SR:
        y = np.interp(np.arange(0, len(y), sr / SR), np.arange(len(y)), y)
    proc = lambda z: tighten(voiced_blips(unvoiced_islands(debreath(inhales(edges(z))))))
    jf = sorted(glob.glob(os.path.join(CLIPS, f'{i}_?.wav')))[-1][:-4] + '.json'
    if os.environ.get('CHUNKS', '1') != '0' and os.path.exists(jf):
        # split at the engine's own phrase boundaries so every phrase gets its lead-in/edge cleanup
        parts = []
        for c in json.load(open(jf))['chunks']:
            seg = y[max(0, int((c['start'] - .03) * SR)):int((c['end'] + .05) * SR)]
            if len(seg) > SR // 5:
                parts += [proc(seg), np.zeros(int((.32 if c['text'].endswith('?') else BEAT if c['text'].startswith('ตัวที่') else LINE_GAP) * SR))]  # a beat after a question / a list item's name
        clips.append(speed(np.concatenate(parts[:-1])))
    else:
        clips.append(speed(proc(y)))

t, out, place = LEAD, [], []
for k, (i, c) in enumerate(zip(ids, clips)):
    d = len(c) / SR
    out.append({'id': i, 'start': round(t, 3), 'end': round(t + d, 3)})
    place.append((int(t * SR), c))
    nxt = ids[k + 1].split('-')[0] if k + 1 < len(ids) else None
    t += d + GAP.get(i, SEC_GAP if nxt != i.split('-')[0] else LINE_GAP)
dur = round(out[-1]['end'] + TAIL, 3)
mix = np.zeros(int(dur * SR) + 1)
for s, c in place:
    mix[s:s + len(c)] += c
mix = voiced_blips(mix, 16, .40)  # final pass on the joined track, where the silences around a blip are final
mix *= 0.89 / np.abs(mix).max()
rng = np.random.default_rng(7)  # faint room tone (-66 dBFS, low-passed) so gated gaps aren't dead digital silence
tone = np.convolve(rng.standard_normal(len(mix)), np.ones(24) / 24, 'same')
mix += tone / np.abs(tone).max() * 10 ** (-66 / 20)
sf.write('vo.wav', np.stack([mix, mix], 1), SR)
json.dump({'duration': dur, 'bpm': 120, 'offset': 0, 'lines': out},
          open('vo.timing.json', 'w'), ensure_ascii=False, indent=1)
for l in out:
    print(l)
print('duration', dur)
