---
name: bbn-clear-vo
description: "Make the narration (VO) for a BBN / Knowledge Clip short in the user's approved clear-reading style — the script written the way the user writes it (one phrase per line, blank line between thoughts, \"-\" syllable hints), generated with the approved BBN cloned voice, checked line by line for unclear words, and assembled tight and rhythmic (EP5 v6, approved 2026-10-16). Use whenever generating or re-generating Thai narration — เจนเสียง, ทำเสียงพากย์, อัดเสียง VO, อ่านบทนี้, แก้คำไม่ชัด — before any motion work."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# BBN clear VO

The recipe the user approved for EP5 (v6, "จะเป็นประมาณนี้"). Their asks, in order of weight: **natural speech**, every word clear,
concise (no dead air), an upbeat teaching tone with rhythm. Voice first: send the VO, wait for approval, only then motion.

## 1. The script — written the user's way

If the user gives a script, use their words verbatim. If you write it, write it in this format and show it before generating.
Reference: `references/example_script_ep5.txt` (written by the user).

- One spoken phrase per line (~2–4 s). Blank line between thoughts.
- A list item opens with its own line: `ตัวที่หนึ่ง โพ-นี-เทล`.
- English names/terms are spelled in Thai; `-` marks syllables so they're read clearly (`ออม-นิ-รูต`, `โท-เค็น`). Never read the dashes.
- Numbers as words (`หนึ่งร้อยห้าสิบ`, `ยี่สิบห้า`). Speaker is ผม.
- Concise and punchy: a hook line, one fact per line, a CTA (`คอมเมนต์คำว่า ปลั๊กอิน ไว้ / เดี๋ยวผมส่งลิงก์ให้`).
- Avoid piling loanwords into one line; prefer plain Thai where it means the same.

Save it as `script.txt` in the episode work folder `~/Desktop/Clip Knowledge/_ไฟล์งาน/EP<n>/` (final deliverables — final clip, caption, DM kit, covers — go in `~/Desktop/Clip Knowledge/Final/EP<n>/`).

## 2. Build

Run from the episode work folder (`_ไฟล์งาน/EP<n>`). `S=~/.codex/skills/bbn-clear-vo/scripts`, `PY=~/.venvs/blender-explainer/bin/python`,
`source ~/.local/share/bbn-ai-cut/env.sh` first (ffmpeg), `HF_HUB_OFFLINE=1` for Whisper.

```bash
python3 $S/prep.py script.txt          # -> vo/text/pNN-1.txt (TTS text), vo/script_asm.txt, vo/captions.txt (user's words)
python3 $S/gen.py                      # one take per paragraph, approved voice, seed 42, pace 1.0 (~20 s each)
HF_HUB_OFFLINE=1 $PY $S/check.py       # every line: TTS text vs what Whisper hears
HF_HUB_OFFLINE=1 $PY $S/assemble.py vo/takes   # -> vo.wav + vo.timing.json (55-60 s for ~10 paragraphs)
ffmpeg -i vo.wav -c:a aac -b:a 192k EP<n>_VO_ตรวจ_v<k>.m4a
```

