# Focused music and real-demo revisions

## Resolve and reuse

1. Probe the reviewed export and latest derivative, then read the existing cue map, mix stems and QA report. If rendering completed but reporting failed, verify that file rather than repeat the render.
2. Write the current brief as separate music, insertion, screen-only and speech-cut intervals against the reviewed artifact. Preserve a recoverable prior export according to the active storage policy; a verified Drive copy does not require another local backup. Resolve the actual named promo before assigning its music cue. Remove superseded pending requirements from the current status while retaining historical notes as history.
3. For music-only work, mix the selected native-speed track beneath speech with gentle fades and ducking; retain the original voice/SFX master outside the cue. Mux with `-c:v copy` and check the copied video payload hash.

## Resolve a supplied editing pack

1. Inventory archive entries before installing anything; read the applicable editing instructions and distinguish recipes from actual media assets. A pack that describes a Subscribe animation does not establish that the animation is included.
2. Check the existing project assets and the exact authorized shared-assets folder for the referenced filename. If absent, inspect suitable older channel exports before asking the owner to resend it; missing standalone media does not mean the graphic is unrecoverable. Prioritize any supplied source clip and timestamp, and follow the recovery recipe below. Ask once for another asset only if the bounded search finds no cleanly reusable graphic. Continue independent requested corrections without fabricating a replacement or claiming completion.

## Recover a CTA from an older rendered episode

1. Resolve the exact supplied media identifier. For Drive, match its file ID in an explicit-root `rclone lsjson` listing before `rclone copyto`; a matching episode filename alone is insufficient. Preserve the downloaded source and record its ID, selected range and hash.
2. Inspect a bounded neighborhood around the supplied timestamp with `ffmpeg -ss START -i SOURCE -t WINDOW -vf 'fps=2,scale=320:180,tile=8x4' -frames:v 1 CONTACT.jpg`, then inspect a full-resolution frame for crop bounds. Identify entrance, like/click, subscribed, bell and exit states. Do not copy the old closing scene wholesale when only its graphic is requested.
3. Prefer original alpha/green-screen media when available. For a baked-in animation on a stationary opaque rounded card, choose the interval where the card is fully expanded and all required states remain inside it. Crop just inside its border, create a matching antialiased rounded alpha mask, and combine with `[crop][mask]alphamerge`. Preserve the actual animated artwork; this is extraction, not a reconstructed graphic. If the card moves or its cursor spills outside the safe region, a fixed mask is insufficient—adjust the method or request the original instead of delivering clipped art or old-background contamination.
4. Export the isolated asset with `-an -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le`. Use brief alpha fades to replace excluded entrance/exit motion and inspect the entire chosen range. Do not copy source audio containing the previous episode's speech, or claim its sound effects have been isolated.
5. Anchor the overlay to the current final edit's spoken invitation, using local shot time derived from the shared frame plan. Shift CTA PTS by that local offset and use `overlay=...:eof_action=pass:enable=between(t\,START\,END)` so the last CTA frame does not freeze through the farewell. Keep it clear of the host circle and necessary UI.
6. Re-encode only intersecting cached picture shots with matching dimensions, FPS, codec parameters and time base. Concatenate unchanged encoded shots and mux the current export's audio with `-map 0:v -map 1:a -c copy`. Assert unchanged frame count/duration, compare copied audio payload hashes, fully decode the new export, and inspect CTA entrance, state changes and exit in the actual delivery file. With unchanged timing/audio, reuse the existing chapters, captions and speech checks rather than retranscribing.
7. Clear the missing-CTA requirement in current package/state fields after verification; retain earlier blocker notes only as history. Report the recovered graphic's source and new cue range, and keep publication approval separate.

## Remove a repeated spoken phrase

