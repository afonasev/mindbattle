# Middle Ages current first-two — whole12 author freeze

**Author:** `01a12fe9-74d9-7272-a1d2-f26317e06001`, resolved from trusted native Codex `create_thread` / `read_thread` evidence supplied with this dispatch. The inherited environment named coordinator `01a12fcd-2bbd-72a3-b127-23455e847ca7`; that is a discrepant coordinator identity, not my author identity. The earlier partial review and receipt which attributed these cards to `01a12fcd` remain preserved unchanged as historical evidence. This review, source ledger, and current literal receipt bind the native author ID `01a12fe9`.

**Scope:** only `middle-ages-shrine` and `middle-ages-indulgence` in `src/content/topics/middle-ages.json`. IDs, order, `easy` difficulty and correct indices 1 and 2 remain unchanged. Only shrine notes 0 and 2 changed in this author slice. The Toronto RPO source title and Becket note/explanation corrections from the prior preserved work remain in place. The other 98 scoped cards match their frozen card hashes. No other Middle Ages card, remaining-six group, Reconquista, Jihad or counter was touched.

**Reading and receipts:** after the two note edits, I personally reread the current prompt-key group (prompt, all four ordered answer texts, and key index), explanation, and notes 0–3 for each card. Exact literals and their declared recipes/hashes are in `author-current-receipt-01a12fe9.json`. Per-field source IDs, quote text, quote hashes, raw-source byte hashes, Git blobs and locators are in `source-bindings-01a12fe9.json`. Those scripts and snapshots preserve values; they do not assign quality verdicts.

## `middle-ages-shrine`

### Prompt + four ordered answers + key (index 1)

- **Source basis:** Toronto’s complete *Representative Poetry Online* (RPO) page says the Tales are framed as a group of pilgrims going “to the shrine of St. Thomas at Canterbury”; its line 17 annotation identifies the martyr as Thomas Becket and gives his murder in 1170 and canonization in 1173. The full source bytes, Git blob, page-header identity and exact quotes are bound in the source ledger.
- **Editorial judgment:** one answer fits the specified literary frame; the other three name different English saints and shrines. I retain `easy`: Chaucer’s *Canterbury Tales* is canonical English literature, and the pilgrimage to St Thomas’s Canterbury shrine is the central frame premise of the work. This is a widely known fact within a large literary-cultural group, which the literal Easy rule permits. The item does not depend on a rare date or secondary detail. This applies `mindbattle-planning/docs/GAME_SPEC.md:138`: an Easy fact may be familiar within a large cultural group. A different reader should independently assess this calibration.

### Explanation

- **Source basis:** the RPO headnote directly supports the pilgrims’ destination and St Thomas; the line 17 annotation supports Becket’s identity and 1170 date. The former unsupported location phrase “in the cathedral” is absent from the current explanation.
- **Editorial judgment:** it states why Becket is the key and gives one concise identifying fact without adding an unsupported location or requiring the notes to repair the prompt.

### Note 0 — Saint Alban

- **Source basis:** Bede, *Ecclesiastical History*, Book I, chapter VII, complete Fordham HTML capture: “gave entertainment in his house to a certain clergyman, flying from the persecutors.” The locator, normalized quote hash, raw HTML SHA-256 and Git blob are recorded in the fresh source ledger. The full page is captured; manual review was limited to chapter VII and this passage.
- **Editorial judgment:** this is a specific, useful fact about the selected Alban option and adds biographical context rather than repeating the asked shrine relation. It is explicitly attributed to Bede’s account.

### Note 1 — Thomas Becket

- **Source basis:** RPO’s line 17 annotation says that Thomas Becket, Archbishop of Canterbury, was murdered in 1170 and canonized in 1173. The exact annotation and its raw-source bindings are recorded in the source ledger.
- **Editorial judgment:** canonization is an independent useful fact about the keyed saint, beyond the destination asked in the prompt; it complements the explanation’s 1170 date.

### Note 2 — Saint Cuthbert

- **Source basis:** Bede, *Ecclesiastical History*, Book IV, chapter XXVII, complete Fordham HTML capture: Cuthbert was “promoted to the bishopric of the church of Lindisfarne” after years of solitary life on Farne. Exact locator and quote hash, full-source SHA-256 and Git blob are recorded in the fresh source ledger. The complete page is captured; manual review was limited to chapter XXVII and the cited paragraph.
- **Editorial judgment:** this replaces the unsupported translation claim with a useful fact specifically about Cuthbert; it does not repeat the shrine/pilgrimage relation in the question.

