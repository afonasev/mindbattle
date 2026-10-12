# V5 author qualification — middle-ages-shrine

Author thread: `01a131f4-5e16-7711-b0bb-c2f98a0c40db`

V5 repairs only `answers[2].note` after the V4 independent reader marked it FIX. V3 and V4 evidence remains immutable history. This is an author assessment, not independent or human acceptance.

## Exact current card literals

- ID: `middle-ages-shrine`
- Difficulty: `easy`
- Prompt: На каком языке преподавали в университетах средневековой Западной Европы?
- Correct index: `1`
- Correct key literal: `Латынь`

| Index | Answer | Correct | Note |
|---:|---|---|---|
| 0 | Французский | no | Французский был одним из народных языков Европы; его нормы развивались иначе, чем закреплённые текстами нормы латыни. |
| 1 | Латынь | yes | На латыни преподавали и проводили диспуты; общее знание языка облегчало общение студентов и преподавателей из разных стран. |
| 2 | Английский | no | После Великого сдвига гласных англичане могли произносить латынь так, что другим европейцам было трудно их понять. |
| 3 | Немецкий | no | Немецкий был одним из народных языков Европы; его нормы развивались иначе, чем закреплённые текстами нормы латыни. |

**Explanation:** Латынь служила языком преподавания и диспутов в средневековых школах и университетах. Общее знание латыни облегчало обмены между европейскими учёными и академические поездки студентов.

V5 note2: `После Великого сдвига гласных англичане могли произносить латынь так, что другим европейцам было трудно их понять.`

## Review and evidence

- The V4 reader’s scoped FIX is addressed: Cambridge says English people spoke Latin, especially after the Great Vowel Shift, and that their Latin pronunciation could impede comprehension. The V5 sentence identifies English people as speaking Latin.
- Source proofs preserve complete source paragraphs and exact quote hashes/offsets. Cambridge Background is all-HTML paragraph 6 / visible paragraph 5. English pronunciation is all-HTML paragraph 30 / visible paragraph 29. Sorbonne remains paragraph 7.
- Locator recipe: Python 3 stdlib HTMLParser with convert_charrefs; ignore script/style/noscript text; add ASCII boundary spaces around p/li/h1/h2/h3/blockquote/div/section; concatenate then collapse Unicode whitespace to ASCII spaces and strip. Paragraph ordinals distinguish all `<p>` start tags, including noscript, from visible paragraphs. Offsets are zero-based Unicode code points in normalized document text.
- Runtime freeze is V4 code commit `bdfc0f25609885449c96b6ea52ee0807345786f1`; V4 evidence freeze is `d1f9885b960987b10b8766dbb470f3429e0ffdff`; source captures remain frozen at `63ac6139f9cb9d8ce3246572632e2258678e1c45`. The older `512f8556ec67bb0bb3c23de0c3667e5d849f2b4c` is a pre-V4 runtime baseline only.
- Easy was personally re-evaluated and remains PASS. Metadata is unchanged and remains PASS. The targeted catalogue search is reused because prompt/key/order are unchanged; V4 reader catalogue dedup was PASS.
- Only the target card differs from baseline `e02389f`; the other 99 cards are protected. No tests, build, Player, deployment, or human acceptance were run or inferred.

Next gate: fresh independent reader review of V5, including the repaired note and Easy.
