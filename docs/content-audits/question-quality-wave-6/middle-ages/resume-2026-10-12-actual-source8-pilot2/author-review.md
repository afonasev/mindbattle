# Fresh actual-author source-only pilot — first two Middle Ages cards

## Scope and identity

- Author task/thread: `01a12fb5-bb2b-7882-a38f-ef1061441573` (identity supplied by coordinator in the native create-thread message; never inferred from the parent thread).
- Scope authority: `docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12f20/middle-current8-fresh-source-only-pilot2-scope.json`, scope commit `95bf793` per coordinator. Only `middle-ages-shrine` and `middle-ages-indulgence` are reviewed here. Runtime remains frozen; no card edits.
- Current source literals were personally read from `src/content/topics/middle-ages.json` after matching each card's canonical SHA-256 to the frozen scope receipt. The complete literal snapshot and 100-card comparison are in `integrity.json`.
- The 12 review units per card follow the scope recipe: prompt; four answer texts; four individual notes; key; explanation; main source. Difficulty is separately assessed below.
- Extraction: `pypdf 6.19.0`, unmodified PDF source bytes, physical page 17 equals printed page 17. No OCR or dehyphenation was used for the selected Schmoelz passage. HTML and JSON passages below are from the complete downloaded source files, with locators in `source-ledger.json`.

## `middle-ages-shrine`

### Current fields, in native order

1. **Prompt** — `Что верующие могли почитать в центре христианской святыни?`
   - **Source verdict: HOLD.** Schmoelz says the image-only arrangement is a *new type* of shrine housed in stone parish churches, where the center held images and no primary or secondary relics. The stem omits that type qualifier and generalizes to a Christian shrine; another listed answer, a saint's remains/relic, can also be venerated at other shrines. A note narrows the type after the question, but the stem itself does not.
   - **Editorial defect:** the stem leaves more than one answer factually possible, conflicting with GAME_SPEC.md §«Контент вопросов», “Каждый вопрос имеет четыре различных варианта, ровно один правильный ответ...” (planning source, line 142).
   - **Narrow correction proposal, not applied:** name the described new type of stone parish-church shrine in the stem. Keep the question tied to the source's category rather than implying every Christian shrine.
2. **Answer 1** — `Останки святого`
   - **Source verdict: PASS as a plausible distractor only after the stem is narrowed; otherwise also a plausible correct answer.** CNRTL/TLFi defines a relic as remains of a saint or martyr. Schmoelz's printed p. 17 excludes relics only in the specific new shrine type, not in Christian shrines generally.
3. **Note 1** — `Останки святого считались реликвией; в описанном Шмёльцем типе святынь их в центре не было.`
   - **Source verdict: PASS.** CNRTL/TLFi supports the remains/relic relation; the actual Schmoelz passage supports absence of primary relics in the named type. The note's restriction is accurate, but cannot repair the broader stem.
4. **Answer 2** — `Изображение святого`
   - **Source verdict: PASS.** Directly supported by Schmoelz's selected paragraph.
5. **Note 2** — `Шмёльц приводит Марианские святыни Суффолка, в том числе в Лонг-Мелфорде, Керси, Садбери и Ипсвиче.`
   - **Source verdict: PASS.** The complete paragraph names these four Suffolk examples as Marian shrines of the image-centered type. The extra detail is useful and specific to this answer.
6. **Answer 3** — `Личная вещь святого`
   - **Source verdict: PASS as a plausible distractor only after the stem is narrowed; otherwise also a plausible correct answer.** CNRTL/TLFi and Académie 9 define relics to include objects used by a saint. Schmoelz excludes secondary relics in the specified type.
7. **Note 3** — `К реликвиям относили также вещи, которыми пользовался святой; в центре этого типа святынь их не было.`
   - **Source verdict: PASS.** CNRTL Académie 9/TLFi supports objects used by the saint; Schmoelz supports that this type had no secondary relics. The last pronoun refers to such objects, not to all Christian shrines.
8. **Answer 4** — `Книга с молитвами`
   - **Source verdict: PASS as an incorrect option for the specified image-centered type.** The source's contrast is images rather than relics; it does not discuss prayer books individually, so the exclusion is an inference from the source's categorical description, not a direct quotation.
