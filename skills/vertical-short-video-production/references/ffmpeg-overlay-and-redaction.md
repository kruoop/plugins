# FFmpeg Overlay and Redaction Pattern

Use this as a pattern, not a blind copy. Replace dimensions, rectangles, intervals, and duration with measured values from the current clip.

## Filter graph

```bash
ffmpeg -y \
  -i source.mp4 \
  -loop 1 -i icon.png \
  -loop 1 -i headline.png \
  -filter_complex "\
[0:v]split=3[base][s1][s2];\
[s1]crop=W:H1:X1:Y1,boxblur=20:2[blur1];\
[base][blur1]overlay=X1:Y1:enable='between(t,T1,T2)'[v1];\
[s2]crop=W:H2:X2:Y2,boxblur=20:2[blur2];\
[v1][blur2]overlay=X2:Y2:enable='between(t,T3,T4)'[v2];\
[1:v]scale=ICON_W:ICON_H[icon];\
[v2][icon]overlay=ICON_X:ICON_Y:shortest=1:enable='lt(t,INTRO_END)'[v3];\
[v3][2:v]overlay=0:0:shortest=1:enable='lt(t,INTRO_END)'[outv]" \
  -map "[outv]" -map 0:a:0 \
  -t SOURCE_DURATION \
  -c:v libx264 -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  output.mp4
```

Use the measured source container duration for `-t SOURCE_DURATION`: looped still-image inputs have no natural end. Filter-level `shortest=1` ends the picture at the source-video EOF; output-level `-shortest` alone is not a substitute for measuring the intended duration.

For overlay-only revisions, replace the example's audio encoding options with `-c:a copy`. Do not add output `-frames:v N`: FFmpeg can stop muxing at the video limit before copying the final AAC packet. Keep the strict verification rather than widening duration tolerance to hide a truncated tail. Assert the source and output video frame counts after encoding, compare container and stream durations, and compare both complete AAC streams:

```bash
ffmpeg -v error -i source.mp4 -map 0:a:0 -c:a copy -f adts - | shasum -a 256
ffmpeg -v error -i output.mp4 -map 0:a:0 -c:a copy -f adts - | shasum -a 256
```

The hashes must match for an audio-preserving revision. A video duration slightly shorter than its source container can be legitimate AAC timing; preserve the source relationship rather than trimming audio to match the last video frame.

## Verification

```bash
ffprobe -v error \
  -show_entries format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels \
  -of json output.mp4

ffmpeg -v error -i output.mp4 -f null -

shasum -a 256 output.mp4
```

Extract full-resolution frames from every redaction interval, including its start/middle/end:

```bash
ffmpeg -y -ss 16 -i output.mp4 -frames:v 1 qa_16.png
ffmpeg -y -ss 20 -i output.mp4 -frames:v 1 qa_20.png
ffmpeg -y -ss 22 -i output.mp4 -frames:v 1 qa_22.png
```

## Redaction correction loop

1. Inspect the unredacted suspect frames.
2. Record every vertical position occupied by the identifier.
3. Start with the smallest rectangle that covers the complete identifier through the interval.
4. Inspect rendered frames at multiple timestamps.
5. If any part remains readable, expand or split the rectangle and rerender.
6. Re-run full decode, probe, checksum, and visual QA after the final correction.

For narrow crops in yuv420p, set luma and chroma blur radii independently: a 48-pixel-high strip has only 24 chroma rows, so inheriting a radius of 20 fails. Use validated values such as `boxblur=luma_radius=20:luma_power=3:chroma_radius=10:chroma_power=3` and rerun the complete decode after correcting the filter.

Inspect sliding-sidebar transitions at subsecond intervals and split the moving region from the settled sidebar: a rectangle measured only after the panel settles can leave names visible during the animation. Limit the wider transition rectangle to the short movement interval to avoid unnecessarily obscuring lesson content.

A concrete failure mode: a URL appeared first inside a response body and later in the browser address bar. A narrow blur rectangle protected only one position. The corrected render used separate time-bound regions and was accepted only after full-resolution frame inspection.
