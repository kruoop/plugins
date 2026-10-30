---
name: bbn-youtube-tags
description: "Research current YouTube/Google Trends keywords and create a relevant Thai/English BoomBigNose Tags-field list within the combined 500-character budget. Use for 500 tags, keyword, yt search or gg trend now. Owns keyword evidence and tags only, not titles, descriptions, thumbnails or video editing."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# BBN YouTube Tags

Create one comma-separated list for the YouTube **Tags field**, not 500 separate tags and not a hashtag block. Read the current episode brief, accepted title if available, final content and prior keyword evidence. Select terms that describe this video.

## Fresh keyword evidence

- For a new full delivery or explicit “now/latest/search/Trends” request, inspect current YouTube search results and/or Google Trends. Default for Thai BBN content: Thailand, past 30 days, YouTube Search property. Respect the user's chosen geography, period or search surface; record the filters actually visible, not merely the requested URL.
- Prefer actual Trends Explore related/top/rising queries or actual YouTube search/suggestions. Search-engine results can help locate videos but do not establish query volume. Use official/current sources for platform limits. Read-only research does not require signing up for paid SEO tools.
- Record the observation date, source URLs, filters and relevant observed queries in the episode. Reuse the same still-current evidence across the title and description work; do not run duplicate research for every field.
- Separate observed search signals from editorial recommendations. A rising query is not automatically the largest query, a relative Trends index is not an absolute search count, and no tag set guarantees ranking. If Trends/search cannot be read, complete a content-based set and state the evidence limitation briefly.

## Choose and count

Lead with the exact product and episode intent; add relevant Thai beginner/use-case searches, English tutorial phrases, demonstrated features and project tools. Exclude `BoomBigNose`, `บูมบิ๊กโน้ส` and episode-number tags such as `EP221` or `EP 221`, including from reused packages. Deduplicate case-insensitively. Preserve useful spelling variants when justified. Do not add unrelated trending products, games or promises to fill space.

Target a useful set within 500 characters; use the budget when relevant terms support it, without padding just to reach exactly 500. Count the final parsed tags, including separators and the extra quotation overhead for tags containing spaces. The [official YouTube rule](https://developers.google.com/youtube/v3/docs/videos#snippet.tags[]) verified on 2026-09-10 is:

```python
tags = [tag.strip() for tag in text.strip().split(",") if tag.strip()]
youtube_count = sum(len(tag) + (2 if " " in tag else 0) for tag in tags) + max(0, len(tags) - 1)
assert youtube_count <= 500
```

For example, `Foo-Baz` costs 7, while `Foo Baz` costs 9; two tags `Foo Baz,AI` cost 12 including the comma. Plain string length alone undercounts multiword tags. Report which counting method was used; do not claim the YouTube Studio counter was tested unless it actually was.

## Save and deliver

Return one copyable `text` code block with the final comma-separated list, plus its checked budget count and a brief research basis outside the block. Save `output/<episode>-YouTube-tags-<version>.txt` and a compact dated keyword/count/source record in the same episode, following existing naming. Keep only safe artifact pointers in memory.

This skill owns the tags and keyword evidence. Other skills may use that evidence, but it does not rewrite their title/description files, render videos, install tools or publish metadata. A focused formatting revision can reuse valid current tags without starting another research cycle. Versioned tag files are local records only; the delivered tags live in `<EP>_Package.txt`, overwritten in place on Drive per [owner rules 2026-10-22](../bbn-ai-edit/references/owner-rules-2026-10-22.md). Never add EP numbers as tags.
