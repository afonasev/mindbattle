# Independent reader — Gypsum1

**FIX_REQUIRED** for `geology-earth-gypsum-plaster` at current canonical card SHA256 `bc41d292aef03dc0cb86c7756d0f8030952f392ccc37b56e3af814e3235d3d44`.

The six manual field decisions and original source bindings are in `independent-receipt.json`:

| Field | Independent verdict |
|---|---|
| `prompt-key` | FIX_REQUIRED — card's sole source URL does not support the medical-use part of the key |
| `note0` | PASS |
| `note1` | PASS |
| `note2` | PASS |
| `note3` | PASS |
| `explanation` | PASS |

The public card source URL opens the NPS gypsum page, which explains gypsum-to-plaster-of-Paris processing but does not state its medical use after fracture. The captured NHS Trust source does state use of a Plaster of Paris backslab after fracture, but the card does not link to it. This is a targeted source-link correction, not a HOLD on missing evidence.

The review independently read the complete question card, the entire visible text of all three complete original NPS/NHS HTML captures, and relevant current catalog candidates. It separately checked raw SHA256 on disk and SHA256 of `git show HEAD:<path>` for every original. The independent reader is `01a12c25-6aa3-70c0-b7b7-8f4b588dacf4`; the author is `01a12c14-c625-70d2-b5e0-aaa87aefedf9`.

No question, source capture, author receipt, or non-owned file was edited. Scope is only this new evidence folder. No full suite, build, runtime, deploy, OpenSpec, archive, or human acceptance was run or claimed. Only the affected proof-format/hash validation and Git identity checks were run.

Cleanup: this reader created no temporary captures, logs, processes, tests, or builds. The three original response bodies remain at the author's tracked paths. Another reader's tracked Middle Ages edit and untracked evidence files were present during final Git review; all were left untouched and unstaged. The current review receipt and its validation/preservation metadata are retained in this folder.

Next step: the author updates the card's source binding so the medical-use claim is reachable from the card, then obtains a fresh independent review against that exact new card hash.
