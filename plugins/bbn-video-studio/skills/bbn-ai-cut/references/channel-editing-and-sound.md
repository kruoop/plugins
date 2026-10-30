# BBN channel editing and sound

Use this reference for BBN presenter/screen edits and their revisions. The user's saved full-edit defaults apply when a footage folder and `$bbn-ai-cut` are supplied without a narrower instruction. The latest explicit request and accepted version govern revisions; never import an unrelated promotion from an old episode.

## Minimal input and scope

A footage folder plus the skill name is enough to start the complete BBN workflow. Inspect existing instructions, footage, previous work and the current conversation; infer routine production choices from the material and these defaults. Complete the local long export and at least one vertical Short without another approval step for these authorized deliverables. Ask only when a missing input or genuinely ambiguous project boundary prevents useful progress.

| Request | Deliverables and scope |
| --- | --- |
| Folder + `$bbn-ai-cut`, or a new full BBN edit | Long video plus at least one strongest coherent vertical Short; channel framing, sound, restrained labels, checked Short captions and export QA; the Long's Title, plain-URL Description/Timeline and Tags through the [separate text skills](../SKILL.md#youtube-text-handoff) |
| Focused revision to an existing video, such as intro music only | Change and validate that part; preserve unrelated cuts/picture, then apply the handoff below when the user clearly approves the Long |
| Only specified times, new inserts, animated fonts or a replacement image | Use [focused visual revisions](focused-visual-revisions.md); retain the complete approved audio and other shots. Reuse a matching Short and metadata. |
| Clear approval of the Long, including after a focused revision | Finish and deliver its coherent Short from the approved version without another request, unless explicitly excluded/deferred or a matching Short is already delivered |
| Explicit long-only or no-Short request | Deliver the long video with the remaining requested/default treatment; omit the Short |

These are active task defaults, not a watcher on a folder or authorization to publish. Existing approved work can be reused after verification; prior exports remain intact.

### Long approval to Short handoff

The user explicitly requests this saved workflow: when they clearly approve the Long, continue in the active task and finish at least one strong, coherent vertical Short from that approved version without waiting for a separate Short request or approval question. Preserve the approved Long and verify its version before deriving the Short. A positive remark about one detail while requesting more changes is not approval of the complete Long.

