# Japan 10 author packet

Baseline: `2410346df0cecff7102f5aee66e29c5822243b67`. Source packet: `12e5581b:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-4f5e-7cb0-b9b6-acba5e06d759/tmp-source-files/japan100-topic-source-author-v4.json`; manifest: `12e5581b:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-4f5e-7cb0-b9b6-acba5e06d759/japancc-manifest.json`. The preimage packet locator adds a `tmp-source-files/` component absent from the Git tree; resolved the saved packet at `.../preserved/mindbattle-source-01a13956-4f5e-7cb0-b9b6-acba5e06d759/japan100-topic-source-author-v4.json` and matched its 341,906 bytes / SHA-256 to the manifest inventory entry.

| Status | IDs |
|---|---|
| READY | history-japan-easy-02a-01, history-japan-easy-02a-04, history-japan-easy-02b-01, history-japan-easy-02b-03, history-japan-easy-02b-04, history-japan-easy-02b-05 |
| FIX | history-japan-easy-02a-02, history-japan-easy-02a-03, history-japan-easy-02a-05, history-japan-easy-02b-02 |
| HOLD | — |

## Review

- Read every full target card from the preimage, including all four choices, key, explanation and four notes; verified each preimage canonical hash.
- Read the relevant target passages from the saved primary bodies and headers at their typed Git blob locators; for PDFs, reviewed the cited page and section. For Hiroshima, the existing body was absent, so the single bounded request succeeded; full response is preserved under `author/sources/`.
- Corrected four bounded issues: Hiroshima prompt precision; Spain/Portugal blanket neutrality note; kamikaze attacks vs pilots; current ninja vs historical shinobi terminology. Other text was retained where no concrete defect was established.
- Neighbor review searched all 110 `src/content/topics/*.json` files for the event names and distinctions; related cards and non-duplicate rationale are attached per entry.
- Frozen invariants checked: ID, difficulty and correctIndex unchanged for every entry. Whole-card and literal hashes use sorted compact UTF-8 JSON or exact literal bytes, without Unicode normalization or trailing newline.
- I did not stage or commit the author package. During this task the shared branch HEAD advanced from the assigned baseline `2410346d` to `adfbbf66` (`Admit independent CURRENT USGS water-color card and preserve Japan10 baseline`); that commit contains the preimage and other coordinator records, not this author folder. The author package remains untracked for coordinator application. I did not modify the catalog, source index, claims or planning. No build, runtime or full tests were run.

## Remaining review limits

- The audit reviewed distractor claims in context and found no definite factual defect outside the changes listed. Existing primary contexts most directly establish each question’s target fact; coordinator and independent CURRENT review should adjudicate the distractor-note evidence and neighbor decisions.
- No full test/build/runtime check was run, per scope.
