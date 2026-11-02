#!/usr/bin/env bash
# KAN-76 sharp render for a HyperFrames motion composition.
# 2x supersample (Chrome deviceScaleFactor) -> lossless PNG -> Lanczos to the
# composition size with full-chroma conversion -> H.264 High, BT.709 tagged.
# Usage: render_sharp.sh <project_dir> <out.mp4> [crf=10]
# Uses plain `npx --yes hyperframes` (override with env HYPERFRAMES="...").
set -euo pipefail
[ $# -ge 2 ] || { echo "usage: $0 <project_dir> <out.mp4> [crf=10]" >&2; exit 2; }
proj=$(cd "$1" && pwd); out=$(cd "$(dirname "$2")" && pwd)/$(basename "$2")
crf=${3:-10}; HF=${HYPERFRAMES:-"npx --yes hyperframes"}
here=$(cd "$(dirname "$0")" && pwd)
node -v >/dev/null 2>&1 || { echo "node does not start; fix it first (e.g. brew upgrade node / brew reinstall node)" >&2; node -v; exit 1; }
python3 "$here/check_motion_html.py" "$proj/index.html"
w=$(grep -o 'data-width="[0-9]*"' "$proj/index.html" | head -1 | grep -o '[0-9]*')
h=$(grep -o 'data-height="[0-9]*"' "$proj/index.html" | head -1 | grep -o '[0-9]*')
fps=$(grep -o 'data-fps="[0-9]*"' "$proj/index.html" | head -1 | grep -o '[0-9]*'); fps=${fps:-30}
if [ "$w" -ge "$h" ]; then res=landscape-4k; else res=portrait-4k; fi
[ "$w" = "$h" ] && res=square-4k
had_cache=0; [ -e "$proj/.hyperframes" ] && had_cache=1
tmp=$(mktemp -d)
cleanup() { rm -rf "$tmp"; [ "$had_cache" = 1 ] || rm -rf "$proj/.hyperframes"; }
trap cleanup EXIT
(cd "$proj" && $HF render --format png-sequence --resolution "$res" --output "$tmp/png") >"$tmp/render.log" 2>&1 \
  || { tail -40 "$tmp/render.log"; exit 1; }
ffmpeg -v error -y -framerate "$fps" -i "$tmp/png/frame_%06d.png" \
  -vf "scale=${w}:${h}:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -preset slow -crf "$crf" -profile:v high \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -movflags +faststart "$out"
ffprobe -v error -show_entries stream=width,height,pix_fmt,r_frame_rate,bit_rate,color_space:format=duration -of compact "$out"
