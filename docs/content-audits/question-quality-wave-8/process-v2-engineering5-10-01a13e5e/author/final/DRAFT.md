# Qualification revision: engineering machines sourceOrder 5–10

Separate `final/` packet; the original `author/` packet is preserved unchanged. Baseline `e581e5a505177afa60eceee1c4a5a0bf192f23f7`.

## Outcomes

- `bolt-fastener` (5) — FIX ready for independent review: now a plain definition of a shear bolt; no bolt/screw taxonomy or article cue. Key index remains 1 (`Срезной болт`). NASA RP-1228 names these for shear loading, warns against tension use, and halves table torque values.
- `screw-fastener` (6) — FIX ready for independent review: now defines a self-tapping screw by the thread it forms in an undersized untapped/punched hole. Key index remains 1. FAA AC 43.13-1B §§7-14 and 7-18 support the definition and note taxonomy.
- `nut-fastener` (7), `rivet-fastener` (8) — carried forward with existing FIX cards and primary-source grounds unchanged.
- `counterweight-balance` (9), `universal-joint` (10) — HOLD carried forward with no new content/source review. Prior HOLD records/evidence requests are retained.

## Sources and peers

Reused the full NASA RP-1228 100-page PDF/text capture. Relevant complete pages, figures and footnotes were read/rendered, including PDF p.26 (printed p.22) for shear bolts. NASA’s captured FAQ remains context only; neither revised stem uses “one of” or asks the player to recall an article.

Captured the official FAA AC 43.13-1B once over ordinary HTTPS. Full 696-page PDF and extracted text are saved under `sources/`; complete relevant printed pages 7-3 and 7-4 (PDF pp.366–367) were read and rendered. Source descriptions are paraphrases, not quotations.

`peer-snapshot.json` contains all 100 actual working-tree cards and hashes, relevant full neighbors, and 15 final-six comparisons. It records current sourceOrder 2 and 4 with full cards and `PENDING_INDEPENDENT_READER`; neither is treated as PASS. HEAD, index and working-tree catalog hashes are distinct.

`candidate.json` contains all six outcomes. `sourceproof.json` carries complete before/after hashes, six literal groups and four individualized prompt-answer-note assessments for revised 5/6; the 7/8 proof objects are unchanged. The 9/10 HOLDs are explicitly not re-reviewed. Quality credit remains 0 pending independent review and coordinator application.

No catalog, planning, Git/index, claim, test, runtime, build or deploy files were edited.
