# Подробные правила проекта

Читай только при триггере из AGENTS.md. Пути в тексте относительно корня проекта.

## Условные процедуры

- Небольшую однозначную правку можно внести напрямую без полного OpenSpec change. Если она меняет правила, опыт игроков или несколько подсистем, считай её нетривиальной.
- Не начинай реализацию, пока необходимое общее понимание не подтверждено; спрашивай только о новых развилках или конфликтах.
- Перед нетривиальным изменением, OpenSpec change, competitive-integrity решением, коммитом или доставкой прочитай [`.agents/references/delivery-workflow.md`](../../../.agents/references/delivery-workflow.md).
- Перед player-visible, input, multiplayer, audio или browser-QA задачей прочитай [`.agents/references/game-qa.md`](../../../.agents/references/game-qa.md).
- Перед делегированием или выбором custom agent прочитай [`.agents/references/model-routing.md`](../../../.agents/references/model-routing.md).
- Перед подключением MCP, плагина или внешнего сервиса прочитай [`.agents/references/external-tools.md`](../../../.agents/references/external-tools.md).
- Для длинной задачи, batch-генерации или после первого compaction прочитай [`.agents/references/context-efficiency.md`](../../../.agents/references/context-efficiency.md).
