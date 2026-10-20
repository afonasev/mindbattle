# Компактная форма SOURCE-пакета

Это точная форма уже действующих six/four/source/peer требований, а не новая процедура приёмки. Для знакомства со схемой не печатать целиком старые candidate/sourceproof/peer-snapshot. Смысловые основания автор пишет сам; поля и hashes формирует инструментом. Никаких автоматически выставленных PASS.

Три файла: `candidate.json`, `sourceproof.json`, `peer-snapshot.json`. В каждом — один и тот же фактический `sourceNativeId`, `topicId`, `cycle`, ID карточки. Native ID подтверждается coordinator по реальному session_meta, а не копируется из task owner. До START никаких записей.

## Хэши: три разных представления

```python
def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False,
        sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def body_sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
```

- Карточка, literal (включая строку), triple и rows: `canonical_sha`.
- Файл: `file_sha`. Не путать с хэшем содержимого строки внутри JSON.
- Полный original tool body, извлечённый по JSON Pointer: `body_sha`. JSON-кавычки и escaping в этот hash не входят.
- Никогда не переписывать hex вручную и не копировать hash между разными представлениями.

## Candidate

`entries[0]` содержит `id`, `topicId`, `sourceOrder`, `status`, `beforeCard`, `beforeHash`, `proposedCard`, `afterHash`, `fieldGroups`.

`status` — `READY_FOR_INDEPENDENT_REVIEW` либо точный `HOLD`; quality credit всегда0. Before — действительный preimage текущего назначения. Frozen ID/topic/order/difficulty/numeric key проверить по selection. Labels не заморожены глобально; править хороший текст без конкретного дефекта нельзя.

Использовать только dict-форму `fieldGroups`: ровно шесть ключей, каждый с вычисленными `beforeCanonicalSHA256` / `afterCanonicalSHA256`:

```python
def groups(card):
    return {
      'prompt_ordered_answers_key': {
        'prompt': card['prompt'],
        'answers': [a['text'] for a in card['answers']],
        'correctIndex': card['correctIndex']},
      'explanation': card['explanation'],
      **{'note'+str(k): a['note'] for k,a in enumerate(card['answers'])}}
```

## Sourceproof

`rawSources[]`: `path`, `url`, `sha256` (реальный file SHA), `captureReadProvenance`, `locator`. Для JSON-container также `completeOutputPointer` и `completeOutputSHA256` (= body SHA). Для общего capture перечислить все реальные URL/locators; не терять их из-за одинакового file path.

`path` — только существующий устойчивый файл. Не `journal item N`, не `file#pointer`, не URL. JSON Pointer хранится отдельным полем. Новый raw сохранять один раз отдельным файлом до создания packet; не делать self-hash текущего sourceproof. Сохранённые immutable full contexts переиспользовать по file/pointer, не копировать в каждый packet.

`entries[0].literalGroups[]`: ровно шесть объектов `group`, `literal`, `literalSHA256`, `primaryGround`, `sourcePaths`, `locator`. Literal — фактическое значение из `groups(proposedCard)`. PrimaryGround объясняет конкретный вывод, границы и qualifiers из полного первичного контекста, а не наличие ссылки.

`fourFullPromptAnswerNoteAssessments[]`: слоты0..3, каждый содержит `fullPrompt`, `answer`, `note`, `tripleSHA256`, `grammar`, `plausibilityUniqueKeyAndNoteTruthUsefulness`, `sourcePaths`, `locator`.

Triple = `{'prompt': fullPrompt, 'answer': answer, 'note': note}`. SourcePaths — голые file paths из rawSources; конкретный JSON Pointer/строки остаются в locator. В оценке явно обосновать грамматику, правдоподобие и единственность ключа, истинность и полезность справки именно для этого варианта. Истинный соседний тематический факт сам по себе недостаточен.

Отдельно `correctNoteNewFact` и `absoluteDifficulty` с конкретным собственным основанием. Факт правильной справки — сверх всего prompt/key; совпадение с explanation само по себе не запрет. Source presence/посещаемость/относительное сравнение не доказывают EASY.

## Peer snapshot

- `globalMAIN`: 110 file bindings, 11000 rows; row shape строго `{topicId,id,prompt,answers:[четыре text],correctIndex}`, sorted topic filenames / исходный порядок вопросов. `rowsCanonicalSHA256` считается инструментом. Указанные file hashes должны соответствовать записанной текущей версии на момент передачи.
- Все100 текущих карточек темы сохранять инструментом, не печатать их целиком только ради формата. `actualCurrentPeers` — полные актуальные body/hash/id/topicId для peer bindings.
- Релевантные ближайшие карточки действительно читать целиком. Для каждой смысловой пары — конкретные entity/relation/value/context в обе стороны и direct reverse check. Лексический hit сам по себе не дубль; self-preimage binding не ещё один DISTINCT peer.
- Новое изменение в другом потоке требует только машинного refresh inventory и проверки действительно затронутых смысловых связей. Не читать неизменный каталог повторно; не называть старые file bindings свежими. Использовать точный questionId изменённой карточки, не угадывать его по номеру или первому hit.

## Передача

Одна законченная карточка на содержательный цикл. READY передать с конкретными границами/HOLD, без запроса GO на каждый патч. Никаких catalog/Git/planning/QA/других чатов со стороны SOURCE-автора. После первой compaction закончить начатый срез, после второй — preservation STOP. Зачёт даёт только точный независимый PASS + required affected QA + coordinator binding.
