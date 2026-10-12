# V3 author manual review — middle-ages-shrine

Author thread: `01a131f4-5e16-7711-b0bb-c2f98a0c40db`

This is the author's review of one candidate, not independent acceptance. V1 and V2 records are historical and untouched.

## Current card literal

**Difficulty:** easy

**Prompt:** На каком языке преподавали в университетах средневековой Западной Европы?

**Correct index:** 1

| Index | Answer | Correct | Per-choice note |
|---:|---|---|---|
| 0 | Французский | no | Парижский университет объединял студентов по происхождению в отдельные «нации», в том числе французскую и пикардийскую; это не был язык преподавания. |
| 1 | Латынь | yes | На латыни преподавали и проводили диспуты; общее знание языка облегчало общение студентов и преподавателей из разных стран. |
| 2 | Английский | no | В Париже была отдельная английская «нация» студентов; это объединение по происхождению, а не язык преподавания. |
| 3 | Немецкий | no | Немецкий был одним из местных разговорных языков; в средневековых школах и университетах преподавали на латыни. |

**Explanation:** Латынь служила языком преподавания и диспутов в средневековых школах и университетах. Общее знание латыни облегчало обмены между европейскими учёными и академические поездки студентов.

## Author verdicts

- Source verdict for prompt/key, explanation, and all four notes: PASS.
- Editorial verdict for prompt/key, explanation, and all four notes: PASS.
- Easy verdict: PASS. The fact is a basic, broad cultural-history association, not a rare date or technical term; this remains an editorial assessment for an independent reader to challenge.
- Correct index remains 1; difficulty remains Easy; id and answer order are preserved.

## Evidence read personally

- Cambridge University Press, *Spoken Latin in the Late Middle Ages and Renaissance Revisited*: the Background section states that Latin was the teaching and disputation language in medieval schools and universities. Its paragraph on vernaculars identifies French and German among regional languages. Complete raw HTML and response headers are referenced in `author-receipt-v3.json` with byte lengths, SHA-256, and Git blob IDs.
- La Chancellerie des Universités de Paris, *The Sorbonne in the Middle Ages*: its page describes student nations by origin and says Latin command eased exchanges in the European university community. Complete raw HTML and headers are referenced and hash-bound in the receipt.
- Proof offsets use the exact recipe recorded in the receipt: Python 3 standard-library `HTMLParser(convert_charrefs=True)`, omit script/style/noscript contents, join text nodes with block separators, collapse Unicode whitespace runs to one ASCII space, strip ends; offsets count Unicode code points in that resulting string.

## Catalog search and semantic comparison

Searched all 110 topic JSON files (11,000 cards) with answer-side inverse Latin/Латин* retrieval, direct prompt/explanation wording, university terms, prompt intersections for language plus education, and an all-field Latin plus university intersection. These searches were targeted retrieval, not a claim of manual review of every card. The closest manually read Middle Ages cards concern scholasticism, disputation, quadrivium, squire/page training, and apprenticeship. Education neighbors cover university identity/age, not teaching language.

One near-overlap is disclosed: `history-france-villers-language` has a wrong-answer note saying Latin was long used by churches, universities, and educated lawyers. Its question asks about the 1539 ordinance and does not test university instruction. An independent reader should decide whether this incidental note is too close.

## Change boundary and acceptance

Compared against baseline `e02389f`: 100 cards in each snapshot; only `middle-ages-shrine` differs, and all other 99 card objects match. No other topic file was edited by the author. No tests, full suite, build, Player, deploy, or human acceptance were run or implied. The revised candidate requires a fresh independent read; earlier V2 Easy HOLD remains an immutable historical record.
