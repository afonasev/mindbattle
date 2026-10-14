# Japan fix-cycle 1 author report

- Scope: the ten frozen IDs from `fix-request.json`; topic/order, difficulty and `correctIndex` are unchanged.
- Result: READY 0, FIX 0, HOLD 10; quality credit 0. The exact `beforeCard` values and SHA-256 values are copied from the request manifest; proposed cards and hashes are included in `candidate.json`.
- The six canonical literal groups (`promptOptionsAndKey`, explanation, and four notes) each have a canonical JSON SHA-256. The entry-level canonical card hash includes `source`.
- No catalog or tracked file was changed; no Git index/history mutation, process, or test was performed/launched. The independent review remains immutable and is not replaced by this author result.

## Content work and holds

- `history-japan-easy-02a-01`: shortened the explanation and yen note to the Bank of Japan’s directly stated 1871 New Currency Act fact. HOLD: won, yuan and baht notes remain unsupported by the saved, personally read primary context; each needs a precise official source or a supported replacement note.
- `history-japan-easy-02a-02`: Hiroshima City’s complete saved page directly supports Hiroshima as the first city bombed with an atomic bomb used against humans and gives 6 August 1945. HOLD: the notes about Nagasaki, Tokyo and Osaka need their own primary contexts.
- `history-japan-easy-02a-03`: tightened the explanation and correct note to JACAR’s full page, which names Japan, Germany and Italy and the 27 September 1940 signing in Berlin. HOLD: the Winter War, Iberian neutrality, and British/French entry notes lack directly read primary contexts.
- `history-japan-easy-02a-04`: the Tokyo 1964 question repeats the existing cross-topic question about the first Summer Olympics in Asia. It needs a genuinely independent easy fact and a complete, sourced replacement answer set/notes; no such fully evidenced replacement was established in this pass.
- `history-japan-easy-02a-05`: same-category variants and full primary confirmation of all notes remain necessary. The NIDS PDF context in the archive was not personally read in full here, so its extraction/index is not credited as semantic review.
- `history-japan-easy-02b-01` and `history-japan-easy-02b-03`: their 2011 tested facts exceed the frozen history-japan boundary through the end of the twentieth century. The scope decision requires distinct, in-boundary replacements and full source-backed notes; no complete replacement card was established from the contexts personally read here.
- `history-japan-easy-02b-02`: corrected service direction in the ninja note and explanation: shinobi gathered information for the lords they served. HOLD: notes for sōhei, ashigaru and bugyō lack their own supporting primary contexts.
- `history-japan-easy-02b-04`: removed the unsupported assertion that acceptance of Potsdam itself was Japan’s formal surrender; explanation now distinguishes August acceptance from the September instrument. HOLD: the three distractor notes need exact primary support. Actual neighbor review found a related but distinct WWII-end-year question.
- `history-japan-easy-02b-05`: HOLD: the League of Nations, UN founding purpose/date and Axis terminology notes are not supported by the read NDL occupation page. Its supported occupation/MacArthur fact remains relevant to the key note and explanation.

## Evidence and neighbor review

`fix-author/sources/index.json` records available exact body/header locators, dates, byte counts and hashes where exposed by the preserved source receipts; `candidate.json` links the sources and states read scope. Saved raw bodies were not downloaded again. For the Hiroshima City page, the complete saved HTML text and headers were read locally. For the Bank of Japan, JACAR, JOC Tokyo 1964, Mie University ninja, National Diet Library occupation and National Archives surrender contexts, the saved full page texts were read; the NIDS PDF was not treated as semantically read. Hashes and transport records are provenance only.

Actual current neighbors were opened as full cards for the Meiji/Tokugawa item, Nagasaki bombing, Italy’s Steel Pact, the cross-topic Tokyo 1964 item, WWII end year, and postwar occupation treaty. Their comparisons are recorded per entry. The Hiroshima/Nagasaki relation and Japan/Italy pact relation are distinct questions; Tokyo1964 is a same-fact semantic duplicate. The paired 2011 items are related but ask different answers.

## Next action

HOLD requires one bounded, claim-specific source pass or a verified replacement for each unsupported option note; use an independent in-scope fact for the Tokyo duplicate and both out-of-boundary 2011 cards. If exact source context remains unavailable after the permitted bounded request and one official alternative, retain HOLD with the unresolved claim and source request. No further author cycle is implied.
