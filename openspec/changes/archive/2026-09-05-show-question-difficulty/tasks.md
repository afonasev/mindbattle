## 1. Presentation implementation

- [x] 1.1 Добавить единый formatter `easy`/`medium`/`hard` → «Лёгкий»/«Средний»/«Сложный» и убедиться, что он не меняет доменное состояние или payload фидбэка.
- [x] 1.2 Добавить скобочную сложность после счётчика в шапки вопроса командной партии и соло-забега; проверить, что question/answer остаётся визуальным центром.
- [x] 1.3 Добавить назначенную сложность на общий и одиночный экраны фидбэка, включая состояние повторной отправки; проверить, что она соответствует текущему round.

## 2. Automated verification

- [x] 2.1 Дополнить UI-тесты для командного easy-вопроса, hard tie-break feedback, соло medium-вопроса и hard feedback; запустить `npm run typecheck` и `npm test -- --run`.

## 3. Target-environment verification

- [x] 3.1 В muted in-app Chromium проверить командный вопрос, соло-вопрос и feedback при 1280×720, сохранить три PNG в evidence-папку, подтвердить их наличие и визуально проверить читаемость.
- [x] 3.2 Сверить `docs/GAME_SPEC.md` с реализацией и change artifacts, выполнить `openspec validate show-question-difficulty --strict`, затем записать краткое доказательство проверок.

## Доказательство проверок

- `npm run typecheck` и `npm test -- --run`: 128 тестов прошли.
- `npm run build`: production bundle собран.
- Playwright Chromium 1280×720: командный вопрос и feedback, соло-вопрос и feedback прошли; PNG сохранены в `evidence/show-question-difficulty/`.
- `openspec validate show-question-difficulty --strict` и `git diff --check`: прошли.
