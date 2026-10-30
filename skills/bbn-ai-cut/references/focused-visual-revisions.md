# Focused visual revisions

Use this reference when the current request changes selected pictures, typography or inserts in an existing BBN export. Read the accepted version and latest brief before applying the full-edit workflow. Channel appearance remains governed by [channel editing and sound](channel-editing-and-sound.md); shared clocks and ordinary export checks remain in [editing and verification](editing-and-qa.md).

## Lock the current scope

The latest instruction can narrow an earlier speech/body review to a picture-only interval. In the EP211 revision, the final scope was **only 0:31–0:57 pictures**. This is a scope example, not a default interval for other episodes. Preserve the original speech, music/SFX, timing and approved shots elsewhere. Keep an existing matching Short and accepted metadata unless the changed content or timing actually affects them. Do not restart the earlier broader review after a narrower instruction.

Record the accepted input, requested interval, allowed visual changes and output filename in the episode's revision evidence. Convert the interval to **half-open integer output frames `[start_frame, end_frame)`** using the declared rational FPS and an explicit rounding rule. Reuse the accepted output clock; do not invent a new source offset or shift later cues. The visible revision interval and the larger encoding span needed for safe GOP boundaries are separate: any surrounding re-encoded frames must still show their original pictures at their original times.

Find speech cues using the cached transcript, existing source/output mapping and bounded review of the relevant passage. A transcript crop or ASR word estimate is not frame-exact speech evidence. Inspect the actual cue neighborhood; use a local waveform/ASR crop only if uncertainty needs resolving. A picture-only change does not require full transcription, speech cuts, denoise, normalization or a new audio mix.

## Choose pictures that match the brief

- Reuse approved website footage for actual UI and results. An illustration can explain the idea beside it; it cannot establish that a product or website performed the shown action.
- For an authorized workshop promotion, show the actual current workshop page over the original invitation voice. Verify the selected page and its visible offer; do not import an older episode's promotion or replace the speech with new narration.
- When the user rejects a photo or recognizable logo over an image-use concern and requests an original replacement, replace that whole asset with a new original illustration. Cropping, recoloring, tracing or covering part of the rejected image does not fulfill that brief. Avoid recreating its identifiable logo in the illustration. This applies to the rejected asset; genuine requested product/BBN logos remain governed by the existing sourcing rules. Original generation is not an automatic legal guarantee.
- Use an available image-generation tool for the requested new illustration. Inspect the completed output before integrating it and retain its prompt, tool, source inputs and output path in episode provenance. A queued request or unfinished generation is not an asset. A generated still animated in the compositor remains an animated illustration; do not describe a poster as generated video or motion.
- If the user changes the selected asset or approach, stop using the superseded generated take. Preserve it in an archive, remove it from the active composition/delivery selection and verify that the new export uses the current choice.
- Keep unrequested editorial update/date/model/provenance notices out of the picture. Store production details in project records; an internal correction does not require an on-screen announcement. Preserve required credits, relevant spoken-topic captions and information naturally present on the real recorded page.

## Deterministic typography and inserts

Use the existing HyperFrames/GSAP stack and its applicable skills when that is the project's animation path. A list mentioning Remotion, Motion or Anime is not a requirement to add every library. Reuse installed fonts, assets and the current composition before introducing another renderer or dependency.

Anchor each graphic to an integer output-frame event. Seek the paused composition explicitly from `frame / fps`, with a declared local offset when rendering a segment, so preview and export evaluate the same state. Give kinetic typography real phrase assembly, stagger, reveal or a short spring-like settle, followed by a stable readable hold and clean exit; a static title with an occasional opacity change does not fulfill a requested kinetic treatment. Animate complete Thai words or safe grapheme groups rather than splitting combining marks.

Retain clean white supporting text, yellow highlights/underlines and **exactly 25% backing fill opacity**, with the existing modest shadow. Apply opacity to the backing only. Check Thai marks, underline clearance, text/backing bounds and maximum overshoot through entrance, hold and exit. Keep the face and necessary UI clear throughout the movement, including transitions between scenes. Improve placement or scale when needed instead of increasing the requested backing opacity. A picture-only revision keeps the original sound even when the new motion would normally invite an accent.

### Rendering failure modes observed in EP211

- **FFmpeg 9 durations:** use a leading zero in duration options, such as `0.18`, rather than `.18`; the latter failed in the tested fade invocation. Verify the installed filter's accepted syntax.
- **Paused GSAP timelines:** a timeline is thenable. A browser seek callback must return void, for example `() => { timeline.seek(t); }`; returning the timeline can leave the caller awaiting completion of a paused animation.
- **PNG sequence clocks:** render a bounded, continuous numbered sequence on its declared frame clock. Include transparent padding for inactive overlay frames, or explicitly preserve the segment offset; do not collapse gaps and shift later stills. Bound still-image input lifetimes and verify the first/last numbered frames so a shifted input or unbounded still cannot stall the render.
- **ExFAT sidecars:** count only the expected numeric frame filenames. Ignore `._*` AppleDouble files rather than counting every `*.png` as a rendered frame.

