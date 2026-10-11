# Winter pilot author repair follow-up

This follow-up edits only winter-sports-007, 008, 017 and 019. Card 024 is content-unchanged and has a fresh author receipt binding its current six literals and current card hash; the older author receipt is preserved as history. The independent reader's current 024 hash is `474b55158928cbaabeb1c42038d1e42d3b8a687c4d6782d8db87924b221b7262`.

`author-current-repair-receipt.json` binds all six fields of each edited card to full source originals, source locators, raw hashes and passage hashes. `author-current024-receipt.json` does the same for unchanged 024. The author card hash is compact UTF-8 JSON preserving property order; sorted-key hashes are recorded separately. Literal hashes have no trailing newline. `source-readback.json` inventories complete primary originals read. `git-roundtrip.json` records the source bytes, current topic blob and scope checks.

Failed Zamboni retrieval attempts remain preserved in the independent reader's `failed/` directory and are explicitly not used as evidence. No change is made to the protected other 95 cards or the remaining 28-card scope. A different reader must re-read the four repaired cards before the pilot may scale; unchanged 024 does not require rereading.
