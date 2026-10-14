# Первый пакет нового процесса: Physics12

2026-10-14. Возобновление пользователем в чате 01a13b21-6800-7843-9ab6-f255503aafda.
Baseline: ветка codex/question-quality-wave-6, 9b2b0b1a225b2970e916c023b35986e0449e4d31.
Сохранённые авторские предложения взяты из codex/question-review-process, 6091195e.

Итог: **7 CURRENT PASS, 5 HOLD**, один адресный fix-cycle.
Зачёт выбранного scope: **590/2000**, осталось1410; wave7:90/500.
Это source/editorial результат на feature, не human acceptance, merge или deploy.

Прошли:

- physics-gravity-direction
- physics-magnet-like-poles
- physics-friction-effect
- physics-water-freezing
- physics-closed-circuit
- physics-sound-loudness
- physics-ext-debroglie-wavelength

Остались HOLD; в игровом JSON восстановлен baseline:

| ID | Что требуется перед новой попыткой |
|---|---|
| physics-ice-state | Подтверждённая справка для полноценного четвёртого варианта той же категории. |
| physics-metal-conductor | Источники для самостоятельных справок о материалах; сохранить исходный смысл и frozen easy. |
| physics-gas-volume | Самостоятельные notes1/3, без служебных отсылок и повтора ключа; правдоподобные дистракторы. |
| physics-light-vacuum | Note2 должна относиться к утверждению о распространении света в веществе, с точным источником. |
| physics-ext-entropy-disorder | Подтвердить определения КПД, дифференциальную формулу энтропии и холодный резервуар либо не включать неподтверждённые факты. |

## Доказательства и проверки

- manifest.json: точные12preimages, исходные proposals и ссылки на сохранённого автора.
- independent-review.json: первое независимое чтение12, результат0PASS/12HOLD.
- author-fix.json: один адресный цикл другого автора;10FIX/2HOLD.
- independent-rereview.json: завершающее чтение изменённых10, результат7PASS/3HOLD.
- adjudication.json: решение координатора, точные текущие hashes, восстановление5HOLD.
- qa-initial.json:18PASS/1FAIL, выявлены однофразовые explanations.
- qa-final.json:19PASS/0FAIL/0pending после всех восстановлений; финальный SHA topic в adjudication.json.

Запуск: node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts
tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json
--outputFile=docs/content-audits/question-quality-wave-7/process-v2-physics12/qa-final.json

Проверены существующие контракты схемы, глобальной уникальности ID, выбора вопросов и notes.
Отдельно подтверждены exact7diff и неизменность всех100ID/order/key/difficulty темы.
Полные тесты, typecheck (TS не менялся), browser, build, installers и deploy не запускались.
Проверки выполнялись в Node без игровых/audio процессов.
Памятка автора синхронизирована с существующим canonical правилом добавочного факта correct-note.

Промежуточный успешный QA-отчёт и служебные логи удалены после финального прогона.
Shared index, чужие файлы и остальные карточки не исправлялись.
Первичные материалы используются по прежним Git locators, без новых raw-копий.

## Продолжение

Не повторять ревизию прошедших7 или прежних583 при неизменных hashes.
Следующий ограниченный пакет:10 из сохранённых45Weather-кандидатов, сначала сверить preimages.
Эти5HOLD не гонять по третьему кругу без конкретного нового источника/решения.
Автор и независимый читатель должны читать canonical GAME_SPEC, раздел «Контент вопросов»,
вместе с памяткой до начала работы.
