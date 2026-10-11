# Independent reader — winter-sports first25

Прочитаны первые25 ID в текущем порядке topic, winter-sports-001…025: все150 indexed fields (prompt-key,note0–3,explanation), четыре ответа с условием и привязанные оригинальные passages. Reader `01a12bed-2f93-7cb2-b624-3e6caf2fecec`, отличный от автора `01a12ba2-6af8-79b3-96c4-14a4e60812b6`. Ветка `codex/question-quality-wave-6`; baseline сессии `99decc10b79a08a959c65066afbf11d59831af3a`. Авторские входы — current `author100-receipt.json`/manifest после READY supersessions, не исторические HOLD.

Результат: **6 independent PASS,19 FIX_REQUIRED**. Поля: **140 PASS,8 FIX_REQUIRED,2 HOLD**. PASS ID:009,011,012,013,014,025. Это завершённое чтение назначенного среза, **не завершение волны и не root certification**. New certified=0; зачёт выполняет координатор по двум ролям и текущим хешам.

## Где читать

- `receipt.json`: полная независимая квитанция с текущими whole-card/literal hashes, своими решениями, source passages/locators/raw hashes.
- `decisions.json`: вручную записанные substantive решения; serializer не выводит PASS.
- `SUMMARY.json`: счётчики, current topicSHA, неизменность ID/order/difficulty/correctIndex,40/40/20 и10/10/5 по позициям.
- `receipt-first5.json`, `roundtrip-first5.json`: сохранённый pilot5/30 до расширения; исторический report указывает имя receipt.json на момент его запуска, байты пилота отдельно сохранены и SHA закреплён в SUMMARY.
- `roundtrip-final25.json`:25/150,0 механических ошибок. Проверяет лишь идентичность/наличие, не фактическую истину.

## Конкретные замечания

1.001–008,015–017,019,021–024: см. per-card analysis о неправдоподобных дистракторах/прямых подсказках. Все альтернативы реально прочитаны; одинаковая широкая категория зимних видов сама по себе не оправдывает хоккей при условии спуска на лыжах.016 слово «парном» непосредственно даёт2.023 medium обходится названием «платформа под крепление» и очевидно неподходящей лыжной палкой.
2.010/note0: классификация «скоростной спуск относится к скоростной группе» фактически истинна, но почти тавтологический ярлык без самостоятельного знания.
3.017/prompt-key и explanation: HOLD полноты доказательств. Привязанный Zamboni passage83 подтверждает очистку льда, но не определяет каток. Вторая фраза explanation истинна; не переносить её proof на первую.
4.018/prompt-key и explanation: COC даёт общий принцип, но FIS ICR September2025,5801/5801.3.5 ограничивает delay максимальным penalty time; DNF также регулируется отдельно. Безусловное соответствие интервалам финиша требует исправления. Полный оригинальный FIS PDF сохранён.
5.020/prompt-key и explanation: сумма4 относится к полному финальному зачёту; OWG2026 Format p1 явно допускает только top20 в4-й заезд. Scope вопроса «результат экипажа» не ограничен финалистами. Note2 о сотых секунды не объясняет ложный метод по времени последнего заезда.
6.022/note3: вариант «Пятка ботинка» — часть обуви; исходный Hockey Canada passage говорит `Your child's heel`, т.е. о пятке человека внутри ботинка. Это точная ошибка соответствия note варианту.
7.024/note0: правило задержки ворот относится ко второму (женскому) этапу; note обобщает на стартовые ворота всего mixed event.

Useful correct-note может повторять дополнительный факт explanation: это нигде не использовано как причина отказа. Все explanation содержат2 предложения. Оценка сложности отдельно от source truth сохранена по карточкам; сами уровни не изменены.

## Оригиналы и сохранность

У16 из25 использованных авторских оригиналов рабочие HTML bytes совпали с прежним receiptSHA, но прежний Git blob был CRLF-normalized. Уже существующий -text атрибут не восстановил старые blobs. **Хеши не переименованы**: точные прочитанные байты сохранены под owned `preserved-originals/` с `-text -diff`, старые авторские файлы/receipts не изменены. `source-byte-preservation.json` хранит оба SHA и проверку причины расхождения. `-diff` относится только к нетронутым сырым оригиналам, чтобы whitespace-проверка редакторских файлов не изменяла/не отвергала HTTP bytes.

Дополнительные sources: `new-originals/fis-sbx-rules-2025.pdf` (полные291страница,200application/pdf) и `owg2026-bobsleigh-full-provider-extraction.txt` (полный текст всех3страниц,114/114строк оригинального олимпийского PDF через web.open). У второго сохранены неизменённый provider response и точное описание удаления только служебных line-prefixes. Это допустимый documented complete extraction, не PDF bytes и не собранная подборка цитат. Прямой curl завершился DNS failure; original PDF byte hash не заявлен. Неудачные404/DNS receipts сохранены, не включены как proofs. IMAGE proofs не использовались; утверждения PDF текстовые.

Независимый global scan: прочитаны найденные prompt/key кандидаты из других тем и exact-key match; football goalkeeper — другая спрашиваемая связь. Внутри назначенных25 основные факты различены вручную. Остальные75 содержательно не читались по scope; reconciliation с их читателями остаётся у координатора. Нет заявления о полной независимой проверке всей темы.

## Проверки и границы

Минимальный достаточный маршрут для evidence-only diff: `verify-proof-format.py` на first5, затем на current25; собственная проверка Git blobs всех proof paths; JSON shape/hash/quota preservation и `git diff --cached --check` только own paths. Runtime/topic/validators/tests не изменялись. Полные suites, npm check/qa/test:browser, build/deploy/release/archive не запускались. Planning/claim/lease/ledger не изменялись; чужие165 не перечитывались и не менялись.

Следующий шаг: координатор сверяет current hashes, учитывает6 PASS только после paired gate и передаёт автору19 карточек на новую ревизию. Для изменившихся карточек нужны новые полные6-field receipts и независимая проверка. Старые ошибки/receipts сохранять. Этот чат не отправляет сообщения родителю и не создаёт новые чаты/агентов.

Cleanup: собственных активных процессов, браузеров, серверов, тестов, сборок нет. Промежуточные разрозненные decision JSON объединены в decisions.json и удалены; повторный сырой diagnostic log заменён сводкой уникальных предупреждений. Полные originals, неудачные fetch receipts, pilot/history, current receipts и handoff сохраняются в Git. Shared worktree/ветка и чужие ресурсы оставлены координатору.
