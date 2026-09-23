#!/usr/bin/env bash
set -euo pipefail

deploy_host="${DEPLOY_HOST:-gfe}"
app_dir="${APP_DIR:-/opt/mindbattle}"
bundle="server-dist/network.js"

if [[ ! -f "$bundle" ]]; then
  echo "Missing local $bundle; run npm run build first" >&2
  exit 1
fi

local_hash="$(shasum -a 256 "$bundle" | cut -d ' ' -f 1)"
remote_hash="$(ssh -o BatchMode=yes "$deploy_host" "sha256sum '$app_dir/$bundle'" | cut -d ' ' -f 1)"
printf 'local  %s %s\nremote %s %s\n' "$local_hash" "$bundle" "$remote_hash" "$bundle"
[[ "$local_hash" == "$remote_hash" ]]
