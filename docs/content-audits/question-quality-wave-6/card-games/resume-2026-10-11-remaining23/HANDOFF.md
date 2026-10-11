# Remaining23 — author handoff

Author `01a12b44-4beb-7aa3-8c23-2916b767b7f1`, 2026-10-11. Branch `codex/question-quality-wave-6`; worktree `/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle`. Baseline `d60ebd4fe38071e92b0ab03b6983b2f8a4a4a296`.

**Author PASS: 23/23, HOLD: 0. Independent review and root certification are pending.** This is not 23 newly certified/completed cards and does not alter root progress. No ledger, stamp, planning, claim or previously certified card was edited.

`author23.json` is the final frozen six-field receipt: 138 explicit substantive decisions, exact source passages, original capture identity and literal/card hashes. `editorial.py` preserves the author's individual rationale; `proof_catalog.py` preserves individually selected passages. `adapt_receipt.py` only serializes these decisions and hashes; it cannot infer a substantive verdict. Pilot5 was roundtripped before expansion; its receipt and interim16 are retained unchanged.

Changes include precise Bicycle Canasta variant scope; corrections to Yu-Gi-Oh!'s ambiguous life-point question; meaningful notes for all four alternatives; and replacement of obvious synonym questions with independent facts at the assigned level. Durable IDs are preserved even where the topic fact changed: tarot-swords now asks about Magic tap, tarot-coins about Pokémon evolution, durak-attack about belote/rebelote, history-poker about Vanderbilt's 1925 vulnerability innovation. These are intentional replacements within card-games scope, not ID renames. History Mamluk removes an unsupported century; early Visconti is distinguished from Visconti-Sforza.

## Checks and limits

- `python3 docs/content-audits/question-quality-wave-6/verify-proof-format.py docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-remaining23/author23.json --repo . --output docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-remaining23/author23-roundtrip.json`: PASS, no errors. It checks exact passage existence and identity, not factual/editorial correctness. pypdf emitted an optional fontTools warning on unrelated font encoding; every selected passage matched exactly.
- `preservation-check.json`: exactly the assigned23 changed; all77 other canonical hashes unchanged; IDs/order/difficulty/correctIndex preserved; quotas40/40/20 and per-position10/10/5 preserved; all note/explanation limits passed. Narrow prompt-only searches for new fact duplicates found no conflicts; no substantive reread of certified77.
- `git diff --check -- src/content/topics/card-games.json`: PASS.
- No full test suite, browser gameplay QA, build, deployment, push or acceptance was performed. These data/source changes need independent content review next; runtime validation is not claimed.

## Source capture limitations

Full original byte captures: Pokémon official41-page PDF, Grimaud23-page PDF including classic belote, Magic complete September25,2026 TXT, Swiss National Museum HTML, LACMA HTML, EBU HTML. The shared ISKO20-page original PDF is referenced by hash and page from `../resume-2026-10-11-standard-skat20/sources/isko-correct-url.pdf`; its provenance is in that sibling directory and no duplicate was made.

Bicycle, Met and Yale have complete original web-tool extractions, with all original lines present. Konami has the complete official FAQ page (337 lines, provenance records the raw tool responses) and full official rulebook landing page. Lorcana has the complete12-page official Quick Start PDF extraction (389 lines), with exact raw-response hash and the label-removal transformation recorded. They are explicitly typed as full extracted original content, **not** original HTML/PDF bytes. Original byte downloads failed with timeout,403/challenge or truncation. The failed captures and download logs are preserved and excluded from proof. No search snippet or quotation collection substitutes for a whole original. If the independent reviewer requires original bytes beyond the accepted proof-format extraction mode, these source families need a transport refresh before certification.

Fournier's full Canasta rules were also read and retained because their concealed-exit bonus differs from Bicycle; they must not be silently substituted for the named Bicycle variant.

## Cleanup and next step

Owned Python cache and `/tmp/mindbattle-author-canasta.html` removed. No owned download, test or build process remains. Evidence source captures (~12.8MB), failed-download history and pilot/final receipts stay in Git for independent review. Foreign changes/processes were preserved. `cleanup.json` records paths and hashes.

One temporary hidden IAB source tab could not be explicitly closed: the Browser Use URL policy rejected the generated `data:` timeout-page URL even for close. It is unmarked and documented to close automatically at turn end; no evidence or continuation relies on it. No policy bypass was attempted. Explicit closure is unverified at handoff.

**Next step:** the coordinator supplies `author23.json` and the frozen commit to an independent reader, who reads all six fields against originals and issues independent full-card decisions. Only root may update certification/stamps after that. This author will not send parent messages, push, or continue another slice automatically.
