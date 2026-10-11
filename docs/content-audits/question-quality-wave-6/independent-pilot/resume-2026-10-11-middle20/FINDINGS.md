# Independent review: frozen Middle Ages 20

Reader: `01a12b59-563f-7102-816b-105461e96a3c`, role **independent**.
Author content freeze: `73d7174`; author evidence: `59e97f1`.
Scope and all 20 current hashes: `freeze.json`; full 120-field receipt: `independent-current.json`.

Independent decisions: **15 PASS, 5 FIX_REQUIRED**. Field decisions: **115 PASS, 5 FIX_REQUIRED**.
These are independent judgments, **not new certified cards**. Coordinator owns reconciliation and counting.
No catalog card, planning, claim, lease, ledger, test or validator was edited.

## Blocking findings

| Card | Exact field / literal | Rule and necessary correction |
|---|---|---|
| `middle-ages-abbey` | `source.url` is Lilleshall; prompt says «В обычной цистерцианской планировке»; explanation names Cleeve | The linked page describes Lilleshall and a typical monastery, not the standard Cistercian arrangement. The correct direct primary page is `https://www.english-heritage.org.uk/visit/places/cleeve-abbey/history/`, retained original L250. Fact and key are correct; replace source binding. This source finding is recorded under prompt-key in the six-field schema and covered by the whole-card hash. |
| `middle-ages-priory` | Prompt asks «монастырь под руководством приора»; `answers[2].text` = «Клуатр», `[3]` = «Капитулярный зал» | Two parts of a monastery are not comparable monastery types. Use four plausible institutions or a different approved medium fact, keeping immutable slots/quotas. Notes themselves are supported. |
| `middle-ages-cloister` | Prompt asks «крытая галерея»; `answers[0].text` = «Аббатство», `[2]` = «Приорат» | Whole monastic institutions do not form plausible types of gallery/architectural parts. Replace the incompatible distractors with comparable components. |
| `middle-ages-chapter-house` | Prompt «В каком помещении»; `answers[0].text` = «Аббатство», `[1]` = «Приорат» | Whole institutions are not rooms; the key is the only explicitly named hall. Four room-level options are needed. |
| `middle-ages-lord` | Prompt «Кто победил войско короля Гарольда»; `answers[1].text` = «Гарольд» | Harold would have to defeat his own army. This is an obviously impossible distractor, forbidden even in easy. Also see the global primary-fact overlap below when choosing a replacement. |

`abbey` also deserves difficulty calibration: exact Cistercian room placement is more specialized than ordinary exposure to medieval history. This is an advisory signal; it is not silently used to move difficulty or relax quotas. Its blocking source mismatch is independently reproducible.

## Duplicate and topic reasoning

The candidate scan searched prompt + correct key across the current catalog using names and relationships for these 20; `duplicate-candidates.json` preserves its results. This is retrieval, not automated semantic certification. Only relevant candidate primary facts were compared; previously saved complete receipts were not reopened or changed.

- `lord` and `history-united-kingdom-easy-02-01` both test the Norman victory that gave William the English crown. The latter asks for Hastings; the former asks for William using Harold's defeat and the crown. This is a close repackaging of the same historical relation. Choose an independent fact when repairing `lord`. The Domesday survey in `world-history-ext-norman-conquest-1066` is a distinct fact and is **not** a duplicate merely because William appears.
- `parchment` asks animal skin construction; `ancient-world-parchment` asks folding into a codex. These are different properties. An overlap in the older explanation/note does not by itself turn the current primary fact into a duplicate.
- `scholasticism` asks the intellectual tradition of logic and authorities; `disputation` asks the formal practice of debate. Related practice/tradition is not a direct/inverse definition of one relation.
- `hanse`, `kontor`, `commune`, `staple`: respectively a league of cities, an overseas trading post, collective urban rights, and a local sales requirement. Shared notes and adjacent terms are not blanket defects.
- `lord` now asks William, so it is no longer the inverse definition of vassal→lord. `vassal` asks a personal relation, `fief` the condition of landholding, `homage` a ceremony, `allod` an unconditional tenure. No automatic rejection for the common feudal vocabulary.
- The clerical cards ask Bruno's distinction between purchase of income and orders, the sanction in 1078, and electoral rights in 1122. The general `investiture` card asks the name of a ceremony. These are separate primary facts.
- `polyptych` now asks the etymology of miniature; `cartulary` asks documentary compilation. No second matching primary question was found in the inspected candidate set.

All 20 are connected to the taxonomy scope «Общества, события и культура Средневековья в разных регионах». Papyrus/modern imaging in distractor notes do not move the primary manuscript question out of the Middle Ages. Stable historical facts require no moving-current-year qualification.

## Evidence procedure and limits

The first five cards / 30 fields were written into `pilot-independent.json` and successfully roundtripped in `pilot-format.json` before the remaining 15 were added. The pilot is retained unchanged. Six additional manually selected source locators strengthen the final receipt; the pilot's verdicts remain the same.

The author receipt was used only as an index of existing originals and exact passages. Independent literal readings, editorial analyses and decisions are in the two `manual-*-decisions.json` files. The binding script hashes scalars and carries those handwritten decisions; it cannot invent a verdict. Correct notes with a useful extra fact may overlap explanation and were accepted on that basis.

The original institutional HTML and complete documented web extraction responses remain in their committed author source locations; relative paths/hashes bind each final proof. Stanford's 495-line extraction was checked against all six raw original response files and their hashes (no missing source lines); live Stanford text in the relevant section also agreed. It is a full source extraction with trace, not a selected-quote summary. The malformed Oxford PDF and failed/challenge captures were not used.

Only focused mechanical receipt/preservation checks were run. Full suite, npm check/qa, browser tests, builds, publication and archive remain outside this task. Mechanical PASS confirms byte identity and passage existence, not editorial correctness or human acceptance.
