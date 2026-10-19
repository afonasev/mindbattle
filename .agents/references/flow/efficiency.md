# Context, models and budgets

No always-running coordinator. Humans choose worker-session count. Use GPT-6 Sol at medium effort as the default implementation model. Use GPT-6 Luna for bounded, well-understood tasks with clear expected results. Use GPT-6 Astra for architecture, complex debugging, material AI/contract uncertainty, or an explicit user request. Explicit model choice wins. Validate model availability; keep these as project preferences rather than a project-level model pin, and do not change credentials or approvals.

Delegate only when explicitly requested or applicable instructions authorize a concrete independent subtask. No blanket delegation requirement. Send minimum scope/spec revision/files/checks, not full discovery history. Parent owns acceptance of returned evidence. Batch only related small changes sharing context/checks, retain separate lifecycle records.

Start focused checks; run required full checks at integration and rerun only for changes/failures. After two unsuccessful attempts reassess approach/model/scope rather than loop. Use configured budgets when present; do not invent a token budget. Log usage externally reported by runtime with unknown fields null. Separate worker, review and coordination costs, cached and uncached input. Optimize accepted-result cost and rework, not just cheapest model per call.

Keep detailed logs outside conversation. Save compact handoff at context pressure: scope, revisions, verified facts, next checks, resources, questions. Replace a saturated session without dropping ownership or restarting completed work. Future runner must use same transitions, locks and evidence contracts.

## Default bounded work and waiting

Use GPT-6 Luna/medium for clear bounded development tasks. Explicit model/effort choices win; never use Luna below medium. Default subagent preferences are not a session-wide model pin.

For multi-chat coordination wait for completion/required-action events with wait_threads timeoutMs 120000 and saved afterCursor for each target. Unchanged timeout is not a reason for read_thread or a status message. Respect tool yielding and current interaction limits. After the second compaction finish only the current verifiable slice, required checks and handoff; do not start the next slice in the saturated session. New chats and messages still require the existing user authorization.


## ACK → START только для опасных переходов (решение 2026-10-19)

Обычная задача в уже разрешённом scope при неизменных ownership, revision и границах записи запускается напрямую. Отдельный READONLY ACK → START нужен для смены/восстановления ownership или lease, перехода из явно read-only scope к записи, изменения authority/schema/pinned process либо другого конкретно названного опасного перехода. READONLY ACK фиксирует идентичность, revision, разрешённые пути и ограничения; START разрешает ровно этот переход после сверки. ACK сам по себе не разрешает запись и не доказывает качество.

Явные действующие READONLY BOOTSTRAP ONLY, preservation-only и запреты конкретных сессий не снимаются общим правилом: сначала отдельный разрешённый переход с согласованием актуальной revision и ownership. Не переписывай immutable pinned artifacts и историю задним числом. Публикация, destructive cleanup и расширение scope сохраняют собственные требования к авторизации; ACK/START их не заменяет. Новые чаты и сообщения другим чатам по-прежнему требуют авторизации пользователя.

Для компактного manifest и ограниченного среза используй context-efficiency.md. Не меняй текущую независимую содержательную проверку: политика третьей оценки ещё обсуждается.
