---
name: bbn-voice-clone
description: Clone BoomBigNose Thai speech using the saved OmniVoice checkpoint and voice profile, with automatic Thai ASR checks, dead-air, inhale (breath) and unwanted filler/repetition cuts, bounded repair of missing phrases, seed retakes, and per-line best-take narration for video (optionally with VoxCPM2, commercial-use licence) on Apple Silicon.
---

# BoomBigNose voice clone

Use the included CLI and saved profile to reproduce the latest voice. This kit contains a personally fine-tuned OmniVoice checkpoint, trained on 343.14 seconds of the user's real recordings for 600 steps. The default profile loads the merged model in `models/boombignose-finetuned`; all trained voice weights and the audio tokenizer needed for inference are included. Use the same reference, timing, and pitch processing for consistency. Do not promise identical voice quality on every script.

## Locate and run

- Accept any user-provided Thai script or UTF-8 text file; the bundled news script is only an example. If the request is to install or update this reusable skill, complete that setup without asking for a new narration script.
- Installed skill: read `assets/kit-location.json` to find the kit. Bundled skill: kit is three directories above `scripts/clone.py`.
- Read `<kit>/runtime/runtime.json` for the Python executable. If unavailable, run `<kit>/ติดตั้ง.command`; it installs the pinned local MLX-Audio wheel and dependencies without downloading additional voice models.
- Save the user's requested Thai narration as UTF-8 text. Keep original content; write names and numbers as Thai pronunciations only with the user's instruction or agreement. Break lines at sentence endings and use blank lines between topics.
- Owner-approved pronunciations (2026-10-26): write these spellings in the text sent to the engine (captions keep the normal words): Hermes → เฮอร์เมส, Desktop → เดสท็อป, then soften its ending with `~/.codex/skills/bbn-clear-vo/scripts/soften_word.py IN.wav OUT.wav`, โปรไฟล์/profile → โปรไฟว, Edit → อีดิท, เหตุผล → เหดผล, n8n → เอ็น เอ๊ดเอ็น (space after the first เอ็น only). The full proven list is `~/.codex/skills/bbn-clear-vo/references/lexicon.tsv`.
- Run with argument arrays or properly quoted paths:

```text
<PYTHON> <skill>/scripts/clone.py --kit <KIT> --text-file <TEXT.txt> --output <NEW.wav>
```

Use a new output name; the CLI rejects overwriting existing files. Default maximum is 5,000 characters. The JSON next to the WAV records actual settings, phrase timings, and automatic quality results. Return a playable absolute WAV path and state any remaining pronunciation or listening limitation.

## Automatic cleanup on every generation

The shared engine used by this skill and the local web app automatically transcribes each generated Thai phrase with the local `models/typhoon-asr` model and compares it with the requested script. It cuts excessive silence, unwanted fillers such as เอ่อ, and repetitions that were not requested in the script. Suspected missing or incomplete phrases are regenerated with a bounded retry count, checked again, and joined into the final WAV. Keep intentional words and repetitions from the script. Do not rerun the old one-off editing script or bypass the shared engine.

Audible inhales (the "ฟืบ" between phrases) are muted on every phrase, and a sound followed by an inhale at the very start of a phrase is dropped as a filler (เอ่อ). This runs before the ASR check, so a real first word removed by mistake is flagged as missing, and repaired when a retry succeeds; a plain pause after a short first word is not treated as an inhale. The JSON records it per phrase under `details[].breath`. `--no-breath-cleanup` keeps inhales; `--keep-lead` keeps phrase starts untouched.

Read `quality.status` in the output JSON before reporting success. `passed` means the automatic checks passed; it does not certify human listening or naturalness. If the status is `needs_review`, report the unresolved `quality.flags` and ask the user to listen to those parts; do not describe the audio as free of stutter or missing words. ASR can misrecognize names and Thai pronunciations.

The local ASR model is required for this cleanup. Keep it with the kit when moving to another Mac. Do not silently skip verification if it is missing. `PHRASE`, `VERIFY`, `REPAIR`, and `CLEANUP` messages show the current stage; repair is limited so generation cannot loop indefinitely.

## Retakes

Same text + same seed always returns the same take, so asking again changes nothing. Retake a bad line with another seed: `--seed 7` (then 11, 23 …). Keep the script wording unless the user agrees to change it.

## Narration for video: one WAV per line, best take kept

