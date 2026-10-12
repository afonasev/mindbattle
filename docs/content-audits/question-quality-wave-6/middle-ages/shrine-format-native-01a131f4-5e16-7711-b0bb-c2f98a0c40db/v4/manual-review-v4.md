# V4 author qualification — middle-ages-shrine

Author thread: `01a131f4-5e16-7711-b0bb-c2f98a0c40db`

V4 is a new author receipt. V3 remains immutable history; no independent or human acceptance is claimed.

## Exact current card literals

- ID: `middle-ages-shrine`
- Difficulty: `easy`
- Prompt: На каком языке преподавали в университетах средневековой Западной Европы?
- Correct index: `1`
- Correct key literal: `Латынь`

| Index | Answer | Correct | Note |
|---:|---|---|---|
| 0 | Французский | no | Французский был одним из народных языков Европы; его нормы развивались иначе, чем закреплённые текстами нормы латыни. |
| 1 | Латынь | yes | На латыни преподавали и проводили диспуты; общее знание языка облегчало общение студентов и преподавателей из разных стран. |
| 2 | Английский | no | В английской речи эпохи Великого сдвига гласных особенности произношения латыни могли затруднять общение учёных из разных стран. |
| 3 | Немецкий | no | Немецкий был одним из народных языков Европы; его нормы развивались иначе, чем закреплённые текстами нормы латыни. |

**Explanation:** Латынь служила языком преподавания и диспутов в средневековых школах и университетах. Общее знание латыни облегчало обмены между европейскими учёными и академические поездки студентов.

The complete, sorted-hash-bound composite literal is in `author-receipt-v4.json` under `promptKeyLiteral`; it carries the exact prompt, four ordered answer texts, index, and key text together.

## Per-group and per-choice judgments

Every one of the six groups and four choices has explicit source and editorial `PASS` verdicts plus `proofRefs` to exact source excerpts. Complete paragraphs and offsets are in the receipt. The author judgments are not independent review.

- French note: sourced as a fact about the French vernacular and how its language norms evolved relative to Latin textual norms.
- Latin note: directly supported as the medieval university teaching/disputation language; Sorbonne context supports cross-European scholarly exchanges.
- English note: supported by the source paragraph on English pronunciation of Latin around the Great Vowel Shift and its effect on understanding.
- German note: supported as a vernacular language whose norms changed differently from Latin textual norms.

## Full source evidence

- Cambridge University Press: complete relevant paragraphs 5 and 29 are reproduced exactly from the saved original and each is bound to its character offset, paragraph offset and SHA-256. The entire HTML body and exact response headers are referenced by path, byte length, SHA-256 and Git blob at capture freeze `63ac6139f9cb9d8ce3246572632e2258678e1c45`.
- Sorbonne Chancellery: complete relevant paragraph 7 is reproduced exactly from the saved original, with matching offsets and hash. The raw body and headers are bound to the same exact capture freeze.
- Capture provenance and effective URLs are recorded. The source manifest was checked against the frozen post-correction header bytes, not the older line-ending-normalized blobs.

- The source metadata (`Spoken Latin in the Late Middle Ages and Renaissance Revisited — Journal of Classics Teaching (Cambridge University Press)`) was inspected separately: article/journal, author, publication date, Cambridge Core identity and exact successful effective URL are recorded in `sourceMetadataReview`.

## Difficulty, catalog boundary, and next review

- Easy verdict: **PASS**, re-evaluated for V4. The candidate tests a broadly familiar medieval cultural-history fact with plain wording and no obscure date or terminology trap. This remains an author judgment for the independent reader to challenge.
- V4 leaves prompt, choices/order, key/index, difficulty, explanation and metadata unchanged; only the three wrong-answer notes were repaired for language-specific ownership.
- V3’s targeted retrieval over 11,000 cards remains the applicable catalog review because the question and key are unchanged. It found one incidental overlap in a wrong-answer note on the Villers-Cotterêts card; the details and manual neighbors remain in V3.
- Compared with baseline `e02389f`, the protected 99 cards are unchanged. V3 remains untouched. No tests, suite, build, Player, deployment or human acceptance were run or inferred.
- Next gate: a fresh independent reader reviews V4 and re-evaluates Easy; V3 judgments are historical only.
