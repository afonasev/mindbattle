# mindbattle — рабочие правила

## Working boundaries

- После публикации удаляй локальные копии релиза, как только проверишь скачивание тех же артефактов из канала поставки. Когда новая локальная тестовая сборка готова к проверке, удали предыдущие версии для той же платформы и сценария. Подробности в [правилах хранения сборок](.agents/references/execution-policy.md#хранение-игровых-сборок).

- При многоэтапном игровом срезе читай `.agents/references/initiative-execution.md`: один ответственный за цельный результат, автономный причинный ремонт и проверки по diff/зависимостям; явные человеческие ограничения сохраняются.

- Preserve scope, product contracts and others' files/processes. Questions/reviews are read-only; create an owned code worktree only before authorized edits when isolation is needed.
- QA и границы автоматической/человеческой приёмки: [execution-policy.md](.agents/references/execution-policy.md); выбор affected-команд: [qa-scope.md](.agents/references/qa-scope.md).
- Модели и разрешённое делегирование: [model-routing.md](.agents/references/model-routing.md); явный выбор пользователя приоритетен.
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

- Commit-bound pending deploy и отдельная публикация: [.agents/references/flow/lifecycle.md](.agents/references/flow/lifecycle.md).
- READONLY ACK → START, сохранение session fences, детерминированная сверка, направленный FINAL и запрет третьей полной ревизии: [.agents/references/flow/efficiency.md](.agents/references/flow/efficiency.md).
- Компактный manifest, активный handoff и остановка после второго compaction: [.agents/references/context-efficiency.md](.agents/references/context-efficiency.md).

## Ревизия вопросов: обновление процесса 2026-10-25

Для exact2000 и редакторского конвейера читать [question-review-process.md](.agents/references/question-review-process.md). Эта явно разрешённая редакция заменяет противоречащие процедурные bootstrap/task дополнения для новых поручений после текущего атомарного результата. Содержательные gates, исторические HOLD/FAIL, ownership и ограничения публикации сохраняются. Не восстанавливать отменённые exact-four/whole-tool-output аудиты через handoff.

## Changelog для деплоя (решение пользователя 2026-10-25)

- Changelog для каждого деплоя/релиза оформляй по категориям маркированными списками: одно самостоятельное изменение — один пункт; не объединяй изменения категории в сплошной абзац. Для наглядных изменений прикладывай реальные скриншоты соответствующей версии рядом с пунктами, где это возможно и формат поддерживает изображения; добавляй краткие подписи и доступные читателю пути/ссылки. Если изображения не поддерживаются, давай ссылки на скриншоты. Скриншоты дополняют текст и не заменяют описание изменений.

- С 2026-11-10. Сравнивай баланс с предыдущей опубликованной версией того же канала и указывай её номер. Для первого выпуска явно обозначь отсутствие предыдущей версии. Каждый изменённый численный параметр описывай отдельным пунктом с названием, значениями «было → стало» и единицей измерения. Для нового или удалённого параметра обозначь отсутствующее значение. Для изменения правила без чисел опиши прежнее и новое поведение. Сверяй полноту и значения по фактическому содержимому обоих выпусков.
- В большом патче сначала вынеси самые важные для игроков пункты в «Главное для игроков», затем перечисли оставшиеся изменения по категориям в разделе «Всё остальное». В локализациях сохраняй одинаковые значения, состав и порядок пунктов.
