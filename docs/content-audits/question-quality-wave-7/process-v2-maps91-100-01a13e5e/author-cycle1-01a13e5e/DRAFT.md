# Author cycle 1 — maps 92, 93, 95

Baseline: `0708bbfcf00bc2fd52df17dd0c19c364f5154e19`. Scope is source orders 92, 93 and 95 only. IDs, topic, order, medium difficulty and correctIndex 3 are preserved.

## Disposition

- **READY_FOR_INDEPENDENT_REVIEW:** 92, 93, 95; one substantive fix per INITIAL finding.
- **HOLD:** none in this bounded author cycle. Any substantive independent objection should hold only its affected ID; no further rewrite cycle is included.
- `qualityCredit` remains **0**. These are author proposals, not independent PASS, applied CURRENT, QA or acceptance.

## Fixes

- **92:** applies the saved 1:50,000 building workflow: `Shape_Area > 100` excludes small buildings, then `Simplify Building` simplifies selected contours. This corrects the prior reversed explanation of the threshold.
- **93:** calculates four boundaries across 0–80 °C (`80 / 4 = 20`) instead of merely naming a method.
- **95:** maps a three-class priority relation to label-class settings, separates priority from feature weight, and states that priority does not guarantee hospital visibility.

## Evidence and handoff

- `candidate.json` records exact before/after canonical hashes, six literal field groups and individual full prompt-answer-note assessments.
- `sourceproof.json` records full saved source paths, raw byte lengths and SHA-256, full reader captures and exact locators. No source was refetched.
- `peer-snapshot.json` preserves the actual receipt-linked CURRENT snapshot, neighbors 71/73/74 and 84/86/87/89/90, plus bidirectional quoted comparisons for every proposal and the three proposal pairs.
- `needed-evidence.json` lists independent and coordinator checks still open. No catalog edits, tests/runtime/build/deploy, commit or process actions were performed.

Next action: independent review of these exact proposals and saved primary context; then coordinator preimage check before any apply.
