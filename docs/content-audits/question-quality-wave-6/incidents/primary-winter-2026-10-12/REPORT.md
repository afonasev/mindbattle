# Primary winter incident — bounded investigation

Owner scope: this incident directory only. Primary was read-only throughout this investigation. No restore, question edit, branch/worktree creation, build, tests, deploy, or archive performed.

## Preserved state

`primary-current.json` is the exact 153102-byte primary capture at 2026-10-11T22:05:44.859106Z (2026-10-12 03:05:44 Yekaterinburg). SHA256 `9aff89f8b4d11480b7ac201df912f30485d13ebcb1ce6ae1649f795b67435c7b`. Primary HEAD was `a898df6be891d6c75e0d83e083ba62d375e60fd3`. `primary-git-diff.patch` is the observed diff against that HEAD, NOT a recovery patch or attribution proof. Coordinator’s separately owned observed backup has the same SHA/size. A later read retained the capture SHA.

## Actual write scope

Native author `01a12cc1-9d5d-74a1-99ba-6377bdfaed21`, full refreshed command inventory in `native-primary-commandtrace-final.json`; exact exec call/output source records with timestamps and original line citations in `author-exec-history.json`.

1. Previous turn `01a12cec-239b-7d01-a356-4a06ee606a09`: command `exec-5820e881-e599-465d-a62d-4bd77198a40d`, source rollout line 950, 21:45:34Z: assigns 017.answers[0].note and rewrites the entire primary JSON. No explicit workdir. Exit 0. Earlier first author turn has no native primary command.
2. Target turn `01a12cf5-9aca-7fe2-848f-7f8b2fe88181`: `exec-e03f5f76-e9f9-4a43-a5c3-b021fc218f4d`, line 1221, 21:56:49Z: rewrites 007 prompt/all answer text+notes/explanation; 008 all answer text+notes/explanation; 017 notes at slots 0 and 2; 019 prompt/all answer text+notes/explanation/source. Rewrites entire primary JSON, no explicit workdir, exit 0.
3. `exec-e055e167-4f04-4d23-b518-a32b5b24a212`, line 1356, 22:02:50Z: first Python fails receipt FileNotFoundError, second still runs and rewrites primary, assigning 008.answers[2].text and note. Shell exit 0 does not mean first script succeeded.
4. `exec-6a5a2c75-099e-4edf-add6-abeb467382ad`, line 1423, 22:04:54Z: first Python assigns 019.answers[1].note and writes primary; subsequent /tmp script generation runs and fails missing followup2 receipt. Overall exit 1 does NOT mean no primary mutation.

Union of explicitly targeted question IDs is 007/008/017/019. Every operation serializes the whole document; byte-level formatting scope cannot be inferred as only these records. The trace also includes all primary-cwd read commands, failed followup2 README creation (line 993; no matching receipts), failed followup3 receipt access, and later absolute-path worktree operations. Primary cwd alone is insufficient to label an absolute-path worktree command a primary mutation. The failed followup3 generator may create a primary directory before the receipt failure; no successful primary receipt creation is shown. No primary Git commit/reset/restore appears in the inventory.

## Recoverable versus unknown

The four exact write programs, after-state, current Git diff, and intermediate 21:57 diff output are preserved. The latter reports 184 changed lines (92 additions/removals) against HEAD and already contains foreign preexisting content. It is not a pre-write diff.

No trustworthy complete raw preimage was found. Author had no pre-write byte backup in this history; nearby worktree topic files and HEAD are not primary preimages. Narrow VS Code and Cursor local-history resource searches found no winter-sports entry. Exact overwritten prompt search in 2026-10-11/12 session files found only post-incident discussion/author diff, not an earlier primary capture. Coordinator backup is an after-state. Author native read_thread and exact local rollout were both inspected; their roles are corroboration, not reconstructed original bytes.

008.answers[2].text was already assigned “Фристайл-могул” by operation 2; operation 3 repeats that assignment. Its note changes from “В могуле качество поворотов даёт 60% результата, а скорость — 20%.” to “В могуле, дисциплине фристайла, качество поворотов даёт 60% результата, а скорость — 20%.” Operation 4 changes the 019 slot-1 note assigned by operation 2. These are known successive authored assignments, not proof of full byte preimages or absence of concurrent foreign edits. Operation 2 also overwrites the 017 note assigned by operation 1. Original values overwritten by operation 1 and operation 2 remain unproven. Do not revert from HEAD or substitute worktree content.

No recovery patch is supplied: a full exact recovery would require guessing foreign WIP and raw serialization. Preserved trace supports attribution and a search for the missing original, not byte-proven restoration. No evidence of an intervening later primary change was observed after the capture; this is only an observation at read times.

## Validation / cleanup / next

Checks are limited to SHA/size, native/local trace correlation, JSON readability, owned staged diff whitespace and Git byte roundtrip. No full tests are relevant to evidence preservation. No processes or temporary files were created outside the owned directory; no foreign resources removed. Active shared worktree and affected data remain preserved. Incident evidence must not be deleted or affected worktree archived until recovery is resolved.

Next: root/coordinator reviews this evidence and seeks a trustworthy raw pre-write primary backup/history from the owner of the foreign WIP. Author may perform recovery only after exact preimage proof and a fresh current-byte comparison; this investigation does not authorize overwriting primary. Missing preimage is the concrete recovery blocker. Investigation session can be archived once this directory is committed; recovery remains open and all continuation evidence is in this directory.
