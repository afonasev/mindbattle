# Independent current Middle rework pilot 5 — 2026-10-12

Reader `01a12cb1-4487-7d91-9bd9-8b07a103edb8` (actual CODEX_THREAD_ID, independent) differs from author `01a12ca5-97a5-7860-9e4a-789a3f6bdcab`. Author receipt is frozen at `d375f6c82537b38db587a4d3d086754e30eb9e0d`, SHA `ab261e5053124fc3ab5b9854087408a0ecad2021d24a08465a397939856b38c1`; metadata roundtrip `e88b2e7`. Historical same-ID reviews remain untouched and do not certify current versions.

All five / all 30 fields substantively read. UNREAD in pilot = 0. Card verdicts: **1 PASS / 4 FIX / 0 HOLD**. Fields: **23 PASS / 7 FIX / 0 HOLD**. Full decisions, exact literals, 64-character current card hashes and source passages are in `reader-receipt.json`. Its manual judgments are independent of author PASS and mechanical byte checks.

| Card | Verdict | Current card canonical SHA256 |
|---|---|---|
| middle-ages-precaria | FIX | 55803f625032beb8c0d877b796bb3eacd801b502456d860bf1b3cad337eb7672 |
| middle-ages-dower | FIX | 5609f47d94e9b5aa25bb1da2c2c08e9a22602cf0c5af3329eb49ff1f6cfaa48e |
| middle-ages-palimpsest | PASS | 724e9c04a4709635a78e6aac37a06c934c3f8648317d90595ca0eb50865534f1 |
| middle-ages-dowry | FIX | 227af2d28bbb49ed00a0ec6fc6732109987cd8ae8d2787a7680954b90d8af472 |
| middle-ages-serf | FIX | 070e7027116eca88798b16d541a2471b9ef490b7a0a522592db0ffbb18decf5a |

## Concrete calibration for author

1. precaria / prompt-key: the question requests a petition; allod/property, benefice/grant, emphyteusis/real right are excluded by entity type. Same broad land-law vocabulary does not suffice. Keep hard/index; repair actual plausibility.
2. dower / prompt-key: primogeniture and apanage are not spousal marriage-property arrangements; removing literal widow cue alone did not repair categories. Latin Douaire is also the only Latin-script choice. Keep medium/index and four consistent labels.
3. dower / note1: “давала старшинство рождения” reverses the source's causal direction. Birth priority carries rights; the institution does not cause birth priority.
4. dowry / prompt-key: brideprice option is the translated system being replaced, excluded by the condition. Widow usufruct is not a contribution upon marriage. The publisher abstract distinguishes two forms of dowry and does not explicitly prove that the bride-family form alone is the replacement. Source the exact discriminating claim and use plausible same-category choices. Keep medium/index.
5. dowry / note2: merely labels a marital gift as a marital contribution. Add its own precise sourced fact. The abstract supplies propter nupcias / in exchange for the bride; it does not by itself identify the recipient as the bride.
6. serf / prompt-key: unqualified manorial tenant overlaps serf; Lancaster explicitly includes free and villein tenants. Specify a distinct personal status while preserving easy/index.
7. serf / note3: opposite-of-serf wording is true but largely repeats the serf definition. Give an actual freehold property. Lancaster supports fee simple “for ever” with homage/service; it does not support exemption from all manorial duties.

palimpsest passes: four consistent manuscript-related labels, key and all four notes from precise originals. Leiden exemplar passage belongs to **Insertion**, so the reader locator corrects the author's “Exemplar” locator. The retained hard is supported by the specific physical manuscript feature and contextual elimination of copy, autograph and exemplar.

No must-add-new-fact rule was applied to notes overlapping explanation. Rental note and brideprice note were accepted as concrete facts. Removed Magna Carta/chevage claims were not certified. UGR source is the full publisher **abstract**, never the broader article. Persee review p119 was not used as the full article.

## Verification and scope boundary

Minimal affected checks: exact five full-card/literal hashes, immutable difficulty/index, role identity distinction, all 30 field records, all 19 working/Git author original files and located proof passages. `source-index.json` binds complete originals to raw SHA and Git blobs; `verification.json` records passage presence. Scripts serialize manual decisions and verify evidence only. No full test suite, build, deployment, merge, push, root certificate or acceptance.

All four literal choices were read; prompt grammar and category, factual claims, note usefulness, topic relationship, difficulty and duplicate risks were considered separately. dower/dowry test different facts. Narrow mechanical catalog candidate search found no other matching ID; this does not certify full semantic duplicate absence. Other 95 cards protected; remaining 23 not substantively read or certified. No source/card/stamp/root ledger/planning changes made.

Next step: coordinator adjudicates these exact current findings, then authorized author calibrates/reworks; scale to 23 follows pilot feedback and root adjudication. This reader does not send cross-chat messages or advance that work.

Cleanup: only this folder is owned by reader. No background processes, downloads, temporary builds or cache created. Other readers' files/processes/worktree remain untouched. Persistent receipts, exact evidence index and reproducible serializer/verifier are retained in Git; no disposable resource debt.
