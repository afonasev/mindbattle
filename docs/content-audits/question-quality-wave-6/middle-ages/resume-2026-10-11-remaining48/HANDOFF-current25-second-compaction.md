# Middle Ages: author handoff after second compaction

Author chat: `01a12bfd-e8b7-7bd2-ad8a-a9b43404f104`.
Branch: `codex/question-quality-wave-6`.
Owned scope: `src/content/topics/middle-ages.json` assigned IDs in `root-scope48.json`, and this evidence directory only.

## Status and continuation

**25 of the assigned 48 cards are author candidates (150 manually read fields); 23 are not author-prepared. The assigned task is incomplete. Independent certification by this author is zero.** Stop after this slice under the second-compaction rule. No additional cards or research were started after that boundary.

Current artifacts: `author-current25.json`, `current25-candidate.json`, `current25-preservation.json`, `current25-mechanical.json`, `current25-focused.json`. Exact remaining IDs: `remaining23.json` (`notAuthorPreparedIds`). Earlier current20/current21/remaining28/remaining27 reports are historical snapshots, not the current count.

The first 20 candidates were committed in `401e5926b811bd4c3b8a2f9f0e72b873f7c803af` (pilot5 in `0cebbe546b7f37e2e9edd1526155a522b4ce7aef`). This final slice adds `middle-ages-great-famine`, `middle-ages-peasant`, `middle-ages-serf`, `middle-ages-tenant-farmer`, and `middle-ages-freeman`. The last ID now asks about barshchina; the assigned ID, easy level and correctIndex 3 are preserved. Sources and explicit field judgments are in `author-famine1.json` and `author-peasants4.json`.

Final topic byte SHA-256: `bfd0d04e3131eb2b3a051d2d42e22209337c9d7f8ae4bd3a58a44d031ca94f38`.
Git source-byte verification and the content commit are recorded in `current25-git-roundtrip.json` after the content commit. The final metadata commit stores that readback; find it with `git log -1 -- this-directory/current25-git-roundtrip.json` using this directory's full repository-relative path.

## Checks and limits

- Affected tests selected before execution in `current25-qa-scope.md`: `vitest run tests/unit/catalog-topics.test.ts tests/unit/content-answer-notes.test.ts tests/unit/content.test.ts --reporter=json --outputFile=<this-directory>/current25-focused.json`. 19 passed, zero failed/pending/todo. No rerun is required for metadata-only commits.
- Proof-format verifier: 25 author records, zero mechanical errors. It checks identity and quoted passage existence; it creates no substantive verdicts or completed cards.
- Preservation: immutable52 unchanged, untouched23 unchanged, frozen20 unchanged; all 100 IDs/order/difficulties/correctIndex preserved; total 40/40/20 and each original package25 10/10/5 preserved; all25 card hashes and note/explanation limits match.
- No full suite, build, Player, deploy, merge, archive, planning/claim or root certification edits. Automated checks are not human, device, visual or independent acceptance.

## Next action

Coordinator can give an independent reviewer `author-current25.json`, the exact current25 candidate, original captures and Git readback for substantive review of all 150 fields. Authoring of the remaining23 must resume in a later authorized session from `remaining23.json`, preserving the frozen25 unless review identifies a specific correction. This session sends no message to the coordinator; the coordinator monitors completion.

Research-only leads are not author PASS: `fordham-statute1351.html` has a wage-cap fact already duplicated by `history-united-kingdom-hard-04-02`; do not reuse that main fact for Black Death. `lancaster-sweating.html` discusses a speculative cause, not established causation. The saved Catholic Encyclopedia interdict page has a problematic England lifting date; do not rely on it. Dancing mania's 1518 example needs a medieval-scope decision. Dowry's plain definition was too easy for its fixed medium level; no replacement is authored.

CNRTL originals are public API JSON with embedded TLFi HTML, intentionally stored as `.html`; capture format is recorded in proofs. For chevalier and dime use the `-nom` captures (noun senses), not the default adjective responses. `sources/** -text` preserves exact original bytes in Git. Do not run whitespace normalization over originals. Exclude `sources/` from authored-file diff whitespace checks.

## Preservation and cleanup

All necessary source originals, capture metadata, explicit author judgments, candidates, tests and this handoff are retained in Git. `current25-cleanup.json` records removal of the incomplete London Museum response (curl exit28; never used as proof) and reproducible Python cache. No active own test/capture process remained. Prior cleanup is in current20 evidence. Shared worktree/node_modules and foreign winter-sports changes remain for their owners. Do not archive or remove this shared worktree.

This chat can be archived after the final Git readback and owned-path clean-status check. The remaining task and independent review do not depend on unsaved files or this chat's context.
