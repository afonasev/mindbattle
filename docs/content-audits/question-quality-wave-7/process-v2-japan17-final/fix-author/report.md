# Авторский результат: history-japan-medium-04a-05

- Статус: **FIX**, один разрешённый адресный цикл. Зачёт `0`; авторский пакет не означает применение, независимый PASS или человеческую приёмку.
- Baseline `d0d18ad9a5662a096e0397e56000955849f31a59`; actual CURRENT совпал с beforeCard. Canonical before SHA-256 `506d4560d4de1d3743ffa69a3d0bc6d61fddb2113e1d349dd42f87f14c8e51e8`; proposed after SHA-256 `a0b1816216456446628935d39f2051f94fbd70bdf9107951fa64aeddae81ed12`.
- Изменены только `answers[0].note` и `answers[3].note`. ID/topic/medium/prompt/ответы и порядок/key2/note1/note2/explanation/source сохранены.

## Исправления

- **Синто:** «В геппайчо подхрама Такамуроин на горе Коя зафиксированы посмертные имена людей после синтоистских похорон.»
- **Конфуцианство:** «В геппайчо подхрама Такамуроин на горе Коя зафиксированы посмертные имена людей после конфуцианских похорон.»

Печатная с. 13 (PDF с. 3), раздел “The Proto-Temple Parishioner of Late Medieval Japan”, описывает геппайчо подхрама Такамуроин на горе Коя. Посмертные имена после синтоистских и конфуцианских похорон названы отдельно от dharma names буддийских школ. Заметки называют конкретную серию записей и место; они не приписывают эти имена буддизму в целом.

## Шесть групп

| Group | Status | Proposed canonical JSON SHA-256 |
|---|---|---|
| `prompt_ordered_answers_key` | PASS | `a9d1b0980de1d2de46db0a5cdd40e9c6b429ceb970891ed90f58ba385ed60a93` |
| `explanation` | PASS | `c604bd32ca8b03b5b5f2f5c6979648bf9816d6a972c555dfd6b2d7bb0e153396` |
| `note0` | FIX | `0c8c33ca6000c80c19fdc95a87aa25852c509dc072adac60a4b46bd0279441dd` |
| `note1` | PASS | `ef2bfe167e598b66399044c55ceee2aca117604a582e50bf70a50103e97ec4de` |
| `note2` | PASS | `54724da5bfcf32a2e10b86a47e656eaf73caee265a632116685931c1935a3093` |
| `note3` | FIX | `e996569524ca0ad03346194f1e5aff59c0c13096e3fe97e16ca026f4d9a74157` |

Основания и before hashes всех групп находятся в `candidate.json`. Ключ — печатная с.18/PDF 8 и отчёт pp.18–19; explanation/note2 — pp.19–20/PDF 9–10; note1 — pp.16–17/PDF 6–7; note0/note3 — p.13/PDF 3.

Четыре подстановки проверены: «исповедовавшие синто», «исповедовавшие буддизм», «исповедовавшие христианство», «исповедовавшие конфуцианство» — PASS. Сложность medium и граница `history-japan` сохранены.

Actual CURRENT целиком проверены: тематические карточки из receipt `history-japan-easy-01a-01`, `history-japan-medium-01b-05`, `history-japan-medium-02a-03`, `history-japan-medium-02a-05`, `history-japan-medium-03a-03`, плюс непосредственные соседи каталога `history-japan-medium-04a-04` и `history-japan-medium-04b-01`. Hashes и конкретные отличия приведены в candidate. Пересечений нет; карточки не менялись, зачёт не начислялся.

Сохранённый PDF: 16 страниц, 209666 bytes, SHA-256 `5476fca5d988a7761d4e3107c48c9633154e45e7087e1766a0c42db58ad589fc`; headers SHA-256 `216df2f52291157ec46eac20ac12410d62bdae3bed30817227432341dbe23a8b`. Полный PDF и headers прочитаны из Git-локатора; повторного скачивания не было. Прочитаны `12e5581b:.agents/references/question-revision.md`, GAME_SPEC «Контент вопросов», памятка и taxonomy scope. Проверены frozen-field diff, canonical hashes и лимит notes (≤35 слов). Runtime/build/full tests не запускались. Следующий шаг: координатор применяет patch, независимый читатель проверяет actual CURRENT/hash; остаточный дефект после цикла — HOLD.
