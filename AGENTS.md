# mindbattle — рабочие правила

## Working boundaries

- Preserve scope, product contracts and others' files/processes. Questions/reviews are read-only; create an owned code worktree only before authorized edits when isolation is needed.
- Select minimal affected checks from recorded baseline/diff/dependencies. Full needs separate human approval for this run, even at merge/release. Preserve test contracts and FAIL/NotRun; never infer human/device acceptance from QA.
- Explicit model/effort wins. Authorized new chats: Sol 6.1/medium; bounded work/subagents: Luna/medium or higher. Astra needs a specific complex decision or explicit choice. No implied delegation/message permission.
- Show real visual alternatives before implementation; concepts do not authorize publication.
- Before QA, delivery or finalization read `.agents/references/execution-policy.md`; it includes preservation/cleanup and reporting. Report branch + SHA and integration separately. Read `.agents/references/portability.md` on a new device or missing dependency. Other references below load only on their stated trigger.
- Autonomous games start silent: `-muted`, Unity `-noaudio -muted`, web `?muted=1` before autoplay. Never change system volume; missing support remains an open gate.

- Planning и `docs/GAME_SPEC.md`: единственный shared root — `/Users/eaafonasev/Projects/mindbattle/planning`, профиль `workflow/project.json`, store `mindbattle-planning`; локальный GAME_SPEC — указатель. `planning/` — отдельный Git-репозиторий, игнорируемый Git кода; коммить планы отдельно через `git -C /Users/eaafonasev/Projects/mindbattle/planning`. Кодовые worktree используют этот же root, не создают свои planning-копии. Подробности и совместимость старых путей: `.agents/references/project-policy/planning.md`.

Подробные правила вынесены без отмены требований. Загружай только строку с подходящим триггером; не читай все references при старте и не перечитывай неизменившееся в одном срезе.

| Когда читать | Файл |
|---|---|
| Выбор модели или делегирование | `.agents/references/model-routing.md` |
| Длинная задача, первый compaction, batch или handoff | `.agents/references/context-efficiency.md` |
| Координация нескольких чатов | `.agents/references/coordination.md` |
| Структурный или широкий поиск | `.agents/references/project-policy/search.md` |
| Новые продуктовые решения или изменение spec | `.agents/references/project-policy/specifications.md` |
| При выборе процедуры под тип задачи | `.agents/references/project-policy/conditional-procedures.md` |
| Изменение архитектуры, правил, состояния или asset pipeline | `.agents/references/project-policy/architecture.md` |
| OpenSpec, claim, lifecycle, вопросы или приёмка | `.agents/references/project-policy/planning.md` |
| Нетривиальная реализация, worktree или поставка | `.agents/references/delivery-workflow.md` |
| Релиз, desktop-установщики, GitHub Releases, обновления content/shell или web-deploy | `docs/desktop/RELEASE.md` |
| Player-visible/input/audio/browser QA | `.agents/references/game-qa.md` |

| Выбор required checks по влиянию на контракты | `.agents/references/qa-scope.md` |

## Уточнения workflow по аудиту (решение 2026-10-19)

- Техническую работу можно финализировать с отдельным commit-bound pending deploy. Публикация требует отдельной команды человека; pending deploy остаётся видимым после приёмки и не заменяет поставку зависимости. Контракт helper: `.agents/references/flow/lifecycle.md`.
- READONLY ACK → START обязателен для опасных переходов; обычные поручения внутри действующего разрешённого ownership/scope не требуют двухфазного запуска. Действующие явные session fences сохраняются до отдельного разрешённого перехода. Детали: `.agents/references/flow/efficiency.md`.
- Начинай с компактного актуального manifest и одного проверяемого среза; историю читай по конкретному расхождению. Остановка после второго compaction сохраняется. Детали: `.agents/references/context-efficiency.md`.

- Координатор выполняет детерминированную сверку evidence; содержательные правки возвращаются текущему reviewer для направленного FINAL. Дополнительный эксперт — только для оставшегося конкретного содержательного спора. Третья полная ревизия запрещена; детали и ограничения pinned process: `.agents/references/flow/efficiency.md`.
