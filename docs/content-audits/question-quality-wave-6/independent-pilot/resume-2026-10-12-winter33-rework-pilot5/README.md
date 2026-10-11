# Независимый пилот winter33 — пять текущих версий

Reader: `01a12ccb-4877-7e60-93e1-5718382ba57f` (`independent`). Автор: `01a12cc1-9d5d-74a1-99ba-6377bdfaed21`.

Source freeze / author commit: `4799684e9adf86532c13423abfe9f559840751ce`. Author receipt SHA-256: `71ca894abdd8bb39d27ee9604c07ec00b44fb3d5c2012b3a868fd3613e45ea00`.

Пилот прочитан независимо от автора. Итог: **5 FIX**, поля **22 PASS / 7 FIX / 1 HOLD**, все 30 substantiveRead=true. Hash/HTTP/авторский PASS не использованы для вывода редакторского PASS.

| ID | Текущий cardCanonicalSha256 | Требуемое действие |
|---|---|---|
| winter-sports-007 | `81e5850e9a5de465a85ac764c099bf0b2439c462ba6db391bedb35b5c1955fa0` | prompt-key FIX: палки не надевают на ноги, крепления названы в условии, лыжи не соединяют с лыжами. Все три дистрактора устраняются предпосылкой. |
| winter-sports-008 | `3477d3d7712c6626eb834644d41af21aaa04e7d680f9198b8df220cfbe8002c9` | prompt-key FIX: среди спорта с программой три варианта на время/игровой счёт; note0 FIX: «все соревнования» чрезмерно обобщает олимпийскую страницу, ISU Rule203 допускает 333 1/3–400m. |
| winter-sports-017 | `498d015a9234675827bd9638236943dc895fbc478ff0439ef3693613ade6ad40` | prompt-key FIX: medium вместо easy; explanation HOLD: COC прямо подтверждает одиночный хафпайп, но не одиночность слоупстайла в выбранном passage. |
| winter-sports-019 | `52d7863fa2873b2193f2de7ef6460cb96fdd96175a1d5a553f353518cafa6c8c` | prompt-key FIX: машина против разметки, ограждения и действия — разные категории; ключ повторяет категорию условия. |
| winter-sports-024 | `c3f7870aa9b06098d86524cdef1a075a56c380519fce4e454bb3788e97768af2` | prompt-key FIX: «креслах» раскрывает «кресельный», «воздушного» исключает surface lift; explanation FIX: автомобили вместо вагонов скимобиля. |

В reader-receipt.json сохранены точные literals/SHA, самостоятельный анализ каждого из шести полей и все proofs. Скрипт только сериализует вручную записанные verdicts в manual-verdicts.json. Он не производит редакторских решений и не обновляет ожидаемые SHA для успешного результата.

Восемь полных исходных публикаций прочитаны с текущими passages. Полные raw-байты сохранены ранее в Git и совпадают на диске/в source freeze. Семь повторных GET200 также байт в байт совпали; World Curling curl GET403, web open дал текущий текст: факт о двух командах, гранитных камнях и House подтверждён. Отсутствие нового curl raw-readback World Curling не скрыто. Полный дополнительный ISU PDF сохранён здесь; непосредственно прочитаны релевантные Rules203–206 (physical page9), схемы/контекст pages27,29–32; чтение всех остальных ISU правил не заявляется.

COC классифицирован как национальный олимпийский комитет, не FIS или ISU governing body. Maine — официальный законодательный источник. Hockey Canada/Bauer — официальный национальный guide по экипировке.

Дубликаты: пять пилотных фактов различны; точное совпадение prompt проверено механически по каталогу без вывода защищённых строк. Семантическая редакторская проверка будущих 28 и других 95 этим пилотом не заявляется; будущие 28 и sourcecert67 не читались.

Source-readback.json содержит 95 защищённых canonical hashes и общий digest. Topic raw полностью равен source freeze. Изменения других авторов в middle-ages/architecture сохраняются. Исторические verdicts/receipts не изменены.

Минимальная проверка по diff: только evidence/docs и два скрипта воспроизведения, без runtime/content mutations. Выбраны непосредственная проверка 30 literals/proofs/raw SHA, защищённых 95 и Git roundtrip, JSON parsing, staged scope и git diff --cached --check. Full suite/build/deploy/merge/push/root certification/human acceptance не запускались.

Команды:

```sh
python3 docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter33-rework-pilot5/serialize-and-verify.py
git diff --cached --check
python3 docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter33-rework-pilot5/serialize-and-verify.py --verify-committed
```

Продолжение: координатор adjudicates конкретные FIX/HOLD; автор исправляет пять пилотных карточек, затем независимый reader повторно проверяет новые versions. Переход к оставшимся 28 допустим после калибровки пилота; этот отчёт его не разрешает автоматически.

Cleanup: собственные временные HTTP headers удалены автоматически; повторные байт-идентичные raw не оставлены дублями. Промежуточный urllib TLS failure удалён после успешного перехода на системный curl с включённой TLS-проверкой. Сохранены исходные Git originals, новый полный ISU PDF и воспроизводимый отчёт. Собственные длительные процессы не оставлены. Общий worktree используется авторами; его удаление/архивирование не входит в ownership.
