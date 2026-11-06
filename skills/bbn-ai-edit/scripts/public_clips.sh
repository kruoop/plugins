#!/bin/sh
# Use the existing environment when possible; isolated optional runtime on Mac Studio.
set -eu
PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
export PATH
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
runtime="$HOME/.local/share/bbn-public-clips/venv/bin/python3"
if [ -x "$runtime" ]; then
  exec "$runtime" "$script_dir/public_clips.py" "$@"
fi
exec python3 "$script_dir/public_clips.py" "$@"
