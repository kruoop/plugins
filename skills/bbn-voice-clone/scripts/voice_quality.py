"""Source-aware Thai speech verification and conservative audio edits."""
import difflib
import math
import re

import numpy as np
from pythainlp import word_tokenize


def normalized(text):
    text = text.lower().replace('ai', 'เอไอ').replace('project', 'โปรเจกต์').replace('นึง', 'หนึ่ง')
    words = []
    for token in word_tokenize(text, engine='newmm', keep_whitespace=False):
        repeats = token.count('ๆ')
        token = re.sub(r'[^ก-๙a-z0-9]', '', token).replace('ฯ', '').replace('ๆ', '')
        if token:
            words.append(token)
        if repeats and words:
            words.extend([words[-1]] * repeats)
    return ''.join(words)


def analyze_phrase(source, transcript, duration):
    expected = normalized(source)
    raw = [w for s in transcript.get('segments', []) for w in s.get('words', [])]
    flags = []
    if not raw or not expected or not math.isfinite(duration) or duration <= 0:
        return {'cuts': [], 'needs_repair': True, 'score': 1.0, 'flags': ['ไม่มีข้อความถอดเสียง'], 'heard': transcript.get('text', '')}
    text, starts, ends, probabilities = '', [], [], []
    previous_end = 0.0
    for word in raw:
        token = str(word.get('word', ''))
        start, end = word.get('start', float('nan')), word.get('end', float('nan'))
        probability = word.get('probability', 0)
        if (not all(isinstance(v, (int, float)) and math.isfinite(v) for v in (start, end, probability))
                or not 0 <= start <= end <= duration + .05 or start > duration
                or start < previous_end - .02 or not 0 <= probability <= 1):
            flags.append('เวลาอ้างอิงคำไม่ถูกต้อง')
            break
        previous_end = end
        if token:
            # shortcut: very long character timestamps are ASR alignment failures, not safe edit boundaries.
            if (end - start) / len(token) > .8:
                flags.append('เวลาอ้างอิงคำไม่แน่นอน')
                break
            bounds = np.linspace(start, min(end, duration), len(token) + 1)
            text += token
            starts.extend(bounds[:-1]); ends.extend(bounds[1:])
            probabilities.extend([float(probability)] * len(token))
    if flags:
        return {'cuts': [], 'needs_repair': True, 'score': 1.0, 'flags': flags, 'heard': transcript.get('text', '')}
    words, offset, position = [], 0, 0
    for token in word_tokenize(text, engine='newmm', keep_whitespace=True):
        value = normalized(token)
        if token == 'ๆ' and words:
            value = words[-1]['normalized']
        if value:
            words.append({'text': token, 'normalized': value, 'start': float(starts[offset]),
                          'end': float(ends[offset + len(token) - 1]),
                          'probability': float(np.mean(probabilities[offset:offset + len(token)])),
                          'lo': position, 'hi': position + len(value)})
            position += len(value)
        offset += len(token)
    heard = ''.join(w['normalized'] for w in words)
    opcodes = difflib.SequenceMatcher(None, expected, heard, autojunk=False).get_opcodes()
    inserted = [(j, k) for tag, _, _, j, k in opcodes if tag == 'insert']
    fillers = {'เอ่อ', 'เอ้อ', 'เอ้า', 'อ่า', 'อ้า', 'อืม', 'อือ', 'อ๋อ'}
    cuts = []
    for i, word in enumerate(words):
        value = word['normalized']
        extra = any(lo <= word['lo'] and word['hi'] <= hi for lo, hi in inserted)
        previous = words[i - 1]['normalized'] if i else ''
        following = words[i + 1]['normalized'] if i + 1 < len(words) else ''
        repeated = value == previous or value == following or (len(value) >= 2 and previous.endswith(value))
        reason = None
        if value in fillers and (extra or value not in expected):
            reason = 'filler'
        elif extra and repeated:
            reason = 'repeat'
        if reason and word['probability'] >= .6 and word['end'] - word['start'] >= .08:
            cuts.append({k: word[k] for k in ('text', 'start', 'end', 'lo', 'hi')} | {'reason': reason})
        elif reason:
            flags.append('พบคำแทรกหรือคำซ้ำที่ตำแหน่งยังไม่ชัด')
        elif extra and len(value) >= 3:
            flags.append('มีคำแทรกต่างจากสคริปต์')
    cleaned = ''.join(c for i, c in enumerate(heard) if not any(w['lo'] <= i < w['hi'] for w in cuts))
    comparison = difflib.SequenceMatcher(None, expected, cleaned, autojunk=False)
    score = (len(expected) + len(cleaned) - 2 * sum(block.size for block in comparison.get_matching_blocks())) / max(1, len(expected))
    for tag, lo, hi, j, k in comparison.get_opcodes():
        if tag in ('delete', 'replace') and hi - lo >= 4 and k - j <= (hi - lo) * .3:
            flags.append('คำต้นหรือเนื้อหาบางช่วงตกหล่น')
            break
    if score > .25:
        flags.append('ข้อความที่อ่านต่างจากสคริปต์')
    flags = list(dict.fromkeys(flags))
    return {'cuts': cuts, 'needs_repair': bool(flags), 'flags': flags, 'score': score,
            'heard': transcript.get('text', ''), 'cleaned_text': cleaned}


