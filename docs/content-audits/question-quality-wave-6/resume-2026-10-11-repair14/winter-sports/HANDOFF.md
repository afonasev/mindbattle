# Winter-sports repair14 author slice — 2026-10-11

Six assigned cards were revised: `winter-sports-007`, `008`, `017`, `019`, `023`, and `024`. The active reader receipts were not edited. The complete current-byte field literals and canonical hashes are in `author-receipt.json`; every card and all six fields remain **HOLD**, with no independent certification and no READY designation.

## Scope preservation

The winter topic remains at 100 cards. IDs and order are unchanged; all six cards retain their difficulty and correct answer index. A canonical comparison against the worktree HEAD found all 94 non-owned cards byte-semantically identical after JSON canonicalization. No other topics were changed by this slice.

## Editorial changes

- 007 replaces a host-city question with a basic ski-pole function question.
- 008 replaces a host-country question with identifying skates for moving over ice.
- 017 replaces Wayne Gretzky recognition with the basic snowboard definition.
- 019 replaces a specialized Zamboni mechanism question with the venue for ice hockey.
- 023 asks which ski surface contacts snow, keeping four ski components as alternatives.
- 024 describes open seats suspended from a cable; the four choices are types of ski lifts. The prior out-of-category funicular option was replaced with a magic carpet.

## Evidence and open work

No new complete source capture was successfully saved in this slice. Existing full originals in the earlier `winter-sports/resume-2026-10-11-fix19/originals/` folder were consulted for context, but this handoff does not claim fresh field-level passage proofs. `author-receipt.json` records each literal, current canonical card hash, the author HOLD, and the specific evidence gap. The next author pass should attach full original captures, exact passages and hashes to all six fields, then make a fresh author decision. A separate reader must review the six current hashes afterward.

## Verification

- `npm run content-check`: one test passed; `catalog-full.test.ts` failed because the existing `architecture` review stamp does not match the current architecture file. This is outside this slice and was not altered.
- `npm run typecheck`: passed (`tsc --noEmit`).
- No full suite, build, browser QA, deploy, or release was run.
