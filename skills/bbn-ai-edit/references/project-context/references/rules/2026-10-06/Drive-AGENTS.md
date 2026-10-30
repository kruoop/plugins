# BBN AI Cut runtime on this Mac

For BBN editing, read `~/.codex/skills/bbn-ai-cut/SKILL.md` and `~/.local/share/bbn-ai-cut/README.md` before running models.

Use the installed isolated environments:
- Qwen / MLX Whisper / Silero: `~/.local/share/bbn-ai-cut/venvs/mlx/bin/python`
- Typhoon CTC / Thai Whisper: `~/.local/share/bbn-ai-cut/venvs/thai/bin/python`

Pinned model paths and download hashes are in `~/.local/share/bbn-ai-cut/models.json`. Actual smoke-check evidence is in `~/.local/share/bbn-ai-cut/checks/`. Run heavy models sequentially on this 16 GB Mac. Reuse this installation instead of downloading duplicates. Follow the skill's offline inference settings; preserve source footage and earlier exports.

Ponytail full remains the default for coding tasks. Reuse existing tools and run checks appropriate to changes.

## Integrated YouTube delivery

A full BBN edit in this project includes the Long, Short, title, description with final-export chapters, tags, and thumbnails in the same task. Honor explicit exclusions and keep focused revisions scoped to the requested change.

The single full-workflow entry point is [BBN AI Edit](../../../../../../bbn-ai-edit/SKILL.md), invoked as `$bbn-ai-edit`. It uses the existing `bbn-ai-cut` handoff: [tags](../../../../../../bbn-youtube-tags/SKILL.md) researches keywords once; [title](../../../../../../bbn-youtube-title/SKILL.md) uses that evidence; [description](../../../../../../bbn-youtube-description/SKILL.md) uses the final title and export timeline. Then apply [thumbnail](../../../../../../bbn-youtube-thumbnail/SKILL.md) using the same episode facts and verified assets. Full edits here include thumbnails by default; follow that skill's variant count and asset requirements. Do not invent a missing portrait or logo; complete available deliverables and identify any essential missing input.

Save everything in the episode folder. Deliver YouTube text as one UTF-8 `<episode>_Package.txt`: Title → Long post captions → Short post captions → Short IG captions → Description with final Timeline → Tags. Title and each caption category include `ตัวหลัก`, `สำรอง 1`, `สำรอง 2`; follow the consolidated-package section of `bbn-youtube-description`. Reuse accepted assets and still-valid drafts. For authorized Drive delivery, put the package alongside the episode's video and keep cover variants in `Thumbnail/`. This workflow creates drafts; uploading or publishing requires user authorization.

## Progressive delivery — updated 2026-09-18

Work and deliver in this order: **Long → YouTube Package → thumbnails → Short**. As soon as a file passes its relevant QA, upload it to the authorized BBN-Video EP folder, verify the actual remote size/hash, and notify Telegram with its review link. Never wait for the whole set before releasing a ready Long, package or cover variant. Continue the remaining authorized work without another confirmation; incorporate arriving feedback. The overall task is complete only when all requested outputs are delivered.

For revisions replace the same owned Drive file, preserving its ID/link and local prior versions; never replace source footage or unowned files. Use one editorial worker per EP, cached transcripts/assets/accepted streams and scoped QA. Stop QA after applicable checks pass; rerender only for a changed plan or failed check. Upload retries reuse verified renders. A stalled transfer is an upload issue, not a reason to rerun the edit.

## Episode cost ceiling — 2026-09-21

The user requests at most 15% overall usage per episode, including Long, Short, the text package, thumbnails, retries and all revisions. Keep one cumulative episode budget record across sessions and reserve room for corrections; never reset the budget on a retry or new task. Establish which quota/budget the percentage refers to before heavy work; the denominator is not yet specified. Use available episode usage reports and quota readings, distinguishing shared account usage from attributable episode usage. Do not invent a token-to-quota conversion or claim an enforced 15% cap without reliable measurement. If approaching the ceiling, deliver already verified files and report the remaining work before incurring further material model cost.