## Patch MP4 pictures only when compatible

Stream copying the unaffected video avoids unnecessary encoding, but codec names and a container keyframe flag alone do not prove a safe splice.

1. Probe the accepted export's **actual IDR positions**, B-frame use, AVC configuration/extradata, pixel format, dimensions, frame rate, time base and relevant stream parameters. Verify random-access boundaries from the bitstream. Enclose every affected GOP: decode from a valid preceding boundary and end the patch at a valid following boundary, preserving the untouched pictures within that enclosing span.
2. Encode only that video patch with compatible parameters and exact planned frame count. Prepare the prefix/patch/suffix inputs, then inspect **the actual files that will be concatenated**. Matching the original file alone is insufficient if segment creation changed their AVC configuration.
3. FFmpeg concat `auto_convert=1` can inject SPS/PPS and change packet bytes. Use `auto_convert=0` **only if every actual concat input has byte-identical `avcC` extradata, zero B-frames and compatible stream parameters**. Never disable conversion blindly to make a hash check pass. If safe compatibility cannot be established, use a proper full video encode and report that the outside video is re-encoded; do not claim packet identity for that fallback.
4. Assemble the video first, then perform a separate final mux with **the whole original mastered audio stream copied unchanged** (AAC in the tested MP4 workflow). Preserve its packet timing and required timing metadata. Do not cap this mux with `-frames:v`, `-t` or another stopping condition that can truncate the audio tail. The video assembly already owns the target frame count; verify the final mux instead of cutting audio to fit a nominal container duration. For another audio codec/container, verify that exact stream copying is supported rather than silently transcoding it and claiming identity.

Use a new versioned output and preserve the accepted export. A successful concat/mux or a playable opening is not proof that the remaining packets or final audio survived.

## Verify the actual final and preview

Reuse valid evidence for unchanged source content and checks. Add the checks needed to establish the revision and its preservation claims:

- Fully decode the final MP4 and supplied preview. Compare decoded frame counts and stream durations with their plans; inspect the complete expected PTS sequence and continuity across every join, plus DTS/reordering as applicable. Use exact rational clocks and justified codec/sample tolerances, not a duration tolerance large enough to hide a missing frame.
- On the stream-copy path, compare **all outside-patch video packet payload hashes and timestamps** with the accepted export. Compare **all original-audio packet payloads and timestamps**, including the tail, to prove unchanged audio; account for codec timing metadata where applicable. Similar duration, an unchanged audio codec or a few matching samples is insufficient. On a full-video-encode fallback, replace the impossible copied-video hash claim with appropriate frame/timing comparisons; the original audio preservation check still applies.
- Confirm that preview pictures correspond to the claimed final interval and frame offset. Prefer deriving the review preview from the completed final; account for codec differences when an independently encoded preview is compared. A separate composition preview alone does not establish final output quality.
- Inspect encoded entrance/hold/exit states for every revised visual, plus the adjacent seams. Check actual motion, Thai spelling/marks, face/UI clearance, requested asset choice and absence of superseded imagery or unwanted notices.
- Compare the re-encoded GOP edges with the accepted frames at the same moments. Inspect edge MAE and nearby candidate frames, then use a low-frequency/downsampled comparison and visual context when codec grain makes an adjacent frame look numerically closer. Do not infer a one-frame shift from raw pixel error alone, and do not dismiss a real timing mismatch as compression without checking it.

Record measured checks, visual inspection and actual listening separately. Packet identity can prove preservation of the accepted audio without a new full ASR pass; it does not turn earlier unlistened audio into a listening claim. Once relevant checks pass, deliver the revised file and useful interval preview, preserving valid existing Short/text deliverables. Keep evidence in the episode and update its memory; do not copy media or transcripts into this skill.

Evidence, captured in the 2026-09-13 skill update: `/Volumes/BoomBigNose/EP211/work/full-edit-v4/` contains `qa/focused-validation.json`, `qa/visual-review.json`, `qa/edge-1710-diagnosis.json`, `qa/concat-probe/result.json`, `kinetic-type/provenance.json` and `ai-original/provenance.json`; implementation/check entry points are `/Volumes/BoomBigNose/EP211/scripts/intro_v4.py` and `check_intro_v4.py`. These are episode evidence references, not fixed frame counts, ports, encoder settings or model presets for new work.
