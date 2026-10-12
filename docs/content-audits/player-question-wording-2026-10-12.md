# Правки формулировок по статистике игроков — 12 октября 2026

Baseline: `a898df6be891d6c75e0d83e083ba62d375e60fd3`.

Исправлены только условия четырёх вопросов:
- `archaeology-refit`: вопрос о названии метода вместо вопроса о выводе.
- `linguistics-writing-isolate`: законченное условие о классификации баскского языка.
- `folklore-fairy-tales-propp-donor`: ситуация с просьбой поделиться едой вместо определения, подсказывавшего ответ.
- `ancient-world-lunar-month`: длительность около 29,5 суток вместо слов «месяц» и «новолуние».

Ответы, правильные индексы, сложности, ID, объяснения и источники сохранены. SHA256 review-манифестов обновлены; узкие поправки и авторская проверка записаны отдельно от исторического независимого review.

Проверки: typecheck; 20/20 affected Vitest tests (catalog-topics, catalog-full, content, content-answer-notes); повтор catalog-full после оформления manifests — 1/1; точное сравнение остальных полей карточек; diff check.

Три исторических editorial gate (legacy answer integrity, reviewed prefix, baseline wrong notes) падают с побайтно одинаковым выводом на baseline и candidate. Их ошибки не исправлялись и не скрывались.

Evidence: `/Users/eaafonasev/Projects/mindbattle-planning/evidence/player-question-wording-2026-10-12/`.

Фактическая основа: [Пропп, оригинальная работа](https://web.mit.edu/allanmc/www/propp.pdf), [NASA: synodic month](https://eclipse.gsfc.nasa.gov/SEhelp/moonorbit.html), [Ben-Gurion University: lithic refitting](https://www.bgu.ac.il/en/researcher/ronen-brafman/computational-flint-refitting-project/). Проверяемые факты и правильные ответы не изменены.

Сборка, browser/device acceptance, полный набор тестов, desktop-публикация и web-deploy не выполнялись. Изменение данных не меняет layout, управление или механики.
