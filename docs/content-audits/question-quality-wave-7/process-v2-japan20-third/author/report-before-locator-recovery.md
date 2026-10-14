# Author review — Japan 20 (third packet)

- Scope: 20 IDs from baseline `a1a9375de0c6defc3a98fc511fdde8bbcdfcecc9`; frozen `topicId=history-japan`, every ID/difficulty/order/correctIndex preserved.
- Status: HOLD 20; READY 0; FIX 0. No text proposed because claim-level evidence is unavailable.
- Blocker: preimage packet locator resolves to a nonexistent path. The manifest names the packet without `tmp-source-files/`; that packet’s source catalog contains none of the 20 exact source URLs.
- Independently opened each baseline card and its immediate neighbors from the baseline Git object; prior labels/verdicts were not used as evidence.
- Source/index artifact records the locator mismatch and exact next action. No raw source was fetched or copied.
- Every card has six literal groups with SHA-256 and per-claim source/editorial reasons in `candidate.json`.
- Every frozen hash was reproduced from the baseline card using canonical sorted-key compact UTF-8 JSON; proposed hash equals before hash.
- Required next step: coordinator supplies correct complete body+headers Git locators and capture metadata; author/reviewer then checks every answer and note, difficulty/key, explanation, and neighbors.