`prep.py` drops the dashes, joins a one-line paragraph (an item's name) to the next paragraph so it isn't a tiny chunk, and
applies `references/lexicon.tsv` to the TTS text only. Subtitles always use the user's words (`vo/captions.txt`).

## 3. Fix unclear words (before sending)

Read `check.py`'s `??` lines (Thai mismatch) and `~` lines (Whisper wrote names/digits in Latin — compare by eye). **False alarms** (ignore): English names coming back in Latin letters, digits for Thai numbers,
โค้ด→"โคต/โคตร" (its tone measures right), โทเค็น→"โทรเค็น", เมื่อไหร่→"เมื่อไร". A whole-file transcript that repeats a word
("คลอดคลอดคลอด") is a Whisper hallucination: re-check that segment alone. **Real problems**: garbled Thai, a dropped word,
a wrong number, a final consonant lost. Fixes, in this order:

1. A known word → add/confirm it in `lexicon.tsv`, re-run prep, `gen.py <id>` for that paragraph.
2. A short line that comes out garbled ("แต่ยังใช้งานได้จริง" → "ในยังชัยงานได้จิง") → put it on the same line as its neighbour
   (`...น้อยที่สุด แต่ยังใช้งานได้จริง`). Same words, just no break.
3. A word that blurs at the end of a phrase → a context word in front (`ด้วยตัวคล็อดโค้ด`), or a nearby word that reads cleaner
   (`กว่า` → `มากกว่าหนึ่งร้อยห้าสิบเจ้า` fixed "159 บาท"). Tell the user about any word you add.
4. Tone errors Whisper can't hear (ว่า, ต่อ, ซี): `HF_HUB_OFFLINE=1 $PY $S/tone.py vo.wav <syllable>...` (F0 contour).
   Try 2–4 spellings of the line at once; pick by check + tone.

Edit `vo/text/<id>-1.txt` directly for a one-off fix, then `python3 $S/gen.py <id>` (makes the next letter, `_b`, which assemble
picks up). Keep the original user script untouched.

## 4. Rules that came from failures

- ONE profile, ONE seed, ONE pace for the whole VO. Mixing paces or splicing takes sounded stitched ("ไม่เป็นธรรมชาติ").
- `clone.py` refuses to overwrite: new take = new letter.
- Approved voice = `assets/profile.json` (refM.wav: the kit reference + an expressive raw tail, seed 42, pitch −0.5,
  guidance 2, 32 steps). Do not change its reference. References cut from BBN camera audio (EP228) gave more pitch range but a
  different recording sound; the reference must be 2–8.01 s.
- Pace 1.0 + TEMPO 1.16 + gaps LINE .12 / SEC .26 / BEAT .30 (pause after `ตัวที่ N <ชื่อ>`) are the v6 defaults
  (env vars `PACE`, `TEMPO`, `LINE_GAP`, `SEC_GAP`, `BEAT` override). Pace 1.1 is clearer but slower; ×1.12 = 57.7 s alt.
- `assemble.py` strips breaths, inhales, fillers (เออ) and the reference's leaked words at chunk edges, and adds faint room tone.
- Send the m4a with `SendUserFile` and stop; the user approves the voice before motion (`bbn-dark-motion-theme`).
- Owner's pronunciations (2026-10-26, Hermes course), now in `lexicon.tsv`: Hermes = เฮอร์เมส (not เฮอร์มีส),
  Desktop = TTS spelling เดสท็อป, then soften (below), profile = โปรไฟล์ (TTS spelling โปรไฟว; the ไฟล์ rule made it "โปรฟาล"),
  Edit = อีดิท (not เอดิท), เหตุผล = เหต-ผล (TTS spelling เหดผล, not เห-ตุ-ผล). The โปรไฟล์ row must stay above the ไฟล์ rows.
- Whisper can't hear vowel length or a split syllable (ท็อป vs ทอบ, เห-ตุ vs เหต both come back as the same word): use the
  owner's own spelling for those, test candidates as a short script first, and send a short m4a of just the changed words.
- Desktop's "top" must be neither the clipped ท็อป nor the soft long ทอบ (owner, 2026-10-26, checked against their own
  voice in EP224 at 0:47). No Thai spelling gives the in-between, so after `assemble.py` run
  `HF_HUB_OFFLINE=1 $PY $S/soften_word.py vo.wav vo_soft.wav` and use `vo_soft.wav`: it finds every Desktop and fades
  0.08 s across the hard stop after the top vowel; timing is unchanged, so `vo.timing.json` still matches. It prints each
  softened window: check it ends before the next word. Use `--match <regex>` for another word that sounds too clipped.
- Fix one word inside a finished VO by editing `vo/text/<id>-1.txt`, `gen.py <id>`, then re-running `assemble.py`; timings of
  later paragraphs shift, so re-derive any downstream cut points from the new `vo.timing.json`.

## Files

- `scripts/prep.py`, `gen.py`, `check.py`, `assemble.py`, `tone.py`, `soften_word.py` (soften a clipped loanword ending)
- `assets/profile.json`, `assets/refM.wav` — the approved voice
- `references/lexicon.tsv` — proven TTS spellings (regex → spelling → why); add new ones as they're proven
- `references/example_script_ep5.txt` — the user's script format
- Worked example: `~/Desktop/Clip Knowledge/_ไฟล์งาน/EP5/STATUS.md` (v1 → v6, what each change fixed)
