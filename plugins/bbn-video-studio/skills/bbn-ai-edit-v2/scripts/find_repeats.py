"""Flag spoken repeats / restarts / fillers in a Thai transcript so they can be cut before the Long is built.
usage: python3 find_repeats.py qwen_windows.json   (the bbn-ai-cut Qwen output: {"windows":[{"start","end","text"}]})
Prints approximate source times. Locate the exact cut with short-window ASR + RMS dips, then ASR-test the seam."""
import json, re, sys
IGNORE = {"นะครับ", "ครับทุกคน", "ทุกคน", "แล้วก็", "ก็คือ", "ตัวของ", "นะครับทุกคน", "ซึ่ง", "เลย"}   # normal Thai speech glue, repeats are fine
FILLER = re.compile(r"เอ่อ|อ่ะ|เอ้ย|ไม่ใช่นะครับ|อะไรนะ")
REP = re.compile(r"(.{4,40}?)(.{0,5}?)\1")   # immediate restart: same phrase again within a short gap
W = json.load(open(sys.argv[1]))["windows"]
seen = []
for w in W:
    t = re.sub(r"\s+", "", w["text"]); n = max(1, len(t)); d = w["end"] - w["start"]
    at = lambda i: w["start"] + d * i / n
    for m in REP.finditer(t):
        g = m.group(1)
        if g in IGNORE or re.fullmatch(r"(นะ|ครับ|ทุกคน|ก็|คือ|แล้ว)+", g): continue
        s = round(at(m.start()), 1)
        if any(abs(s - x) < 2 for x in seen): continue
        seen.append(s); print(f"~{s:7.1f}s  repeat  '{g}' -> {t[max(0, m.start() - 12):m.end() + 12]}")
    for m in FILLER.finditer(t):
        s = round(at(m.start()), 1); print(f"~{s:7.1f}s  filler  '{m.group(0)}' -> {t[max(0, m.start() - 15):m.end() + 15]}")