Reuse transcripts, accepted assets, encoded streams and valid QA; use local deterministic tools for render/upload waits and bookkeeping, with no repeated model narration or speculative variants. Keep Long → Package → thumbnails → Short delivery. Savings must preserve sentence completeness, sync, secret masking and source-versus-export visual clarity checks at matched timestamps; a decode pass or matching hash alone does not establish image quality.

## EP intake with confirmation — updated 2026-09-17

New EP folders in BBN-Video (`13PTVmiD5YJPVgytx5WLYpJs3M-EvpcwZ`) or the existing BoomBigNose Video intake (`1ZpXuUP54cPM78xskh8ICyJRYU1bmLzQA`) authorize Telegram notification only. After ten minutes of unchanged inventory, notify through the existing Hermes bot `@YoutubeAuto_001_bot` and wait for the user's explicit command such as `ยืนยันตัด EP214` before queuing a full BBN AI Edit. This replaces the 2026-09-15 automatic-start rule. A direct user edit request is authorization for its stated scope; watcher output is not. Baseline historical folders without retroactive processing. Once confirmed, process one EP at a time and deliver to BBN-Video. Preserve source footage, including originals already in the destination EP folder.

Use `<EP>/<EP>_Long.mp4`, `<EP>/<EP>_Short.mp4`, `<EP>/<EP>_Package.txt`, and `<EP>/Thumbnail/<EP>_Cover.png`, `thumbnail-2.png`, `thumbnail-3.png`. Keep execution logs, QA and intermediate artifacts locally. Preserve prior revisions; never overwrite a different source folder's existing episode delivery. Telegram controls the durable Hermes queue; GPT does editorial work using the installed BBN skills. Deliver only after verifying the actual uploaded files. Upload failures must be reported honestly and retries must reuse verified renders. This authorization does not include YouTube/social publication.

For each episode, transcribe unchanged footage once and retain a concise current-state manifest. Batch all known feedback into one canonical plan. Before the first full encode or a revised full encode, inspect one compact review bundle containing the opening, all changed seams/timecodes, text/CTA/presenter clearance, comparison layouts, sound cues, ending and a source-versus-output clarity sample. Do not start the long render until these checks pass. Reuse accepted streams and QA; patch a local interval when safe instead of rebuilding the whole episode.

## CTA placement — 2026-09-15

For the like/share/subscribe invitation, place the supplied CTA animation prominently in the center, substantially larger than a corner label. This is an exception to upper-right explanatory text. Synchronize it with the spoken invitation, preserve its native entrance/click/exit and existing sound, remove green-screen spill, and keep the presenter clear. Inspect a recent channel example when requested; prioritize the current explicit placement/size instruction.

## Presenter obstruction review — 2026-09-15

Before delivery, review the presenter against the actual controls named in the narration, including account/settings menus, Computer use and project creation. A fixed corner is only a default, never proof of clearance. Record any necessary interval-specific move and inspect the old and new face regions plus both transition boundaries in the encoded file.

## Spoken editing instructions — 2026-09-15

Treat recorded remarks to the editor (for example “เอาตรงที่เลื่อนหาออกเลยนะ”) as editing directions, not audience content. Remove both that spoken aside and the complete matching search/wait/retry action from picture and sound, after checking the surrounding explanation. Resume at the actual completed action; remap every downstream cue and final package chapter through the shared cut plan.

## Corrected pronunciation and text inset — 2026-09-15

When the presenter immediately corrects a mispronounced word, discard the first failed attempt and retain the later complete correction. Check surrounding silence and preserve meaningful demo actions through the same frame cut for screen, presenter and audio. Keep upper-right explanatory boxes slightly inset from the top (EP213 uses y=36 at 1080p); retain the centered CTA exception.

