# Independent read — two geology fix2 cards

Reader: `CODEX_THREAD_ID:01a12b98-18ee-7b73-bf14-b432d49a7df1`.
Distinct author: `01a12b7e-fdfc-7283-98d7-d7879121bad6`.
Branch: `codex/question-quality-wave-6`.
Assigned author snapshot: commit `08acaf4`; both current hashes matched its receipt.

| Card | Current canonical SHA-256 | Independent decision |
| --- | --- | --- |
| geology-earth-earthquake-epicenter | c45e63c97390da4e8411084a46976cd29082c3c50cf1498e2790a4cc49c5f903 | PASS, all six fields |
| geology-earth-gypsum-plaster | 67095aa63435c51575440729d4dedfe888431acb3106e8a5bbec1c5bec899698 | FIX_REQUIRED: semantic duplicate; all factual claims read |

The current `gypsum-plaster` stem asks for Earth's outermost main layer. Existing
`geology-earth-earth-crust` already asks for its outermost solid layer, with the
same four answers in the same order and the same correct index. This is the same
tested fact, not independent variety. The six fields were read in full: five
notes/explanation fields PASS; prompt-key is factually true but FIX_REQUIRED for
duplication. The duplicate snapshot is retained in `current-snapshot.json`.
Only this exact finding justified reading the saved neighbouring card; no saved
card was changed or recertified.

The current epicenter options are comparable location statements. The general
definition is uniquely the surface point directly above the focus. A possible
coincidence with maximum intensity or surface displacement is not an alternative
definition, so the earlier blanket non-overlap argument is not carried forward.
All six fields were independently read against raw originals. The local-ground
claim additionally uses Earle PDF page 292, read along with page 293 in context.

`independent-receipt.json` contains the 12 current field hashes, explicit
judgments, analyses and passages. `proof-index.json` indexes bindings by reader,
role, current card and literal hash. Four complete HTML originals were fetched
independently using curl (HTTP 200, verified TLS); their visible text matches the
fully read saved originals. The failed web/urllib retrieval attempts remain in
`fetch-log.json`. The complete tracked PDF remains at its existing path and is
bound by hash/page locator; no assembled summary was treated as an original.

Checks completed:

- Unmodified `verify-proof-format.py` roundtrip: 2 cards / 12 fields, zero errors,
  all selected passages present in the bound raw captures. This creates no PASS.
- Source topic bytes unchanged from baseline `3d24a899`; ID/order/difficulty/index
  preserved; quotas remain 40/40/20 and positions 10/10/5 per index.
- `git diff --cached --check`: original downloaded HTML contains upstream
  whitespace (recorded in `whitespace-check.json`); original bytes are preserved.
  The separate authored-evidence-only check passes. No runtime, tests or
  validator changed.
- Cleanup: no owned ignored files, background jobs, temporary builds, renders or
  caches; no foreign resources removed. Shared worktree remains in active use.

No full suite, browser QA, build, deployment, release or archive was run.
No ledger, claim, lease, root certification or wave counter was changed.
New root-certified cards from this reader: **0**; certification belongs to the
coordinator and requires both roles. The wave is not declared complete.

Next step: coordinator assesses the current epicenter receipts; author replaces
the duplicate crust fact in the `gypsum-plaster` slot with an independent easy
fact, preserving invariants, then a distinct reader checks its full six fields.
Continue from this directory and the commit containing this handoff.

Сессию можно архивировать без потери данных после сохранения этого среза в Git.
Открытая редактура дубля и зачёт координатором остаются отдельными действиями.
