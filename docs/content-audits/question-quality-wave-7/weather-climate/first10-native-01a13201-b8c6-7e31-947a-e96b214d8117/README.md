# Weather/climate first-ten author review v2

- Author native thread: `01a13201-b8c6-7e31-947a-e96b214d8117` (the ID supplied for this running native thread).
- Coordinator native thread: `01a131f2-9f5f-74f3-b0fe-e0a7d7f99e18`.
- Exact scope: the same 10 IDs in `coordinator-continuation-01a131f2/weather-climate-first10-exact-scope.json`; no new IDs, no editorial review or changes to the other 90, no items counted.
- The root-named predecessor package remains unchanged at commit `0a85b4644dd222e6e59892f944c51c726248abd1`. This package does not reuse its author verdict or its incorrectly attributed nativeThreadId.

## Review outcome

The current full card for every selected ID was read as prompt + four ordered answer strings + correctIndex/key + explanation + each of four answer notes. Difficulty and card-level source metadata were considered separately. The audit contains 60 component groups: 59 author-rechecked provisional passes and one HOLD on `weather-climate-barometer-pressure` because a manually read card in another topic asks the same basic instrument/pressure fact. The coordinator later clarified that the selected fact may be replaced while preserving ID, easy difficulty, key slot/index, and position. This author slice stopped before selecting, drafting, and re-reviewing a replacement, so the prior HOLD remains and author qualification is incomplete. The independent reader has not been launched, and the future count remains 0.

Five later exploratory source captures are retained with exact body/header hashes in `source-manifest-v2.json`. They were not reviewed, used to justify a card, or added to passage evidence. One unrelated URL response is also retained as a raw diagnostic capture. They require review in the next author slice before use.

The review made narrow same-scope corrections: the hail distractor note now describes NWS-supported hail growth; the snow distractor note compares the separately defined NWS rain and drizzle thresholds; the cloud prompt specifies elevated formation to distinguish it from surface fog; the rain prompt rules out mixed/solid precipitation; and the thermometer prompt asks about the weather-station sun shield rather than restating the generic instrument/temperature relation.

## Source and locator evidence

`source-manifest-v2.json` extends the old 15-source package with two captured NWS primary sources: the drizzle definition and the complete hail-growth paragraph. All saved old source bodies and response headers were rechecked against both disk and the predecessor Git commit; all two new body/header pairs are SHA-256 recorded.

`source-passages-v2.json` records 30 raw byte ranges and the complete enclosing glossary entry, paragraph, or table row, with separate raw-context hashes and normalized readable context. Bytes are decoded as strict UTF-8; locator display text removes HTML tags, decodes HTML entities, then collapses Unicode whitespace runs using Python `str.split()`/space joining. No Unicode normalization or editorial correction is applied. The 10 listed literal-spacing differences are from retained line breaks/indentation in the old quote strings; each range equals its old quote after the stated whitespace collapse. No old body bytes or expected SHA values changed.

`manual-neighbor-review-v2.json` contains 29 current full neighboring cards. Candidate discovery references the saved targeted scan of 110 files / 11,000 cards; only the relevant neighbors are claimed as manually read. There is no claim of a manual whole-catalog review.

## Checks and remaining gate

Performed source-byte/hash/locator checks, full-card snapshot and fixed-field comparisons against the frozen baseline, 90-card preservation comparison, and receipt/source-reference consistency checks. No app tests, build, full suite, independent-reader pass, coordinator count, deployment, or merge is claimed.
