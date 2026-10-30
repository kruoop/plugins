---
name: long-form-video-edit-review
description: "Use when reviewing a long-form video edit before upload."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# Long-form Video Edit Review

Review a completed long-form video as a real media artifact before upload. Produce a grounded diagnosis of pacing, continuity, privacy, audio, and technical integrity. Remain read-only unless the user explicitly asks for an edit.

## Resolve the Correct Artifact

- Enumerate the requested project/episode folder and preserve the exact item identifier.
- Distinguish long-form files from Shorts, vertical/TK cuts, proxies, raw captures, and prior versions.
- When multiple storage roots exist, pair root + exact path; never infer that same-named folders contain the same artifact.
- Verify filename, modification time, duration, dimensions, codecs, and file size before reviewing.

## Full-coverage Review

1. Probe technical metadata.
2. Decode the full file; header probing alone is insufficient. A truncated Matroska chunk can advertise the planned duration and return exit code zero while reporting `File ended prematurely`; require the expected decoded frame count and inspect stderr before accepting it. For independently encoded FLAC chunks, decode audio per chunk before joining PCM: concat-demuxer reuse of the first stream header can produce block-size decode failures even when individual chunks are valid. Preserve the cached video stream, assert exact PCM sample counts against the frame plan, and fail on decoder errors rather than trusting FFmpeg's exit code alone. For interrupted renders, use the scoped recovery recipe in `references/focused-media-revisions.md` rather than restarting the whole edit.
3. Scan for black frames/tail, malformed frames, audio discontinuities, and suspicious static runs.
4. Build timestamped contact sheets covering the entire duration. For an explicit edit-review request, sampling every five seconds is appropriate; increase density around suspect cuts.
5. Extract full-resolution frames at loading states, browser/account surfaces, checkout flows, system dashboards, pairing screens, and the outro.
6. Use local transcription when available to align visual holds with narration and detect likely dead-air. Do not send unpublished media to an external transcription service without consent.

Treat automated scan events as inspection candidates, not edit commands. `freezedetect` can flag normal static tutorials, `blackdetect` can flag intentional dark diagrams with visible labels, and `silencedetect` flags audio below its threshold rather than proving missing speech. Inspect the exported candidate and its source before changing anything; retain valid content instead of re-rendering merely to clear a detector. Label contact-sheet times as sampling bins unless exact source PTS was retained, and use direct seeks or frame indices for frame-specific findings.

## Compare a Replaced Video Before Reusing Metadata

- Preserve a recoverable reviewed artifact and its provider ID/hash before editing. If the owner disallows local backup/version piles, keep the verified reviewed copy on Drive and only the active candidate locally; do not download or duplicate old exports merely to satisfy a naming convention. Never delete originals or the sole recoverable copy. Compare duration, frame count, full decode and decoded PCM hashes; file size alone cannot distinguish a recut from a re-encode.
- If duration or audio changed, align short audio windows across the timeline and inspect matched frames. For a known insert/cut with a verified edit plan, reuse the transcript and remap affected chapters, subtitles and CTA cues piecewise; do not rerun full ASR just because music or duration changed. Unknown recuts or unexplained variable offsets require renewed local transcription and chapter reconciliation, not one global SRT offset. Preserve old transcripts and bind the package validator to the exact reviewed replacement and its timing evidence.
- Recheck the exact remote video hash immediately before delivering metadata. If it changed during review, stop the write and inspect that version too. Identical full decoded audio and duration allow the new ASR/timings to carry forward, but still inspect visual changes and privacy; altered framing is not proof of redaction.
- Keep review corrections in existing deliverables, upload only authorized content files, and verify their original IDs plus read-back byte hashes. Keep comparison logs and source derivatives local rather than creating extra remote companion documents.

## Recovering a newer flattened edit

When Drive has a newer recut than local plans, use that exact export as the picture/audio authority rather than offering an obsolete local version. Search scoped provenance first, then correlate short distributed audio windows with the clean source microphone stem to recover piecewise source offsets. Reject silent-window correlations and numerically invalid normalized scores above one; retain a runnable synthetic-offset check. Quantize candidate cuts to the actual frame clock and validate them against unmasked instructional pixels in the clean screen source across each interval. Do not infer silent insert mappings from audio, and do not replace baked masks until the relevant source frames are verified. Preserve unaffected export pixels, real presenter layers and accepted text graphics; verify all newly exposed privacy regions after restoration.

## Audio QA

Measure, do not guess:

- integrated loudness and loudness range;
- true peak;
- mean/max volume;
- silence or low-activity intervals.

If average speech is low while peaks are already high, do not recommend raw gain. Recommend loudness normalization with limiting, while labeling the target as a delivery recommendation rather than a measured fact.

