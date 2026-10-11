# Winter-sports repair14 author freeze — 2026-10-11

Six assigned cards are revised and frozen for independent reading: `winter-sports-007`, `008`, `017`, `019`, `023`, and `024`. All six cards and all 36 audited fields have manual author PASS decisions. Current canonical card hashes, literal hashes, source passages, locators, and full-source SHA256 values are in `author-receipt.json`. `source-manifest.json` identifies the 11 full HTML/PDF originals used; two new full HTML captures (Maine ropeway definitions and NPS snowshoeing guidance) are retained under `sources/`.

## Editorial results

- 007 asks which ski equipment helps maintain balance; FIS defines the function of ski poles.
- 008 asks what is worn to glide on ice, with sourced winter-equipment distractors.
- 017 asks for the winter sport performed on one board; alternatives are alpine skiing, bobsleigh, and cross-country skiing.
- 019 asks which venue hosts ice hockey; all alternatives are venues for other winter sports.
- 023 asks which longitudinal ski surface contacts snow and supports glide; alternatives are other ski components, supported by FIS equipment specifications.
- 024 distinguishes a chairlift from a T-bar, gondola, and skimobile. All four alternatives are actual mountain-lift types under the cited state definitions.

## Preservation and limits

The winter catalog remains at 100 cards with 40/40/20 difficulty quotas and 10/10/5 correct-answer positions per slot. IDs and order are unchanged; the six cards retain difficulty and `correctIndex`. All 94 non-owned cards are canonically identical to the baseline at `35fad8e4ef690de8b1048dc99e7f083fa4af0f8d`. No active reader receipt or other topic was changed in this slice.

This is an author freeze only. Independent reading of these six exact hashes and coordinator certification remain pending. The author PASS is not human/product acceptance. No full test suite, build, browser QA, deployment, release, or archive was performed.

## Checks

- `npm run typecheck`: passed.
- Focused `npx vitest run tests/unit/catalog-topics.test.ts`: blocked by the current foreign `middle-ages` working-tree file (39 medium / 21 hard versus its 40/20 quota); that file was preserved untouched, so the loop fails before it validates winter-sports.
- For winter-sports, the author preservation check confirms 100 cards, 40/40/20 quotas, correct-key slots 10/10/5, stable ID order and non-owned card hashes. All 36 receipt literals and 65 proof locators were re-read and checked against the exact raw captures.
- The broader `content-check` and build are not repeated; full-suite/build/deploy/release remain outside this author slice.
