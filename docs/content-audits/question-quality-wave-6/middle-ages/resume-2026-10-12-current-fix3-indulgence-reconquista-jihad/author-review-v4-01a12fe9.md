# PDF quote provenance correction — three-card freeze v4

V4 changes evidence provenance only. It preserves runtime, scope, and historical v1–v3 receipts. All 18 field groups remain. Existing human-readable citation quotes and their hashes are unchanged; v4 separately records exact PDF page-text excerpts and hashes, physical pages, full page-text hashes, `pypdf 6.19.0` extraction and the explicit alignment recipe. No expected or raw-source hash was substituted.

The Siyar note points to Bonner physical p.3. Bonner’s qital context crosses the p.2/p.3 boundary, so its exact extracted text is recorded as two physical-page fragments mapped to the retained combined readable citation. Line reflow, dehyphenation, ligature and punctuation treatment are declared as matching transformations only.

No source was fetched. Static provenance checks only; no tests, counters, full QA, build, deploy, or reader verdict. Independent reader qualification remains pending.
