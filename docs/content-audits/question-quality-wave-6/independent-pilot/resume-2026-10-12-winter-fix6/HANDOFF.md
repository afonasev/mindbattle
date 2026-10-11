# Winter6 — distinct independent read, 2026-10-12

Native reader chat: `01a12c65-7c69-74d1-a107-6d7c4e58c621` (`CODEX_THREAD_ID` read in this session). Role: **independent-reader**, not author. Dispatch identifies the actual author chat as `01a12c2b-8908-7971-8d70-7dbac0316099`; frozen author metadata retains historical identity `01a12c0c-9bf3-77d1-9328-374ef53d32e4`. Both differ from this reader. No identity was inferred from a source filename or another reader's verdict.

Exact author freeze: `3b4a8f2` + `753ab51` + `b5e7375` + `bb1075e`. Current working Winter topic bytes equal the committed freeze bytes, SHA256 `0621a3f5c91256d9bbf7ac458b6adaa22c124c6eeb54253b3be2cb83699b6c56`. All six canonical hashes and all 36 field literals match that freeze. Previous HOLD receipts are historical and were not substituted for this read.

## Result

Six assigned cards freshly reread on current hashes, 36 fields, 73 source passage mappings from 11 full original HTML/PDF captures. Card results: **0 PASS / 6 FIX / 0 HOLD**. Field results: **23 PASS / 13 FIX / 0 HOLD**. These are six repeated current-card reads, zero newly unread-card reads, zero new certifications. Assigned unread remaining: zero; cards still requiring repair and subsequent independent reading: six.

| Card | Concrete current defect requiring repair |
| --- | --- |
| 007 | Broad “equipment that helps balance” does not uniquely exclude skis/boots/bindings. Correct note only repeats balance; note1 says “движения лыжнику” instead of movement from the skier. |
| 008 | Snowshoes and boot-only alternatives do not offer plausible skating equipment in the rink context. Correct note again describes putting skates on for ice, without a substantive new property. |
| 017 | “One board” self-excludes the two ski-named alternatives, with bobsleigh also a different motion/track. Correct note repeats the fixed feet. Detail about both feet/bindings is explicit in WTGF rather than the cited COC overview passage; the selected source URL must support the complete main fact. |
| 019 | Slope, bobsleigh track and jump are visibly inappropriate geometry for a team puck match. Correct note's Olympic ice-arena sentence repeats the same venue–sport relation rather than an additional useful fact. |
| 023 | “Surface ... provides sliding” effectively gives the key “Sliding surface”; medium is not justified by this wording. Correct note repeats precisely the lower longitudinal gliding surface. The edge distractor itself is a real neighboring contact surface, not rejected merely for being wrong. |
| 024 | “In chairs” directly cues “Chairlift”; merely being four real lift types does not remove that cue. Skimobile note grammatically attributes the cable drive to the guide instead of the cars. Correct note PASS: partial enclosure is a real additional property. |

`manual-decisions.json` contains the independently written judgment on each of six fields per card and the actual governing rule. `independent-receipt.json` binds each judgment to literal SHA256, current card SHA256, native identity/role, source class, raw path/SHA256, committed Git blob/SHA256, explicit locator, and quote from the original. Factually correct source statements are distinguished from editorial defects. A false answer alone is not treated as an impossible distractor. No verdict was generated from author PASS or from a script.

## Original source and locator findings

Originals were reopened from the working tree and compared byte-for-byte with `git show bb1075e:<path>`; all 11 equal committed blobs. PDF/HTML content was read from these originals, not search summaries, failed captures, or old extracted text files. The six actual original/literal/identity/Git rounds preceded writing manual decisions. Existing capture dates and question `verifiedAt: 2026-10-11` remain historical; **2026-10-12 is this independent stored-original reading date, not a new HTTP capture date**.

Two provenance corrections are recorded only in this reader's folder:

- Author PDF `pdfPage` values use one-based physical page numbers despite their capture-method label claiming a zero-based index. For example FIS pole §3.3 is physical page27/index26, Hockey Canada SKATES is physical page8/index7. The receipt explicitly records both bases. The original passages exist; this is not a missing-source HOLD.
- The WTGF HTML title and metadata name **World Transplant Games Federation**, not “World Snowboard Guide”. This is an institution's explanatory sports guide, not a snowboarding governing federation. The retained page explicitly supports both-feet/bindings content. Its class/title are corrected in this independent proof without editing the author's metadata.

`candidate-pairs.json` records seven actual semantic main-fact comparisons: three cross-topic lexical candidates and four named Winter neighbors. All seven pairs are distinct facts; this does not certify any neighbor. No whole reread of the remaining 94 Winter cards or old root-certified19 occurred. The assigned six are inside Winter's ski/ice discipline scope; there is no demonstrated cross-topic duplicate or required topic transfer in the named pairs.

## Mechanical checks and preservation

Only mechanical own-proof checks were run: `python3 docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter-fix6/check-proof.py`, JSON/card/literal validation, original-source Git byte readback, staged-scope/diff checks and committed-own-folder readback. The first mechanical attempt found HTML whitespace normalization differences; own quotes retain the original parsed whitespace, while comparison with historical author quotes normalizes whitespace explicitly. No semantic judgment was changed to make this comparison pass.

No catalog, source original, author receipt, stamp, root ledger, or planning file was edited. No full suite, npm check/QA, browser test, build, Player, release, push, merge, deployment, OpenSpec archive, or human acceptance occurred. The dispatch root baseline was 331/500; this reader performs no source-certifier action and adds zero to root coverage.

The worktree is shared with active foreign author/readers. Foreign tracked and untracked work is preserved; no reset/checkout/clean or foreign stage operation was used. This task started no persistent processes and created no temporary copies, caches, or duplicate raws. Needed original captures remain in their existing committed paths; own receipt/decisions/checker/pairs/readback remain in Git. See `cleanup.json` and `committed-readback.json`.

Next step: the coordinator/authorized author reviews these six concrete FIX findings, repairs the affected texts and freezes new hashes; a distinct independent reader then rereads all six whole cards. No repair or coordinator certification is performed by Winter6. Human acceptance and any delivery remain separate commands.

This reader session has no further planned actions once committed readback completes. Сессию можно архивировать без потери данных; continuation uses this folder on `codex/question-quality-wave-6` and its preserved commit, without relying on transient chat context.
