## Context

Репозиторий содержит утверждённую `docs/GAME_SPEC.md` и OpenSpec workflow, но не содержит package manifest или исходного приложения. См. `proposal.md` — Why. Основа должна работать на одном общем desktop Chromium-экране, оставаться offline-first и не закреплять игровые правила преждевременно.

## Goals / Non-Goals

**Goals:**

- Создать минимальный React/TypeScript/Vite runtime и production build.
- Зафиксировать расширяемые границы модулей до появления игрового ядра.
- Дать визуально осмысленный DOM/CSS shell, пригодный для screenshot и browser-smoke проверки.
- Создать быстрый единый check для последующих changes.

**Non-Goals:**

- Реализация match state, таймеров, scoring, tie-break или выбора вопросов.
- Физическая маршрутизация WASD, стрелок и геймпадов.
- Загрузка полного контентного каталога, persistence партии, звук и Steam/PWA packaging.

## Decisions

### React + TypeScript + Vite без игрового renderer

Приложение использует React для экранов, TypeScript для contracts и Vite для development/build. UI остаётся в DOM/CSS, потому что основная информация текстовая и должна поддерживать масштабирование, контраст и browser accessibility. Phaser, canvas и WebGL не добавляются: они увеличивают стоимость текстового UI и тестирования без игрового преимущества.

### npm и зафиксированный lockfile

Зависимости устанавливаются через npm, а lockfile входит в репозиторий. Это делает local/CI checks воспроизводимыми и не требует дополнительного package manager.

### Границы исходных каталогов

`src/domain` владеет будущими сериализуемыми правилами и не импортирует browser/UI modules. `src/application` будет оркестрировать команды и часы. `src/adapters` будет содержать input/storage/audio adapters. `src/ui` владеет React views и theme. `src/content` станет entrypoint статического каталога. Bootstrap создаёт минимальные entrypoints и автоматическую architecture-проверку, но не подменяет будущие contracts заглушечными правилами.

### Тестовая пирамида

Vitest выполняет быстрые unit и architecture checks. Playwright открывает реальную страницу в Chromium для smoke-проверки. Полный физический controller playtest остаётся обязательным для будущего input change и не имитируется bootstrap smoke-тестом.

### Статические локальные assets

Production build содержит только локальные assets. Кириллический variable-шрифт Onest поставляется через пакет `@fontsource-variable/onest` и собирается Vite в локальные font assets; системный sans-serif остаётся только аварийным fallback. Это выполняет offline-first требование и сохраняет лицензионное происхождение зависимости проверяемым через lockfile.

## Risks / Trade-offs

- [Playwright может потребовать отдельной загрузки Chromium] → использовать установленный browser при наличии, а отсутствие binary явно отделять от unit/build результата.
- [Пустые каталоги не сохраняются Git] → добавлять небольшие typed entrypoints с архитектурными комментариями, а не `.gitkeep`.
- [Стартовый shell может быть принят за готовую игру] → явно маркировать его как foundation и не заявлять игровую готовность до следующих changes.
- [Fallback-шрифты могут отличаться при ошибке загрузки Onest] → smoke проверяет отсутствие внешних запросов, а production build содержит локальный font asset.

## Migration Plan

1. Добавить package/config files и установить lockfile.
2. Добавить module entrypoints и React shell.
3. Добавить unit, architecture и browser smoke checks.
4. Проверить production build и текущий desktop Chromium.
5. При rollback удалить только новые runtime/config/source files; `docs/GAME_SPEC.md` и существующий OpenSpec workflow остаются источниками решений.
