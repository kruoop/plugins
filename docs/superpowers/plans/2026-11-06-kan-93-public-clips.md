# KAN-93 public clip insertion implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement in this session. The owner approved the six-step chat plan with “เริ่มทำเลย”. Keep one editing owner; no parallel editors.

**Goal:** One command inserts credited public reference, meme and gag excerpts into an already-cut EP on Mac Studio.

**Architecture:** Add a Python CLI in the existing bbn-ai-edit skill. A JSON cue sheet binds public URLs/source ranges to final EP times, protected teaching windows and audio policy. FFmpeg downloads bounded excerpts through yt-dlp, composites them over the base without changing its duration, and emits credits plus a provenance/QA report. Skill instructions route Slack requests to this command; no new Slack bot or watcher.

**Tech Stack:** Python 3, FFmpeg/ffprobe, yt-dlp, Pillow with Thai-capable fonts.

**Spec:** https://boombignose.atlassian.net/browse/KAN-93 and the six-step plan approved in this chat. KAN-76 requires newly drawn icons instead of emoji.

## Global Constraints

- Preserve original media, existing working-tree changes and accepted episode outputs.
- Download only requested bounded excerpts, cap time/size, keep free-space reserve; no whole-video fallback.
- Support ref, meme and gag with on-screen channel/URL credit and Description credit list.
- Reject cues overlapping protected teaching windows; source audio cannot replace active narration.
- Preserve final EP clock; use cut-plan/transcript-derived final times. No source-to-final remap guessed by the script.
- Use existing layouts, fonts and delivery paths; no YouTube publication.
- Completion needs a demo with all three modes and Patsinee approval; never claim the latter before it occurs.

## Review Focus

- Invalid or out-of-range/overlapping cues fail before downloads or output writes.
- A cache hit with different source metadata must not reuse the wrong clip.
- Network failure or oversized download cannot consume unbounded disk or overwrite an existing output.
- An audio-less source must still render correctly; source audio cannot swamp narration.
- Frame/time boundaries, credits and final duration must be correct in actual encoded output.

### Task 1: Validate and acquire bounded clips

**Files:** `skills/bbn-ai-edit/scripts/public_clips.py`, `skills/bbn-ai-edit/scripts/public_clip_sources.py`, `skills/bbn-ai-edit/tests/test_public_clips.py`

**Interfaces:** `load_plan(path) -> dict` resolves relative media paths and validates cues against probed base duration; `fetch_clip(cue, cache, limits) -> dict` produces a bounded local asset and provenance.

- [x] Write failing behavior tests for missing CLI, invalid windows, protected windows and audio replacement without a speech-free window.
- [x] Add validation and bounded section-only downloader with metadata/credit capture, cache integrity and time/size guards.
- [x] Verify tests; test a real short public-source download and inspect downloaded duration/size.

### Task 2: Composite video/audio and generate evidence

**Files:** `skills/bbn-ai-edit/scripts/public_clips.py`, `skills/bbn-ai-edit/scripts/public_clip_render.py`, same test file.

**Interfaces:** `render_plan(plan, plan_path) -> Path` downloads/cache-resolves assets, renders output, and writes credits/report alongside it. CLI `python3 scripts/public_clips.py render --plan PLAN.json`; `validate` performs preflight without network.

- [x] Write failing integration tests using real small FFmpeg fixtures for three modes, protected teaching preservation, missing source audio and final duration.
- [x] Implement credit cards with original drawn icons, reference overlay, full-frame meme/gag and bounded audio mixing.
- [x] Inspect rendered frames and encoded audio, then run the meaningful test suite.

### Task 3: Package, install and demonstrate on Mac Studio

**Files:** `skills/bbn-ai-edit/references/public-clips.md`, `skills/bbn-ai-edit/assets/public-clips-plan.example.json`, routing additions in bbn-ai-edit and bbn-ai-edit-v2 SKILL.md. Generated plugin copy via repository sync script.

- [x] Document actual Slack request syntax, cue schema, risks and supported-platform verification limits.
- [x] Validate skill links/manifests and synchronize distribution without staging unrelated work.
- [x] Back up changed files and install only task files/routing blocks on local Codex and Mac Studio active skill paths.
- [x] Produce a clearly marked KAN-93 demo with all three modes from real public excerpts; record environment, source hashes, frames and audio checks.
- [ ] Upload demo/report, attach links to KAN-93, and submit review to the configured Patsinee route. Keep approval pending.

## Progress

- Initial check: Mac Studio reachable; FFmpeg/yt-dlp/rclone available; about 18 GiB free. Canonical repository has unrelated motion/skill edits, retained in place on task branch `codex/kan-93-public-clips`.
- Ruling: use the existing checkout on a task branch, preserving unrelated edits, rather than create an extra worktree. This makes the new insertion route work with the latest locally accepted skill rules.

- Tasks 1–2 complete: 19 real-media/resource behavior tests pass locally (FFmpeg 8.1) and on Mac Studio (FFmpeg 9.0.2).
- Runtime: isolated Pillow 13.0.0 / yt-dlp 2026.10.26 environments; no global tool upgrade. Mac Studio installed task files across five existing skill locations, with per-file backups and SHA-256 checks.
- Independent read-only code review found six important issues. Fixed all in one pass, with reproducing RED→GREEN tests: no-clobber sidecar transaction/rollback; corrected cache channel credit; sample-precise narration duck; 60-fps end frames; signed-URL rejection; sound gag after the base narration stream ends. No deferred minor findings.
- Ruling: demo uses a clearly marked landscape test canvas with an unchanged copy of the existing EP258 Short on the right. This verifies insertion safely without replacing any accepted EP output; it is a technical demo, not an editorial revision of EP258.
- Ruling: duck source audio under active narration; source audio replaces narration only in reviewed speech-free windows. Replacement uses integer 48-kHz sample boundaries to avoid audio-frame overshoot.
- Platform coverage: live YouTube section retrieval verified (3-second 1080p excerpt 988,968 bytes); other public-platform extractors are documented as dependent on the actual link and installed yt-dlp, not claimed tested.
- Plugin validation passes for local use. Existing marketplace-directory warnings: missing license declaration and listing icon; do not invent a license for this repository.

- Final Mac Studio demo verified: 46.4s/1392 frames at 30fps; 15 boundary/hold frames inspected; protected-picture SSIM 0.999314, -17.31 LUFS and -4.25 dBTP. Real-time listening and Patsinee approval remain pending.
