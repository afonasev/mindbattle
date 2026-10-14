# Addressed fix cycle: CURRENT2

Baseline: `b964dcd0347cb8f1746489b72acba4241bbbafe7`. Scope is exactly `weather-climate-iod-indian` and `weather-climate-mediterranean-dry-summer`; one addressed cycle each from `reviewer/fix-requests.json`. Candidate only: no catalog/current card changed.

- `weather-climate-iod-indian`: **FIX candidate**. Removed the ocean name from the prompt while preserving the content task: recognize opposing west/east SST anomalies and associated rainfall contrast. All four options remain climate-mode labels; key 2 and medium difficulty are frozen. CPC IOD, NWS ENSO and CPC NAO primary contexts read; complete full-card neighbor review covers El Niño, La Niña, NAO and monsoon.
- `weather-climate-mediterranean-dry-summer`: **FIX candidate**. Narrowed note3 to ice-cap climate and its monthly-mean threshold. Met Office full climate-zones context read; complete full-card neighbor review covers equatorial, desert and Köppen C/B/E.

All six groups are recorded literally with canonical hashes and individual source/editorial reasons. Frozen ID/topic/order/difficulty/correctIndex remain unchanged. Existing source bytes/header bytes and SHA-256 were checked; no source was downloaded again or copied. Eight unrelated initial HOLD cards are untouched and do not block these candidates.

Checks: before/after and group canonical hashes; source byte counts and SHA-256; full card reads for both targets and listed neighbors; frozen fields and topic positions. No full tests, build, runtime, browser, catalog/index/claims edits, commit or apply performed. Next: coordinator reviews this candidate and exact-applies if accepted; then returns actual CURRENT hashes to the assigned independent Sol 6.1 reviewer.