## Spoken text cue timing — 2026-09-15

Anchor explanatory text to the actual spoken clause: reveal when the presenter begins that topic, hold through the complete explanation, and start the exit only after the clause finishes. Do not use a fixed five-second duration. Move the existing matching text sound with the entrance. Verify the text remains visible near the spoken ending in the encoded output, including presenter and control clearance.

## Skool music entrance and ending — 2026-09-15

For Skool BoomBigNose+ promotions, enter directly on the established main instrumental phrase of the selected music, not its sparse introduction/break or a long quiet fade-in. Tie entry to the spoken promotion, use a modest single bell/accent after the logo appears, and finish the bed shortly after the offer/benefit sentence ends. A return to teaching must not retain the promo bed. EP213 v16 uses the existing Do It full instrumental section, a 30 ms anti-click entrance, +3 dB on the existing logo accent, and a 0.5 s exit after the promo. Preserve voice, video and unrelated sound cues.

## Package caption rules — 2026-09-22

For each main/alternative Short post caption, reuse the corresponding YouTube title/post copy verbatim for YouTube Shorts, Facebook and TikTok; do not write separate platform copy or a different generic hook. Label this shared usage in the package. IG Short captions must start with `ฟรี✨ พิมพ์ "<keyword>"` and say the user will send the relevant full-video/learning-resource link. Do not replace this with a generic topical caption. Use the episode keyword (`jev` for EP216); do not imply that the product is free or that automatic replies are configured. Keep `ตัวหลัก`, `สำรอง 1`, `สำรอง 2` for both sections. A caption correction changes only these package sections and preserves video, cover, title, description, timeline and tags.

## Rejected thumbnail identity — 2026-09-23

The user explicitly states that the person in `macmini:Desktop/youtube/_assets/face/image.webp` (local copy `EP217/thumbnail-revision-face/face.webp`) is NOT them and forbids using that face in any future thumbnail. Do not use this image, copies of it, or the EP217 thumbnails generated from it as identity references. Its SHA256 is `052122b84ac0f5a3f87268016f3cfdb1d2df130b79a11f80e3bc828f3c805b5e`. EP217_Cover.png and thumbnail-3.png from the face revision are rejected; previous QA likeness claims are invalid. A folder named Face is not identity confirmation. Use only the user's subsequently identified correct portrait; do not extract a video-frame substitute (also explicitly rejected).

## Confirmed thumbnail identity — 2026-09-23

The user explicitly confirmed the faces in `~/Desktop/BBN AI Edit/EP216/Thumbnail/EP216_Cover.png` and `~/Desktop/BBN AI Edit/EP216/Thumbnail/thumbnail-3.png` as their correct appearance. Use these user-confirmed references for identity and retain their facial proportions and hairstyle. The previously rejected `_assets/face/image.webp` remains forbidden. For the current EP217 correction: no Qwen; open palm holding Mac mini, with M6 and short headline.

## EP219 Long rejected as a style reference — 2026-09-25

The user reports that the published EP219 Long does not follow the brief they taught. Publication and technical QA do not mean editorial acceptance. Do not use EP219 Long as an accepted style/template for future episodes; follow the user's established instructions and explicitly accepted examples. The latest feedback does not identify the exact deviations or request another render/replacement; do not invent either. Details are recorded in `EP219/revision-request.json`.

## Short font and framing reaffirmed — 2026-09-25

Shorts include soft, audible background music by default, as reaffirmed by the user on 2026-09-28. Clicks and bells supplement the music; they do not replace it. Preserve clear speech and native music speed, ease music into the opening and out of the ending, and verify the music in the actual export. Do not equate an extremely quiet measurable stem with an acceptable audible mix.

Use Canva Sans as in the user's previous Shorts, with no filled textbox or Long-style text panel. Keep the screen above and presenter below from the first frame. Select complete opening and closing speech, check cut syllables and sound transitions, and retain repetition/dead-air checks. Existing font reference: `EP216/work/graphics/assets/CanvaSans-Bold.ttf`; verify Thai glyph rendering in the actual export.