1. Map the complaint timestamp from the reviewed export into source frames using the existing shared edit plan. Inspect the cached timing JSON's keys and value types before indexing; serializers may nest segments under `result` rather than at the root.
2. Locate both occurrences and retain the one that completes the thought. Verify word boundaries in a short contextual crop rather than deleting a guessed second at the reported timestamp.
3. Apply the same frame-exact removal to picture and audio. For an already mastered mix, splice the existing PCM at derived sample indices, with very short in-place seam fades if needed; assert the exact new sample count and do not remaster unrelated audio.
4. Remap subtitles, chapters, guide timestamps and CTA anchors piecewise. Inspect any subtitle cue crossing the cut: shifting its times alone can leave the removed phrase in its text. Preserve raw ASR and record the correction separately.
5. Run local ASR only on a short crop from the actual final encoded seam to check phrase count and context. Reuse the verified local model path from the existing transcription script rather than guessing a model identifier or downloading another model. Keep perceptual seam listening explicitly pending unless actually performed.

## Remove a timestamped screen shot without restoring full-face coverage

1. Resolve the timestamp against the exact reviewed version, then map output frames to source frames and apply the measured screen offset. Inspect both the reviewed export and the underlying screen recording; a camera overlay can conceal the actual start or end of the unwanted window.
2. Sample a bounded neighborhood at roughly 0.5–1 second intervals, then inspect transition boundaries more closely. Choose the smallest speech-safe interval containing the unwanted shot. Remove a complete incidental transition utterance when necessary; do not silently discard substantive narration to make a visual cut easy.
3. Subtract the same half-open frame interval `[start, end)` from picture and audio. Keep assertions for intervals before, inside and spanning the cut, total output frames, contiguous output positions and exact PCM sample count. Reuse the existing mastered audio outside the cut.
4. Drop subtitle cues wholly removed by the cut and review text crossing either boundary; shift later cues and current chapter/guide anchors by the computed duration. Do not apply the shift twice to already-revised metadata.
5. Inspect the final encoded seam at approximately 0.1-second spacing and its immediately adjacent frames to catch a brief flash of the removed window. Run the existing local recognizer only on the final seam crop; distinguish that check from actual listening.
6. Update current status, shared-plan pointer, duration, delivery gate and QA references together. Keep old results explicitly historical so a completed new revision does not still present an old pipeline or obsolete blocker as current.

## Retrieve a supplied real clip

For a user-authorized local download, try the installed downloader directly; opening a browser is not a prerequisite:

```sh
yt-dlp --no-playlist --no-overwrites --write-info-json \
  --merge-output-format mp4 -o 'work/assets/demo-%(id)s.%(ext)s' "$URL"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height -of json "$FILE"
ffmpeg -v error -xerror -i "$FILE" -f null -
```

Use the exact supplied URL. Download success is not insertion success or publication permission. If access requires login, involve the user rather than bypass authentication. Inspect multiple decoded frames and the selected excerpt's audio boundaries before choosing in/out points; a changing contact sheet establishes sampled visual movement, not full playback or listening.

## Confirm the promised output asset

1. Inspect the cached result shot and its surrounding screen recording before searching for an export. “Output” may mean the result demonstrated in the editor, not a separate MP4. Distinguish a standalone export, real-time preview playback, paused/scrubbed editor footage and a third-party demo; do not impose the first category when the owner means another.
2. If the owner identifies the on-screen result, reuse it immediately and remove the missing-file requirement from current state. Do not ask for a standalone export again. If no relevant result is visible or identified, search the exact EP Drive folder recursively and the existing local project, then ask once for its location; report the bounded search rather than claiming global absence.
3. Inspect start, interior, scrub/play transitions and the final frames at full resolution. Crop the demonstrated canvas proportionally with plain side pillars when appropriate; retain necessary captions and label it as a result captured in the editor. Exclude incidental placeholder-text edits or selection transitions at the end where a clean earlier boundary exists. Never invent motion, reconstruct a result, or pass third-party footage off as this episode's output.
4. For a punchier opening, select short cached reaction, action and result excerpts; preserve whole spoken phrases and the actual meaning. Preview the assembled opening rather than just its title card. Adjust music separately from speech, and do not use louder music as a proxy for excitement. Inspect crop/text at delivery resolution before rendering the rest.
5. Move or append the recorded result at the requested end position, using the current reviewed frame plan. Re-encode only the changed opening and result crop; concatenate unchanged body shots, preserve body PCM, and remap captions for both duplicated highlight speech and relocated result material. Check whether relocation removes an earlier occurrence or adds another; do not accidentally duplicate a long waiting shot.

