# Independent read: five current fixes, 2026-10-11

Reader: `01a12be3-22a2-7af0-ad6f-5e6c30aafd33`; distinct author: `01a12bd2-207a-7da1-9035-d9c7d5eeaa37`.
Branch: `codex/question-quality-wave-6`; reviewed baseline: `c1ded1d` (author changes `67ad48a`, `37af99c`). Ownership is this directory only. Topic, author, planning and certification files were not changed.

All five current cards and all 30 fields were actually read, including full questions with all four options and original-source passages. Decisions: **3 PASS / 2 FIX_REQUIRED**, field decisions **26 PASS / 4 FIX_REQUIRED**. These are independent judgments, not new coordinator certifications.

| Card | Independent result | Reason / action for author |
| --- | --- | --- |
| middle-ages-priory | FIX_REQUIRED | The Tyne → Tynemouth name cue replaces history knowledge; without it the landmark is still too narrow for ordinary medium in the broad Middle Ages topic. Rework the tested fact. In note2, replace ambiguous administrative independence of Finchale with the supported establishment/status as a priory; Durham remained its parent monastery. |
| middle-ages-cloister | PASS | Architectural identification, notes and two-sentence explanation supported. The correct note adds the concrete Lilleshall example and four walks; repetition of that additional fact in explanation is permitted. |
| middle-ages-lord | PASS | Familiar nickname, useful Third Crusade note, corrected 1194 return and separate 1152 royal / 1155 imperial periods supported. Contradictory clauses in older Westminster/Met source prose were explicitly rejected, not silently adopted. |
| geology-earth-gypsum-plaster | FIX_REQUIRED | The dissolution property is scientifically true but not an adequately justified Easy fact. Only the key is a mineral; the three rock distractors allow category elimination. Correct note entirely repeats prompt/key. Rewrite with an honest Easy cue, comparable options and an additional correct-note fact. |
| geology-earth-granite-coarse | PASS | Full fresh Syracuse HTML supports the current building-material/continental-crust prompt and countertops/library-steps explanation. All six fields independently read; historical missing SHA `20d62285…` stays unresolved and old bindings stay HOLD. |

## Exact author-proof defects to retain

The current author receipt has current gypsum literal hashes but still describes **basalt** for note1 and explanation and binds NPS basalt passages. A successful mechanical format check cannot certify these two fields. They need actual author reading and freshly correct substantive bindings after the content fix; this independent receipt does not replace the author role.

The author granite explanation passage omitted the countertops/library-steps sentence; this independent receipt binds both sentences from the raw abstract. The author Richard note3 passage supported dates but omitted the nickname translation; this receipt separately binds the Met nickname clause while explicitly rejecting the adjacent emperor-at-1152 claim. Edward's completed Westminster rebuilding is bound beyond the author's isolated conditional clause.

New NPS gypsum raw HTML was independently fetched over HTTPS with curl (200, 36,604 bytes), read, and preserved unchanged. The preceding Python certificate failure remains recorded. No failed response or extracted snippet is used as an original. Other proofs point to already committed full HTML or documented full original rendered responses after reading their actual passages and context. The prior hand-written gypsum extraction is not the raw source of this independent verdict.

## Duplicate screening

Targeted catalog prompt/key screening found `materials-granite-counter`: both involve granite as a usable stone. It asks about a durable countertop; the current geology prompt additionally distinguishes igneous rock characteristic of continental crust, with basalt as a meaningful competing rock. I judge these related, not the same tested fact, and record the near match rather than claim no overlap. Granite's texture and igneous-class neighbors test different properties. Gypsum hardness-2 and the outer-crust question test different facts from dissolution. Cloister identification differs from `middle-ages-abbey`'s refectory position opposite the church. No existing certified verdict was reissued or changed during this narrow duplicate check.

## Minimal checks and reproducibility

Scope is review evidence only; no runtime code, content or validator changes. The sufficient checks are five-card proof roundtrip and working/Git byte preservation with fixed IDs/order/difficulty/key/quota checks. No full suite, npm QA, browser, build, deployment or release command ran.

1. `python3 docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-11-five-fixes/bind-independent.py` — serializes explicit decisions and current hashes only.
2. `python3 docs/content-audits/question-quality-wave-6/verify-proof-format.py docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-11-five-fixes/independent-receipt.json --repo . --output docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-11-five-fixes/pilot-roundtrip.json` — first pilot is the entire bounded five-card scope; no expansion.
3. After preserving evidence in Git, `python3 docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-11-five-fixes/verify-committed.py` — compares every used raw to its committed blob, and current topic/card bytes to the reviewed baseline. Both SHA-256 of Git blob bytes and Git object ID are recorded.
4. `git diff --cached --check` and exact owned staged-path inspection before commits.

The original-inclusive whitespace check reports original HTTP CRLF/trailing spaces and original HTML whitespace (exit 2). These source bytes are intentionally preserved; the same check restricted to authored files passes (exit 0). `whitespace-check.json` retains the exact diagnostics. No validators, tests or raw originals were altered to hide this result.

## Handoff / cleanup

Coordinator may use the three independent PASS results only with corresponding valid author-role evidence. Author must resolve the two FIX_REQUIRED cards and rebind the affected current fields; then an independent reader reviews the revisions. Certification, planning updates and wave completion remain coordinator work. No messages were sent to another chat.

Task-cleanup instructions were read. No persistent task processes or temporary build/cache folders were created. Source/HTTP/error evidence stays in Git; own raw-source folder has `-text` to avoid line-ending conversion. All unrelated shared-worktree files and processes remain untouched. This reader session can be archived once its evidence commits and committed-preservation report are saved; further work continues from this directory and branch, not this chat's transient context.