Distinguish these carefully:

- `digital silence detected`;
- `no speech found by local transcription`;
- `low-level background/system audio remains`.

## Final-export Subtitle QA

- When no timed subtitle source exists, transcribe the exact final export locally with word/segment timestamps; include inserted source-audio excerpts. Padded Qwen/ASR input bounds are not caption timestamps.
- Inspect unusually long word entries and VAD-covered gaps: a full Whisper pass can omit complete clauses while stretching a final subword over the missing speech. Recover these with short contextual crops, preserve raw recognizer wording separately, and use the recovered word times rather than fitting text into an old window.
- Re-crop insert/outro seams when a phrase starts implausibly early. Never restore a word from the longer source when the final insert cuts before it. Cross-check isolated filler words against another recognizer and VAD before captioning background music.
- Preserve paired raw/corrected SRT timing, record every wording change internally, and validate numbering, positive durations, nonoverlap, exact video bounds, and deliberate non-speech intervals. Independently parse with FFprobe. Label model timing estimates and lack of real-time listening honestly.
- Apply owner-confirmed wording literally in the corrected captions, including command slashes and unusual English spelling; do not let a later ASR pass or assumed brand normalization replace it. Preserve raw ASR separately. A wording confirmation resolves that caption question, not independent factual claims about the named product. After cuts, remove deleted words from crossing cues as well as remapping their timestamps; valid SRT syntax alone does not verify spoken content.

## Privacy QA

Inspect the whole interval, not one frame. Common surfaces include:

- browser tabs, address bar, local `file://` paths and OS usernames;
- IP, hostname, server ID, account email/name and order/payment data;
- workflow IDs/names, credentials, internal endpoint URLs and node labels;
- session IDs, Recent Sessions, prompt/message previews and local data paths;
- profile avatars/names and notification counts;
- QR codes, pairing tokens, OTPs and authorization states.

Never reproduce a readable secret in the report. Name the category, timestamp interval, and blur region. Pairing QR codes must be redacted for their full visible interval.

Evaluate privacy coverage throughout each shot, not only at its start: dialogs, scrolling and desktop switches can reveal data inside an otherwise safe shot. Inspect the pre-dialog list, open dialog and closing transition separately. Apply masks to the screen layer before compositing the presenter so a sidebar mask cannot clip the face circle. Do not automatically conceal a private desktop transition with full-frame presenter footage: this defeats the channel's screen-first layout. If the user requests removal of that shot, locate its complete visible interval and cut it at speech-safe boundaries; otherwise flag the interval and use only the scoped protection allowed by the active brief. Verify the encoded interval boundaries and interior before rebuilding other shots.

For BoomBigNose screen tutorials, preserve the instructional UI: do not blur an entire webpage merely because it contains a credential field. Prefer tightly scoped soft blur over large opaque black rectangles, preserving navigation and demonstration controls. A request to reduce censorship is not permission to expose receipts, other people's private data or complete credentials; retain those protections and explain the remaining regions briefly. Redact the readable complete key/secret with a tightly fitted region for its full visible interval; do not cover adjacent headings or controls. Do not add redundant blur to a key already masked or genuinely incomplete, but inspect surrounding frames and scrolling to ensure separate views cannot reveal the complete value. This exception concerns keys, not passwords, OTPs, payment details or other private information. Treat OCR/privacy detections as candidates requiring visual confirmation, not automatic proof that every detected region needs a mask. Distinguish reduced censorship from an explicit request for an unredacted private review: scope the latter to that version, do not turn it into a standing no-privacy-check rule, and retain a timestamped risk report and the publication gate. Never attempt to reconstruct information already obscured in source media. When editor-added masks are intentionally disabled, assert their absence in the actual render graphs and inspect the resulting frames instead of claiming that the file is free of sensitive information.

## Editorial Checks

Evaluate:

- hook length and time-to-value;
- whether prior-episode references prevent the video from standing alone;
- loading/skeleton screens and cursor waiting;
- long static screens relative to ongoing narration;
- false endings, such as saying goodbye before another promo section;
- promo/outro length and CTA readability;
- changing claims such as price, discount, date, or availability;
- final-frame cleanliness and black tail.

Separate **must-fix defects** from **retention recommendations**. A visible pairing secret or broken audio is a defect; shortening a hook is an editorial recommendation.

## User-directed Revisions and Handoff

