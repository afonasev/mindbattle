#!/usr/bin/env bash
# Explicit release operation. Requires production authorization; never called by build/deploy.
set -euo pipefail
kind="${1:-}"
case "$kind" in content|installers) ;; *) echo 'Usage: publish.sh content|installers' >&2; exit 2;; esac
node scripts/desktop/verify-release.mjs "$kind"
source_dir="desktop-release/${kind}"
test -d "$source_dir"
release_id="$(date -u +%Y%m%dT%H%M%S)-$(openssl rand -hex 6)"
remote_host="${DEPLOY_HOST:-gfe}"
remote_base="/var/lib/mindbattle-desktop/${kind}"
ssh -o BatchMode=yes "$remote_host" "mkdir -p '${remote_base}/incoming-${release_id}'"
rsync -az "${source_dir}/" "${remote_host}:${remote_base}/incoming-${release_id}/"
ssh -o BatchMode=yes "$remote_host" python3 - "$kind" "$release_id" < scripts/desktop/publish-remote.py