For clips where each line is placed on its own (captions, scene cuts), use `best_take.py`. It generates each line, cleans breaths, checks it with the Thai ASR and retries seeds until the take passes and the voice added no particle the script lacks (ครับ, นะครับ, เนี่ย, ค่ะ, น่ะ — picked up from the reference's speaking style):

```text
<PYTHON> <skill>/scripts/best_take.py --kit <KIT> --text-file <lines.txt> --out-dir <DIR> [--seeds 42,7,11,23] [--ignore คล็อดดอตเอ็มดี]
```

`lines.txt` has one clip per line, `id|ข้อความ` (or just the text). Output: `DIR/<id>.wav`, every take in `DIR/takes/`, and `DIR/report.json` with the chosen seed, what the ASR heard and `needs_listening` for lines no seed fixed — report those to the user by id. ASR writes English terms in Latin letters (คล็อดดอตเอ็มดี → cross.md), so pass each Thai-spelled English term with `--ignore` or correct takes are rejected. A transcriber loop after an English word ("cross.md สินค้า สินค้า สินค้า…") is cut automatically; a take far longer than its text is rejected as a run-on.

Write the script for speech: English as Thai pronunciation (Claude Code → คล็อดโค้ด, context → คอนเท็กซ์, CLAUDE.md → คล็อดดอตเอ็มดี, npm test → เอ็นพีเอ็ม เทสต์, AI → เอไอ, MCP → เอ็มซีพี), ๆ written out (เรื่อยๆ → เรื่อยเรื่อย), digits as Thai words. If one line keeps swallowing its first word on every seed (this voice did it with a leading แล้ว), drop that word from the caption text rather than forcing it.

### Optional second engine: VoxCPM2

`--engine voxcpm --voxcpm-python <python with voxcpm>` (for example `~/.venvs/bbn-video-studio/bin/python` from bbn-video-studio; ~5 GB model download on first use) clones the same consented `voice/reference.wav` with VoxCPM2 (Apache-2.0 per its model card, "free for commercial use"; impersonation and fraud are prohibited — unlike the CC-BY-NC OmniVoice weights here). It uses timbre-only cloning: its continuation/prompt mode was tested and leaked the reference's own words and garbled short lines. Expect it to sound less like the owner than the trained OmniVoice model (5.6 s reference vs 343 s of training), to add particles and to slip tones (ขั้น → คัน), so give it more seeds. Say which engine produced the audio.

## Tune only the requested part

Read `<kit>/voice/profile.json`. Latest approved settings: 32 steps, guidance 2, seed 42, pace factor 0.85, pitch -0.5 semitone. Pauses: phrase 0.14 s, sentence 0.40 s, topic 0.60 s, paragraph 0.75 s.

- `--pitch -0.8`: slightly lower voice, preserving total length. Safe range -2 to +2 semitones.
- `--pace 0.90`: more time to speak each phrase; 0.80 is faster. Safe range 0.70–1.15. Test a short passage first; excessive duration can cause repeated or unclear speech.
- `--pause-scale 1.15`: longer pauses; 0.85 is tighter. Safe range 0.5–1.5.
- Edit the four pause values in a copy of `profile.json` and select it with `--profile` if the user needs independent control.

Change one requested setting, generate a short example, then apply it to the long script. The model weights and reference stay at their saved versions unless the user asks to change them. Avoid model comparisons, new downloads, or training when the request is only to use this approved voice.

## What matters for reproducibility

The model plus bundled audio tokenizer, reference WAV with its matching transcript, local MLX-Audio wheel, and profile are all needed. Loading the model file alone will not reproduce this voice. Do not use a duration slider to stretch a short sentence into a long file. The engine splits at Thai word boundaries and reads each phrase with a shared reference before joining it.

Use the user's current authorization for their voice. This skill processes locally and does not publish audio or upload the reference. The included reference is personal voice data; sharing the full kit exposes that reference. For a new person's voice, use that person's authorized reference instead of retaining the BoomBigNose profile.

The engine validates finite, non-silent output and text/tuning bounds. File generation, hashes, and ASR do not certify perceptual naturalness. Compare to `samples/latest-approved.wav` when the user asks to assess sound; state whether a person has actually listened.

## Personally trained checkpoint

Use the default `voice/profile.json` for the trained model. This package contains the merged native MLX model, so inference does not need the original base model or a separate LoRA adapter. Training evidence and source metadata are in `<kit>/provenance/`, including `training-report.json`. This package is for voice generation; the original training data, optimizer, and resume state are not included. This is real weight training, not a saved voice prompt. The held-out loss improvement is not a subjective similarity score.

Keep the weight licensing conditions in `<kit>/NOTICE.md` when using or sharing this package; fine-tuning does not remove the base model's restrictions.
