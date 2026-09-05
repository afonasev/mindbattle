## 1. Закрытый production read-контур

- [x] 1.1 Удалить HTTP-маршрут агрегированной feedback-сводки и обновить healthcheck так, чтобы unit/integration-тест подтверждал `404` для публичного чтения и сохранение `POST`-записи.
- [x] 1.2 Сохранить append-only/idempotent v3 persistence и добавить coverage двух независимых client-event с общим журналом, duplicate retry и отсутствием device/gameplay данных.
- [x] 1.3 Обновить Caddy/systemd/deploy документацию: журнал вне web-root, service-user права и SSH-only read; проверить, что deploy healthcheck больше не запрашивает аналитику.

## 2. SSH-only редакторский отчёт

- [x] 2.1 Реализовать CLI-отчёт, читающий переданный production NDJSON путь и выводящий v3 totals, complaints, no-complaints, complaint rate, причины, catalog revisions, historical/invalid diagnostics без заметок; покрыть его fixture-тестами.
- [x] 2.2 Добавить операторскую SSH-команду без записи raw data или отчёта в репозиторий и проверить её на временном журнале с v3, старой ревизией, дубликатом и повреждённой строкой.

## 3. Спецификация и проверка

- [x] 3.1 Синхронизировать утверждённый production/SSH-only контракт в `docs/GAME_SPEC.md` и canonical OpenSpec specs; проверить сохранение требований о анонимности, local retry и запрете автоматической переклассификации.
- [x] 3.2 Выполнить `npm run check`, targeted API/CLI tests и `openspec validate secure-production-feedback-analysis --strict`.
- [x] 3.3 Выполнить muted target-Chromium smoke в production-like runtime: два независимых browser-клиента отправляют фидбэк, public read возвращает `404`, SSH CLI отражает оба события; сохранить проверочный скриншот только если UI менялся.
