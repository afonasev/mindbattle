# Winter38 independent current reader — 2026-10-12

Actual native reader `01a12ca1-f316-7433-9639-e3821672f899`, distinct from author `01a12c87-f8e7-7232-823d-c0be717a70dc`.

Read all 38 current cards / 228 fields. Scoped UNREAD = 0. Card verdicts: 6 PASS / 29 FIX_REQUIRED / 3 HOLD. Field verdicts: 166 PASS / 33 FIX_REQUIRED / 29 HOLD. FIX cards may also contain source-HOLD fields; these are preserved individually in receipt/summary.

IDs below all use `winter-sports-` prefix:

- PASS: 042, 079, 080, 084, 089, 069
- FIX_REQUIRED: 019, 026, 029, 030, 031, 032, 035, 036, 038, 039, 043, 082, 090, 091, 095, 097, 098, 100, 007, 008, 017, 023, 024, 057, 058, 059, 060, 067, 068
- HOLD: 076, 092, 073

## Important findings

- 073: current physical PDF page25 defines retention brake and boots; preset-load release-binding definition is on physical24, section3.1.4.1. Frozen current prompt-key, explanation and note0 at25 remain HOLD. Current hash `8a90114b9977db1901cb970b0519b034764793715e10d0c42132eb98faebbea1` actually read; older history not replaced.
- 007: several frozen proofs still describe snowboard/luge instead of current ski claims.
- 008 and023: explanations still refer to older question/options; current notes include unsupported construction claims.
- 017: notes1–3 are cyclically bound to other snowboard discipline paragraphs; prompt also admits simultaneous two-rider parallel format.
- 060 note2: `В каждом спице` has gender agreement error; ISU fact itself supported.
- 067 note1 and068 main/accepted note: frozen proof is a heading, not definition. Complete original contains definition at adjacent node; frozen expected passage/hash not silently replaced.
- 076 note1 and092 note0: frozen pages do not contain their claimed rules.
- Many easy cards retain explicit body-part, object, phase or cardinality eliminations. Medium43/90/95/98/100 also contain literal premise/category exclusions; medium permits knowledge-based narrowing, not obviously impossible entities.
- 097/098 additionally require root duplicate adjudication for inverse versions of the same steering relationship. Protected62 and whole-catalog semantic review are not claimed anew.

## Evidence and recipes

`receipt.json` is canonical reviewer schema; each current field has literal, SHA, manual claimAnalysis, verdict, substantiveRead and raw proof. `summary.json` contains exact current IDs/hashes and non-PASS field findings. `identity-scope-source-binding.json` pins exact31+7 scope, native identities, all authored receipt SHA/commits and frozen source chain. Author prompt-key recipe is exact UTF-8 `prompt + '\n' + keytext`. Reviewer recipe is canonical UTF-8 JSON array `[prompt,correctIndex,keytext]` (ensure_ascii=False, sort_keys=True, compact separators). Notes/explanation use exact UTF-8 strings; whole cards use canonical JSON objects.

PDF passage recipe is exact pypdf extract_text per physical one-based page. HTML recipe is whitespace-collapsed visible nodes excluding script/style, inclusive zero-based range joined with spaces; Maine statute frozen passage uses newline joining. Its initial space-join mismatch was only an extraction recipe difference: declared newline recipe matches frozen passage/hash exactly. No expected SHA was edited to fit.

All23 current URLs returned200. Eighteen full responses matched frozen bytes; five raw HTML responses changed but their entire extracted visible-node sequences remained identical. Changed current complete bodies are retained in `current-originals/` with exact disk/Git SHA. `current-url-readback.json` and `current-visible-text-readback.json` distinguish response byte identity from substantive text identity. Source classes name actual COC,IIHF,FIS,Hockey Canada,Skate Canada,IBU,ISU,BCS,WTGF and Maine Legislature institutions.

Git sequence: first5/30fields `75cf79c` then exact Git readback, next25 `35277a6` then readback, final8/full38 `24f5e00`, current-response CRLF byte preservation `49a9e48`. `final38-roundtrip.json` at49a9e48 confirms 38 current hashes,228 literals,254 exact extracted passages/proof hashes, author bindings and disk/Git bytes. Root ledger/source/topic/planning were not changed. Protected62 canonical hashes and order/difficulty/correctIndex remain unchanged against coordinator baseline.

Only owned evidence/mechanical checks ran; no npm qa/check/full suite/build/deploy/merge/push/OpenSpec archive/human acceptance/root certification. Writer intermediates and owned __pycache__ removed; current originals retained as proof. Shared worktree/branch and foreign work preserved.

Next step: coordinator/root adjudicates these exact current findings and author prepares scoped repairs/evidence updates where approved. This reader has no further active work. Session can be archived without data loss; continue from this directory on `codex/question-quality-wave-6`.
