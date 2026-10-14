# Author packet — Japan history, 17 frozen IDs

Baseline: `826b2dd5f1cfe72476d6527e5205d1870b644b4a`. Scope is exactly the 17 entries in `candidate.json`. ID, topic, difficulty, answer order, and key are frozen. Candidate statuses: **FIX 1, HOLD 16, READY 0**. The single FIX is an author proposal for independent review, not a coordinator approval.

## Work completed

- Read all 17 complete baseline cards and stored their full immediate-neighbor snapshots from the baseline. Immediate neighbors were calculated from the full baseline topic-array order and stored as complete card snapshots; all adjacent cards are in this 17-card range except the terminal `04b05`, which has no following card in the baseline array. The full Met chronology for `03a03` is cited as source context for `04b05`.
- Read every complete newly captured primary/official source body, including the Shift_JIS National Archives page, the Nanzan 16-page scholarly PDF, and the stored full Met chronology for `04a02`. Recorded URL, capture time where available, status/transport, body and header locators, byte counts, and hashes in `candidate.json` and source manifests. `04b01` additionally cites a related full-range NDL chapter as supplemental context; it has no ETag and is not the exact card-linked PDF URL.
- `04a05` is proposed as FIX: the question now asks the article-supported claim directly (Christian peasants in Shimabara and Amakusa, 1637). Its explanation and four option-specific notes use passages from Nanzan pp.13 and 18–20. The key and difficulty are unchanged. A reviewer should check the Russian wording and educational fit.
- The other 16 remain HOLD because at least one material claim in the prompt, explanation, or notes lacks complete exact support. Every field group states its own confirmed fact or unresolved claim; a source that supports the key does not automatically clear the distractor notes.

## Source limits and stop handling

- Incomplete response bodies were discarded; original response headers and transport records remain. No exact failed URL was repeated, no TLS or authentication control was bypassed, and no incomplete body is treated as a source.
- After a primary failure, one distinct official alternative was tried where available. A timeout on one source route did not stop work on other distinct routes. An HTTP 403 and a 404 remain unusable evidence.
- Notable holds: `03a04` alternate supports Gregorian reform but not calendar distractor notes; `03b04`, `03b05`, `04a01`, `04a04`, `04b02`, and `04b03` lack complete usable source text; `04b01` has related NDL support for the key but not all slogan notes. `03a05`, `03b01`, `03b02`, `03b03`, `04a02`, `04a03`, and `04b04` have main-claim support but unresolved card-level claims.

## Handoff

Review `candidate.json` and `sources/` together. Coordinator should independently verify the proposed FIX and resolve each HOLD from the specific field-group gaps before any catalog change. No runtime, test, build, catalog/index, or Git operation was part of this author packet.