9. **Note 4** — `В центре описанных Шмёльцем святынь находились именно изображения, а не книги.`
   - **Source verdict: HOLD.** Schmoelz supports the image-centered type but does not discuss books; the note only repeats the keyed answer and asserts an unsupported book exclusion. That is not a useful independently verified fact for the option under GAME_SPEC.md §«Контент вопросов» line 143. A candidate replacement, not applied: `В часослове XIII века для мирянки были разделы «Часы Девы Марии» и покаянные псалмы.` The British Library catalogue for Egerton MS 1151 identifies a Book of Hours made c.1260–70 for a laywoman and lists both sections.
10. **Key** — `correctIndex: 1` (`Изображение святого`)
    - **Source verdict: HOLD pending prompt correction.** The key matches Schmoelz only for the specified type; under the literal broad stem, a relic is also possible. This is the same one-answer defect as field 1, not a separate source error.
11. **Explanation** — `Шмёльц описывает новый тип святыни в приходской церкви: в центре находилось изображение святого, а не первичная или вторичная реликвия. Примеры относятся к позднесредневековой Восточной Англии.`
    - **Source verdict: PASS.** The complete passage states a new type in stone parish churches, images instead of primary/secondary relics, and locates examples in Suffolk/East Anglia in a discussion of later medieval pilgrimage. The explanation is factually accurate and useful but supplies the qualifier missing from the prompt.
12. **Main source** — Michael Schmoelz, *Pilgrimage in Medieval East Anglia: A Regional Survey of the Shrines and Pilgrimages of Norfolk and Suffolk*, https://ueaeprints.uea.ac.uk/id/eprint/63940/1/Pilgrimage_in_medieval_East_Anglia.pdf
    - **Source verdict: PASS for the explanation and intended image/relic contrast.** The complete 316-page PDF was captured; actual manual review was limited to physical/printed pp. 13 and 17. On p. 17, the paragraph beginning “In addition to these new monastic pilgrimage centres...” states the image/relic distinction; p. 13 was checked to avoid overgeneralizing. No whole-book reading is claimed. The sentence directly states that this new type used images rather than relics; following context describes the regional/local pilgrimage setting.

### Difficulty and single-key check

- **Difficulty:** recommend `medium` if the stem is narrowed. Under GAME_SPEC.md §«Контент вопросов» line 138, Easy tests a widely known fact and excludes rare or secondary details. This asks about a specific shrine type in specialist regional scholarship; the plausible distractors do not make the tested fact broadly known. No runtime difficulty change is made.
- **Parallel plausible key candidate:** `Останки святого` (answer 1) is another plausible object venerated at Christian shrines generally. The primary source itself distinguishes bodily and secondary relic veneration elsewhere, then excludes them only in the newly described image-centered type. That substantiates the ambiguity rather than merely suggesting it.

## `middle-ages-indulgence`

### Current fields, in native order

1. **Prompt** — `Какую церковную практику обсуждают знаменитые «95 тезисов» Мартина Лютера?`
   - **Source verdict: PASS.** Fordham's complete Latin source is headed *Disputatio Pro Declaratione Virtutis Indulgentiarum*, identifies the work as “95 THESES” by Martin Luther, and gives the Weimar edition attribution. The prompt asks for the practice, not a doctrinal definition.
2. **Answer 1** — `Покаяние`
   - **Source verdict: PASS as a plausible religious-practice distractor.** The CNRTL Académie 9 and TLFi repentance entries distinguish repentance from indulgence.
3. **Note 1** — `Покаяние означало раскаяние в совершённом грехе и стремление исправить содеянное.`
   - **Source verdict: PASS.** TLFi describes religious repentance as sorrow for sins with desire to repair and not relapse; Académie 9 also includes sorrow for offending God and a resolve not to repeat faults. This is useful and pertains to the option.
4. **Answer 2** — `Паломничество`
   - **Source verdict: PASS as a plausible but different religious practice.** Schmoelz describes pilgrimage as travel to and veneration of a relic or image in a church, clearly separate from Luther's theses.
5. **Note 2** — `Паломничество было религиозным путешествием к почитаемому святому месту.`
   - **Source verdict: PASS.** Schmoelz's definition and following description of local journeys to a reputed image support the brief paraphrase; the statement is a useful fact about the selected distractor.
6. **Answer 3** — `Индульгенция`
   - **Source verdict: PASS; key candidate supported.** Both Fordham's primary text title and the Vatican Catechism's treatment identify indulgences as the subject.
