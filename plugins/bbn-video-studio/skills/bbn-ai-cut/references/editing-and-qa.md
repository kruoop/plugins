# Editing, frame plans, and verification

## Cost-aware iteration

Use local deterministic work for media analysis and rendering; do not spend language-model context rereading raw FFmpeg logs, full transcripts or unchanged project history. Maintain one small current-state JSON or Markdown record with source hashes, reviewed export, accumulated brief, canonical plan, accepted assets/stems, open defects and the paths of valid evidence. Update it after each accepted revision. Keep detailed logs as evidence and open only the relevant range when a failure needs diagnosis.

Keep a short requirement-to-evidence checklist in that record, including every requested deliverable and any unresolved limitation. Choose the smallest operation that covers the change: remux unchanged streams, remix an affected stem, patch a reviewed interval, then use a full render only when required. Invalidate caches and dependent checks when their actual inputs, settings or timeline change; otherwise reuse them. Retry only after diagnosing a failure and changing its cause, or for a bounded transient-error retry. A sound-only correction needs its changed cues and speech boundaries reviewed, not a new visual review bundle for identical pictures with valid prior QA.

For unchanged sources, reuse the transcript and alignment cache. Use the primary transcript for the whole episode once; use independent ASR, CTC and waveform work only for ambiguous phrases or cut boundaries. Reuse accepted graphics, renders and QA by content hash or authoring state. Do not regenerate an image, shot, stem, Short, thumbnail or metadata field merely because another interval changed.

Accumulate all feedback received for the reviewed version before compiling the next plan. For a full edit, derive Long and Short from the same source evidence but give each its own output plan. One compact review bundle per changed output may concatenate short excerpts; keep enough preceding and following context to judge each edit. Include:

- the full opening and its transition into the lesson;
- every new speech cut, edit seam and user-reported timecode;
- every changed overlay through entrance, complete spoken hold and exit;
- layouts where narration names visible left/middle/right items, presenter moves or CTA placement;
- each changed music/SFX cue with the preceding and following speech;
- the ending, plus source/output crops that expose any clarity loss.

The bundle must use the same plan, crops, captions, assets and mix as the final. Accept it only when (1) the retained speech before and after every cut forms complete clauses, without an accidental repeat, missing number/word, or editor aside; (2) the shown screen action matches references such as left/middle/right and remains visible; (3) the face, CTA and text stay clear of needed UI, with each text cue held until the spoken clause ends; and (4) voice, music and SFX enter and end at the intended beats, without a masked pause or lingering bed. Compare a source frame with its output counterpart for clarity. For a Short, also inspect the first sentence, final CTA, complete upper screen, face clearance and captions at phone size. Fix only failed excerpts before a full encode. Then encode each deliverable once, decode it once and run its final distributed checks. A new full encode needs a changed canonical plan/asset/mix or an actual final-file defect. For a local defect, prefer an interval patch that preserves accepted streams outside it and verify both boundaries; use a full encode when patching is unsafe.

Stop when the current brief's checks pass. Do not create another version for speculative polishing, duplicate evidence, or a different filename alone.

## Synchronization and layout

Extract analysis audio from both recordings and estimate normalized cross-correlation over several spaced speech windows. Record each offset and correlation, choose the sign convention explicitly, and check residual drift. Silence or unrelated audio can give a spurious peak. A measured offset from an earlier project is never a preset for new footage.

Inspect the screen's important text and the presenter's movement. For a 1920×1080 output, a circle around one quarter of the output height with roughly 24 px margin is a useful starting preview, not a fixed layout. Find a square camera crop containing the whole face through movement. Render a supersampled antialiased circular alpha mask with Pillow, optionally add a thin border/shadow, and composite with FFmpeg `alphamerge` and `overlay`. Rebuild masks when diameter/style changes; a filename-only cache can reuse the wrong size.

Fit the screen at its original aspect ratio and preserve legible UI. Scaling a 720p screen to 1080p adds no native detail. Change the circle corner or size if it covers relevant content. Keep intentional zooms or layout changes tied to the brief.

## Portable plan compiler

The bundled `scripts/compile_edit_plan.py` needs Python 3.9+ and only the standard library. It consumes **already reviewed** cut intervals. It does not make editorial choices, decode media, infer synchronization, or render video.

Example input with synthetic times:

