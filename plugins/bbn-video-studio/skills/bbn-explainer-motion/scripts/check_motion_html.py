#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KAN-76 preflight for a HyperFrames motion composition (index.html).

BBN motion uses NO emoji of any kind (SKILL.md rule 1). Fails on:
  1. any emoji character anywhere in the HTML (text, attributes, scripts,
     styles, comments) or inside a local .svg/.css/.html asset
  2. any emoji font (local("...Emoji") or "... Emoji" in a font-family stack)
  3. any emoji image asset: a src/href/url() path, or a file/folder in the
     project, whose name contains emoji / fluent / twemoji / openmoji / noto-emoji
     -> use drawn SVG icons (assets/icons/), real logos, or real footage
  4. @font-face files missing, or (when fontTools is installed) a text
     character that no bundled font covers -> fallback/tofu
  5. local src/href/url() assets that do not exist
Usage: check_motion_html.py path/to/index.html   (exit 1 on any FAIL)
"""
import re, sys, html
from pathlib import Path

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF\u3030\u303D\u3297\u3299\uFE0F\u200D\u20E3\U000E0020-\U000E007F]")
EMOJI_NAME = re.compile(r"emoji|fluent|twemoji|openmoji|emojione|joypixels", re.I)
SKIP_DIRS = {".hyperframes", "node_modules", ".git"}

def chars(s):
    return " ".join(sorted({f"{c}(U+{ord(c):04X})" for c in EMOJI.findall(s)}))

def main(p):
    p = Path(p); root = p.parent
    s = p.read_text(encoding="utf-8"); fails = []; warns = []
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", s, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    if EMOJI.search(html.unescape(s)):
        fails.append("emoji character in index.html (no emoji allowed): " + chars(html.unescape(s)))
    if re.search(r"local\([\"']?[^)]*Emoji", s, re.I) or re.search(r"font-family\s*:[^;}{]*Emoji", s, re.I):
        fails.append("emoji font referenced (local()/font-family ... Emoji); no emoji allowed")
    refs = set(re.findall(r"""(?:src|href)=["']([^"':#]+)["']""", s))
    refs |= set(re.findall(r"""url\(["']?([^"')#:]+)["']?\)""", s))
    for a in sorted(refs):
        if EMOJI_NAME.search(a):
            fails.append(f"emoji image asset referenced: {a} (use assets/icons/*.svg, a real logo or footage)")
        if not (root / a).exists():
            fails.append(f"missing asset: {a}")
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        if EMOJI_NAME.search(f.name):
            fails.append(f"emoji asset in project: {rel} (remove it)")
        elif f.is_file() and f.suffix.lower() in {".svg", ".css", ".html", ".htm"} and f != p:
            t = f.read_text(encoding="utf-8", errors="ignore")
            if EMOJI.search(html.unescape(t)):
                fails.append(f"emoji character inside {rel}: " + chars(html.unescape(t)))
            if re.search(r"font-family\s*[:=][^;>]*Emoji", t, re.I):
                fails.append(f"emoji font referenced inside {rel}")
    fonts = re.findall(r"@font-face\s*{[^}]*?url\([\"']?([^\"')]+)", s)
    if not fonts:
        fails.append("no bundled @font-face; Thai text would use a system fallback")
    paths = []
    for f in fonts:
        fp = root / f
        (paths.append(fp) if fp.exists() else fails.append(f"missing font file: {f}"))
    try:
        from fontTools.ttLib import TTFont
        cov = set()
        for fp in paths:
            cov |= set(TTFont(fp).getBestCmap())
        need = {ord(c) for c in text if not c.isspace() and not EMOJI.match(c)}
        miss = sorted(chr(c) for c in need - cov)
        if paths and miss:
            fails.append("characters not in bundled fonts (fallback/tofu): " + "".join(miss))
    except ImportError:
        warns.append("fontTools not installed: glyph coverage not checked (pip install fonttools)")
    for w in warns: print("WARN", w)
    for f in dict.fromkeys(fails): print("FAIL", f)
    print("OK" if not fails else f"{len(dict.fromkeys(fails))} problem(s)")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "index.html"))
