# Architecture remainder16 authoring checkpoint

Baseline: `afef4bf51c04b961fa149aad23b25019fcd3c35d`; scope is frozen in `remainder16-freeze.json` from the committed coordinator continuation manifest. Author identity: `01a12cc1-a1d0-75e1-9145-70e564a68e5b`.

## Current state

- Fifteen scoped cards have editorial candidate changes in `src/content/topics/architecture.json`; the Mont-Saint-Michel card is unchanged pending a source-quality decision.
- The intended changes preserve all 16 IDs, order, difficulty, and correct-answer indexes. A focused invariant check passed for four options and nonempty notes.
- Existing raw source captures referenced by the earlier findings were copied byte-for-byte into `sources/`; `source-copies-git-roundtrip.json` records lengths, SHA-256 and Git blob IDs.
- This is **not ready for independent review**. A fresh author receipt with the required 96 field-level reads, exact passages and claim analyses has not been completed. Do not treat previous author or reader receipts as evidence of my own current-field review.
- Mont-Saint-Michel remains a specific evidence blocker: the complete original source for the gazebo/belvedere/veranda/follies claims was unavailable in captured Git bytes. IFAS web material was readable in the browser/search result, but direct raw capture failed with DNS resolution errors; it cannot satisfy the raw-source requirement. Keep its existing card untouched and do not certify it. If it remains HOLD, cite the canonical Easy criterion exactly and name this unresolved source defect.

## Next required work

Read every current field directly against complete source bytes, establish field-level exact-byte receipts and analyses, repair source-backed issues, then run the authorized minimal source/invariant checks. Only after a complete honest author receipt exists should the candidate be frozen for a distinct independent reader. No reader certification, commit, build, deployment, or full-suite run has occurred in this checkpoint.
