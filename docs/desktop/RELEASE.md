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
npm run desktop:catalog
```

macOS produces a universal Intel/Apple Silicon DMG. Windows produces an x64 per-user NSIS installer. The first distribution has no developer certificate/notarization. Install warnings are expected; this does not weaken content signature verification. The normal `npm run build` / web deploy does not rebuild installers. Reserve several GB of free disk space for universal packaging. Build installers sequentially.

`desktop:content` prepares `desktop/bundle` and `desktop-release/content`. Installer commands refresh shell sources before packaging so an old staging directory cannot ship stale main/preload files. Do not edit code while packaging. The bundled game corresponds to the most recent `desktop:content` invocation.

## Publish (requires explicit production authorization)

The Caddy `/desktop/` routes must first be deployed from this change. Runtime assets live under `/var/lib/mindbattle-desktop`, outside `/opt/mindbattle` and its rsync `--delete` scope.

```sh
bash scripts/desktop/publish.sh content
bash scripts/desktop/publish.sh installers
```

Publishing uploads to an isolated directory, checks all hashes/sizes under a lock, atomically switches `current`, then removes previous completed releases of that kind. Incomplete uploads are not activated. `downloads.json` is switched with the pair of current installers. Only the newest completed installer per target is retained. Content is published independently; an interrupted client download retains the installed game and retries a complete current release later. Server retention and client last-good recovery are separate.

After publication, verify `/desktop/downloads.json`, both installer URLs and sizes/hashes, `/desktop/content/latest.json`, and the actual installed N→N+1 path. A build is not a deployment. Do not claim installation acceptance from packaging alone.

## Shell update boundary

Unsigned macOS applications cannot use the stock Electron/Squirrel.Mac autoUpdater. Content self-update does **not** update Electron, main or preload. The decision between a replacement installer for rare shell upgrades and a separately engineered unsigned-shell replacement helper is still pending. No automatic shell-upgrade guarantee is made by this implementation. Updating Electron for security still requires a new shell release, even when gameplay changes are small.

## Verification

`npm run test:desktop` exercises signatures, corruption, interruption/replay, rollback and protocol limits. `npm run check` covers the shared game. With `MINDBATTLE_CONTENT_KEY` set, `npm run desktop:smoke` launches real Electron with an isolated profile and a test-only fake upstream (never production), verifies offline launch, statistics persistence/ack, saved resolution, explicit signed update and storage survival. Optionally set `MINDBATTLE_DESKTOP_TEST_API=http://127.0.0.1:PORT` for the real local network API/SSE check. Evidence path can be set with `MINDBATTLE_DESKTOP_EVIDENCE`.

Human acceptance: install/open from DMG and NSIS on macOS/Windows; confirm offline play with actual input, full screen/windowed switching, exit, re-open; update a previously installed build; connect real phones in network mode. Track these separately from automated smoke.
