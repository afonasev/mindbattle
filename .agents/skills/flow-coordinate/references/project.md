# Профиль: mindbattle

Пути ниже — от корня code-репозитория. Сначала прочитай актуальный `AGENTS.md`; профиль не содержит команды на запуск исторической инициативы или разрешения на публикацию.

- Это игровой проект. Канонические planning_root/store и main_branch разрешай из `workflow/project.json`. Не копируй planning в каждый code worktree.
- Используй существующие `flow-explore`/`flow-apply`/`flow-inbox` и `.agents/references/flow/initiative.md`. N/M считай по уникальным обязательным конечным задачам текущей инициативы; техническую готовность отделяй от human acceptance.
- QA выбирай по `.agents/references/qa-scope.md` и diff/зависимостям. Полный игровой набор — только с отдельным явным разрешением на этот прогон. Команды в workflow-профиле — кандидаты для проверки маршрута, не автоматический gate.
- Browser/Player QA — по проектным game-qa правилам, тихо с самого старта (`?muted=1` до autoplay). Release/deploy требует отдельной команды; N=M его не разрешает.
- При question-quality следуй действующему pinned процессу и `.agents/references/flow/efficiency.md`. Автор и независимый reviewer сохраняют свои роли; координатор сверяет комплектность/версии/evidence, без третьей полной ревизии. Явные READONLY/START/STOP fences и exact source/ID contracts сохраняются. Группируй поставку по связанному целому результату, отдельный HOLD не задерживает независимую готовую работу.
- Перед интеграцией/cleanup используй `.agents/references/project-policy/planning.md` и применимые delivery/git правила; человеческая приёмка и её evidence независимы от технического счётчика.
- Перед финализацией читай `.agents/references/execution-policy.md`; отчёт содержит branch + SHA и отдельно проверенный факт интеграции. Очищай только собственные временные ресурсы после сохранения.
