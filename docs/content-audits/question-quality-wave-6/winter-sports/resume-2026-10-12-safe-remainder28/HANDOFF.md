# Winter sports exact28 handoff

Scope remains exactly these IDs, in topic order: 023, 026, 029, 030, 031, 032, 035, 036, 038, 039, 043, 057, 058, 059, 060, 067, 068, 073, 076, 082, 089, 090, 091, 092, 095, 097, 098, 100. Do not change `difficulty`, `correctIndex`, ID order, key slots, quotas, or the other 72 cards.

## Current evidence

- `author-repair-whole6-freeze.json` is the author's manual read of all 28 post-repair cards (168 units: prompt/key, four answer text/note pairs, explanation). It includes source pointers and the fresh raw captures' byte counts, SHA-256, Git blob IDs, and URLs. Its manual PASS marks are not computed from hashes.
- `author-whole6-read.json` is pre-repair historical evidence only; its FIX/HOLD judgments do not describe the repaired text.
- `handoff-baseline.json` stores the initial hashes for all 100 cards and the property-order-preserving compact-JSON SHA-256 recipe. The post-repair comparison confirmed the protected72 match and exact28 difficulty/key/order locks.
- Primary originals retained from the earlier capture are in `../resume-2026-10-12-rework31/sources/`; the five new captures are under `sources/`. The new files are raw PDF/HTML captures with TLS verification enabled; no TLS bypass was used.
- `supplemental-agent-history.json` records interrupted child identities and status. Any agent artifact is supplemental and is not author or independent-reader evidence.

## Next action

An independent reader should inspect the committed current topic literals and source claims for these exact28 cards, report field-specific evidence and any remaining issues, and leave the protected72 untouched. Do not start another batch until the coordinator explicitly assigns it.
