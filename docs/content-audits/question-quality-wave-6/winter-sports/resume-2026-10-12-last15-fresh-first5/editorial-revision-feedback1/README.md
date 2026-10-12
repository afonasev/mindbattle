# Wave6 first five: feedback-specific author revision

The earlier first-freeze receipt and its old scalar hashes/grouping remain historical. The appended `correctedWholeSixSourceEditorialReread` defines the six required groups for every current card: prompt-key object, explanation, notes 0–3. Each group has the native literal and hash, distinct source analysis, distinct editorial analysis, and source quote IDs bound to exact locators, quote SHA, raw source SHA and Git blob ID. Card metadata and full card hashes are also recorded.

Card 068 covers an IIHF empty-net goal; the football hat-trick card was not edited. IDs, order, difficulty, correct-index slots and the other 95 cards remain unchanged. Full raw sources remain directly tracked. Manual reading extent is stated by passage/page; complete capture does not imply every page was read.

Card 067 is HOLD for Medium literal 139: its ratios and the common meaning of “Большинство” may reveal the answer without hockey knowledge. This is a source-only receipt; runtime is unchanged and the counter remains zero. The independent reader must review all current fields. The remaining ten questions are still HELD.

PDF locator provenance is now explicit in `author-grouped6-source-editorial-review.json`: pypdf 6.19.0 on Python 3.13.0rc2 extracts physical pages, then Python whitespace collapsing (`" ".join(extract_text().split())`) yields derived page text. The 11 PDF quote offsets/lengths, per-page derived-text SHA-256/length, raw extraction SHA-256/length, and unchanged raw source SHA/Git blob are recorded. Historical locator strings and quote hashes are preserved; HTML locators remain zero-based raw-byte offsets/lengths.
