# Wave 6 author reread v4

Narrow locator correction to the v3 author freeze. V3 remains unchanged and is preserved by its recorded commit and receipt SHA-256. No runtime literals, groups, or canonical hashes changed.

The Syed chapter citation was re-read from the complete source PDF at physical page 12. A direct `pypdf 6.19.0` extraction (`PdfReader(original).pages[11].extract_text()`) was saved without a header or normalization to `sources/ucdavis-jihad-physical12-pypdf-6.19.0.txt`: 3,197 UTF-8 bytes, SHA-256 `cc31201aa68fc5e606b85eaa189892687b6e55751dfcc62343a24c2a6a665dd5`. The earlier 3,202-byte saved extraction differs; v4 does not infer a header adjustment from that difference. The collective-to-individual sentence occurs at Unicode character offset 2222; the following individual-obligation phrase occurs at offset 2512. Each of the three affected binding groups now carries both complete quotes and exact offsets.

This corrects source-location evidence only. Independent reader review remains pending (reader count 0); no certification is claimed. No tests, build, sourceQA/full QA, publication, push, merge, or deployment were performed.