Honor explicit no-Short, long-only or not-now instructions. If a corresponding Short is already delivered and still matches the approved content, reuse that delivery instead of making a duplicate; revise it only when the approved content requires a change. A focused Long correction keeps its narrow scope until approval, then this requested handoff applies. Follow the [vertical Short deliverable](#vertical-short-deliverable) defaults and verify the actual Short independently. This handoff runs during active work; it creates no watcher, scheduled job, background continuation or publication authority.

## Revision and pacing

Apply the speech-editing bullets below when speech tightening is in the current scope. A later picture-only or time-bounded request supersedes earlier broader plans, even when a reviewer found other possible improvements. Preserve those findings as notes rather than silently applying them.

- Read the latest brief, accepted export, shared frame plan and project evidence before revising. Keep prior exports and source recordings intact. A rejected background or older hook in project history is not the current design.
- Review the actual screen alongside the speech. Remove repeated explanations, abandoned starts, personal digressions and waiting that adds no instruction before attempting tiny word cuts. Preserve the one complete explanation and the actions/results that let a viewer follow it.
- Then check ก็คือ, เอ่อ, อ่า, repeated names, pronouns and connectors. ก็คือ can introduce a necessary definition; an idiom or deliberate emphasis can legitimately repeat. Resolve each candidate in context rather than applying a deletion list.
- Save integer source frames, cut reason, before/after meaning, local ASR evidence, screen evidence and confidence. Check the quantized waveform at both edges. A shorter whole-clause cut is preferable to a syllable splice that leaves fragments. Keep ambiguous speech when an independent crop and waveform do not establish a safe boundary.
- Verify joins on the revised retained timeline. A raw source crop may contain a phrase already removed by an earlier version, so source-neighborhood ASR alone does not verify the final join.

## Camera, screen and the opening

On 2026-09-09, the user established original-room footage, natural neutral face color and a strong opening as saved BBN editing defaults. The **2026-09-10 revision** refines the opening to lead with real recorded results and a highlight/demo montage showing several distinct benefits, retaining the original voice. A face is optional in the hook. Around 30 seconds remains a starting point when the source supports it; keep complete beats and do not pad a shorter suitable opening. The latest explicit brief can change these defaults.

- **Face color correction, confirmed 2026-09-10:** inspect the actual camera frames for yellow/warm skin casts. If the face looks yellow, correct camera white balance and tint toward natural neutral skin before compositing. Check representative lighting/movement and encoded before/after frames; avoid trading yellow for pink, grey or blue skin, preserve face detail and identity, and keep the screen layer unchanged. Reassess each recording rather than reusing fixed correction coefficients from another episode.
- Keep the actual face and original room. Compare representative source and encoded frames when correcting white balance. Apply the correction to the camera layer only, before compositing, and inspect natural skin tone, face detail, highlights and movement. A replacement background trial is not evidence of accepted matting quality.
- Place the circle where it clears the current UI. Reassess its corner when the view changes, particularly prompts, send controls, code, result calculators and promotional content. Preserve the screen aspect ratio; output resolution does not add source detail.
- Choose genuine eye contact for each selected presenter emphasis shot, including a full-frame hook, reaction or direct-to-viewer bridge. The hook can omit the face entirely; do not force an off-axis or downward-looking camera moment into the opening. Return to the screen before an action or result the viewer needs to follow. Preserve camera/audio source time and inspect the complete shot for face clipping; a layout change does not justify an independent audio shift.
- Lead with the actual completed result, then select complete original spoken highlights and readable demonstrations that establish several different benefits and lead naturally into the tutorial. Use the current episode's real actions, UI states and working results. Do not import unrelated gameplay from a style reference; the earlier Claude tutorial's exclusion does not prohibit relevant game, 3D model or Muay Thai website demonstrations in another episode. Keep a result's qualification/context intact and do not turn a developer's claim into a verified benchmark.
- Source snippets may move earlier. Move their complete intended audio/video beats together, remove the exact repeated excerpts from the body, and keep the remaining explanation and steps understandable. Record moved ranges separately from deletions and remap every dependent stream/cue once. An opening revision may require these duplicate removals; copy the approved remainder unchanged only where the resulting sequence, stream compatibility and boundary checks permit it. Preserve an agreed hook during a body-only revision.
- Restrained, large Thai labels and the available `boom-tech-news-video` skill can supply the requested visual style. That is a supporting style layer; the source timeline and this editing workflow remain authoritative. Use the HyperFrames entry-point skill when creating or revising animated inserts or an editable companion with HyperFrames.

### Modern typography and transitions

The 2026-09-09 V5 direction established modern clean white supporting text with yellow accents; the later 2026-09-16 correction removes automatic underlines from captions. Use restrained yellow emphasis without underlines by default in both Long and Short. The earlier direction superseded V4's cool/cyan accent choice; do not restore dated gold bevel or extrusion. The motion/editing reference priority is **[Riley Brown](https://www.youtube.com/@rileybrownai) first**, with **[Nate Herk](https://www.youtube.com/@nateherk)** and **[Jedi](https://www.youtube.com/@jeditrinupab)** secondary. A later explicit brief can change these saved choices.

For Long explanatory overlays, use a local backing at **exactly 25% opacity (alpha 0.25)** with a modest shadow. Apply that alpha to the backing only, not to the text. The current Short caption reference uses a black outline/shadow with no filled box. These are contrast treatments, not changes to the presenter's room background.

- Use clean, readable Thai type and deliberate spacing. Keep supporting text flat white; reserve yellow for key highlights. Do not turn this yellow-accent request into gold 3D lettering or a heavy full-screen theme.
- Size the Long overlay's 25%-opacity backing around its complete phrase group with comfortable padding, rounded or softly feathered edges and a modest shadow. Keep its footprint local to the text rather than adding a full-width slab. If a busy frame still competes with the words, improve placement, spacing or text contrast while retaining the requested 25% fill. A 25% plate cannot hide native UI text: move or resize the entire group into a verified blank region throughout entrance, hold and exit instead of darkening the plate.
- Choose a clear position for Long text before applying its backing. If any text group would hide a necessary control, result, source claim or the face, move or reduce it. Darkening important UI does not make the placement acceptable. Preserve the original room and camera grade; do not interpret this request as a presenter-background replacement.
- Give phrases a deliberate entrance, a stable reading hold and a clean exit. Motion should follow the emphasis of the speech. Keep Thai glyphs and combining marks readable throughout; do not use constant wobble or deep perspective that distorts the wording.
- Keep the full phrase and any Long backing inside safe bounds through the entire movement. Animate their entrance/hold/exit together and inspect the encoded maximum scale and settled state at delivery size. Check subtitle contrast as well as the headline, especially over existing screen text. Keep UI actions, results, credits and the presenter circle clear.
- An authorized sound accent can support the entrance or main benefit reveal. Place it on the same frame event as the animation and keep it below speech. Do not add a separate hit to every letter, keyframe or edit.
- After speech changes, remap text, backing, animation and its sound cue together. Keep the actual video and screen action visible beneath the motion.

**2026-09-13 refinement:** “font still normal” calls for designed typography and actual phrase motion, not just a larger static label. Pair a verified Thai display font with a compatible condensed Latin face where useful; emphasize a few words or numbers, stagger their entrance and allow a stable reading hold. Inspect real font loading and Thai marks at maximum scale. Hyperframes/GSAP is a verified available combination, while a specifically requested equivalent can be used. Choose one stack and reuse it; detailed deterministic render and alpha checks live in [focused visual revisions](focused-visual-revisions.md).

Keep operational notes such as website-version dates, renderer/model labels and generation provenance in project records. Do not burn them into a video unless requested. This does not prohibit a spoken-topic caption, a required credit, or dates that naturally belong to the actual recorded webpage. An approved picture-only change does not itself authorize new SFX.

### Real imagery and licensed SVG

The **2026-09-10 preference** combines purposeful imagery with kinetic white/yellow typography and light accents. A succession of text cards alone is insufficient. Use relevant person, AI-robot, cloud or connected-workflow imagery at the corresponding spoken idea, plus genuine Claude/product artwork where that product is discussed. Give each image a clear purpose, brief entrance, readable hold and clean exit; leave actual UI/results readable. A small highlight or sound accent should support a meaningful beat, not decorate every word.

Use existing recordings first, or record a needed real Claude Code/UI/website demonstration within the active task's authorized work. Keep the original voice, genuine presenter and actual application results. **The latest 2026-09-10 user permission allows generated 3D supporting AI imagery when requested**, superseding the earlier blanket no-generated-imagery choice only for those illustrative objects. It does not authorize invented interface recordings, fabricated results, an AI replacement for the presenter or a generated/lookalike product logo. Do not replace a necessary demonstration with an illustration.

When the user requests a faster opening, process the original voice stem with pitch-preserving tempo adjustment and retime intro pictures, text, graphics and cue anchors together. Keep music at its original 1.0× tempo on a separate stem unless the user explicitly requests a music-speed change; never apply atempo to an already mixed voice/music master. SFX retain native speed and duration while their start cues follow the revised picture clock. EP210 v6 retains speech at 1.15× and music at 1.0×; restoring the original greeting makes its intro 683 frames / 22.7667 s at 30 fps. The earlier 616-frame intro belongs to v5. These are episode choices, not a forced speed or duration for every speaker. Keep the body at its existing speed, preserve complete phrases, and verify native music timing plus encoded intelligibility and entry timing. For connected AI workflow graphics in this treatment, favor smooth curved paths with a bright core and restrained glow/aura over rigid right-angle lines. Avoid flat horizontal/vertical zero-area gradient bounds that can make an SVG path disappear; inspect every connector in the encoded video.

For the requested 3D upgrade, use a cohesive polished visual family for relevant person, AI-robot, cloud and workflow concepts: controlled materials, lighting, depth and readable silhouettes. Avoid childish flat emoji mixtures, toy-like clutter and mismatched clip-art styles. Keep these elements secondary to the recorded result and kinetic text. Record the actual generation prompt, inputs, output and tool beside the episode assets, and identify illustrations as authored support rather than captured evidence. This permission does not make 3D generation mandatory for every edit; the current brief governs.

Free-license SVG/emoji from the internet remains allowed when appropriate to the selected visual style; it is not the default substitute for a specifically requested polished 3D treatment. Fetch a small relevant set from its primary repository, verify the exact asset and license, and retain its source URL, retrieval date, hash, license and attribution text in the episode. For example, [Twemoji graphics](https://github.com/twitter/twemoji) use [CC BY 4.0](https://github.com/twitter/twemoji/blob/master/LICENSE-GRAPHICS); keep the required credit with the delivered project and in the video's credits/description when those graphics are used. Preserve original SVGs and note any adaptation. Inspect rendering, transparency and edges in the actual composition; an illustration represents an idea, not evidence of a result.

Prefer the supplied, verified Claude/Claude Code and BBN artwork. Keep logos genuine, proportionate and readable; do not synthesize or redraw lookalikes. When the user requests a standalone transparent Claude logo, use a genuine PNG with actual alpha, or faithfully rasterize the authentic source SVG without changing the mark. Inspect its alpha channel and composite it over both light and dark backgrounds to reject baked white/cream rectangles, app-icon tiles and checkerboard patterns. Preserve the original mark; 3D supporting-illustration permission does not extend to inventing brand artwork. Product logos are separate from the emoji license: [Anthropic's trademark guidelines](https://www.anthropic.com/legal/trademark-guidelines) are not a free-content license. Record the actual supplied/source provenance and any known use terms rather than claiming all downloaded brand assets are freely licensed. Assets and credit records stay in the episode, not this shared skill.

When the user rejects a supplied image over rights or style concerns, replace that selected photograph/artwork, including a previously generated video derived from it. An original unbranded illustration plus separately authored product-name typography is a useful alternative when it fits the brief; never present it as an official product logo or guarantee legal clearance. Use the available image-generation/editing workflow for requested bitmap art, save the selected result in the episode and retain the prompt/tool/provenance there. A rejected asset stays out of the deliverable even if its render was technically successful. This is not a blanket ban on genuine logos requested elsewhere.

For a website refresh or workshop insert, record the actual current requested page and choose shots that support the retained voice. Preserve the original invitation audio when only replacement visuals were requested; show the relevant page action or offer, then return to the presenter at a suitable sentence boundary. Do not fabricate interface controls or repeat an obsolete screen capture just because it is already in the timeline. Keep source-page facts distinct from new editorial labels, and do not import another episode's promotion.

### Latest concrete Riley reference — 2026-09-10

The user supplied [this Riley Brown video](https://www.youtube.com/watch?v=3cYTWLdHgAE) as the primary concrete reference for the current revision, with Nate supplementary. The coordinating editor inspected these paused-player states on 2026-09-10:

| Sampled seconds | Observed visual state |
| --- | --- |
| 0 | Presenter. |
| 5 | White “to build” phrase. |
| 9 | “FRONTEND” appears blurred in an entering state. |
| 10 | “FRONTEND”, “BACKEND” and “DATABASE” arranged around the presenter. |
| 15 | Clean presenter shot. |
| 20 | Gameplay demonstration in a browser inset over a white dot-grid treatment. That Claude tutorial brief excluded gameplay; the current episode's brief governs which subjects are relevant. |
| 25 | Presenter with “you can build a real app”. |

Use the observed hierarchy, purposeful phrase assembly, selected image emphasis and readable demo framing as direction. Substitute the current episode's real demonstrations and results for the reference's subject matter. The user's request for results first and an optional presenter takes precedence over the reference's presenter opening. The white/yellow palette, exact 25% backing and light BBN accents are user choices; exact easing, blur amount, movement and duration are authored decisions, not measurements recovered from these samples.

For the supplementary [Nate video](https://www.youtube.com/watch?v=FBVNS1l5Vb8), the editor rechecked presenter states at 0, 10 and 15 seconds and, at 5 seconds, laptop/people B-roll with dimensional translucent Claude logo cards. These samples support relevant real B-roll and product artwork beside the text; they do not establish a card's motion duration or an audio/SFX match. No reference audio audition was performed. This is a sampled visual review, not a whole-video timing analysis. Episode evidence/hand-off notes are in `/Volumes/BoomBigNose/EP210/work/intro-v3/assets-review/skill-update/`; keep any actual captures in the episode.

### Observed primary reference: Riley Brown

The user requests Riley's text animation, movement and highlighting as the primary direction. On **2026-09-09**, the team inspected timed paused-player states from two public videos.

In [I Spent 100 Hours Using GPT-6 Astra (This Feels Like AGI)](https://www.youtube.com/watch?v=Ju41cQSe7hY):

| Sampled seconds | Observed visual states |
| --- | --- |
| 0, approximately 0.5–1.5 | White words build in groups to the right of the presenter, who becomes closer and shifts left. Incoming words appear softer and lower before becoming crisp; this particular phrase has no opaque plate. |
| Approximately 2.0–2.5 | A brief blurred reframe is followed by a sharp centered presenter as the phrase leaves to the right. A separate rounded ChatGPT icon appears beside the host at 2.5. |
| Approximately 3, 5, 10 | Inset proof/B-roll appears with a dotted outer treatment and orange lower edge; a large pale-yellow product headline is present by 5, and another result occupies the inset at 10. |
| 15, 20 | Different presenter footage has an incoming lower caption at 15. At 20, a large currency figure with smaller support appears in an outlined rounded card beside the studio presenter. |

In [8 ChatGPT Agents That Do My Work for Me (Steal These)](https://www.youtube.com/watch?v=ubzhh4kMCLo):

| Sampled seconds | Observed visual states |
| --- | --- |
| 0, approximately 1–3 | Clear medium presenter; a floating rounded ChatGPT icon appears beside the face while a dark prompt UI enters and its words build with a cursor. |
| Approximately 4–5 | The picture is pushed closer and blurred; a centered white benefit phrase builds across two lines. |
| 10, 15 | An outlined guide tag appears beside the clear presenter at 10; the main overlay is absent in the sample at 15. |
| 20, 25 | A white dotted-grid explainer shows an app-icon branch diagram and feature labels; a second part heading is present by 25. |
| 30 | A solid blue panel covers part of the frame beside the presenter, a sampled state during a transition. |

Adapt the purposeful phrase assembly with short soft-to-crisp travel, selected icon/number emphasis and brief focus or scale changes to the spoken point, then leave a stable reading hold. Give only the key number or benefit a larger impact group with restrained yellow emphasis; preserve complete Thai words and combining marks. A diagram or short wipe can mark a real change of idea when useful; keep necessary screen actions and results readable. Exact animation curves and durations are authored choices, not recovered from these sparse samples. The exact 25% backing, white/yellow palette, soft music, standalone centered BBN logo and original room are user choices, not claims about Riley's palette or mix.

The first video's evidence is in the episode's `motion-v5/references/riley/findings.json`, `captured-frames.json` and its local screenshots. Honor each capture's `valid_visual_evidence` flag: captures taken during playback or with the player outside the viewport are excluded. The second video's evidence is `work/edit-v5/style-reference/riley-secondary-observations.json`; those root-reviewed screenshots were inspected in CUA tool outputs, and no local screenshot files are claimed for them. Actual recorded player times govern rather than filename labels. These are bounded opening samples, not a whole-video motion audit. No reference video was downloaded and no reference audio audition or SFX identity match was performed.

### Observed secondary reference: Nate Herk

On **2026-09-09**, actual paused public-player samples established the following. The times identify inspected states, not frame-exact transition boundaries or measured easing curves.

| Public video and sampled seconds | Observed visual states |
| --- | --- |
| [I Tested GPT-6 Astra vs Fable 5.1 on 15 Real Use Cases](https://www.youtube.com/watch?v=WfJPBVXPt8k), 0, 0.5, 1.5, 5, 10, 15, 20 | Clean full presenter at 0–0.5; a source app at 1.5, Slides at 5 and Sheets at 10; full presenter again at 15 and 20. Readable source UI and neutral host framing dominate these samples. |
| [How Anthropic ACTUALLY Prompts Fable 5.1](https://www.youtube.com/watch?v=FBVNS1l5Vb8), 0, 5, 10, 15 | Clean full presenter at 0, 10 and 15. At 5, laptop B-roll carries multiple translucent rounded app-icon cards at different sizes and depth positions. Their orange is the app logo color; the samples do not establish card animation duration. |
| [GPT-6 Astra Finally Solves AI Video Editing (full guide)](https://www.youtube.com/watch?v=o3IEkKXXXvo), 0, 0.5, 1.5, 10, 20 | Three vertical edited tutorial examples appear on a blue backdrop; the active example changes across samples. Compact white captions, off-white information cards, limited green keywords and inserted B-roll belong to those displayed examples, not a demonstrated continuous treatment of the surrounding long video. |

This secondary reference supports selective emphasis, clean presenter/screen changes and readable UI. A short slide/reveal with slight scale settling is a BBN editorial choice; do not describe its exact duration or easing as copied from Nate. Use icon cards or relevant B-roll only where they explain the spoken point, with authorized assets. Riley now governs the primary motion direction; retain clean source cuts wherever a demonstration needs continuity and do not restore the old warm-flare plan by default. The latest white/yellow palette and 25% backing are BBN user choices, not claims that every Nate clip uses them.

Evidence remains in `work/intro-v4/style-reference/findings.json` and `captured-frames.json` in the episode project. Actual player times govern; filenames are labels. Only sampled frames were inspected: no remote video was downloaded and no audio audition or Nate music/SFX identification was performed. Do not infer absence of an effect throughout a video from its absence in these sparse samples. Keep captured frames in the project rather than the shared skill.

### Observed secondary reference: Jedi

On **2026-09-09**, paused public-player frames from the user-supplied [@jeditrinupab](https://www.youtube.com/@jeditrinupab) reference established these visual patterns:

| Public video and sampled seconds | Observed visual states |
| --- | --- |
| [GPT 6 Astra ลืม Claude ไปได้เลย](https://www.youtube.com/watch?v=MsJcq-xmOAs), 0.30–3.0 | A large app icon near the bottom becomes smaller and centered by 1.0; the 6 ASTRA label is partly revealed from left to right at 1.0 and complete at 1.5. A Thai headline is partly revealed at 2.0 and complete at 3.0. |
| Same Astra video, 15–16 | A large white Thai keyword and separate app icon sit beside the full-frame presenter, with a soft shadow and no rectangular panel; the phrase remains stable across these samples. |
| [คู่มือใช้ ChatGPT ฉบับ กันยายน 2026](https://www.youtube.com/watch?v=KAzfLTQHaz4), 0–6 | Tight presenter framing at 0 changes to medium framing by 1 with a large low white phrase; the phrase is absent at 2. Another low phrase is present at 4–5 and absent at 6. |
| Same guide video, 9.5–10.5 | A group photo at 9.5 has a warm orange flare at 9.9, followed by a near-white frame at 10.0, presenter with fading warmth at 10.1 and normal presenter by 10.5. |

Use these secondary patterns only where they fit the latest modern BBN treatment and the primary reference:

- Assemble two or three meaningful phrase groups, settle size/position, then hold for reading. Keep Thai words and combining marks intact. Any chosen overshoot is an adaptation, not a measured reference easing curve.
- Place concise emphasized words beside or below the face where space permits, using the current palette and user-requested local text backing. The observed unboxed Jedi words do not override that newer readability request. Reserve accent color for meaningful emphasis, leave gaps between phrases and keep necessary UI visible.
- Choose presenter close/medium shots and screen/presenter switches for a reaction, bridge or change of idea. Preserve the screen through necessary actions and results. The observed Jedi warm flare is historical reference evidence; it does not override the current Riley-primary direction or automatically restore the earlier flare plan.
- Keep transitions, text and sound on the shared source/output mapping. Use authorized footage and assets; borrowing a motion pattern does not require copying another channel's identity or artwork. These frame observations establish no SFX or music identity.

Secondary evidence remains in the episode's `work/intro-v4/style-reference/findings-jedi-historical.json` and `captured-frames.json`. Actual player timestamps in the manifest govern; filenames are labels and can differ from sample times. Paused samples show states, not frame-exact onset/end or source-project keyframes. No remote video was downloaded and no audio audition was performed for this visual inspection. Keep captured frames in the project rather than the shared skill.

## Vertical Short deliverable

For every new full BBN edit, deliver at least one strong vertical Short unless the user explicitly excludes it. Choose a coherent moment with an immediate reason to watch, a useful explanation or demonstration, and a clear payoff. Roughly **30–60 seconds** is the default; preserve the complete thought rather than stretching or amputating a sentence to fit that range. Choose the strongest finished moment instead of automatically copying the long video's montage.

- Reuse reviewed source footage and cleaned voice. Derive a separate Short output plan from those source intervals, with the same measured camera/screen mapping and frame/sample rules. A Short can reuse material from the long video; the no-repeat hook/body rule applies within a single edit, not across these separate deliverables.
- Default to **9:16**, normally 1080 × 1920 at the established output FPS when appropriate. Reframe each shot around the real subject and action. Use the presenter full frame when their reaction carries the point; during an essential demonstration, preserve the relevant screen area with a readable crop or a screen/presenter layout that fits vertically. Do not stretch the screen, invent UI or crop away the control/result needed to understand the claim.
- **Current BBN tutorial Short references (confirmed 2026-09-16):** use EP205 for story and picture layout: begin with a complete sentence that sets up the result, maintain a 50/50 upper-screen/lower-presenter composition for the tutorial, and end with a short CTA that sends viewers to the Long video or its link below the post. Do not retain an extended farewell after that CTA. The upper half must show the complete source screen needed for the spoken explanation; use a fitted full-screen view over a subdued fill instead of cropping away controls or results. Use EP208 for subtitle typography: Canva Sans (Canva's Noto Sans Thai fallback for Thai glyphs), large white text with restrained yellow emphasis, a clear black outline/shadow, no underline and no filled caption box. Keep the captions below the presenter's face. Remove repeats and dead air only at complete phrase boundaries; never leave a number, noun phrase or sentence unfinished. Review the words on both sides of every Short cut before rendering.
- Include checked Thai captions by default on the Short. Correct names, numbers, negation and claim qualifiers against the source and actual screen; ASR output is a draft. Time the captions to the Short's edited voice, use short readable phrase groups, and keep them clear of the face, relevant UI and platform-overlay areas. Inspect Thai glyphs, line breaks and caption changes on actual portrait frames at phone-like size. A caption word-timing estimate does not replace a source speech check.
- Adapt music, SFX and labels to the Short's pace and complete message. Keep speech intelligible, avoid replaying the long intro before the useful moment, and remap every cue to the Short plan. Keep any call to action relevant and brief; do not insert an old workshop offer merely to fill the ending.
- Save the Short MP4, its source/output plan and caption text/timings alongside the related long edit. Check its actual encode, duration, frames, audio clocks, mix, first/last spoken words, portrait framing and caption readability independently. Deliver the playable file, not only suggested timestamps.

### Short images and logo animation

When an image helps explain the selected speech, include purposeful image animation in the Short, including the Long-approval handoff. It need not appear in every shot.

- Inspect relevant real images, logos and screenshots from user-supplied links/folders and existing project assets first; use task-appropriate sources when needed. Verify what each asset depicts and save the selected file with local provenance: original path or source URL, retrieval date, hash and any known usage/attribution information. Keep assets and their provenance in the episode folder, not this shared skill.
- Match the image to the spoken product, idea or result. Treat an illustrative image as illustration, not proof of a claim; do not fabricate results or add unrelated decorative images. Keep a necessary live demonstration visible instead of replacing its evidence with a logo.
- Use the existing HyperFrames workflow and read its relevant authoring skills. Anchor a short reveal, movement or scale-and-settle to the matching speech/source beat, then provide a stable reading hold and clean exit. Map image, captions and any sound accent through the Short's frame plan together; preserve image proportions, logo identity and camera/screen/voice synchronization after cuts.
- Keep the face, checked Thai captions and necessary UI clear throughout motion. Verify the actual encoded entrance, hold, exit and adjacent seams at portrait viewing size for readable images/text, unobscured screen actions and correct timing. An HTML preview alone does not validate the delivered animation.

## Shared time mapping

Keep one camera-based source clock. Measure `screen_seconds = camera_seconds + offset_seconds` for each recording, verify distributed windows for drift, and quantize once for the chosen output FPS. EP209's measured −0.5975625 seconds / −18 frames at 30 FPS is an episode result, not a reusable preset.

Store each source-bound event with its source frame and intended occurrence (hook or body). Resolve it against the final retained intervals. If its source action is removed, drop or deliberately re-anchor the event; never clamp it blindly onto an unrelated cut. Hook-only or outro music can instead use a declared output span derived from the final hook or end frame.

After a content revision, rebuild camera/screen selections, audio samples, chapters, labels, presenter placement, included captions, promo beats, music and SFX from that plan. Use one edit plan for each MP4 and its editable companion, with the same source mapping for the long and Short outputs. Check the existing [frame and sample rules](editing-and-qa.md#rendering-from-a-shared-clock), especially VFR normalization, offset signs, frame quantization and rational sample boundaries.

## Music and SFX

The full-edit invocation includes BBN music and restrained effects as saved defaults; an explicit sound restriction or focused revision controls its own scope. The latest **V5 preference on 2026-09-09** is **soft music under clear voice, with gradual rises during genuine pauses**. This supersedes the earlier intro music-above-voice direction. Keep narration clear in the hook, body and promotion; do not mark every speech cut with a sound.

### Earlier library verification — 2026-09-09

The earlier verified **Common Sound and Music** copy was in `~/Downloads/Common Sound and Music/` on the earlier Mac; the current preferred shared source is the user-selected kit below. The supplied [Drive asset folder](https://drive.google.com/drive/folders/15-CtSct24_8LiheV2ac2BYLZR0n9iGLa) is an additional source for assets actually present. Record source/hash in the episode and keep media in project folders, not this shared skill. On 2026-09-09, the six curated audio/video files were copied from Downloads into episode `assets/Common Sound and Music/`, with exact hashes in `manifest.json`. The Drive import separately verified **36 images**, recorded in `assets/Brand Assets/drive-manifest.json`; it did not establish a new reference video or fresh Drive audio download. Do It is a selected intro track, not a newly fingerprinted reference identity.

On 2026-09-09, the six Downloads files were fully decoded and hashed in the episode's `work/edit-v5/audio-analysis/downloads-audit.json`: **Do It**, **ช่วงขายElevator Music**, **Mouse Click**, **Ding**, **Correct and Incorrect**, and **subscribe green screen.mp4**. Five match the earlier local library by hash; the subscribe clip is an additional 7.894-second source with audio. Smiling Faces is absent from this curated selection, so do not bring it back from the older cache by default. Use the verified positive section of Correct and Incorrect for positive accents, and inspect any subscribe animation/audio before selecting a useful cue.

### User-selected reusable media kit — 2026-09-10

The user explicitly selected this local kit and requested that it be remembered for BBN edits. Prefer the existing shared sources below over searching or downloading replacements:

`~/Desktop/new-news/ตัดต่อข่าว AI-automation/Common Sound and Music/`

| Exact filename | Role |
| --- | --- |
| `Fashion Saxophone Hip-Hop by Infraction [No Copyright Music]  Do It.mp3` | User-selected music bed; keep soft under narration and shape gradual pause rises |
| `Elevator Music  (Waiting) - Background Music HD.mp4` | User-selected music; use the established Skool treatment when that promo is present |
| `Mouse Click Sound Effect.mp4` | Restrained action/click accent |
| `Correct and Incorrect sound effect - right or wrong.mp4` | Select the appropriate useful region; the verified positive region below supports a benefit beat |
| `Ding Sound Effect.mp4` | Optional result/reveal accent, below speech |
| `subscribe green screen.mp4` | Existing Subscribe animation, preferably at the spoken like/share/subscribe invitation |
| `Split screen line.png` | Supplied white vertical divider for an appropriate split-screen layout |

Inventory this kit at project entry and report missing files accurately. Recheck decoding, alpha, dimensions and usable regions; copy only needed assets into the current project with source/hash provenance. A full BBN edit includes purposeful channel sound and the existing Subscribe animation when the source has a suitable invitation; a focused revision keeps its scope. Do not force every effect or music track into every scene. Existing logos, profile images and other useful art should be found and verified alongside this kit or the user's supplied brand assets; do not substitute invented branding.

Key the actual green background from `subscribe green screen.mp4` and inspect entrance, click/subscribed/bell state and exit in the encoded composition for green spill, clipped artwork and legibility. Place it clear of the face and essential UI. Inspect its embedded audio before mixing: retain only useful animation SFX below narration and avoid duplicating them with added click/ding cues. Anchor the animation and any sound to the same final frame plan after speech edits.

The supplied divider was verified on 2026-09-10 as the existing **500 × 500 RGBA** `Split screen line.png`, byte-identical to the user attachment (SHA-256 `95440428520cebf6cdee185301f8261a120d23e3d918c5d9b4dfbed6c3b6a2d2`). Preserve its transparency; black in a preview does not mean it needs black backing. Use it only where a split layout clarifies comparison or separation; retain the source screen's aspect ratio and keep important content clear. The shared file is the durable reference, never the temporary clipboard path.

A later screen-only recording can replace a failed section of a longer main screen recording. Inspect whether it has its own narration: if so, edit that screen and its own audio together, without showing unrelated lip movement from the earlier camera. If it has no narration, align its demonstrated actions to the retained master voice. Keep the original main screen elsewhere, omit off-take remarks and superseded repeated farewells as editorial content, and show a real completed result before resuming the main summary. Recompute each replacement's mapping; a main-camera offset does not synchronize a separately recorded take.

### Previously verified local library

On 2026-09-09 the EP209 source audit fully decoded and hashed the following files under:

`~/Desktop/new-news/ตัดต่อข่าว AI-automation/Common Sound and Music/`

| File | Useful role when requested |
| --- | --- |
| `Upbeat Rock Funk by Infraction [No Copyright Music] ⧸ Smiling Faces.mp3` | Upbeat opening or closing |
| `Fashion Saxophone Hip-Hop by Infraction [No Copyright Music]  Do It.mp3` | Low chapter contrast where it supports the voice |
| `Elevator Music  (Waiting) - Background Music HD.mp4` | Verified music for the supplied BBN Skool reference; use for that requested treatment |
| `Mouse Click Sound Effect.mp4` | Verified reference click; a short accent on a verified UI action |
| `Correct and Incorrect sound effect - right or wrong.mp4` | Verified positive section only, source approximately 3.6676–4.5337 seconds, for a requested benefit accent |
| `Ding Sound Effect.mp4` | Optional editorial result accent; not matched to the supplied reference |

The audit evidence lives in the episode's `work/tight-v3/music/manifest.json`; keep media and derived audio in project folders, not this shared skill. Recheck file existence, usable regions, decoding and current authorization in a new task. Filenames and historical use do not establish licensing or the exact music in a public reference. The current local files were verified locally; a fresh Drive download or matching Drive library was not established.

### Sound placement and levels

- Use quiet musical beds where they support the opening, included promotion, chapter change or farewell. Fade at musical phrase boundaries when practical and preserve the final video duration. Choose musical energy through the track and arrangement while keeping voice clearly in front.
- Shape smooth rises in genuine pauses and lower the music before the next spoken onset. Use the retained voice waveform and actual phrase boundaries; do not swell between every syllable or abruptly pump the gain. Let short gaps stay quiet when there is insufficient time for a natural rise and return.
- Derive levels from the actual voice and curated track, with comparable channel configurations. The earlier V4 +1 LU music-over-voice calibration in `work/intro-v4/audio-analysis/candidate-report.json` is historical evidence and is not the current target. Verify words, encode loudness and true peak, and avoid applying master gain twice when stems already include it.
- Audition a representative voice/music passage when playback is available. Check first consonants, quiet endings and dense musical beats. If listening is unavailable, report the measurements and that limitation without claiming the perceptual balance was confirmed. Derive levels from the actual source/stems and measure the actual final master gain, loudness and true peak after encoding; an assumed mastering gain or an old render's value is not current evidence.
- Apply speech-triggered or manual ducking to keep words clear, with the quiet baseline and gradual pause rises chosen for the actual phrases. Inspect first consonants and quiet endings when tuning the envelope; do not speed up speech to make music fit.
- Trim an effect to its useful transient and tail, with brief in-place fades. Align its audible onset with the verified visual action, accounting for silence inside the sample. Distinguish a visual response timestamp from a measured mouse-down or recorded acoustic click; a keyboard submit may receive an editorial UI accent without being labeled an original click.
- Keep SFX below the voice and infrequent: useful candidates are a real create/open/submit action, a major benefit reveal, or one completed result. A starting check for the final mix is clicks near −22 to −25 dBFS and a quiet ding near −24 dBFS, adjusted for the actual sample and voice. Measure after final master normalization and AAC encoding; pre-master gain alone does not establish final loudness.
- Keep voice, music and SFX stems and a cue manifest when they are needed for revisions. Store source asset/region, source or output anchor, onset compensation, gain, fades, ducking and purpose. Remap cues after cuts and check cues within the final file.

### Skool promotion

Include the **genuine BoomBigNose+ logo** in the authorized Skool promotion. The latest user instruction is a **standalone centered logo pop at one meaningful impact beat**, such as the spoken Skool name. Give the asset its own graphic layer and cue, **outside every text box, caption backing or lower-third**. Do not place adjacent duplicate logos beside the other CTA labels. Use a brief readable entrance/settle/exit and an appropriate restrained sound accent when authorized; the image itself must remain undistorted.

Locate the supplied or verified brand asset and record its provenance; do not substitute plain typed text or an invented logo. Preserve its proportions and transparency. Choose a centered beat that keeps the face and necessary course/destination/QR information clear. Map the logo animation and its sound with the same final source/output plan as the promo text and music, while retaining its independent visual placement.

The V5 episode's verified source is `assets/Brand Assets/BoomBigNose+.png`, a 2149 × 732 PNG imported from the supplied Drive folder; the exact Drive item, size and hash are recorded in `assets/Brand Assets/drive-manifest.json`. Reuse the real asset after checking it in the current project, without copying it into this shared skill.

The supplied public reference is [สร้างแอปด้วย ChatGPT Work พร้อม Deploy ใช้งานจริง!](https://youtu.be/HRfZFvrAKOE), with the Skool music passage at approximately **5:54–6:38**. On **2026-09-09**, a 75-second live-player PCM capture was compared against the local library. Eight distributed 3-second stereo-side windows matched **`Elevator Music  (Waiting) - Background Music HD.mp4`** at the same advancing offset, with refined 48 kHz normalized correlations **0.710–0.950**; competing Smiling Faces and Do It searches were at most **0.123** in absolute correlation. This verifies the bed's identity by waveform evidence, not by an assumption from its filename or subjective listening.

The fitted pre-fade gain was approximately −23 to −25 dB relative to the matching asset; the bed fades near reference seconds 395–398 and its side energy reaches the capture noise floor by approximately 400 seconds. These measurements include playback/codec effects and do not recover an original editor fader. Set gain and fades for the actual edited promo and voice. For a request to follow this BBN Skool reference, start with the verified Elevator Music bed unless the user changes that choice; do not apply it automatically to every sales segment or as a waiting gag.

Evidence remains in the EP209 project's `work/tight-v3/music/reference-skool-findings.md`, `reference-match.json`, `reference-music-refined.json` and `reference-skool-live-355s.json`. The capture came from the authorized live player using `captureStream` and Web Audio, without an ambient microphone or remote-video download. Keep captured audio and other media in the project, never in this shared skill.

The same capture also verified two reference effects on 2026-09-09, with evidence in `work/tight-v3/music/reference-sfx-match.json`:

- **Mouse Click:** local source approximately 0.5253–0.7155 seconds matched reference seconds **364.900** and **378.534**. Correlations were **0.816** and **0.840** on the stereo-side residual after subtracting the aligned music bed; the reversed-template control was at most 0.421. The residual is a comparison signal, not an isolated clean SFX stem.
- **Positive accent:** source approximately **3.6676–4.5337 seconds** of `Correct and Incorrect sound effect - right or wrong.mp4` matched reference seconds **362.243** and **365.343**, with mid-channel correlations **0.601** and **0.714**, above the reversed-template control of 0.408. Use only this verified positive region, not the entire file or its negative sound.

These are approximate player timestamps mapped from capture callbacks, not reusable output cue positions. Nearby screenshots establish the app switch, brand-title and course-grid context, not frame-exact graphics onset; the local source frame at 3.9 seconds shows the positive green check. When following this Skool treatment, align a modest number of clicks and positive accents to the current edit's actual UI or benefit beats, keep them below speech, and do not use the positive sound to imply an unverified factual verdict. **Ding was not matched** in the captured reference passage; it remains an optional editorial choice, not part of a claimed exact recreation. Waveform matching does not constitute real-time listening or prove that every effect in the reference was identified.

When a Skool promo is present in the authorized edit, structure its sound around a small number of beats:

1. **Entry:** introduce the bed from its useful main melody rather than a long silent intro as the speaker moves into the promotion; preserve the first spoken line clearly. Place any requested bell/impact after the logo becomes visible and keep it below speech.
2. **Concrete benefit:** leave time for actual course material, source code/templates, workflows and expert help to be seen. Use at most a restrained accent where a real visual reveal supports it.
3. **Call to action:** support the spoken invitation and supplied destination/artwork. Keep important text or a QR code unobscured and legible.
4. **Exit:** fade the bed shortly after the promotional sentence, before it trails into the resumed tutorial, and land on the retained explanation or action.

Cut rambling or repeated emotional claims without deleting the distinct offer or actual demonstration. Repeated pans, zooms and speech edits inside the promo do not each need a whoosh, click or ding. Record any later reference SFX identification with the exact evidence and distinguish waveform matching from real-time listening.

## Skill and agent routing

`agents/openai.yaml` keeps `allow_implicit_invocation: true` so the installed skill remains eligible for automatic selection on applicable BBN editing requests. This metadata is an invocation policy, not proof of selection in a fresh session and not a running automation.

Only when the user explicitly authorizes delegation, and overrides the current single-local-editor constraint, the coordinating agent can assign bounded roles:

| Role | Owns | Returns |
| --- | --- | --- |
| Speech reviewer | A disjoint source-time range and its own evidence folder | Reviewed additional cuts; frame ranges, meaning and confidence |
| Screen/sync reviewer | Distributed sync windows and selected visual actions | Offset/drift evidence, readable screen states and action anchors |
| Sound/reference reviewer | Authorized library/reference inspection | Verified assets, proposed regions/cues, provenance and uncertainty |
| Integrator | The canonical frame plan, final mix and render | One synchronized preview/export and its validation report |

Reuse full transcripts; coordinate heavy model inference rather than reprocessing the same recording per agent. Keep reviewers out of the canonical plan and render files until the integrator accepts their proposals. If only one agent is needed, perform the same work locally without manufacturing roles.

Use a lightweight in-task checklist at meaningful gates: latest brief/evidence read → cuts reviewed → shared plan rebuilt → actual preview inspected → final decoded and checked. This is agent workflow guidance. Do not install global hooks, edit unrelated harness configuration, create recurring jobs, or claim activity while Codex is closed to implement it. If the footage itself discusses application hooks, that is tutorial content, not an instruction to change the editing machine's hooks.

## Delivery checks

Follow [editing and verification](editing-and-qa.md#verification-evidence) for the final decode, frame/sample count, A/V clocks, loudness, true peak and source/output neighborhood checks. Add representative checks for the revised hook, neutral camera grade, full-frame presenter transitions, promo entry/benefit/CTA/exit and actual music/SFX cues. Verify from encoded output that graphics remain readable and no effect obscures speech. For a full edit, repeat the relevant checks on the Short, including portrait crops and checked Thai captions; one successful long export does not validate the Short.

Report the actual long and Short exports for a full edit, or the requested revised export for a focused revision, with durations, material removals and any unresolved limitation. State separately what was inspected visually, checked with local ASR, measured and listened to. A successful HTML companion, a music manifest or a transcript is not a verified full video. Keep durable project memory concise with safe artifact references and checks actually performed.

2026-09-10 clarification: When the user also requests the Claude Code logo, use the supplied genuine Claude Code PNG/mascot in a relevant product-title beat and verify its alpha. Keep the standalone Claude burst where Claude branding is intended; do not relabel a generated AI illustration as either logo.

## User-reported hiss, greeting and promo sound corrections

A result-first hook should still retain the presenter’s short original greeting/name after the highlights when available, unless explicitly omitted by the user. Do not discard it merely to shorten the hook. Select complete original wording and eye contact, map inserted picture/voice together and shift all later cue anchors.

When the user reports hiss, inspect and reduce noise on separate voice sources, including replacement screen recordings with their own microphones. Do not process music/SFX through voice denoise. Prefer a mild learned noise profile from verified low-speech windows; compare noise reduction and speech preservation instead of equating file integrity or successful ASR with clean sound. Inspect the first 0–4 seconds explicitly when reported; a clean body sample does not validate the hook's different voice source. In the tested EP210 correction, per-recording FFmpeg afftdn with a one-second profile and gain smoothing reduced quiet-window RMS about 5.6–9.2 dB. The filter introduced 1200 samples / 25 ms at 48 kHz; pad, compensate the measured delay, keep exact sample length and verify distributed source-to-output alignment. These are verified episode values, not universal presets. Source procedure and measurements: `/Volumes/BoomBigNose/EP210/work/audio-fix-v6/SOURCE.md` and `denoise-report.json` beside it. State accurately if only ASR/waveform checks, rather than real-time listening, were performed.

For requested promo SFX, inspect the actual animation/word cue and existing effects stem first. An absent cue needs adding, while a quiet existing cue needs a gain change without doubling the hit. Anchor to the relevant graphic entrance, preserve native effect speed and complete tails, and verify the effect survives in actual encoded audio below clear speech. Recheck both corrected screen takes and their joins when the user asks; do not assume the main camera’s noise treatment or retained-source clock also fits those recordings.

Treat user timecodes as anchors in the version they reviewed. Locate the corresponding scene before adding a sound, then map it through any inserted greeting or moved highlights; report changed output times when useful. Use [focused sound verification](editing-and-qa.md#focused-sound-revision-checks) for the final evidence.
