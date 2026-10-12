# Architecture current5 author repair — 2026-10-12

Author phase only; coordinator certification awaits a different reader’s whole-card reread.

- `architecture-empire-state-city`: corrected the Leade note to preserve “usually made of metal.”
- `architecture-skyscraper-definition`: corrected explanation and Leade note; current item is the LPC water-outlet question, not the historical building-addition item.
- `architecture-mont-saint-michel`: replaced duplicate façade-definition content with an independent easy parapet question; protected Burj Khalifa is unchanged.
- `architecture-cartagena`: narrowed the stem to the fate of all natural harbour passes and added named fortress examples to the correct note.
- `architecture-samarkand`: replaced the unsupported Xinjiang trend with an NPS-supported qualified fact about fired adobe-like bricks. Difficulty remains hard.

## Integrity

The 100-card ID order, 40/40/20 quotas, all five difficulty/correctIndex values, four-answer structure, and 95 protected card hashes match the frozen baseline. The personal author read covers all 30 fields across five complete current cards. `invariant-checks.json` records unchanged IDs/order/difficulty/key indices, 40/40/20 quotas, protected95 hashes, field bindings, and raw-source Git roundtrip. All six cited complete raw originals match their SHA-256 and Git blob; no capture was rewritten or freshly fetched. The duplicate scan and rejected first receipt are preserved in this folder.

## Focused check

`npm run content-check`: `catalog-topics.test.ts` passed; `catalog-full.test.ts` failed because `src/content/reviews/architecture.json` still has the previous topic hash. That file is outside this author workstream’s exact write scope, so it remains a coordinator follow-up. Full application tests, build, Player, device, deploy, merge, push, and human acceptance were not run or inferred.
