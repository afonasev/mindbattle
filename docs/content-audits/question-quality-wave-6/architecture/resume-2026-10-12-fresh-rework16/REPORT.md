# Architecture16 fresh author rework — 2026-10-12

Scope: exactly 16 approved Architecture IDs in `src/content/topics/architecture.json`; current author review covers 96 fields. Source baseline is `cf60970`, review input is `independent-pilot/resume-2026-10-12-architecture16-current/`.

## Changed IDs

- `architecture-skyscraper-definition`
- `architecture-alhambra`
- `architecture-mont-saint-michel`
- `architecture-machu-picchu`
- `architecture-parthenon-city`
- `architecture-colosseum-city`
- `architecture-hagia-sophia-original-purpose`
- `architecture-entasis-effect`
- `architecture-cantilever-support`
- `architecture-empire-state-city`
- `architecture-statue-liberty-city`
- `architecture-fez`
- `architecture-cartagena`
- `architecture-durham`
- `architecture-samarkand`
- `architecture-bam`

## Author result

- All 16 target cards were reworked or individually retained after reading the current literals against the cited complete originals. `author-review.json` preserves each prior field verdict/defect, the previous reader's literal, this author's current literal, a direct source passage, locator, URL, raw SHA-256, Git blob, and a field-level decision.
- `sources/` contains the 27 source captures used by the independent review plus captured NPS and USGS originals for the new Samarkand distractor facts. `sources-manifest.json` records complete raw format, URL, byte length, SHA-256 and Git blob. All 96 cited passages were checked against these complete captures.
- Main fact changes include the distinct gutter/downpipe item replacing the duplicate building-addition question; removing the awning/hood overlap; correcting the Forth Bridge components; aligning Durham cathedral notes to their own UNESCO originals; tying all Cartagena notes to their option; and putting Samarkand options in the construction-material class while retaining hard difficulty.
- IDs/order/difficulty/correctIndex are unchanged. The full catalog difficulty and answer-key-slot distributions match baseline. All 84 protected cards match their expected per-card canonical hashes; no protected text was edited. The original 16 whole-card HOLD and field labels remain unchanged; this work does not certify cards PASS.

## Verification

- Exact scope: 16/16 changed IDs; 96/96 field bindings and exact quotes verified.
- Raw source captures: 29/29 byte lengths, SHA-256 values and Git blob IDs verified.
- Source file parsed and serialized back to byte-identical JSON; protected84 hash list and catalog identity checks pass.
- `npm run content-check` was run because this is a content catalog change. At frozen HEADs `cc90be7f5005859c30121dbad1a4f270b09d7aec` and, after these final Architecture text edits, `134cb42a50afcbf66700773cf6d80e4f13ebcce2`, it failed only on `winter-sports/winter-sports-007` and `winter-sports/winter-sports-008`, each with a one-sentence explanation. No Architecture error was reported. The coordinator will handle that exact Winter fix; it is outside this author scope.
- Full suite, build, deployment and certification were not run/claimed.

## Remaining review

The coordinator and a different independent reader must re-read all 16 current cards / 96 fields and decide whether each repair resolves its historical HOLD. Until then, all 16 remain whole-card HOLD and all 38 historical field HOLD remain in history.

Author record: native author `01a12e95-b8fd-7430-8c4b-e7117a71a378` reviewed 16 cards / 96 fields. The field-level author source/editorial verdicts are recorded in `author-review.json`; these do not replace the preserved independent historical HOLD labels or coordinator/different-reader closure.