## Insert without changing unrelated material

1. Anchor the insertion to the verified edit plan, preferably at the existing transition into the closing when the request is an end example.
2. Use one frame/sample clock for every stream. At 30 fps and 48 kHz, one frame is 1600 samples; derive counts in code for the actual rates. Normalize only the new excerpt as needed and add short in-place seam fades without shortening its agreed duration.
3. Preserve vertical content and its captions with proportional scaling and plain side pillars in a landscape export. Do not stretch it or invent a generated replacement.
4. Concatenate prefix, excerpt and suffix; remap the closing and all later graphics/CTA/subtitle anchors by the same exact duration. Keep original PCM outside the insertion unchanged. Re-encode picture only when the actual composition requires it.
5. Update the existing package's current timeline and status; do not create another prose deliverable per revision.

## Preserve exact audio length through normalization

1. Compute the intended output sample count from the shared frame clock, then assert the edited voice and premix both have that count before mastering.
2. Resample explicitly **after** `loudnorm` and **before** sample-count trimming: `loudnorm=... ,aresample=48000,apad,atrim=end_sample=N` (use the actual target rate and computed count). Dynamic normalization can operate at 192 kHz; `-ar 48000` on the output occurs too late to make an earlier `atrim` count 48 kHz samples.
3. Keep a small executable regression: process one second of a 48 kHz sine through dynamic loudnorm and the production resample/trim tail; assert exactly 48000 mono output samples. Then assert the full master rate and length again before muxing. Padding is not a repair for accidentally truncated speech: rebuild that master from the intact premix.
4. Keep the verified source and useful failure evidence under the active storage policy; do not create another backup of an invalid generated master when backup piles are prohibited. Reuse the verified voice, music, premix and first-pass loudness measurements, and rebuild only mastering. Do not rerun transcription or picture rendering for an audio sample-rate bug.
5. For repeated frame-exact excerpts from an AAC export, decode its reviewed audio once to PCM (`ffmpeg -i REVIEWED -vn -ar 48000 -ac 2 -c:a pcm_s16le REVIEWED_PCM.wav`) and use `wave.setpos(round(start_seconds * sample_rate))` plus `readframes(frame_count * samples_per_frame)`. Repeated compressed-input `-ss`/`-t` extraction can return slightly fewer samples due to timestamp/packet boundaries; caching PCM also avoids repeated full decoding. Assert each excerpt's byte count and the assembled total, then compare unchanged mapped regions byte-for-byte against that PCM.
6. Investigate any PCM shortage before padding: identify whether it is at the true source end, measure it, and inspect the final spoken cue. Only an explicitly bounded, verified terminal silence gap may be zero-filled to the frame clock; never pad an interior short read or conceal missing speech. For interrupted generated WAVs, validate sample count before reuse and rebuild only the incomplete mix from intact cached stems. Promote a completed mix only after its expected sample count passes.

## Reuse picture shots safely

- Key cached shots by exact source files and in/out points, output frame count, filter graph, used graphic asset hashes and relevant encoder settings. Exclude bookkeeping-only fields such as sequential shot IDs, segment IDs and output timeline positions unless they affect the actual rendering; a cut that renumbers later parts must not force unrelated shots to render again. A matching graph alone cannot prove matching source content; a hash of the whole editing script invalidates unrelated shots unnecessarily.
- For picture-only corrections, retain the audio master and unaffected encoded shots. Verify full encoded audio identity with `ffmpeg -v error -i FILE -map 0:a:0 -c copy -f hash -hash sha256 -` before reusing previous seam-ASR results. If packet hashes differ, compare decoded PCM/timing rather than assuming speech changed or blindly retranscribing everything.
- Name the active corrected output explicitly and preserve a recoverable reviewed artifact under the owner's storage policy. Before remuxing a changed concat plan, check whether the assembler skips an already-existing destination; bind the candidate to the new plan fingerprint and reject stale media rather than accidentally validating it. Do not create another local backup when the owner has prohibited backup piles. Inspect changed intervals in the exact active export, then perform the final full decode; cached visual checks remain valid only for provably unchanged shots.
- For crop-and-overlay soft blurs, derive the blur radius from the smallest cropped plane, including chroma subsampling. Thin title/address strips can reject a radius that works on a large receipt region. Test the narrowest region in an encoded preview first; apply redaction before compositing the circular presenter and inspect moving content through the entire interval.

