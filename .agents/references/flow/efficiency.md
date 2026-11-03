# Context, models and budgets

No always-running coordinator. Humans choose worker-session count. Model/effort, availability, authorization and bounded delegation: [model-routing.md](../model-routing.md). These are preferences, not a session-wide pin; do not change credentials or approvals. Batch only related small changes sharing context/checks, retaining their lifecycle records.

QA selection, repeat conditions and human/device boundaries: [execution-policy.md](../execution-policy.md) and [qa-scope.md](../qa-scope.md). After two unsuccessful attempts reassess approach/model/scope rather than loop. Use configured budgets; do not invent one. Log runtime-reported usage with unknown fields null; separate worker/review/coordination and cached/uncached costs. Optimize accepted-result cost and rework.

Compaction, active handoff and replacement ownership: [context-efficiency.md](../context-efficiency.md). Event waits, cursors and reusable tool calls: [coordination.md](../coordination.md). Future runners retain the same transitions, locks and evidence contracts.

## ACK → START только для опасных переходов (решение 2026-10-19)

Обычная задача в уже разрешённом scope при неизменных ownership, revision и границах записи запускается напрямую. Отдельный READONLY ACK → START нужен для смены/восстановления ownership или lease, перехода из явно read-only scope к записи, изменения authority/schema/pinned process либо другого конкретно названного опасного перехода. READONLY ACK фиксирует идентичность, revision, разрешённые пути и ограничения; START разрешает ровно этот переход после сверки. ACK сам по себе не разрешает запись и не доказывает качество.

Явные действующие READONLY BOOTSTRAP ONLY, preservation-only и запреты конкретных сессий не снимаются общим правилом: сначала отдельный разрешённый переход с согласованием актуальной revision и ownership. Не переписывай immutable pinned artifacts и историю задним числом. Публикация, destructive cleanup и расширение scope сохраняют собственные требования к авторизации; ACK/START их не заменяет. Новые чаты и сообщения другим чатам по-прежнему требуют авторизации пользователя.

## Граница сверки и содержательной оценки (решение 2026-10-19)

- Координатор детерминированно сверяет ID, hashes/revisions, schema и обязательные поля, frozen key/difficulty/order, привязку источников и independent verdict к точному CURRENT. Сверка literal/locator подтверждает идентичность и наличие evidence, но не истинность вывода из источника. Независимая содержательная оценка сохраняется.
- Содержательная правка после ревью возвращается текущему независимому reviewer для направленного FINAL по изменённому тексту и затронутому контексту. Существующие содержательные расхождения сначала проходят тот же направленный цикл.
- Дополнительный эксперт нужен только для оставшегося неразрешённого спора: о следствии из источника, однозначности ответа либо конфликте содержательных заключений автора и reviewer. Поручение фиксирует конкретный вопрос, точную revision, спорный фрагмент и необходимый контекст; арбитраж заканчивается мотивированным ответом на этот вопрос.
- Третья полная ревизия карточки, пакета или неизменившегося evidence запрещена. Точечный арбитраж допускается только в рамках действующего разрешённого процесса; при конфликте с pinned process сначала требуется отдельное решение человека. Не переписывай immutable pinned artifacts, действующие ownership и session fences. Одобрение этой политики само по себе не разрешает создавать чаты/подагентов или отправлять им сообщения.

## Редакция процесса вопросов 2026-10-25

Для exact2000 действует явное решение пользователя в [question-review-process.md](../question-review-process.md): компактные пакетные поручения и технические проверки без ручного аудита формы каждого вызова. Оно разрешает описанный там переход после текущего атомарного результата и заменяет противоречащие старые процедурные дополнения. Исторические artifacts, quality gates и исчерпанные циклы остаются неизменными; повторное согласование уже разрешённого перехода не требуется.
