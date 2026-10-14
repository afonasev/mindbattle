# Author checkpoint — Japan history, 17 frozen IDs

Baseline: 826b2dd5f1cfe72476d6527e5205d1870b644b4a. Status: HOLD 17; READY 0; FIX 0.

## Findings

- Four new exact URLs returned complete HTTP 200 bodies: 03a05, 03b01, 03b02, 03b03. Existing full body captures are indexed for 03a01 and 03a02. The reviewed NDL pages support lead facts for 03a05, 03b01, 03b03, but not every distractor note.
- Two technical failures reached the stop threshold: 03a04 (NDL calendar page, 15,199/22,543 bytes) and 03b04 (NDL Atagoshita page, 16,085/732,635 bytes). Incomplete bodies were discarded; raw headers and transport records remain. No alternate was fetched after the second failure.
- 03b02 was decoded as Shift_JIS per the page charset and fully read: the Archives page confirms the San Francisco Peace Treaty took effect on 28 April 1952 and restored sovereignty, but its four option notes still lack exact supporting contexts. 04b01 has a preserved full NDL PDF, but it was not personally read; the previous author PASS is not inherited.
- Each HOLD records claim-specific gaps, six field hashes, and actual adjacent baseline IDs/hashes. No proposed rewrite is made without full evidence.

## Next action

Read the complete existing captures and make the Japanese source readable, then continue exact contexts for remaining IDs without exceeding the two-failure stop rule. Reassess each whole card only after verifying all options, notes, and actual neighbors.
