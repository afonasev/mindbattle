# Сохранение уже полученного первичного ответа

Этот способ сохраняет прежний full-context контракт; он не меняет попытки, источники или содержательную приёмку.

Вызов web в functions должен вывести original result полностью: `const r=await tools.web__run(...); store("source39_primary",r); text(r);`. Не предполагать наличие `content`/`result.content` или форму MCP CallToolResult; сохранять original result как есть. Не выводить только title/URL/linecount.

После завершения вызова: `python3 -B capture-native.py NATIVE_ID EXACT_URL OWN_OUTPUT/capture.json`. Скрипт сохраняет точный уже записанный native output record и выводит path/fileSHA/pointer/bodySHA. Он не делает network calls и отвергает metadata-only record. Лично читать нужный полный первичный контекст и оценивать следствие всё равно должен автор/reviewer. Успех захвата не даёт PASS.

Если запись файла упала после успешного web, восстанавливать тот же result через store/native record; не тратить новый источник на файловую ошибку. Если original body действительно утрачен — точный HOLD, без reset уже использованных network attempts. Новые действительно непокрытые claims сохраняют действующий лимит одна попытка плюс одна официальная альтернатива.
