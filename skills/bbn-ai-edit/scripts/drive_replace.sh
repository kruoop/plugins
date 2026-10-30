#!/usr/bin/env bash
# Upload a deliverable into BBN-Video/<EP>/ by overwriting the same-named Drive file in place
# (same file ID, no _v2/_v3 copies, no duplicates), then verify ID + md5.
# Usage: drive_replace.sh <local-file> <EP-folder> [remote-name]
# Env: BBN_DRIVE_REMOTE (default: bbndrive: if configured, else gdrive:)
#      BBN_DRIVE_ROOT   (default: BBN-Video 13PTVmiD5YJPVgytx5WLYpJs3M-EvpcwZ)
set -euo pipefail
src=$1; ep=$2; name=${3:-$(basename "$src")}
remote=${BBN_DRIVE_REMOTE:-$(rclone listremotes | grep -qx 'bbndrive:' && echo bbndrive: || echo gdrive:)}
root=(--drive-root-folder-id "${BBN_DRIVE_ROOT:-13PTVmiD5YJPVgytx5WLYpJs3M-EvpcwZ}")
list() {  # missing folder = empty; any other rclone error aborts the script
  local err out; err=$(mktemp)
  if out=$(rclone lsjson "${root[@]}" --files-only --hash --hash-type md5 "$remote$ep/" 2>"$err"); then rm -f "$err"; echo "$out"; return; fi
  grep -qi 'directory not found' "$err" && { rm -f "$err"; echo '[]'; return; }
  echo "ABORT: rclone lsjson failed: $(cat "$err")" >&2; rm -f "$err"; return 4
}
pick() { python3 -c 'import json,sys; m=[f for f in json.load(sys.stdin) if f["Name"]==sys.argv[1]]; print(len(m), *(m[0]["ID"], m[0].get("Hashes",{}).get("md5","")) if m else "")' "$name"; }

listing=$(list) || exit 4; read -r n before_id _ <<<"$(pick <<<"$listing")"
[[ "$n" =~ ^[0-9]+$ ]] || { echo "ABORT: could not parse Drive listing" >&2; exit 4; }
[ "$n" -le 1 ] || { echo "ABORT: $n files named '$name' in $ep — clean duplicates first (rclone dedupe)" >&2; exit 2; }
rclone copyto "${root[@]}" "$src" "$remote$ep/$name"
listing=$(list) || exit 4; read -r n after_id md5 <<<"$(pick <<<"$listing")"
local_md5=$(md5 -q "$src" 2>/dev/null || md5sum "$src" | cut -d' ' -f1)
[ "$n" = 1 ] || { echo "FAIL: expected 1 '$name', found $n" >&2; exit 3; }
[ -z "$before_id" ] || [ "$before_id" = "$after_id" ] || { echo "FAIL: file ID changed $before_id -> $after_id" >&2; exit 3; }
[ "$md5" = "$local_md5" ] || { echo "FAIL: md5 remote $md5 != local $local_md5" >&2; exit 3; }
echo "OK $remote$ep/$name id=$after_id md5=$md5 $([ -n "$before_id" ] && echo replaced-in-place || echo new)"