## Recover an interrupted streamed render

1. Match the failed process to its exact shot and active candidate. Inspect the cached completion record, actual file and current process state before retrying; a late failure notice may belong to a superseded attempt. Keep verified prior shots unchanged.
2. Probe the incomplete shot with `ffprobe -v error -count_frames -show_streams -show_format -of json SHOT`, capture stderr, and compare video `nb_read_frames` to the frame plan. Treat `File ended prematurely` as failure even when duration looks correct or the process exits zero. Do not promote an existing partial merely because it opens.
3. Separate storage, source access and rendering: check free space, issue a bounded HTTP Range read against the same source endpoint, and decode a short source window near the stalled position. Successful later probes establish present reachability, not the original cause; label an intermittent read/render stall as suspected unless logs isolate it.
4. For remote reads, inspect the installed FFmpeg HTTP options before using bounded reconnection. Supported options used successfully are `-rw_timeout 20000000 -reconnect 1 -reconnect_on_network_error 1 -reconnect_max_retries 2 -reconnect_delay_total_max 30`, placed before each remote `-i`. Do not enable endless retries or reconnect-at-EOF on finite source files. Add per-shot `-progress PATH` so a later timeout identifies the last actual output position instead of encouraging a blind timeout increase.
5. Remove only an agent-generated incomplete chunk whose failed validation and missing completion record are confirmed; never delete original footage or the sole reviewed export. Render into a `.partial.mkv` path, require a clean decode and exact frame count, then rename to the completed path and write its cache record. Refuse an unexpected leftover partial until inspected.
6. Resume the existing renderer/cache rather than submitting a new episode job. Require the formerly failing shot to pass and the next shot to advance before reporting recovery; process startup alone is not proof. Continue final assembly and complete-export QA without retranscribing or rerendering verified earlier shots.

## Verify the exported result

- Decode the full export and assert expected frame count and audio/video duration against the insertion plan.
- Set each concat segment's duration from its exact frame count/FPS when container durations are rounded; verify the entire final video PTS grid, not just frame count. A correct number of frames can still accumulate sub-frame timing errors across concatenated parts.
- Reject silent/near-constant windows as unmeasurable for cross-correlation lag. Record RMS/variance and select an informative adjacent speech window before diagnosing an edge-of-search argmax as desynchronization; keep the lag tolerance strict.
- Anchor a promo-entry logo/music cue to the first verified painted destination page, inspecting neighboring frames rather than assuming an old editorial source boundary equals the actual tab switch.
- Assert sample identity outside changed regions in the working PCM. AAC is lossy: use correlations against that master in representative encoded windows for the music cue, unchanged Workshop, inserted demo and closing rather than claiming encoded byte identity.
- Inspect encoded frames on both sides of each join and through the excerpt; measure loudness and true peak on the actual delivery file, not just the WAV.
- Parse FFmpeg loudness JSON with `json.JSONDecoder().raw_decode(text[text.rfind('{'):])[0]` when the log includes a trailing progress summary; `json.loads` of the entire suffix can reject an otherwise valid completed measurement.
- Deliver the exact revised file, actual cue times and duration. Distinguish full decode, sampled visual inspection, waveform verification and real-time listening; none substitutes for another. Keep unresolved unrelated assets visible but do not call the requested completed music/insert revision blocked by a canceled music requirement.
