# Проверки ограниченного среза

Baseline: e717b9f (independent23); фактический исходный card-games сохранён в baseline-topic.json.
Изменение: только семь справок и три source в 13 разрешённых карточках; правила приложения не меняются.

Минимально достаточные команды:
- python3 verify-proof-format.py author13.json --repo <repo> --output author13-roundtrip.json: 13 current-card hashes, 78 literal hashes, существование и точность passages. Не фактический PASS.
- npm run typecheck: импорт JSON и типы каталога.
- npx vitest run tests/unit/content-answer-notes.test.ts tests/unit/catalog-topics.test.ts tests/unit/catalog-full.test.ts --reporter=json --outputFile=<evidence>/focused-content-tests.json: контракт notes/источников, валидность пакетов и действующий review-stamp gate. Это ограниченный content набор, не полный suite. Последний gate может оставаться красным на ещё не сертифицированных темах; валидатор и stamps не меняются.
- preservation-check.json: сравнение с baseline, unchanged87, IDs/order/difficulty/correctIndex, 40/40/20 и позиции10/10/5, hashes разрешённых13.

Full suite, npm run check/qa, browser, build, deploy, release и archive не выполняются. Root certification требует нового independent full6 по каждой из13.