### Note 3 — Saint Edmund

- **Source basis:** the complete captured Abbey of St Edmund Heritage Partnership page states that “the shrine of St Edmund attracted pilgrims from all over Europe.” The quote locator and complete raw-byte/Git-blob identities are retained in the current source ledger.
- **Editorial judgment:** this is a useful, option-specific fact about Edmund’s shrine and supplies context for why pilgrims knew that destination.

### Main source metadata

- **Source basis:** the complete University of Toronto page header identifies the site as *Representative Poetry Online (RPO)* and the work as *The Canterbury Tales: General Prologue*.
- **Editorial judgment:** the previous “Records of the Past” expansion was wrong and has been corrected to the actual site name. The runtime source still points to the same complete page used for the question and key.

## `middle-ages-indulgence`

### Prompt + four ordered answers + key (index 2)

- **Source basis:** Oxford’s complete translation prints thesis 27: “Those who say that the soul flies out of purgatory as soon as the money clinks in the tin are preaching a man-made fiction”; its note 18 says Luther refers to a saying believed to have been used by indulgence preachers. Both exact passages and the complete-page byte/Git-blob identities are bound in the current source ledger.
- **Editorial judgment:** the prompt describes the historical criticism; “Индульгенция” is the unique key among penance, pilgrimage, indulgence and monastic rule. These are related but distinct practices. The Luther/Reformation context is broadly taught and the prompt does not ask for an obscure date or specialist detail, so `easy` remains appropriate.

### Explanation

- **Source basis:** the Oxford thesis 27 text and note 18 support the coin/purgatory criticism and its link to indulgence preachers. Vatican Catechism §1471 supports the definition of an indulgence and the partial/plenary distinction.
- **Editorial judgment:** the explanation separates the historical criticism from the Catechism definition and does not claim that the definition itself is Luther’s wording.

### Note 0 — Penance

- **Source basis:** Oxford thesis 1 says that Christ’s “Do penance” meant “the whole life of the faithful to be penance.” The full translation and the quote locator/hash are in the source ledger.
- **Editorial judgment:** this gives a distinct, useful account of the penance distractor and does not confuse it with the indulgence practice asked about.

### Note 1 — Pilgrimage

- **Source basis:** Schmoelz’s complete captured dissertation, physical/printed page 17, defines pilgrimage in terms of travel and veneration of a relic or image in a church. The source ledger retains the exact reviewed quote and hashes. Only page 17 was manually reviewed for this claim; no whole-book reading is claimed.
- **Editorial judgment:** the note explains the listed religious practice in terms specific to the pilgrimage distractor.

### Note 2 — Indulgence

- **Source basis:** Vatican Catechism §1471 defines an indulgence as remission of temporal punishment for sins whose guilt has already been forgiven, and distinguishes partial from plenary indulgences. The complete HTML bytes, Git blob, locator and exact quote hashes are recorded.
- **Editorial judgment:** this is a concise, accurate definition tied to the correct option and adds the permitted partial/plenary distinction.

### Note 3 — Monastic rule

- **Source basis:** the complete Fordham HTML reproduction of the Rule of St Benedict describes cenobites as “living in a monastery, serving under a rule or an abbot.” The source ledger retains the complete raw capture, hash and locator. The page is an excerpted translation, not the entire Rule; the note uses only the stated excerpt.
- **Editorial judgment:** the note explains the named monastic-rule distractor rather than making an unrelated claim about monasticism.

## Freeze boundary

This is a new author whole12 freeze under native author ID `01a12fe9`, not independent-reader review or human acceptance. The current evidence resolves the previously missing Alban and Cuthbert raw-source proofs, preserves honest manual-reading extent, and provides a reason for retaining Easy on the Chaucer literary premise. No remaining-six or Reconquista/Jihad work is included. No tests, builds, counters, publication, push, merge or integration were performed.

**Next gate:** a different actual reader should review these exact whole12 literals and the Easy calibration before certification. The branch and evidence are committed; this author session can stop here.