```json
{
  "fps": "30",
  "source_duration_seconds": 12,
  "source_start_seconds": 0,
  "source_end_seconds": 12,
  "screen_duration_seconds": 13,
  "sources": {"camera": "Footages/camera.mp4", "screen": "Footages/screen.mov"},
  "sync": {"screen_offset_seconds": 0.5},
  "cuts": [
    {"start": 3, "end": 4.2, "reason": "reviewed restart", "evidence": "work/seam-001.json"},
    {"start": 8, "end": 9, "reason": "reviewed wait", "evidence": "work/seam-002.json"}
  ],
  "layout": {"canvas_width": 1920, "canvas_height": 1080},
  "audio": {"sample_rate": 48000, "target_lufs": -16, "true_peak_dbtp": -1.5}
}
```

Invoke using the actual installed skill path:

```bash
python3 /path/to/bbn-ai-cut/scripts/compile_edit_plan.py \
  --input work/reviewed-cuts.json --output work/edit-plan-v2.json
```

Use rational FPS strings such as `30000/1001` when applicable. Output includes `segments` with `start_frame`, `end_frame` (exclusive), `output_start_frame`, and `frame_count`, plus `start_seconds`, `end_seconds`, `output_start_seconds`, `duration_seconds`, and plan-wide `total_frames`. Top-level descriptive metadata is retained; media paths remain as supplied. Resolve those paths against the owning project when rendering, not the shared skill directory. Existing project renderers may use a different schema; adapt them explicitly rather than assuming this JSON is a drop-in replacement.

Retained intervals are rounded inward: ceil at their start and floor at their end. This avoids reintroducing explicitly cut material, but can remove a partial frame at a boundary. Inspect the actual quantized gaps before accepting the plan, especially around adjacent syllables. Do not blindly assume fractional timestamp changes are inaudible.

The compiler rejects nonfinite numbers, overlapping/out-of-range cuts, empty output, and a selected source range that maps outside known screen bounds. Supply the probed `screen_duration_seconds` for upper-bound checking. For a negative screen offset, explicitly select a valid camera source start; do not silently truncate the original. Inspect speech outside the shared range. If it matters, preserve a camera-only lead/tail in the final composition and account for its frames/audio on the same output clock; this helper compiles only the shared-source portion. Existing output is protected unless `--force` is requested. The input is never an output target.

## Rendering from a shared clock

Use the integer frame intervals as the authority for both pictures and audio. Inspect exact rational rates/time bases from ffprobe; do not substitute decimal `29.97` for `30000/1001`. Choose one output clock and normalize **every video input** to that FPS before applying shared frame selection, including two constant-rate recordings with different rates (for example 30000/1001 camera and 30 screen), as well as variable-rate recordings. Applying identical native frame numbers to unequal rates produces drift.

With a fixed screen offset, seek the screen to `camera_start + offset` and camera to `camera_start`, after validating nonnegative mapped times; do not apply the offset twice to an already aligned audio master. If the screen recording began 1.2 s later than the camera, the convention here requires an offset of **−1.2 s**. Respect the frame-number origin if selecting after a seek.

Treat genuine recorded demo/MV playback as an explicit audio cue in both Long and Short before accepting the preview. A camera-only voice master can omit desktop music even when sync and loudness pass. Locate the actual screen-recording audio on the current output clock; use its isolated desktop stem when available, or its verified mic-plus-desktop mix only within the example span without doubling the same narration. Preserve native playback speed and verify the source audio actually reaches the encoded export, not only the plan.

Use one clean aligned audio master, preferably 48 kHz PCM, rather than mixing the two microphones. Handle PCM dtype correctly: SciPy reads 24-bit PCM as left-justified int32, so scale by `2147483648`, not `8388608`. Do not apply that rule to int16 or float WAVs.

For fractional FPS, **do not use `sample_rate // fps`**. Compute cumulative output audio boundaries with rational arithmetic, such as `round(output_frame * sample_rate / fps)`, then derive each segment's sample count from the difference of adjacent boundaries. Resample/pad only the necessary sub-sample rounding and verify the final duration. At 48 kHz and 30 FPS there happen to be 1600 samples per frame; that shortcut does not generalize.

Use brief in-place fades at audio cuts to reduce clicks without shortening the timeline. The tested workshop used 4 ms seam fades, 18 ms at the beginning and 60 ms at the end. Adjust if they soften a needed consonant. Do not crossfade overlapping durations without accounting for the resulting clock change.