1. Resolve the exact reviewed version before applying timestamped feedback. Treat the user's times as positions in that version, then map them to the editable source/timeline; report changed positions when a cut shifts later content. A mismatching local timeline is not itself a missing-source blocker: inspect the authoritative Drive episode originals, recover piecewise source offsets with normalized audio correlation, and validate unmasked screen pixels at frame resolution against the current export. Exclude near-silent windows from correlation normalization. Preserve the current edit and patch only authorized regions; never substitute an obsolete export. For concatenated H.264 chunks whose stream parameters vary, tile/fps filters can reset and silently omit visual coverage despite a valid final frame count; validate continuous PTS and build independently sought, timestamp-labeled samples. Bound boxblur chroma radius by the actual cropped chroma dimensions, especially for narrow identity fields.
2. Preserve the reviewed artifact under the active storage policy and reuse its project, edit decisions and verified checkpoints. Render one explicitly identified active derivative without overwriting the sole reviewed copy or rebuilding unrelated assets. Do not create local backup/v1 piles when the owner has excluded them; retain source preservation and exact-artifact QA.
3. Keep Long and Short briefs separate. For this channel, center the host within the intended camera panel/crop in both formats; verify the rendered face position rather than assuming a centered source crop centers the person. Apply logo/music changes only to the formats requested.
4. For a requested cough/throat-clear removal, listen around the reported time, remove the actual event without clipping nearby words, and check both sides of the rendered seam for audio/video continuity and sync.
5. When asked for a larger BoomBigNose+ logo, enlarge the existing official asset without redesigning the layout or obscuring content. Use a genuine high-resolution asset rather than enlarging a captured webpage logo. When asked for quieter music, reduce the music track rather than the complete mix; listen with speech and report the actual adjustment, not an invented target.
   - For BBN screen tutorials, keep the normal instructional screen with a small circular host camera; do not introduce full-face emphasis cuts unless requested. An explicit no-full-face revision means zero full-face frames, including greetings, private desktop transitions and the outro—not merely fewer cuts. Assert that count from the edit plan and inspect the newly exposed screen intervals; previous camera coverage may have concealed receipts or private lists. Preserve separately requested illustrative footage rather than replacing unrelated inserts.
   - Resolve music cues independently from the cached transcript and frame plan: intro, Skool and company/Workshop are not interchangeable. Restrict the music stem to the requested sections rather than leaving a quiet bed across the tutorial. If the named promo is absent, clarify only that cue while continuing independent edits; do not silently substitute a different promotion and explain it only after rendering. Use the intro track for Skool when requested, and keep Workshop without added music when directed. A later cue decision replaces earlier missing-track requirements; update the current package status instead of continuing to request the canceled asset.
   - When the owner asks for an opening preview like a previous EP, inspect the actual reference opening and distinguish a standalone motion preview from the spoken hook. Reuse supplied footage with its original labels and attribution, then map the added duration into the existing timeline; a hook label alone does not satisfy a missing-preview correction.
   - For specified screen-only result/waiting intervals, omit the host layer for the complete requested shot, not just one sampled frame. Keep a small circular host over the instructional screen elsewhere unless the brief says otherwise.
   - Enlarge and position the existing Like/Subscribe artwork by its visible bounds, not just the surrounding green-screen canvas. For a bottom-center request, check entrance, click/bell states and exit for centering and clipping, and raise its SFX stem independently of narration when the effect is too quiet.
   - Resolve “output/result” from the owner's demonstrated workflow before requiring a standalone export. For this channel, the result visible in a CapCut screen recording can be the intended deliverable; inspect that existing footage first rather than blocking on another file. Once the owner identifies it, use that recording, label it as an on-screen result, and clear the missing-export blocker. Never substitute another creator's demo or imply that a paused/scrubbed preview is a finished exported video.
   - Place the result at the actual requested end position: use the transition into the closing by default, but append it after the farewell when the owner wants a final result showcase. Preserve its native aspect ratio and requested source audio; omit the presenter for a result-only close-up. Inspect through the last frame and exclude accidental editing states such as a newly inserted placeholder heading. Do not stretch or loop a still to fabricate playback. Remap moved material, captions and CTA anchors from the current reviewed timeline.
   - Make an “exciting highlight” through short, truthful reaction → action → result cuts and legible concise text, not by making the music louder. Use cached speech boundaries so the reaction is a complete phrase. If only opening music is too loud, adjust that bed independently and preserve the body, promo and SFX mix; audition a short opening candidate before another full assembly.
   - Reuse completed mixes after an interrupted run; verify the latest artifact before adding music again. An audio-only correction should preserve the picture stream without re-encoding. For insert verification and source retrieval, use `references/focused-media-revisions.md`.
   - Before asking the owner to resend a missing Like/Subscribe animation, inspect existing shared assets and suitable older channel exports. Prioritize an owner-supplied clip and timestamp over broad searches. If the original graphic can be cleanly isolated, reuse it without the old presenter, background or mixed narration; retain the current episode's voice and re-encode only affected picture shots. See the CTA recovery recipe in `references/focused-media-revisions.md`.
