---
name: bbn-ai-cut
description: "Edit BoomBigNose/BBN Thai presenter and screen videos with local AI: concise speech, synchronized real demonstrations, clean sound, kinetic graphics and verified exports. A footage folder requests a Long and vertical Short; an existing-video request can revise only specified times, audio, imagery, fonts or website inserts. Use for BBN tutorials/workshops/news, ตัดคำซ้ำ, แก้เสียง, แทรกแอนิเมชัน, or the approved-Long to Short handoff."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# BBN AI Cut

## Current BBN routing override — 2026-10-09

For new BBN Shorts, bbn-ai-short-fullscreen replaces the older split-screen presentation in this skill and its historical references. Use bbn-tutorial-hook only for selecting genuine recorded hooks/results from Long, adapting into fullscreen, and bbn-explainer-motion for separate conceptual explanation in Long/Short. Shared transcription, speech completeness, synchronization, privacy, audio and export QA tools remain valid. Do not delete this shared tool skill or reinterpret existing accepted exports as new-format requests. Imported layout examples do not override the new Short profile.

Turn recorded speech into concise, faithful BBN videos using local inference. A footage folder plus `$bbn-ai-cut`, with no narrower instruction, is a request to complete the full edit: **one long video plus at least one strongest coherent vertical Short**, including the sound, framing and caption defaults below, plus the [YouTube text handoff](#youtube-text-handoff) for the completed Long. Inspect the folder and proceed without requesting another brief for routine choices.

For a new full edit, lead with real recorded results and a concise highlight/demo montage showing distinct benefits in the original voice; around 30 seconds is a starting point when the source supports it. The hook needs no presenter face. Choose genuine eye contact for selected presenter emphasis shots, retain the original room and natural neutral face color, and use a circular presenter clear of essential demonstrations. Keep music soft beneath clear speech with gradual pause rises and restrained channel SFX. Combine purposeful real images, appropriate illustrations and genuine product logos with kinetic white text, restrained yellow highlights and 25% text backing. Riley Brown is primary, with Nate Herk and Jedi secondary; the [latest concrete Riley reference](references/channel-editing-and-sound.md#latest-concrete-riley-reference--2026-09-10) governs the current direction. Pop the genuine BoomBigNose+ logo as a separate centered graphic at one meaningful Skool beat, outside all text boxes. Make the Short roughly 30–60 seconds with checked Thai captions; preserve a complete thought. Read the relevant sections of [channel editing and sound](references/channel-editing-and-sound.md) for defaults and evidence.

Use actual recorded product/UI/website results for the current subject. The earlier Claude tutorial's no-game-footage choice does not exclude a user's relevant game, 3D model or Muay Thai website demonstration in another episode. Generated 3D supporting AI illustrations are allowed when requested; they do not replace real demonstrations, presenter identity or genuine brand marks. When a supplied image is rejected, replace that asset according to the current brief rather than retaining it because an earlier render succeeded. A text-only hook does not satisfy a requested visual treatment. When moving source highlights earlier, remove their exact repeated excerpts from the body and preserve the instructional sequence and original voice through the shared frame plan.

The current request overrides these defaults. An explicit no-Short or long-only request omits the Short; not-now instructions defer it. A focused revision such as changing only intro music preserves that scope while the revision is underway; subsequent clear approval of the Long uses the saved handoff below. Use the active conversation and latest brief to distinguish approval of the Long from feedback on one detail.

After clear approval of a Long, automatically finish and deliver at least one coherent Short from that approved version under the [Long approval to Short handoff](references/channel-editing-and-sound.md#long-approval-to-short-handoff), without waiting for another request; honor explicit no-Short/not-now instructions and do not duplicate an already delivered matching Short.

Use this as the primary workflow for applicable editing requests, including follow-up revisions. For channel pacing, the approved camera look, hook construction, music/SFX or a Skool promotion, read [channel editing and sound](references/channel-editing-and-sound.md). It also describes bounded agent roles and automatic skill routing; it does not install runtime hooks or create background work.

## Owner rules 2026-10-22 (EP239)

[owner-rules-2026-10-22.md](../bbn-ai-edit/references/owner-rules-2026-10-22.md) overrides conflicting text in this skill and its references: revisions overwrite the same Drive file (same name and ID) via `../bbn-ai-edit/scripts/drive_replace.sh`, never `_v2`/`_v3` uploads; demos the speaker describes are real screen recordings (`screencapture -v`) timed to speech with private data blurred; work to the end without asking back; paths are `~`-relative.

## Choose the current revision scope first

The numbered full-edit stages below are not a requirement to restart completed work. Read the latest request against the version the user reviewed, then take the applicable route:

| Current request | Route |
|---|---|
| New full edit | Follow the full workflow, including Short and text handoff. |
| Repeated or rambling speech | Reuse transcripts and inspect complete clauses and demo actions; follow stages 3–4 and remap every affected stream. |
| Noise, yellow face or sharpening | Use the existing correction workflow on the affected voice/camera source; leave unrelated screens and stems intact. |
| Remove/adjust music, Erase song, or a music copyright claim | Follow [music claims and local audio revisions](references/editing-and-qa.md#music-claims-and-local-audio-revisions). Edit the reviewed file locally, preserve speech and copy unchanged video; do not restart the full package or substitute a Studio processing wait. |
| Picture-only time range, insert, font/motion change, rejected image or banner removal | Read [focused visual revisions](references/focused-visual-revisions.md) and revise the selected picture interval. Preserve approved audio, timing, other shots, a matching Short and still-valid metadata. Skip new full ASR, denoise, tempo changes and loudness processing. |

An explicit later “only this section” supersedes earlier broader edit plans; keep outside findings as unapplied notes. New feedback is not another approval gate when the requested local revision is already authorized. Keep generation prompts/provenance in project records, not as unrequested update/date/model notices burned into the video.

## Control cost and revision count

For full BBN episodes, follow the cumulative 10% Codex weekly-quota ceiling in [BBN AI Edit](../bbn-ai-edit/SKILL.md#episode-cost-ceiling--updated-2026-10-06), including all deliverables and revisions; it is not a new allowance per render, session or weekly reset.

Delivery priority: **Long → YouTube Package → thumbnails (when included) → Short**. Release each file after its own QA, immediately uploading and verifying it when Drive delivery is authorized; notify with that file’s review link. Do not wait for the whole episode package. In the Hermes worker use its incremental artifact manifest. Continue remaining authorized outputs, and replace the same owned Drive file for later revisions.

Treat the episode directory as the durable working memory. Probe and transcribe each unchanged source once, then reuse its hashes, transcript, alignment, accepted assets, edit plan, stems and prior QA for **both Long and Short**. Run a second ASR model or CTC only on uncertain local crops. Keep one concise current-state manifest with the reviewed input version, accumulated brief, accepted regions, open defects and reusable artifact paths; read it before long logs or old drafts. At the start of a new edit, inspect one recent accepted channel example for Long style and the saved EP205/EP208 Short references; record concrete layout, caption and sound choices once. Read only the reference sections needed for the current edit.

Batch all known feedback into one canonical plan per output. Before encoding a changed deliverable, check every planned speech seam against the retained words on both sides and the matching screen action; the opening, each explanation and the ending must remain complete. Render one compact review bundle from that output's exact plan covering the opening, changed seams/user timecodes, comparisons, presenter/UI clearance, text entrance/hold/exit, CTA, sound cues, ending and a source-versus-output clarity sample. Fix failed excerpts **before** the first full encode. Deliver the checked result without asking the user to teach routine editing choices through repeated drafts. If final QA reveals a local defect, patch that interval when safe and reuse accepted streams and evidence. See [cost-aware iteration](references/editing-and-qa.md#cost-aware-iteration) for the acceptance checks and stopping rule.

## The tested combination

| Job | Tool | Role |
|---|---|---|
| Primary Thai transcript | Qwen3-ASR-1.7B BF16 via MLX Audio | Preserve spoken wording, including restarts |
| Independent transcript check | Whisper large-v3-turbo via mlx-whisper | Check uncertain/repeated passages; Thonburian is an optional additional opinion |
| Fine Thai timing | Typhoon Whisper Thai CTC + its matching encoder | Locate candidate characters, then inspect waveform boundaries |
| Speech and pauses | Silero VAD + waveform/RMS | Limit ASR inputs and identify pauses for review |
| Synchronization and export | Audio cross-correlation + FFmpeg | One shared edit plan for both pictures and a single audio master |
| Designed animation and editable graphics | HyperFrames + an existing seekable motion runtime | Render genuine motion and readable kinetic type; keep an editable composition |

This is a tested combination, not a claim of best-in-class recognition or automatic editorial judgment. See [local models](references/local-models.md) for exact tested versions, load recipes, and failure modes. Consult it before installing or running the model stack. See [editing and verification](references/editing-and-qa.md) before compiling cuts or rendering.

## 1. Inspect the actual project

Read applicable project instructions and memory. Find `Footages`, `footage`, or the user-selected inputs without assuming names or case. Probe duration, frame rate/time base, dimensions, audio tracks, rotation, and available encoders. Inspect representative source frames to identify camera/screen and choose a face crop that survives movement.

Keep source media and prior exports intact. Store derived audio, transcripts, model provenance, and candidate decisions in that project's working directory. Store only safe artifact references in durable memory. Do not copy private media or transcripts into this shared skill.

Check the current machine and cached models before downloading. The tested MLX runtime needs Apple Silicon. On other hardware, choose a supported local backend and validate a representative sample before treating it as equivalent. Do not silently substitute a cloud transcription API when the user asked for local processing.

If an external footage volume disappears, verify the mount before diagnosing missing source files or software. Preserve the current work and resume after reconnection; do not initialize an empty replacement project at the missing path. Installed tools, cached model files, a running inference job and a decoded usable output are separate facts.

## 2. Synchronize before editing

Choose an explicit master timebase, normally camera source seconds. Measure the audio offset over several widely spaced windows, not only the opening clap. Record the sign convention as:

`screen_source_seconds = camera_source_seconds + screen_offset_seconds`

Check offset consistency for drift. A single constant offset is insufficient when offsets change over time; correct the time mapping before applying shared cuts. Check mapped timestamps are inside both source durations. If meaningful speech falls outside their overlap, preserve it with an explicit camera-only lead/tail rather than silently dropping it to satisfy shared-range bounds. Choose one clean aligned audio master to avoid doubled voices. Recompute all offsets for new footage.

Treat separately recorded screen replacements as their own source clocks. Inspect their own narration and screen actions, then map retained source ranges into the shared output plan; do not inherit the main camera/screen offset. Check both ends of every inserted take and remove failed or duplicated demonstrations only from reviewed source evidence.

## 3. Transcribe with evidence

Run Silero VAD and primary Qwen transcription on padded, overlapping speech windows. Save source bounds and overlap explicitly. **Input crop bounds are not word timestamps, and duplicated overlap text is not repeated speech.**

Review candidate restarts against an independent Whisper crop with surrounding context. Use the same waveform and gain for comparisons. Keep the spoken disfluencies in the evidence transcript; a polished transcript can conceal the very repetitions being edited. Resolve product-name spelling from the source screen/context.

Use Typhoon CTC only where precise Thai timing is needed. A forced alignment can fit words into noise: combine it with the independently heard/recognized wording and waveform. Re-crop uncertain passages; preserve ambiguous speech rather than deleting it on one model's authority.

## 4. Make explicit editorial decisions

Keep candidate suggestions separate from selected cuts. Review redundant clauses and digressions first, then repeated words and fillers such as ก็คือ, เอ่อ and abandoned connectors. A request to tighten speech calls for another content pass, not only a few isolated word cuts. Retain definitions, meaningful emphasis, complete intended statements, demonstrations and pauses needed to follow the screen; do not delete every occurrence of a filler by text matching.

When the presenter restarts or rephrases the same explanation, remove the first attempt and retain the later complete version. Do not keep both merely because the wording differs. Check surrounding meaning and retain any unique necessary information; genuine emphasis or separate ideas are not duplicates.

Remove spoken instructions to the editor together with the associated search/wait passage, then resume at the successful action while preserving any necessary explanation. Do not remove only the aside and leave the unwanted search in place.

For each selected cut, record source start/end frames, reason, before/after meaning, evidence and screen preservation. In revisions, compare against the existing retained intervals: propose only additional removals and preserve an approved hook unless the current request changes it. A whole-clip speech-tightening request includes the intro: preserve its distinct promises and meaning, while removing repeated wording and retaining the approved visual design where compatible. A body-only or picture-only request keeps its narrower scope. Reuse full transcripts and re-run only uncertain local crops.

Find boundaries near low-energy valleys with room for the last kept syllable and next onset. Inspect the resulting frame-quantized boundary as well as the proposed timestamp. For every Long and Short cut, compare the retained transcript and decoded audio with enough context to confirm that subjects, verbs, numbers and corrections still form a complete thought; verify that the visible action matches the words. Shorten long waits only after checking the **voice stem** and screen; music can hide dead air, and absent ASR text alone does not establish silence.

Use the bundled [plan compiler](scripts/compile_edit_plan.py) once cuts have been reviewed. It does not transcribe, decide deletions, or render. Its exact schema and CLI are in [editing and verification](references/editing-and-qa.md#portable-plan-compiler). Compile to a new versioned file, review the actual quantized gaps, and make that plan canonical for every stream.

## 5. Compose and render

During demonstrations, show the screen at its natural aspect ratio with a modest circular presenter clear of key content. Let real results carry the hook; if selecting a full-frame presenter reaction or bridge, choose genuine eye contact and return before necessary screen action. Recompute framing from the actual footage. Use the original room and camera-only natural neutral grade unless the current brief changes that choice. Inspect for yellow skin; correct any yellow cast with camera white balance/tint and verify encoded before/after frames. Keep screen colors and the presenter's identity intact. The full-edit invocation authorizes the channel sound, restrained labels and Short captions described here; focused revisions retain their narrower scope.

Place added explanatory text at the upper right, clear of the application content underneath. Keep the presenter inset in one stable safe position; move it only when an actual screen change would obscure necessary content, not merely because a new shot or segment begins. When narration compares left, middle or right examples, keep the complete comparison arrangement visible for that wording; do not crop away a referenced panel.

For the like/share/subscribe invitation, place the supplied CTA animation prominently in the center, substantially larger than a corner label. This is an exception to upper-right explanatory text. Synchronize it with the spoken invitation, preserve its native entrance/click/exit and existing sound, remove green-screen spill, and keep the presenter clear. Inspect a recent channel example when requested; prioritize the current explicit placement/size instruction.

After the highlight montage, retain the presenter's short original greeting/name when available unless the user asks to omit it. Preserve complete wording and map its picture, voice and subsequent cue shifts together. For reported hiss, missing greetings or weak/missing promo sound, follow [the correction workflow](references/channel-editing-and-sound.md#user-reported-hiss-greeting-and-promo-sound-corrections): treat each voice source separately, preserve native music/SFX and verify the requested change in the encoded export.

Use purposeful real recordings, relevant person/AI-robot/cloud/workflow imagery and genuine Claude/product logos alongside the text where they clarify the actual speech. Use a cohesive polished 3D style for supporting AI imagery when requested, avoiding childish flat emoji mixtures. A requested standalone Claude mark must be a genuine PNG with verified transparent alpha and no baked background tile. Follow the [real imagery and SVG sourcing rules](references/channel-editing-and-sound.md#real-imagery-and-licensed-svg) and keep source/license/credit or generation records in the episode. Record a needed real demo only within the active task's authorized app work; never fabricate the UI/result or generate a lookalike logo.

Give Long explanatory overlays a compact dark backing with exactly 25% fill opacity and a modest shadow. Keep supporting text clean white with restrained yellow highlights; do not add automatic underlines to Long or Short captions. Fit the backing to the complete Long text group. The established Short captions use an outline/shadow without a filled box. Keep text, face and necessary UI clear, and inspect the encoded entrance, complete spoken hold and exit. The original room remains unchanged.

For “normal/boring font” or missing-animation feedback, redesign the hierarchy and motion: a suitable display face, stronger key-word scale, staggered word reveal, a brief settle and a stable reading hold. Do not merely enlarge the same static card. Preserve Thai words and combining marks. Use one available animation stack; a list such as Hyperframes, Remotion, Motion or Anime.js is not a requirement to install all of them. Read the selected entry-point/domain skills and follow [the focused motion workflow](references/focused-visual-revisions.md) for actual renders, alpha and timing checks.

Map camera, screen, voice, hook/body shots, graphics, logo, music and SFX from the same frame plan. After speech cuts, rebuild their output anchors together; do not leave overlays or audio cues at old output times. Use the [user-selected reusable media kit](references/channel-editing-and-sound.md#user-selected-reusable-media-kit--2026-09-10), including the existing Subscribe animation at an appropriate invitation, and verified supplied brand assets. Prefer the recorded shared library paths; inspect replacement screen takes for their own narration before integrating them. Adjust intro speech speed on its separate voice stem; preserve music and SFX at native speed unless explicitly requested otherwise. Remap their cue anchors without speeding a mixed master. Keep music soft beneath clear speech, rising gradually during genuine pauses and returning before the next words; the earlier music-above-voice intro preference is superseded. Set the actual mix by the source and verify the encoded result.

Render the cost-aware review bundle from the canonical plan, using the actual crop, motion and audio. Inspect it, then render the full version locally with FFmpeg. For newly cut or changed audio, use brief in-place seam fades and appropriate normalization, then measure the encoded result. For a picture-only revision, preserve the complete mastered audio instead; do not add new fades, SFX or normalization to an unchanged mix.

If providing a HyperFrames companion, read its entry-point and relevant authoring/CLI skills first. Generate it from the same frame plan. A successful HTML preview is not evidence of a full MP4 render.

For a full edit, also finish the [vertical Short](references/channel-editing-and-sound.md#vertical-short-deliverable): choose the strongest complete takeaway, derive its own output plan from reviewed source intervals and the same sync mapping, reframe for 9:16, correct and time Thai captions, then render and check the actual Short. It can reuse a strong moment from the long video; it need not copy the long opening montage. When real images or logos clarify the selected speech, use the [Short image animation workflow](references/channel-editing-and-sound.md#short-images-and-logo-animation), including for the Long-approval handoff.

## 6. Verify and deliver

For Shorts, use the fullscreen background and moving presenter video cutout specified by bbn-ai-short-fullscreen, and inspect every encoded caption event, including every new line; distributed sample frames alone are insufficient. Preserve ASS line-break escapes when adding word styling, and check that no font/color control syntax appears as literal text. Reuse a compatible existing caption checker if present, alongside actual frame review. Imported paths such as `EP219/short-v4/check_captions.py` and `EP216/work/graphics/assets/CanvaSans-Bold.ttf` must be located and verified on this host rather than assumed available; retain Canva Sans with a verified Thai fallback.

Mask readable secrets tightly around the exposed value and check temporal boundaries frame by frame. Public URLs, field labels and already-masked fields do not need blanket censorship merely because they mention a key. Continue protecting private personal information under the current brief; the secret examples are not an exhaustive privacy policy. Never copy actual secret values into logs or delivery text.

Use the user's latest accepted style reference. The supplied history identifies EP219 Long as rejected for style; technical QA or a public upload does not make it an accepted style example. Current project references such as the explicitly selected EP221 take precedence over older channel examples.

Decode the completed media once and compare decoded frame count and stream durations with the plan. Check codecs, dimensions, loudness, true peak, and audio/video agreement. Inspect distributed contact frames and the source/output neighborhoods around edited speech. State accurately whether real-time listening occurred; ASR comparison and waveform inspection do not count as listening.

For sound revisions, use [focused sound verification](references/editing-and-qa.md#focused-sound-revision-checks) to check source-specific noise reduction and timing, native music speed, actual encoded SFX, the opening and replacement-take joins. Reuse valid checks for unchanged material; do not restart full transcription or render another version after all relevant checks pass without a new change or unresolved defect.

For picture-only revisions, use [focused visual verification](references/focused-visual-revisions.md): verify the unchanged audio and outside picture intervals, exact preview placement, actual generated imagery, kinetic entrances/holds/exits and transition boundaries. Deliver a review excerpt of the changed interval alongside the completed export when useful; a still layout proof or successful HTML preview is not the requested animated clip.

Deliver the actual long video and Short for a full edit, or the specifically revised deliverable for a focused revision, with durations, material edit counts and any unresolved quality limitation. Verify each delivered export separately and link the editable companion when created. Update project memory with artifact paths and checks actually performed. Do not stop at a transcript, suggested cuts, or an unrendered plan when the user requested edited videos.

## YouTube text handoff

Complete the Long's YouTube text package immediately after delivering the Long, without waiting for separate requests or delaying the Long for metadata. Keep field expertise in separate skills: [bbn-youtube-tags](../bbn-youtube-tags/SKILL.md) researches current relevant terms once; [bbn-youtube-title](../bbn-youtube-title/SKILL.md) preserves the accepted title/`101`; [bbn-youtube-description](../bbn-youtube-description/SKILL.md) writes the description with full plain URLs and final-export chapters and assembles the package under its consolidated-package instructions. User preference confirmed 2026-09-15: deliver one UTF-8 `<episode>_Package.txt`, containing Title → Long post captions → Short post captions → Short IG captions → Description with Timeline → Tags. Title and each caption category have `ตัวหลัก`, `สำรอง 1`, and `สำรอง 2`. Reuse still-valid drafts as inputs; the consolidated file is the current user-facing text deliverable. Preserve previous drafts as history, without generating separate field files as additional package deliverables.

A focused request owns only its field: title-only, description-only or tags-only work goes directly to the corresponding skill and does not rerender media. After a video revision, refresh metadata only where the changed content or timing requires it, preserving accepted wording. If metadata is requested for a Short, derive it from that Short and omit the Long's chapters. Thumbnail artwork remains the responsibility of `bbn-youtube-thumbnail` when requested. This handoff creates local drafts; it does not authorize publication or background work.

## Local media cleanup after owner acceptance — 2026-10-06

The owner requests automatic disk cleanup after a clip has been uploaded to Drive and the owner explicitly confirms that the latest delivered version passes. Upload success, technical QA, silence, and a request to change rules are not owner acceptance. Tie acceptance to the specific clip/version and its verified Drive file ID and hash; any later revision needs acceptance of that new version.

Before deleting local media, recheck the current remote file ID, size and checksum, and confirm that the accepted file is available to play or download. Once these conditions are met, delete that clip's local video copies, superseded renders and regenerable intermediate media to reclaim disk space without asking for a second cleanup confirmation. Delete downloaded source copies only when their original Drive IDs/files are verified as recoverable and they are no longer needed for any unfinished Long, Short or revision. Keep files still needed by active work.

Delete only within the accepted episode's local workspace. Never delete or trash Drive files, a sole remaining original, unrelated jobs, shared music/SFX, presenter portraits, logos, fonts, models or tools. Retain lightweight source/delivery manifests, Drive links and hashes, approval evidence, transcripts, cut plans, compact QA reports, package text and a cleanup record listing removed paths/bytes and actual disk space recovered. Re-download verified Drive media if a later edit is requested.

This rule supersedes earlier requirements to retain local originals, prior renders and intermediate media indefinitely only after all cleanup conditions above are satisfied; preserve them during editing and review. Adding this rule does not approve EP229 or authorize a retrospective bulk purge of other episodes.
