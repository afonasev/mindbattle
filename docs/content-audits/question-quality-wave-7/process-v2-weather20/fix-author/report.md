# Авторский fix-cycle 13: погода и климат

Baseline: `dd091c9838678996a7aa6b5063f5c4199e2ff99e`. Ровно 13 ID: 11 FIX, 2 HOLD. ID, topic, порядок позиций ответов, difficulty и correctIndex сохранены; keyed satellite answer уточнён в той же позиции. Хэши карточек и шести literal-групп рассчитаны как sorted compact UTF-8 JSON с Unicode.

## FIX

- `weather-climate-cin-cap` — FIX. Заметка ключа добавляет единицу измерения; SRH дан по отдельному SPC shear context, формулировки русские.
- `weather-climate-cold-front-symbol` — FIX. Заметка ключа добавляет плотность воздуха; описание дождя и грозы ограничено влажностью/неустойчивостью.
- `weather-climate-desert-dry` — FIX. Вопрос о субтропической циркуляции, не об определении группы B Кёппена; полярный и горный соседи проверены.
- `weather-climate-lifted-index` — FIX. Удалено необъяснённое английское слово; знак разности задан корректно по SPC, а SRH переведён на русский.
- `weather-climate-occluded-front` — FIX. Справка холодного фронта описывает вытеснение тёплого воздуха без ошибочного отношения погони.
- `weather-climate-polar-cold` — FIX. Сохранён вопрос о центральной Антарктиде; note2 использует проверенный пример холодной пустыни Гоби, а не Антарктиды.
- `weather-climate-polar-easterlies` — FIX. Вопрос проверяет связь с полярной ячейкой без называния ключа или направления; note3 добавляет независимый факт.
- `weather-climate-satellite-clouds` — FIX. Уточнён тип геостационарного метеоспутника; вопрос остаётся про наблюдение облаков и не повторяет космический вопрос.
- `weather-climate-stationary-front` — FIX. Убрано неподтверждённое обобщение об осадках; объяснение опирается на баланс масс из NWS.
- `weather-climate-stratus-layer` — FIX. Справка ключа добавляет связь тумана с приземной формой слоистых облаков.
- `weather-climate-westerlies-midlat` — FIX. Справка больше не повторяет оба признака вопроса; соседние пояса и высотное течение различены.

## HOLD

- `weather-climate-bergeron-ice` — NWS glossary body сообщает об отсутствии совпадений для aggregation; сохранённый AMS alternate — страница перенаправления/Cloudflare, не определение. Следующее действие: только полный первичный capture, уже доступный локально, либо adjudication замены дистрактора; повторный поиск в этом цикле не выполнялся.
- `weather-climate-warm-cloud-collision` — механизм тёплого дождя подтверждаем, но aggregation distractor остаётся неподтверждённым; тот же конкретный next action. Оба HOLD не блокируют 11 FIX.

## Проверки и границы

Прочитаны сами сохранённые primary bodies; новые источники не скачивались и body не дублировались. Полные Met Office и NOAA JetStream body/headers уже находятся в `author/sources/`; для остальных capture сохранены Git body/blob, byte count и SHA. Для CIN/LI использован отдельный SPC shear body. Reviewed verdicts не наследовались: читались тексты карточек соседей в baseline catalogue.

Выполнены только JSON-format, canonical-hash и frozen-field проверки. Не запускались full tests, build или runtime. Это авторский результат, не CURRENT independent review и не приёмка. Каталог, индекс, claims, commit и foreign paths не менялись.
