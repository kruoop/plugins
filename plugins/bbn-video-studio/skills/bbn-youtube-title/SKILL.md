---
name: bbn-youtube-title
description: "Write or revise Thai BoomBigNose YouTube video titles: catchy, searchable and faithful to the actual episode. Use for ขอ title, ชื่อคลิป, ขอโดนๆใน YouTube, or the title portion of a BBN delivery. Owns the video title only, not thumbnail artwork, descriptions, tags or video editing."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# BBN YouTube Title

Write the public video title for the current episode. Read the current request, project instructions and episode brief, final content summary, existing title choices and any current keyword research. A title-only request does not start a video edit or generate unrelated assets.

## Editorial choice

- Put the real product/topic and a concrete viewer benefit early. For tutorials, prefer a clear learning promise and demonstrated result over vague hype. Use natural Thai with accurate English product names.
- Lead with one recommended title. Supply up to two alternatives when the user asks for options or a stronger hook; do not keep reopening a settled choice.
- Preserve the user's selected wording. If asked only to add `101`, add it without rewriting the accepted promise. Use `101` for the requested beginner/foundation positioning; do not force it into unrelated news or advanced topics. An episode's “อัปเดต” is not evidence of a new product version number.
- Every promise must fit the actual delivered video: real website creation/deployment, agents, automation or other demonstrated outcomes. Avoid invented benchmarks, income claims, guaranteed results or unsupported “free” claims.
- Reuse fresh episode keyword findings when available. A creative title request does not require a separate keyword audit. If the user explicitly requests current search/trend evidence and none exists, use [bbn-youtube-tags](../bbn-youtube-tags/SKILL.md) for that bounded research, then return to the title; do not repeat the same search.

## Check and deliver

Check spelling, exact requested terms, topic/result consistency and the [YouTube title limit](https://developers.google.com/youtube/v3/docs/videos#snippet.title), verified as 100 characters on 2026-09-10. A limit is not a target: retain useful wording without padding.

Return the recommended title directly, with no essay. For an existing episode project, save the accepted title or clearly labeled recommendation as a versioned `output/<episode>-YouTube-title-<version>.txt`, following existing naming. Record only safe artifact pointers in project memory. The title skill owns this file; it does not rewrite the description or tags. Creating title text is not publication. Versioned title files are local working records only; the delivered title lives in `<EP>_Package.txt`, which is overwritten in place on Drive (same name and ID) per [owner rules 2026-10-22](../bbn-ai-edit/references/owner-rules-2026-10-22.md). Do not ask back: pick the recommended title from the episode evidence.