def remove_intervals(audio, sample_rate, cuts):
    if not cuts:
        return audio.copy()
    spans = []
    for cut in sorted(cuts, key=lambda row: row['start']):
        start, end = round(cut['start'] * sample_rate), round(cut['end'] * sample_rate)
        if not 0 <= start <= end <= len(audio):
            raise ValueError('ASR edit falls outside the recording')
        if spans and start <= spans[-1][1]:
            spans[-1][1] = max(spans[-1][1], end)
        else:
            spans.append([start, end])
    chunks, cursor = [], 0
    for start, end in spans + [[len(audio), len(audio)]]:
        chunk = audio[cursor:start].copy()
        fade = min(round(sample_rate * .003), len(chunk) // 2)
        if fade:
            chunk[:fade] *= np.linspace(0, 1, fade)
            chunk[-fade:] *= np.linspace(1, 0, fade)
        chunks.append(chunk)
        cursor = end
    return np.concatenate(chunks)


def _frame_features(audio, sample_rate):
    """10 ms frames of 40 ms: level, 95th-percentile level, spectral flatness and centroid up to 8 kHz."""
    hop, window = round(sample_rate * .01), round(sample_rate * .04)
    if len(audio) < window:
        return np.zeros(0), 1.0, np.zeros(0), np.zeros(0)
    frames = np.lib.stride_tricks.sliding_window_view(audio, window)[::hop] * np.hanning(window)
    freqs = np.fft.rfftfreq(window, 1 / sample_rate)
    power = (np.abs(np.fft.rfft(frames, axis=1)) ** 2)[:, freqs <= 8000]
    freqs = freqs[freqs <= 8000]
    level = np.sqrt(np.mean(frames ** 2, axis=1))
    total = power.sum(axis=1) + 1e-12
    centroid = (power * freqs).sum(axis=1) / total
    flatness = np.exp(np.mean(np.log(power + 1e-12), axis=1)) / (total / power.shape[1])
    return level, float(np.percentile(level, 95)) or 1.0, flatness, centroid


def breath_spans(audio, sample_rate, min_seconds=.12):
    """Audible inhales: noise-like (spectral flatness ≥ .09), quiet (≤ 35 % of the loud frame level), centroid
    2.3–4.2 kHz measured up to 8 kHz, lasting ≥ min_seconds. Aspirated consonants (ถ ท พ ข …) are the same kind
    of noise but shorter, so they are kept. Near-silent frames between breath frames join the same span."""
    level, loud, flatness, centroid = _frame_features(audio, sample_rate)
    if not len(level):
        return []
    hiss = (flatness >= .09) & (level <= .35 * loud) & (centroid >= 2300) & (centroid <= 4200)
    noisy = hiss | (level < .03 * loud)
    spans, start = [], None
    for index, flag in enumerate(list(noisy) + [False]):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            if (index - start) * .01 >= min_seconds:
                spans.append({'start': start * .01, 'end': min(index * .01, len(audio) / sample_rate),
                              'hiss': round(float(hiss[start:index].sum()) * .01, 2)})
            start = None
    return spans


def clean_breaths(audio, sample_rate, drop_lead=True, lead_max=.40):
    """Mute inhales (short fades, no clicks). With drop_lead, a sound followed by an inhale inside the first
    lead_max seconds is a filler such as เอ่อ: the phrase then starts after that inhale. ASR verification runs on
    the result, so a real word removed by mistake is flagged as missing (and repaired when a retry succeeds)."""
    spans = breath_spans(audio, sample_rate)
    lead = 0.0
    # only a real inhale (≥ 60 ms of hiss) marks a filler; a plain pause after a short first word is speech
    if drop_lead and spans and 0 < spans[0]['start'] <= lead_max and spans[0]['hiss'] >= .06:
        lead = spans.pop(0)['end']
        level, loud, _, _ = _frame_features(audio, sample_rate)
        frame, stop = round(lead / .01), round((lead + .15) / .01)
        while frame < min(stop, len(level)) and level[frame] < .15 * loud:  # the quiet tail of the same inhale
            frame += 1
        lead = frame * .01
    out = audio.copy()
    fade = round(sample_rate * .012)
    for span in spans:
        start, end = round(span['start'] * sample_rate), round(span['end'] * sample_rate)
        if end - start <= 2 * fade:
            continue
        out[start + fade:end - fade] = 0
        out[start:start + fade] *= np.linspace(1, 0, fade)
        out[end - fade:end] *= np.linspace(0, 1, fade)
    out = out[round(lead * sample_rate):]
    if lead and len(out) > fade:
        out[:fade] *= np.linspace(0, 1, fade)
    return out, {'lead_cut': round(lead, 3), 'breaths_muted': [{k: round(v, 3) for k, v in s.items()} for s in spans]}


def silence_cuts(log, duration):
    cuts, start = [], None
    for kind, value in re.findall(r'silence_(start|end): ([0-9.]+)', log):
        if kind == 'start':
            start = float(value)
        elif start is not None:
            end = min(float(value), duration)
            if end - start > .15:
                cuts.append({'start': start + .04, 'end': end - .04})
            start = None
    if start is not None and duration - start > .15:
        cuts.append({'start': start + .04, 'end': duration})
    return cuts


class ThaiChecker:
    def __init__(self, model_path):
        if not (model_path / 'weights.safetensors').is_file() or not (model_path / 'config.json').is_file():
            raise FileNotFoundError('ไม่พบตัวตรวจภาษาไทย models/typhoon-asr กรุณาติดตั้งชุดโมเดลให้ครบ')
        self.model_path = str(model_path)

    def __call__(self, audio, sample_rate):
        import mlx_whisper
        from scipy.signal import resample_poly
        divisor = math.gcd(sample_rate, 16000)
        audio = resample_poly(audio, 16000 // divisor, sample_rate // divisor).astype(np.float32)
        return mlx_whisper.transcribe(audio, path_or_hf_repo=self.model_path, language='th',
                                      condition_on_previous_text=False, word_timestamps=True, temperature=0.0)
