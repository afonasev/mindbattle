## 1. Контракты и миграция состояния

- [x] 1.1 Ввести discriminated feedback schema v1/v2, перечисления сложности, отношения и флагов; проверить unit-тестами допустимые/недопустимые payload и отсутствие teamId в v2 event.
- [x] 1.2 Расширить serializable `difficulty-feedback` phase независимыми анкетами active teams и snapshot schema v2; добавить сохраняемый default-on `collectQuestionFeedback`; проверить round-trip, повреждённый snapshot и legacy v1 snapshot с pending retry.
- [x] 1.3 Реализовать domain-команды выбора, подтверждения и блокировки анкеты; проверить deterministic обработку разных команд в одном frame, invalid input, completed team, pause/resume и tie-break со зрителями.

## 2. Ввод и интерфейс

- [x] 2.1 Сопоставить keyboard/gamepad directional press с последовательными шагами фидбэка и per-source neutral gates; проверить adapter-тестами четыре схемы, holding и keyboard repeat.
- [x] 2.2 Реализовать DOM/CSS-экран параллельного фидбэка с отдельной карточкой active team, прогрессом и статусом готовности без раскрытия выбора соперникам; добавить в нижний раздел «Настройки» перед стартом default-on флаг «Собирать обратную связь по вопросам»; проверить component/UI-тестами все шаги и locked completed card.
- [x] 2.3 Проверить экран фидбэка с крупным текстом, повышенным контрастом и отключёнными анимациями; приложить browser screenshots 1280×720 и 1920×1080.

## 3. Локальная запись и аналитика

- [x] 3.1 Обновить controller и client sink для единственного v2 event после completion barrier; при выключенном флаге не создавать event и не вызывать sink; проверить success, error, retry с тем же eventId и сохранённый ответ без teamId.
- [x] 3.2 Обновить local API/NDJSON writer для валидации и идемпотентного хранения v1 и v2; проверить create, duplicate, conflict, malformed input, mixed legacy journal и failure write.
- [x] 3.3 Расширить read-only summary отдельными v1/v2 агрегатами сложности, similarity, flags и `unfamiliar-topic`; проверить пустой, повреждённый и смешанный журнал и отсутствие автоматической переклассификации.

## 4. Сквозная проверка и документация

- [x] 4.1 Синхронизировать `docs/GAME_SPEC.md` с реализованными labels, flow, privacy-моделью и journal entry; проверить поиском отсутствие описаний одного общего выбора в актуальных разделах.
- [x] 4.2 Выполнить Playwright flow обычного, бонусного и tie-break-вопроса: две или более команд параллельно проходят разные анкеты, готовая команда заблокирована, ошибка API повторяется тем же eventId; отдельно проверить отключённый флаг без API-вызова; в hotfix/browser flow выключать флаг явно; сохранить актуальные screenshots с выключенным звуком.
- [x] 4.3 Провести реальный локальный плейтест минимум двух команд с разными назначенными схемами keyboard/gamepad, подтвердить одновременный ввод и отсутствие раскрытия конкретных ответов; зафиксировать краткое свидетельство результата: ручной плейтест подтверждён пользователем 2026-09-04.
- [x] 4.4 Выполнить typecheck, unit tests, production build, `openspec validate expand-independent-question-feedback --strict`, `git diff --check` и review точного staged scope перед отдельным change-коммитом.