For a newly built or changed mix, run two-pass FFmpeg `loudnorm` when appropriate. A spoken-video starting target is −16 LUFS, −1.5 dBTP. Measure the encoded AAC output because encoding can create inter-sample overshoot. Handle silence/nonfinite loudness explicitly; do not feed `-inf` measurements blindly into pass two. Parse FFmpeg's JSON with `JSONDecoder.raw_decode` or a bounded JSON parser because logs can contain trailing text. For picture-only changes, preserve the approved mastered audio and prove identity instead of normalizing it again.

The verified baseline used FFmpeg 9.0.1, `h264_videotoolbox`, 1080p/30, 10 Mbps target / 16 Mbps max, yuv420p, BT.709, AAC 192 kbps/48 kHz, and `+faststart`. These are a reference export profile, not mandatory settings for other source resolutions or platforms. Probe the actual encoder; use a local software encoder such as `libx264` if VideoToolbox is unavailable. FFmpeg 9 removed the old `-filter_complex_script` option; the tested render passed the graph via `-filter_complex`.

Render to a new versioned filename. Inspect a representative preview before a long encode. Preserve original footage, previous exports, the selected-cut file, the compiled plan, and the render command/settings.

Normalize actual pixel range, pixel format and color interpretation across video inputs before concatenation/compositing, then write consistent metadata. Merely tagging full-range samples as limited range is not conversion. Mixed full/limited-range inputs caused filter reinitialization and duplicated/dropped frames in a tested FFmpeg workflow; check final timestamps and decoded counts as well as color tags. Preserve camera-only grading and genuine screen colors.

Cache derived shots only against their actual inputs, render settings and authoring state. When an image, PNG sequence or HTML changes at the same path, invalidate that shot and its downstream composites; a filename or unchanged command alone does not prove the media cache is valid. Preserve the superseded draft and avoid rerendering unrelated shots.

## Focused visual revision checks

Read [focused visual revisions](focused-visual-revisions.md) for picture-only time ranges, motion/text changes, rejected imagery and website replacement. It owns the verified MP4/GOP/AVC compatibility checks, complete AAC reuse, frame-exact preview placement, deterministic graphics pitfalls and boundary verification. Keep those mechanics in that reference rather than duplicating episode render scripts in this shared skill. Reuse an existing project renderer where it satisfies those invariants; the portable speech-cut compiler is not required for a picture-only patch.

## Optional HyperFrames companion

Generate the companion from the canonical frame plan, with the same source time mapping. Use muted video elements and one separate audio element per segment to avoid accidental doubled audio. Serialize shared boundaries consistently; independently rounding each start and duration to six decimals caused false microsecond overlap reports.

Use relative media references or symlinks only when appropriate to the project's layout. Do not install/update dependencies through a shared `node_modules` symlink. Run the composition's applicable checks and inspect snapshots after HTML changes.

If the companion uses source audio while the MP4 has fades/normalization, document that difference. A verified companion preview does not mean that every frame of it was rendered, and its audio does not automatically equal the exported MP4.

## Music claims and local audio revisions