6. Recheck privacy after reframing and cutting: a new crop or shifted timeline can invalidate old mask coordinates and intervals. Inspect complaint locations before/after, plus the complete resulting files.
7. Before handing editing between agents/apps, confirm the actual owner and checkpoint. A request to wait for the current version to finish forbids immediate takeover. A later instruction that the episode is finished cancels stale recovery work; do not restart it on a delayed reply.
8. Report only the stage evidenced: message accepted, worker active, render complete, or QA complete. A relay exit code proves message delivery at most; a heartbeat does not prove rendering, and a timeout does not prove the worker stopped. Attribute another agent's report until independently verified. Never promise automatic completion alerts without a verified notification path for the actual owner. Match delayed process notices to recorded process IDs: do not restart a failed attempt whose replacement already succeeded.
9. Follow the requested delivery order and send each completed, checked piece without waiting for the whole EP. When the owner explicitly asks to inspect the current Long on Drive, deliver the existing version as a private review copy even if subtitle wording or perceptual audio review remains pending; clearly name those limits rather than claiming final QA. Resolve the exact EP folder, upload only that requested file without changing sharing permissions, then read back its provider ID, size and checksum before giving the review link. A review-copy request does not approve publication or authorize more editing.

## Report Format

Lead with one decision:

- `ready from an edit-QA perspective`;
- `should be revised before upload`;
- `not safe to upload yet`.

Then provide:

1. strengths;
2. must-fix issues with verified timestamps;
3. optional pacing/retention improvements;
4. measured technical facts;
5. explicit note that no edit or publication occurred.

See `references/screen-tutorial-review-checklist.md` for a compact operator checklist.

## Budget-conscious BBN production

- Treat the owner's usage cap as one budget across the entire EP, all deliverables and every correction round. Establish the quota window, initial remaining percentage and agreed interpretation of the cap before substantial model work; retain that baseline through retries and version changes. When the agreement is a maximum percentage-point drop, compute the remaining floor from that original baseline with code. Read supplied usage screenshots rather than continuing to claim no baseline exists; never convert token counts into subscription-quota percentages.
- Reuse verified downloads, transcripts, edit decisions, privacy findings and checkpoints. Send only relevant evidence to AI calls; avoid unnecessary subagents, repeated full-context reads, retranscription and renders of unaffected material. Keep full safety and final-export QA.
- Report input, output and cache-read counters separately with their actual session scope. Do not attribute all usage of a session to an episode merely because it mentions that episode. Distinguish main-session totals from a verified complete total including child sessions; never double-count cache fields or infer quota percentage from token totals.
- Measure account-quota before/after when available and identify the quota window; label contamination from concurrent jobs and reset boundaries. If no baseline exists, state that episode-specific percentage is unknown rather than estimating it as fact.

## Original-voice and official-insert revision checks

- For hiss corrections, denoise the unmixed microphone stem, measure matched quiet and voiced windows, then measure filter latency by distributed correlation and compensate it before applying the shared cuts. Preserve exact sample length; normalization alone is not denoising. Use smooth attenuation rather than assuming a hard gate is harmless, and do not claim listening from ASR or waveform checks.
- When a user still hears noise after a measured reduction, compare new candidates against the rejected version at matched voiced RMS; inspect residual frequency bands before strengthening processing. Separate source-only noise tests from retained-output tests: a quiet source window removed by the edit cannot validate final audio. Save bounded A/B samples and keep perceptual acceptance explicitly unresolved without listening.
- For promo-only music, derive the complete spoken promo range from transcript plus final frame plan, including internal camera bridges but excluding unrelated screen inserts and the farewell. Assert exact-zero music-stem samples outside that range and compare encoded in-promo music contribution with the prior mix; a raised pre-master fader alone does not prove a louder delivered bed.
- For an uncertain product name, reconcile contextual local ASR with a first-party model card before adding version-specific media. Distinguish an official still showcase from motion footage or a live run; neither proves performance on the presenter's device.
- For power-consumption inserts, preserve the actual published table's mode, units and configuration context and explicitly separate manufacturer data from a measurement of the featured device. Never turn an idle specification into an AI-load benchmark or invent a meter display.
- When a final black scan locates a gap inside genuine external footage, inspect the source transition. Select a clean semantic source range where appropriate, rebuild only that affected picture shot and its downstream assembly, then fully decode the final. If narration is unchanged, verify complete audio packet identity to reuse already completed seam ASR.

## Completion Standard

Do not finish after viewing only an opening frame or a sparse timeline. The review is complete only after full decode, full-duration visual coverage, audio measurement, targeted full-resolution inspection, and a timestamped risk report.
