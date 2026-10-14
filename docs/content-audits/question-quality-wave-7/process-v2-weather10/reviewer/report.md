# Независимая проверка CURRENT Weather 10

Reviewer: `01a13b89-56e0-7661-a8d3-88b67254735f`. Baseline `31aa848b`, рабочая ветка `codex/question-quality-wave-6`. Проверены только 10 ID из exact-apply.json: русский prompt, все четыре подстановки/ключ, explanation, четыре notes, реально прочитанные первичные контексты, абсолютная сложность, дистракторы и CURRENT тематических соседей. Старые авторские оценки не использованы. Старый packet прочитан только для primaryContextIndex и схемы literal групп.

**PASS (4):** cape-buoyancy, trough-elongated-low, ridge-elongated-high, jet-stream-fast. Полные ID и точные CURRENT hashes — в `pass-current.json`. Для ridge/trough явно зафиксирована тематическая зеркальность; морфология вытянутого поля и замкнутой циркуляции рассматривается как отдельное знание о барических объектах. Это редакторское суждение для adjudication, а не автоматический результат скана.

**FIX (5):**

- environmental-lapse: узнавание наблюдаемого градиента среды соответствует medium, а frozen уровень hard. Нужна содержательная hard-задача без повторения двухслойного расчёта dry-adiabatic-rate.
- inversion-positive: рост температуры с высотой уже однозначно называет инверсию; добавка о плавучести не нужна для решения, hard не достигнут. CURRENT сосед inversion-warmer-above проверяет приземное основание, поэтому первоначальное подозрение прямого дубля снято.
- lightning-electric: prompt сообщает более редкую положительную полярность и фактически подсказывает отрицательную; специальный факт сам по себе не easy. Дистрактор «Заряд не достигает земли» противоречит cloud-to-ground и не подставляется как название заряда.
- el-nino-warm: вопрос о «фазе ENSO» автоматически исключает Североатлантическое колебание как чужую категорию. Изменить рамку на режим/явление при том же ключе.
- la-nina-cool: та же чужая категория плюс зеркальное повторение warm/cool связи El Niño. Сохранить El Niño как якорь, La Niña дать другой независимый medium-факт при том же ключе.

**HOLD (1):** nao-pressure. CPC действительно подтверждает североатлантический диполь pressure/height anomalies, jet/storm track и европейские temperature/precipitation эффекты, но не называет Исландский минимум/Азорский максимум. Climate.gov вернул robot challenge; один официальный альтернативный Met Office URL вернул 404. Нужен полный официальный контекст этих точных центров или адресное исправление на проверенный диполь. В prompt также есть географическая подсказка к одноимённому варианту. Note о IOD отдельно проверена по реально прочитанному BOM, старый HOLD не наследован.

Источники из primaryContextIndex прочитаны через сохранённые Git blobs; SHA-256 всех 15 использованных bodies совпали. Отсутствующий worktree question-review-process не восстанавливался, доступна его ветка. Дополнительно прочитаны [NWS Cyclone/Anticyclone](https://forecast.weather.gov/glossary.php?word=Cyclone), [NWS Theta-e](https://forecast.weather.gov/glossary.php?word=Theta-e) и [BOM IOD](https://www.bom.gov.au/climate/iod/); результат web-чтения сохранён в sources/supplemental-web-read.json. Python urllib capture получил certificate-verification failure; маршрут остановлен, TLS не ослаблялся. Supplement содержит представление web-reader, не объявлен byte-exact HTTP capture.

Проверки: 10/10 exact afterHash; 10/10 frozen ID/difficulty/correctIndex относительно baseline; 60 групп с exact literal и SHA-256 compact sorted Unicode JSON; четыре различные подписи и четыре notes в каждой карточке; hashes CURRENT соседей; git whitespace check только reviewer/. Правильные подписи у inversion-positive и lightning-electric изменены относительно baseline, но смысл ключа сохранён: переименование профиля инверсии и сокращение подписи отрицательного заряда. Это раскрыто поштучно в frozenContract, не выдано за literal equality.

Все замечания в fix-requests.json рассчитаны на один адресный fix-cycle. После исправления проверяются только изменённые карточки и затронутые соседи. Каталог, индекс, unchanged590, full QA/build/runtime не менялись и не запускались. Своих фоновых процессов, claims, новых worktree и временных сборок нет. reviewer/build_review.py — воспроизводимый генератор exact literals/hashes и независимых ручных оснований, не автоматический сертификатор содержания.

Следующий шаг: координатор выполняет adjudication, передаёт адресные FIX автору и сохраняет результаты в Git. Коммит по поручению делает координатор; этот reviewer ничего не коммитил и не интегрировал в main. До сохранения reviewer/ в Git сессию архивировать без потери данных нельзя.