For ASS captions, preserve linebreak escapes before applying word-color/font styling. EP219 Short v3 incorrectly styled the N in a linebreak and displayed raw font/color commands. Run `EP219/short-v4/check_captions.py` for this renderer, and visually inspect every distinct caption event in the encoded output, including all multiline cues; a few distributed contact frames missed this defect. Short v4 corrects it without changing audio.


## Timeline chapter count — 2026-09-26

For Long episode packages, use 10 meaningful Timeline chapters by default and never exceed 10 unless the user explicitly asks. Group small demo steps under the main topics; preserve verified final-export timestamps, start at 0:00, and retain adequate chapter duration. Do not invent topics or pad a short video just to reach 10. This preference applies to EP220 and future episodes; Shorts keep their separate no-Long-chapters rule.

## Expired Claude Workshop — 2026-09-28

The user confirmed Claude Workshop @ Bangkok has ended. Remove and do not reuse its registration CTA or https://forms.gle/aqPpPap63z1nqMDL6 in current/future packages, even when copying EP215 description formatting, unless the user explicitly reauthorizes a new event. Keep Skool only when promoted in the episode; keep the general organizational Workshop contact section.

## Description promotion priority — 2026-09-28

Use this order at the top of the YouTube description: Workshop → Skool → Hostinger. By default include promotions present in the episode, but the user's supplied description overrides this selection. Put the applicable Hostinger CTA immediately after the preceding promotion, before the three episode summary lines; never put its hosting CTA in “💎 ลิงก์สำคัญ”. Preserve the user's exact promotional wording and URLs; do not substitute a generic Hostinger homepage for https://hostinger.com/boombignose.

The user supplied the authoritative EP223 description after rejecting repeated rewrites. It includes all three promotional blocks, including Skool. Exact approved plain-text reference: `EP223/work/package-user-approved/description.txt`. Preserve this structure and supplied copy; adapt only episode-specific summaries, resource links and final verified chapters for later episodes. Do not add event dates/conditions or rewrite promotional copy on your own. Explicit new user wording takes precedence.

## Tags exclude channel and episode labels — 2026-09-28

The user does not want channel-name or episode-number tags. Omit `BoomBigNose`, `บูมบิ๊กโน้ส`, and `EP<number>` from the YouTube Tags field in current and future packages. Keep relevant topic/product tags; this preference does not remove branding from titles, captions, descriptions or artwork.


## Greeting, stable presenter and precise blur — 2026-09-29

The EP224 greeting/name introduction should show the presenter large, then smoothly shrink to the lower-right circular face while revealing Hermes. Keep the lower-right position stable unless it obstructs an actual essential control; terminal overlap is explicitly allowed. Do not move the face solely because a shot changes.

Use localized blur for readable private data, not solid gray bars. Track the actual field during scrolling/window movement and remove the blur immediately when the sensitive content leaves. Native password bullets do not need an additional broad cover. Preserve ordinary public URLs and useful controls.

## Kruoop TH package promotion — 2026-10-02

The user now requests Kruoop TH as the sole external URL in current and future YouTube package descriptions. At the top of YouTube Description use this exact line: `🌟 เรียนรู้และติดตาม Skill บน Kruoop 👉 https://kruoop.com/s/post/a24dcfa0-ed3e-442b-b802-262a271f2b2f`. This supersedes the earlier Workshop → Skool → Hostinger promotional selection and the resource-link list; do not carry those URLs or the LINE URL forward unless the user explicitly requests them again. Keep organizational contact email, captions, title, tags and verified Timeline. Put technical resource links in separately requested learning content instead. Preserve the latest remotely edited package when updating chapters. This preference changes package text only, not video or recorded promotions; a Skool lesson request does not itself restore a Skool promotion in the YouTube description.

