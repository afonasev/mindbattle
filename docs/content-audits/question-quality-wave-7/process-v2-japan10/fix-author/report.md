# Japan fix-cycle 1 author report

- Scope: ten exact frozen IDs; IDs, topic, order, difficulty, and correct index are retained. Baseline `2410346df0cecff7102f5aee66e29c5822243b67`.
- Final author result after claim-specific source work: READY 3, FIX 0, HOLD 7; quality credit 0. `candidate.json` contains exact before/proposed cards, canonical card hashes, six literal groups and their canonical JSON SHA-256 values.
- Exact pre-source-pass candidate and report are preserved byte-for-byte as `candidate-before-source-pass.json` and `report-before-source-pass.md`.
- No catalog or shared source index was edited; no Git index/history mutation was performed by this author. No tests/runtime/build or other agent/chat was used. Independent reviewer output remains unchanged.

## READY

- `history-japan-easy-02a-01`: kept the yen question. The explanation and correct note use Bank of Japan’s direct facts: the 1871 New Currency Act introduced the yen; the first Bank of Japan ten-yen notes appeared in 1885. Replaced unsupported notes with directly sourced facts: Bank of Korea lists a 50,000-won denomination; Bank of China records certificates denominated in yuan as the RMB unit; Bank of Thailand issues Thai banknotes and names baht-denominated reserve securities. The complete official captures, headers, date, byte length and SHA-256 are in `sources/index.json`.
- `history-japan-easy-02a-02`: Hiroshima City’s complete saved page supports Hiroshima as the first city hit with an atomic bomb used against people, 6 August 1945, and its estimate of about 140,000 deaths by year end. A bounded official Nagasaki City capture supports the 9 August note; JOC Tokyo 1964 supports the Tokyo Olympics note; a bounded Osaka City capture supports Minato ward’s six raids and 88.6% burned. Full actual neighbor `history-japan-easy-01b-02` asks the second atomic bombing on Nagasaki; the proposed item asks the first bombing in Hiroshima.
- `history-japan-easy-02a-04`: replaced the Tokyo 1964 semantic duplicate with a distinct easy question about the Meiji Restoration ending over 260 years of feudal government. JapanGov supports the key, explanation and Iwakura distractor; NDL supports Perry/opening and the Charter Oath. Full actual neighbors Charter Oath, Iwakura mission, Tokyo–Yokohama railway and Tokyo Olympics were personally compared; none asks the Meiji Restoration tested fact.

## HOLD

- `history-japan-easy-02a-03`: JACAR fully supports the pact’s parties/date. The Winter War, Iberian neutrality, and Britain/France entry notes still lack primary contexts.
- `history-japan-easy-02a-05`: the full NIDS PDF was not semantically read in this pass; extraction/index is not accepted as evidence. Same-category options and complete notes remain unresolved.
- `history-japan-easy-02b-01` and `history-japan-easy-02b-03`: no fully supported independent easy replacement was established. JMA alternate was fully read and covers the 1923 Great Kanto earthquake, already asked by actual medium neighbor `history-japan-medium-01a-04`; National Archives alternate was read in full after decoding its declared Shift_JIS as CP932 and covers the Boshin War, already asked by actual medium neighbor `history-japan-medium-02a-05`. I did not repeat either tested fact. This is a source/difficulty evidence gap, not an unresolved boundary decision.
- `history-japan-easy-02b-02`: corrected service direction: shinobi gathered intelligence for the lords they served. Mie University supports the key, but notes about sōhei, ashigaru and bugyō need exact contexts.
- `history-japan-easy-02b-04`: corrected the explanation to distinguish August Potsdam acceptance from September’s surrender instrument. Three distractor notes need primary support.
- `history-japan-easy-02b-05`: NDL supports Allied occupation and practical U.S./MacArthur direction. League of Nations, UN founding purpose/date and Axis terminology notes remain unsupported.

## Evidence and neighbor review

`sources/index.json` links exact primary URLs, titles, capture/HTTP dates, body/header byte counts and SHA-256. Existing raw captures were read from their saved paths, not downloaded again. New official pages were obtained once each with bounded curl time/size limits; successful responses are recorded with their actual HTTP dates. No failed source attempt was bypassed.

The two supplied JMA/National Archives alternate pairs were personally read. Their bodies and headers are now immutable at `codex/question-quality-wave-6`, commit `826b2dd5f1cfe72476d6527e5205d1870b644b4a`, paths in `sources/index.json`. The transfer manifest records `headers.complete=false`; that transport flag is preserved, not treated as semantic acceptance. The JMA manifest carries its exact HTTP Date and a separate observation UTC; the producer’s `captureDateUTC` is not treated as a verified UTC instant.

Actual full neighbors reviewed: Tokugawa leader; second Nagasaki bombing; Emperor Showa name; Charter Oath; Iwakura mission; Tokyo–Yokohama railway; Tokyo 1964 Olympics; Italy’s Steel Pact; 1923 Great Kanto earthquake; Boshin War; WWII end year; and the 1952 occupation treaty. Every entry’s neighbor comparisons are in `candidate.json`.

## Remaining action

For each HOLD, use a full primary context for every remaining claim or a genuinely independent in-boundary easy fact with four supported notes. If a bounded request and one official alternate cannot resolve a specific claim, retain HOLD. This is still cycle 1; no new cycle or independent CURRENT review has been started.