7. **Note 3** — `Индульгенция относилась к временной каре за грехи, уже прощённые церковью; она могла быть полной или частичной.`
   - **Source verdict: PASS.** Vatican Catechism §1471 directly defines indulgence in terms of temporal punishment for sins whose guilt is already forgiven, and distinguishes partial and plenary indulgences. This definition is not present in the card's Fordham main-source page; the card's current source metadata therefore does not point readers to this additional authority.
8. **Answer 4** — `Монастырский устав`
   - **Source verdict: PASS as a plausible but distinct religious institution/text type.** The complete Fordham sourcebook page reproduces extended Rule of St Benedict excerpts and identifies a rule for monastic life, with an explicit monastery/rule distinction.
9. **Note 4** — `Монастырский устав устанавливал общие правила жизни монашеской общины.`
   - **Source verdict: PASS.** The Rule of St Benedict source describes cenobites as living in a monastery and serving under a rule or abbot; the chapters prescribe communal service and conduct. The note is a useful, accurate paraphrase about this distractor.
10. **Key** — `correctIndex: 2` (`Индульгенция`)
    - **Source verdict: PASS.** The primary text's title identifies indulgences as the subject; no other option names the practice treated in the 95 Theses.
11. **Explanation** — `В заглавии тезисов Лютера говорится о силе и действенности индульгенций. В церковном определении это освобождение от временной кары за уже прощённые грехи; паломничество и монастырский устав относятся к другим сторонам религиозной жизни.`
    - **Source verdict: PASS factually, with a source-attribution gap.** The first sentence follows Fordham's Latin title. The second definition is supported by Vatican Catechism §1471; the final contrast is supported by Schmoelz and the Benedict Rule text. The only URL in the current card is Fordham, so it does not expose these two supplementary authorities.
12. **Main source** — Martin Luther, *Disputatio pro Declaratione Virtutis Indulgentiarum (95 Theses)*, https://sourcebooks.web.fordham.edu/source/95theses-latin.asp
    - **Source verdict: PASS for the stem/key.** The full original-source page is captured. It attributes the Latin text to Luther and the 1883 Weimar edition; its title explicitly names indulgences and identifies it as the 95 Theses. It does not itself provide the Catechism definition or define the two distractor practices.

### Difficulty and single-key check

- **Difficulty:** `easy` is appropriate: Luther's 95 Theses are a broadly taught adult-history reference and the prompt asks for their well-known subject, not for a technical definition. The four answers are distinct, recognizable Christian practices/institutional forms; the distractors are plausible rather than absurd.
- **Parallel plausible key candidate:** none. The other three are related Christian concepts, but the source title specifically names indulgences; repentance, pilgrimage and a monastic rule are not the theses' named subject.
- **Source-traceability note:** the current Fordham source field is accurate and strong for the central question. The unlisted Vatican, Schmoelz and Benedict captures support factual additions; they are preserved here as supporting evidence, not silently substituted for the runtime's main source field.

## Manual source excerpts and extraction boundary

- Schmoelz, physical/printed p. 17: “neither primary nor secondary relics at their centres, but merely images of the saints”. The immediately following parenthesis gives four Suffolk Marian shrine examples; see the complete captured PDF and extraction file.
- Schmoelz, physical p. 13: the introduction discusses bodily relics and secondary devotional objects, establishing why the p. 17 statement cannot be generalized to every Christian shrine.
- CNRTL API `relique`, TLFi definition: “objets ayant été à son usage”. Académie 9 is present in the same complete API response and likewise identifies an object used by a saint.
- Fordham complete Luther page: DOM title “Disputatio Pro Declaratione Virtutis Indulgentiarum”; immediately below it the page says “95 THESES” and attributes the text to Martin Luther.
- Vatican Catechism, section X, paragraph 1471: “An indulgence is a remission before God of the temporal punishment due to sins whose guilt has already been forgiven”. The next sentence distinguishes partial and plenary remission.
- Fordham complete Rule of St Benedict, Prologue and introductory classification: “school for the Lord's service”; cenobites are monks “living in a monastery, serving under a rule or an abbot”.

## Closure boundary

This is an author source review only. The shrine prompt/key has a concrete HOLD recorded above. No source verdict here is a different-reader certification, acceptance of the two-card pilot, authorization to review the remaining six, a runtime repair, a QA result, or a content-counter change. Wait for the coordinator's separate-reader gate before proceeding beyond these first two.
