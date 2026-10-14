# Author fix packet: process-v2-weather10

- Scope: exactly the six IDs in `reviewer/fix-requests.json`. CURRENT6 hashes still match those requests. Fix-cycle baseline is HEAD `348a0fae46b8fd030f492d751f73f92f1fc998d7`; original task baseline was `e78ccdbe2e6d8e296bee2b7248d4ddd662c2fdd2`.
- Read `.agents/references/question-revision.md`, wave-7 proposal and parent initiative proposal. Frozen invariants: ID, topic, card order, `correctIndex`, difficulty and quotas. Independent replacement may change the correct answer's meaning while preserving its slot.
- Read the primaryContextIndex from immutable Git object `12e5581b`, then read each cited `gitCommit:body.path` via Git and verified byte length/SHA-256 against its index receipt. Source bodies were neither downloaded nor copied.
- **FIX, awaiting independent review:** El Niño asks the supported rainfall distribution; La Niña asks the independent equatorial-easterly response. The pair is no longer a mirrored SST question and no longer gives away ENSO by a phase-only answer category.
- **FIX, awaiting independent review:** observed environmental lapse rate becomes a multi-level radiosonde calculation (5.4 °C/km). The inversion card becomes an elevated cap/parcel-buoyancy inference and avoids the surface-base neighbor.
- **FIX, awaiting independent review:** lightning replaces the specialty polarity fact with the broad easy fact that lightning is a visible electrical discharge; the answer remains at correctIndex 1.
- **FIX, awaiting independent review:** NAO drops the unsupported named centers and geographical clue; its CPC-grounded pressure dipole and jet/storm-track signature identify the regime.
- All six cards retain their ID, topic, difficulty, order and correctIndex; each proposed card has four distinct options and six literal+SHA field groups with separate source reasons and editorial reasons. Candidate status FIX is a proposal, not acceptance. Same independent reviewer should inspect the exact six cards and neighbors.
- Checks: request/current hash equality, canonical sorted compact UTF-8 before/after and field-group hashes, frozen invariants, four unique answers, and source-body receipt SHA/byte equality. No catalog application, full tests, runtime, build or deploy.
- Only `fix-author/candidate.json` and `fix-author/report.md` were updated; `fix-author/technical-intake-hold.json` preserves the earlier technical intake. No commit was created.

**Next:** coordinator applies only independently accepted exact proposals; the same reviewer checks the changed cards and neighbors against the immutable source locators.
