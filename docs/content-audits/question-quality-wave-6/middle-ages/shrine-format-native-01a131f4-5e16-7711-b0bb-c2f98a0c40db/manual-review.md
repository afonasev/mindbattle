# Manual review — middle-ages-shrine

Author thread: `01a131f4-5e16-7711-b0bb-c2f98a0c40db`; date 2026-10-13. Baseline `f6fca5356827e63014075e8656dd6ac7fbfaafaa`; baseline whole-card SHA-256 `92073b8cedc4590afedcd319345ef2dbf790a60a7611766caecb4a5edc5f9de1`.

## Current six-field read

**Prompt + all ordered answers + key, read together:**

> К чьей святыне направляются паломники в «Кентерберийских рассказах» Джеффри Чосера?
> 0. Святого Альбана
> 1. Томаса Бекета (key, correctIndex 1)
> 2. Святого Кутберта
> 3. Святого Эдмунда

**Explanation:** “Чосер описывает группу паломников, направляющихся в Кентербери к святыне святого Томаса — Томаса Бекета, убитого в 1170 году. Поездка к этой святыне служит рамкой для «Кентерберийских рассказов».”

**Notes read separately:**

- note0 / Святого Альбана: “По рассказу Беды, Альбан укрыл у себя христианского священника, бежавшего от преследователей.”
- note1 / Томаса Бекета: “Томас Бекет, архиепископ Кентерберийский, был убит в 1170 году и причислен к лику святых в 1173-м.”
- note2 / Святого Кутберта: “Беда сообщает, что Кутберт стал епископом Линдисфарна после долгих лет отшельнической жизни на острове Фарн.”
- note3 / Святого Эдмунда: “Святыня Эдмунда в Бери привлекала паломников со всей Европы.”

Difficulty and source metadata were reviewed separately. Easy is borderline but plausible only within the large literary-cultural audience allowance; leave unchanged and have the independent reader/coordinator adjudicate. The full review receipt includes exact literals, per-group hashes, source/editorial reasons for each choice and group, complete-source byte identities, exact quotes and offsets.

## Manual assessment

RPO’s full headnote states the pilgrims are headed to “the shrine of St. Thomas at Canterbury”; the line 17 annotation identifies Thomas A Becket and says murdered 1170, canonized 1173. That makes answer 1 the unique key. Bede I.VII supports Alban’s note; Bede IV.XXVII supports Cuthbert’s note; the St Edmund Heritage Partnership page supports Edmund’s burial at Bury and the shrine’s European pilgrims. These are useful facts about their own answer choices and make them plausible, distinguishable distractors.

The added second sentence only explains that the journey to the shrine frames the Tales, as stated in the RPO headnote. No unsupported fact was added.

## Catalog retrieval

Scanned 11,000 cards across 110 topic files with targeted exact-name and Russian-stem retrieval over prompts, explanations, answers and notes. The broad lexical pass surfaced 248 candidates; that is a retrieval count, not a quality score. I manually read the relevant group: Middle Ages pilgrimage, relic, indulgence, priory and crusade; reverse authorship for the same work; the Camino, Shikoku and Hajj items. The reverse authorship card asks who wrote the Tales and is medium; other route cards test different destinations. The only other exact Canterbury title hit is the unrelated Dudeney puzzle-book question. This is targeted overlap review, not manual review of all 11,000 cards.

## Integrity / next gate

Parsed comparison to the frozen baseline shows only the target explanation changed; catalog order/count, answer texts, notes, difficulty, correctIndex and source metadata are unchanged. A different actual reader must now read the current card and source originals and independently adjudicate it. Prior certification is historical after mutation. The existing unrelated modified `newadvent-rule-benedict.html` was preserved untouched. No tests, builds, publication, merge, push or deploy were performed.