1. **Identify the reviewed input and requested result.** Reuse its manifest and downloads only after matching the supplied file ID/version and content hash; stale local exports may have different music or timing. Record the requested cue and, when accessible, the actual platform claim's track, affected interval and status. “Ineligible to earn” alone does not identify the cause. Missing platform details need not block an explicitly requested, locally identifiable music removal.
2. **Choose the authorized local correction.** The latest request to remove a song supersedes an earlier preference to keep it. Edit the file directly by default; use Studio editing only when explicitly requested. Read-only claim inspection is separate from applying an irreversible platform edit. If a platform job was already submitted, record its state honestly and continue independent local work without repeated waiting or implying it was canceled.
3. **Preserve speech first.** Prefer the original separate voice/music/SFX stems and exact timeline. Remove or reduce only the requested music stem. With mixed audio, mute an interval only after establishing that it contains no wanted speech or effects; claim timestamps, VAD silence or music correlation alone are insufficient. Inspect context at both ends and use source/transcript evidence. If speech overlaps music and clean stems are unavailable, try an available local separation tool on a short affected crop, check intelligibility and residual music/artifacts, then process only necessary intervals. Do not replace uncertain speech with silence or claim perfect separation.
4. **Keep the picture and clock intact.** Unless the user requests a picture/timing change, stream-copy the complete video and retain its timestamps. Build the revised audio from the best original master rather than repeatedly encoding prior revisions; encode audio once for delivery. Use brief boundary fades only where they preserve syllables, retain wanted SFX and closing speech, and avoid global normalization or tempo changes unless needed for the requested correction.
5. **Verify the actual export once.** Check removed/changed music and both boundaries, compare unchanged voiced windows for level, intelligibility and alignment, measure encoded peak/loudness, and run the final decode/duration checks below. For copied video, compare packet payloads and timestamps/frame count to the reviewed input and reuse its still-valid visual QA. Container hashes will change after an audio edit; lossy audio re-encoding need not preserve PCM identity. Record actual listening separately from waveform, ASR and correlation evidence. Fix failed intervals rather than restarting unrelated checks.
6. **Deliver and distinguish outcomes.** Preserve the original and earlier local revisions, update the current manifest, replace the same owned Drive file when authorized, and verify remote size plus checksum or downloaded readback. Do not regenerate unchanged thumbnails, Short or text metadata for a timing-preserving audio-only request. Report “file edited and verified” separately from “platform claim cleared”; only a completed platform check establishes the latter. Do not upload/publish/create a platform draft or activate monitoring without authorization.

Lowering volume, shortening a song or changing pitch/speed does not establish usage rights or guarantee claim removal. Honor an explicit gain/duration request while stating that limitation; do not cycle through attenuations as a substitute for removing or licensing the music. For a requested replacement, use an asset with verifiable terms covering the intended use and keep license/attribution evidence; a filename saying “No Copyright” is not evidence. Never promise a claim-free result before platform verification.

## Focused sound revision checks

- Compare matched quiet and voiced windows before/after denoise for each microphone source. Measure actual noise reduction, speech-level change, filter delay and output sample length. Compensate measured delay with adequate tail padding, then verify distributed alignment; exact duration alone does not prove sync. Choose settings from the current recording, not a previous episode's numbers.
- Keep voice, music and SFX separate through tempo and noise processing. Compare source music windows at native speed and preserve unchanged music regions; a correct total duration or manifest cannot prove the song was not accelerated.
- Locate each requested cue in the reviewed version and remap it to the revised picture clock. Check the actual encoded neighborhood for the effect and its complete tail below intelligible speech. For a weak existing cue, change its gain once; do not layer a second full copy. A sound listed in the edit plan is not proof it reached the export.
- Review the encoded opening, restored greeting/name, lesson entry and both joins of each replacement recording, including its own narration and screen action. Reuse source transcripts and make bounded independent ASR/waveform comparisons where wording is uncertain. Product-name spelling variance alone is not a speech defect; do not alter original words simply to satisfy an ASR model.

Record which checks were measured, visually inspected, recognized by ASR or actually listened to. Run the ordinary final-export checks below, reusing existing evidence for unchanged pictures and source intervals when it remains applicable.

## Verification evidence

- Decode the whole completed file once with FFmpeg error detection; compare actual decoded frames to `total_frames`, not only the container's header count.
- Compare video duration to the rational frame duration; compare audio duration and A/V difference with a justified time-base/codec tolerance. At fractional FPS, an audio sample boundary cannot always equal the video boundary exactly. Do not hide a missing frame behind a large tolerance.
- Verify the requested dimensions, aspect ratio, FPS, codecs, audio sample rate/channels, and finite loudness/true peak. For exact reused mastered audio, retain its valid loudness evidence and verify complete packet/sample identity. Use the current export profile rather than hardcoded 1080p/30 checks.
- Inspect distributed contact frames for black/frozen sections, face cropping, occlusion, and screen readability. Generated contact sheets are not automatically visually reviewed.
- For selected speech cuts, compare source neighborhoods with output neighborhoods using context, waveform, and independent local ASR; inspect both ends of removed phrases. Listen when playback is available and report it accurately.
- Distinguish file-integrity results, visual inspection, ASR comparison, and human/real-time listening. None alone proves all of the others.

Write the evidence report and contact sheet into the project. Do not claim zero editorial errors, measured Thai recognition accuracy, or listening that did not occur. Stop broadening tests when relevant checks pass and no unresolved concern remains; deliver the completed artifact.
