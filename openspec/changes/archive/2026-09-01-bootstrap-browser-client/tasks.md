## 1. Runtime и конфигурация

- [x] 1.1 Создать npm manifest, lockfile, TypeScript/Vite/Vitest/Playwright конфигурации и проверить успешную установку зависимостей.
- [x] 1.2 Добавить команды `dev`, `typecheck`, `test`, `build`, `test:browser` и `check`; проверить, что каждая команда запускается и возвращает диагностируемый exit code.

## 2. Архитектурная основа

- [x] 2.1 Создать typed entrypoints `domain`, `application`, `adapters`, `ui`, `content` и проверить ожидаемую структуру файлов.
- [x] 2.2 Добавить автоматическую architecture-проверку запрета React/DOM/browser imports из `domain` и подтвердить её прохождение в Vitest.

## 3. Browser shell

- [x] 3.1 Реализовать React DOM/CSS shell Mindbattle в тёмном направлении интеллектуальной телеарены и проверить доступное название страницы и ясное основное действие.
- [x] 3.2 Проверить читаемую 16:9-композицию при 1280×720 и 1920×1080, отсутствие runtime-сетевых запросов к внешним сервисам и сохранить актуальные скриншоты.

## 4. Проверка и завершение

- [x] 4.1 Добавить Playwright smoke на загрузку shell без page errors и выполнить его в реальном Chromium; отдельно зафиксировать, что multiplayer/controller playtest не применим к bootstrap без игровых правил и ввода.
- [x] 4.2 Выполнить `npm run check`, `openspec validate bootstrap-browser-client --strict`, `git diff --check` и сверить реализацию с актуальными разделами `docs/GAME_SPEC.md`.
- [x] 4.3 Обновить checklist фактическими отметками, проверить точный staged scope и подготовить краткое evidence для отдельного verify-этапа.
