# Public reference, meme and gag excerpts — KAN-93 v1.0

Read this when the owner asks to insert a public video link into a BBN EP. Use the existing final cut plan and transcript. The helper changes pictures/audio only inside the requested cue windows and keeps the EP duration unchanged; it does not insert extra seconds or regenerate speech. A request to extend the EP needs a new cut plan and downstream chapter remap first.

## One-request workflow / Slack

Example owner request through the existing Slack editor route:

> แทรกคลิปใน EPxxx จาก https://www.youtube.com/watch?v=aqz-KE-bpKQ ช่วง 02:17–02:20 เป็นเรฟที่ EP 00:05; มีมช่วง 02:30–02:32 ที่ EP 00:12 ปิดเสียง; gag ช่วง 02:40–02:41 ที่ EP 00:18 ใช้เสียงคลิปแทนช่วงเงียบ พร้อมเครดิต Blender

The editing agent translates this request to a cue sheet, checks the final transcript/screens, and runs the command below once. Do not create another Slack bot, watcher or credentials. If the Slack route is not configured, return the same command/result in the current chat. Do not promise a new slash command or claim every social platform works without a live test.

1. Resolve the specific EP/base review file and requested source URLs. Convert source/EP `hh:mm:ss` to numeric seconds. All `at`, `protected` and `speech_free` times belong to the **final EP**, after speech cuts. Reuse the existing cut-plan remapping; never use raw footage times as final times.
2. Read the transcript and actual frames; mark every teaching/demo window in `protected`. During an explanation, use an explicit reference `box` that clears the presenter and meaningful content. No cue may overlap `protected`, including a reference. If a requested time conflicts, find a nearby explanation/pause and tell the owner what moved; do not mark it safe without checking.
3. Copy/adapt [the cue sheet](../assets/public-clips-plan.example.json). Set `timing_reviewed: true` only after the check. The template's false value is intentional. Add source/channel credit and a rights/music note. Use original geometric icons drawn by the helper; no emoji.
4. Run from the installed skill (paths are relative to the plan file):

```sh
sh scripts/public_clips.sh render --plan /path/to/EP/public-clips.json
```

This one command validates, downloads just the requested ranges, composites all cues, and emits `output.mp4`, `output.credits.txt`, and `output.report.json`. `validate --plan ...` is a network-free optional preflight. Existing output files are never overwritten; select a new local review output, then deliver accepted revisions through the normal same-name/same-ID Drive route.

5. Inspect every cue's entrance/hold/exit and return to teaching in the **encoded output**. Read the complete on-screen credit and check presenter/controls, lip sync and audio. Measure final loudness/true peak using the episode's existing QA. Record whether real-time listening happened; numerical checks are not listening. Include `credits.txt` in the existing Package's Description source section, preserving owner-edited text and the fixed Package format. Check episode chapters again if another edit changed time.
6. Deliver through the already authorized episode route. For KAN-93, attach demo, skill changes, tests and risks to the ticket and submit to Patsinee; approval remains pending until explicit evidence arrives. Publication is separate.

## Cue sheet fields

| Field | Meaning |
|---|---|
| `base`, `output` | Existing already-cut EP, new local review output; no source overwrite |
| `timing_reviewed`, `protected` | Explicit final-clock review; `[start,end]` teaching windows |
| `speech_free` | Reviewed windows with no narration, required for replacement source audio |
| `cache` | Optional excerpt-only cache directory, relative to cue sheet |
| `font` | Optional Thai-capable TTF path; otherwise discovers Sarabun/IBM Plex Sans Thai in user Fonts |
| `cues[].url` | Public source link; HTTP(S), no embedded account credentials |
| `credit_url` | Optional shorter canonical public source page; defaults to source link; shown in full |
| `start`, `end`, `at` | Source range and EP placement in seconds; each excerpt >0 and <=30s |
| `mode` | `ref` (inset), `meme` or `gag` (full frame) |
| `box` | Optional `ref` rectangle `[x,y,width,height]` in output pixels; choose from actual frames |
| `audio` | `mute` default; `under` normalized to -20 LUFS then attenuated (default -20 dB); `replace` only inside `speech_free` |
| `clip_gain_db` | `under` attenuation -60 to -12 dB; source loudness normalized before attenuation |
| `channel` | Owner-supplied correct credit, or extracted channel/uploader; required for local excerpts |
| `rights_note` | License/permission evidence, music check and remaining Content ID risk |
| `local_excerpt` | Optional **already-trimmed** supplied excerpt with matching duration; retains source URL/range/credit and records its hash; never downloads a full source to populate this field |
| `limits` | `max_clip_mb` default 128 (max 512); `download_timeout_seconds` default 180 (max 600) |

`gag` supports picture-only (`mute`) and picture + source sound (`under`/`replace`). For a sound-only gag, set `visual: false`; the source credit still appears, so place it in a reviewed free area. A helper version without sound-only support must not claim it rendered that variant.

Reference defaults are a starting point, not verified safe placement. Cues cannot overlap each other. Excerpts with no audio remain valid; an audio replacement cue with a silent source leaves the original audio intact and is reported as silent in the media metadata.

## Runtime and acquisition

Dependencies: FFmpeg/ffprobe, yt-dlp and Pillow with RAQM for Thai shaping. Use installed tools first. On Mac Studio the optional isolated runtime is `~/.local/share/bbn-public-clips/venv/`; the launcher uses it when present. Setup when missing:

```sh
python3 -m venv ~/.local/share/bbn-public-clips/venv
~/.local/share/bbn-public-clips/venv/bin/python3 -m pip install 'Pillow>=12,<14' 'yt-dlp[default]'
```

The downloader uses `--ignore-config --no-playlist --download-sections '*start-end' --downloader ffmpeg --force-keyframes-at-cuts`. It never falls back to full download. A watchdog kills downloader/FFmpeg children on size, time or free-space limits (1 GiB reserve). Some servers require seeking/index/initialization data, so requested playback length does not equal exact network bytes. A section-only output and disk cap do not prove the server transferred only that range. Stop rather than bypass DRM, login or access prompts. X/Facebook/TikTok are supported only to the extent the installed yt-dlp extractor can access that **public link** and retrieve its range; report failures per source. YouTube can also fail when extractor support drifts.

The cache key includes URL and exact range; cache reuse checks SHA-256 and source identity. Reports keep public source identity and hashes, not signed playback URLs/cookies. Temporary failed fetch/render files are removed; retained excerpt caches stay available for active revisions. Normal accepted-episode cleanup rules still apply.

Use short, relevant excerpts, credited on screen and in Description. Credit and public availability do not establish permission or prevent Content ID claims. Avoid unlicensed music; record what was checked and remaining risk. For an initial demo, use a source with explicit reuse evidence such as Blender's Big Buck Bunny, link the [publisher's license information](https://peach.blender.org/about/), indicate excerpts/edits, and still leave publication review pending.

## Added in v1.0

- Section-only URL acquisition, verified excerpt cache and resource limits.
- Final-clock protected teaching windows; three insert modes with source credits.
- Mute/under/replace audio policies, normalization and short fades; no active-narration replacement.
- Description credit list and hash/provenance/QA report.
- Original drawn credit icons and Thai font shaping, consistent with KAN-76.
- Real-media behavior tests and a Mac Studio demo; no replacement of the existing Slack workflow.
