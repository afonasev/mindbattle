# Independent current-five review

Reader `01a12b98-1551-7a63-9e63-d1555b6ae364`, separate from author `01a12b73-5581-7200-86b7-d9f3274c148a`.
Baseline: author commit `0f97808`. Scope: exactly the five cards in its `middle-ages/resume-2026-10-11-fix5/author-current.json`, all 30 current fields.

**Independent decisions: 2 PASS, 3 FIX_REQUIRED; fields: 26 PASS, 4 FIX_REQUIRED.** This is no coordinator certification and no new coverage count. The saved 165 were not reopened or changed.

| Card | Decision | Remaining issue |
|---|---|---|
| middle-ages-abbey | PASS | Source now correctly points to Cleeve. All six fields reread, including unchanged notes. Earlier difficulty advisory retained in receipt. |
| middle-ages-priory | FIX_REQUIRED | prompt-key: factual key is correct, but recalling Tynemouth's particular dependency on St Albans is a narrow historical detail beyond the medium audience rubric. Four regional priory names give no useful context. Rewrite under the immutable medium/index constraints; do not silently change difficulty. This is an editorial difficulty judgment, not a claim that the historical answer is false. |
| middle-ages-cloister | FIX_REQUIRED | explanation: one sentence with a semicolon; explicit rubric requires 2–4 sentences. All other fields pass. |
| middle-ages-chapter-house | PASS | Room-level alternatives repair the earlier mismatch. Correct note adds “usually after Mass”; its overlap with explanation is permitted. |
| middle-ages-lord | FIX_REQUIRED | note3 confuses the 1152 royal accession with imperial status; explanation imports an erroneous return-from-crusade chronology. Key and remaining notes pass. |

## Historical discrepancies requiring author correction

- **lord/explanation:** Westminster's current paragraph really contains the erroneous connection. [Royal Household](https://www.royal.uk/richard-i) instead places departure in 1190, the return journey in 1192, and return to England in 1194 after captivity. The father's death in 1189 cannot be the news prompting that return from the Third Crusade. This is why a literal quote match alone does not warrant PASS. The current English Heritage/Westminster captures and the contradictory complete Royal Household response are retained and hash-bound.
- **lord/note3:** Met's chronology says “elected emperor” under 1152. The [Lower Saxony State Archives](https://nla.niedersachsen.de/startseite/landesgeschichte/aus_den_magazinen_des_landesarchivs/2022/aus-den-magazinen-des-landesarchivs-juni-2022-206223.html), describing its own original charter and golden seal, distinguishes royal period 1152–1155 from imperial period 1155–1190; its 1154 seal bears the title King of the Romans. Correct the title/date or retain only the verified meaning of Barbarossa.

## Reading and proof procedure

`manual-decisions.json` contains the independently authored per-field decisions and explicitly chosen source-line IDs. `bind-receipt.py` only binds those decisions to current card/scalar hashes and retrieves the selected unaltered passages. It never generates a substantive verdict. `proof-index.json` is the passage index; `independent-current.json` binds each proof to reader, role, card and literal. `freeze.json` saves the exact five reviewed cards.

The ten existing original institutional responses were read directly from their source files, not from author conclusions. Their complete line coverage and byte identity were checked in `source-read-inventory.json`. Relevant full paragraphs and adjacent context were inspected. The fresh Royal Household/NLA response is saved unchanged in `sources/additional-original-web-response.txt`; it contains both complete source extractions, not stitched selected claims. Live Westminster/Met/Cleeve/Lilleshall opens were also used to inspect source wording. Raw downloads that timed out or returned challenges were explicitly excluded; their error receipts and hashes remain in `capture-manifest.json` and `capture-attempt-urllib-errors.json`.

All five / thirty fields were roundtripped as the complete pilot before any expansion; no expansion was undertaken. `roundtrip.json` reports no mechanical errors and zero script-created verdicts/certifications. This proves source-passage existence and hash identity, not historical correctness.

Prompt/key candidate retrieval found no second matching fact for these five. The unrelated Richard Nixon/III/James/Steiff hits were rejected after comparing their prompts and keys, not treated as duplicates from a shared name. Shared monastery notes across these five are not primary-fact duplicates: planning, jurisdiction, cloister and chapter-house function test different relations.

## Continuation and boundaries

Next action belongs to the coordinator: reconcile the two passing cards against the author role and route the three FIX cards for bounded author revision, then obtain a full current-six-field independent read of the revised cards. This session does not edit the catalog, planning, claim, lease, ledger, certification, tests or validators. It does not merge, push, deploy, build or archive the wave. No full suite or browser checks were run; source-only receipts require the focused hash/format/preservation checks recorded here.

All owned durable evidence is committed on `codex/question-quality-wave-6`. The original existing worktree remains shared and active for other owners. No new chats, agents, worktrees or branches were created. No task-owned running process or temporary dependency remains.
