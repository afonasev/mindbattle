# Desktop releases

Mindbattle packages a sandboxed Electron renderer with the complete offline game. Runtime/main/preload are the **shell**; signed JS/CSS/catalog/assets are **content**. Content updates download in the background and are applied with the update icon in the menu. Active matches are never reloaded by the updater. A stable `mindbattle://game` origin and persistent partition keep localStorage and the IndexedDB statistics outbox across releases. Statistics upload uses the existing acknowledgement/idempotency contract, startup/online triggers and bounded retries.

## Build

Use Node matching package.json and `npm ci`. The pinned public key is `desktop/content-public.pem`. The corresponding Ed25519 private key is held by the release operator outside the repo; set `MINDBATTLE_CONTENT_KEY` to its absolute path. Never put its contents in Git, build output or logs. `npm run desktop:key` is only for the initial key creation; do not rotate the pin for an existing installation without a separate migration.

```sh
# Rebuild game/content, not installers. The sequence must increase.
MINDBATTLE_CONTENT_KEY=/secure/path/content-signing.pem npm run desktop:content
# Only for a new shell release (version in desktop/config.json).
npm run desktop:mac
npm run desktop:win
MINDBATTLE_CONTENT_KEY=/secure/path/content-signing.pem npm run desktop:shell
npm run desktop:catalog
```

macOS produces a universal Intel/Apple Silicon DMG. Windows produces an x64 all-users NSIS installer, `Mindbattle-<version>.exe`, with Program Files as the default path and UAC elevation at installation. Desktop shortcut and launch checkboxes are together on the last page and checked by default. The first distribution has no developer certificate/notarization. Install warnings are expected; this does not weaken content signature verification. The normal `npm run build` / web deploy does not rebuild installers. Reserve several GB of free disk space for universal packaging. Build installers sequentially.

`desktop:content` prepares `desktop/bundle` and `desktop-release/content`. Installer commands refresh shell sources before packaging so an old staging directory cannot ship stale main/preload files. Do not edit code while packaging. The bundled game corresponds to the most recent `desktop:content` invocation.

## Publish (requires explicit production authorization)

The Caddy `/desktop/` routes must first be deployed from this change. Runtime assets live under `/var/lib/mindbattle-desktop`, outside `/opt/mindbattle` and its rsync `--delete` scope.

```sh
bash scripts/desktop/publish.sh content
bash scripts/desktop/publish.sh shell
bash scripts/desktop/publish.sh installers
```

Content and shell publishing upload to an isolated directory, check all hashes/sizes under a lock, atomically switch `current`, then remove previous completed releases of that kind. Installer publishing uploads both assets to the public `afonasev/mindbattle` GitHub Release tagged `v<shellVersion>`, verifies GitHub SHA-256 digests and sizes, and publishes the release. The VPS downloads and hashes both public assets before atomically switching its metadata-only catalog and deleting previous installer payloads. Requires authenticated `gh` with repository release write access. Incomplete uploads are not activated. `downloads.json` is switched with the pair of current installers. GitHub retains versioned releases; the VPS retains only download metadata. Content is published independently; an interrupted client download retains the installed game and retries a complete current release later. Server retention and client last-good recovery are separate.

After publication, verify `/desktop/downloads.json`, both installer URLs and sizes/hashes, `/desktop/content/latest.json`, and the actual installed N→N+1 path. A build is not a deployment. Do not claim installation acceptance from packaging alone.

## Native shell updates

Ordinary shell upgrades use a separate native helper compiled with Go (CGO disabled), universal on macOS and x64 on Windows. Build requires Go and macOS lipo. A signed platform manifest includes every runtime file, mode, internal framework symlink and the executable entry point. The game downloads/verifies the complete runtime into userData. Clicking the update icon in a safe menu prepares a sibling installation, preserves installer/user extras using the installed inventory, then launches the independent helper from userData and exits. The helper verifies the pinned signature and hashes again, renames old/new directories, and launches the game at the same path with the same profile. A real rendered-menu acknowledgement confirms startup; failed startup restores and relaunches the previous installation. A failed release is not offered again until a newer signed sequence appears.

Full shell packages are published explicitly alongside installer rebuilds. Gameplay/catalog updates only need content publication. Updating Electron for security requires a shell release even when gameplay changes are small. The VPS retains only the latest complete runtime per platform and installer catalog; local last-good recovery is separate.

The replacement uses two directory renames with a journal, not an atomic exchange. Power loss between renames, an unwritable install directory, running from DMG/translocation, or failure to restore a damaged installation can require exceptional manual recovery. Do not delete a transaction backup while recovery is required. No sudo/UAC or policy bypass is used. Initial installers remain unsigned.

A writable installation is required. Windows NSIS installs in Program Files for all users. The existing runtime helper does not elevate privileges: in protected Program Files, shell upgrades may require the new installer; signed game/content updates in userData continue to work. On macOS, copy the app from DMG into a writable applications folder before launching. Preserve the private signing key permanently: installed games trust the pinned public key and cannot accept releases signed by a replacement key.

## Verification

With the signing key set, `node scripts/desktop/smoke-shell.mjs` verifies packaged macOS N→N+1 through the actual menu update button, and recovery after a candidate exits without acknowledging startup, using an isolated profile and loopback HTTP server. Windows helper is cross-compiled; macOS evidence does not establish Windows installation/update acceptance.

`npm run test:desktop` exercises signatures, corruption, interruption/replay, rollback and protocol limits. `npm run check` covers the shared game. With `MINDBATTLE_CONTENT_KEY` set, `npm run desktop:smoke` launches real Electron with an isolated profile and a test-only fake upstream (never production), verifies offline launch, statistics persistence/ack, saved resolution, explicit signed update and storage survival. Optionally set `MINDBATTLE_DESKTOP_TEST_API=http://127.0.0.1:PORT` for the real local network API/SSE check. Evidence path can be set with `MINDBATTLE_DESKTOP_EVIDENCE`.

Human acceptance: install/open from DMG and NSIS on macOS/Windows; confirm offline play with actual input, full screen/windowed switching, exit, re-open; update a previously installed build; connect real phones in network mode. Track these separately from automated smoke.

## Current version footer

For a publication build, set `MINDBATTLE_PUBLISHED_AT` to the release UTC ISO timestamp when running `desktop:content` (for example `2026-10-04T08:00:00Z`), and reuse that same value for the web publication build. `game-version.json` and the bundled HTML carry that timestamp; changing it requires rebuilding/re-signing content. Ordinary local builds leave it unset and display “Ещё не опубликована”. The footer reads the loaded HTML, never a newer upstream release. `scripts/deploy.sh` sets the web release timestamp unless the release operator supplies one. This setting does not authorize deployment.
