## Context

См. `proposal.md`. Browser уже отправляет v3 по same-origin `POST`; Node runtime хранит NDJSON в `/var/lib/mindbattle`, однако агрегированный `GET` сейчас проходит через Caddy, а редакторский script привязан к историческому v1-снимку. Игровое ядро и его сериализуемый state не участвуют в хранении и анализе после успешной отправки.

## Goals / Non-Goals

**Goals:**

- Принять анонимный v3 feedback от любого browser-клиента одного production origin и сохранить его в общем durable журнале.
- Убрать все HTTP read-пути к feedback данным.
- Дать оператору воспроизводимый v3-отчёт, запускаемый по SSH на VPS над production-файлом.
- Сохранить retry с тем же `eventId` и существующую idempotency-семантику.

**Non-Goals:**

- Синхронизация незавершённой партии или неотправленного события между устройствами.
- Учёт пользователей, устройств, IP, игровых ответов, счёта или команд.
- Веб-админка, API выгрузки, автоматическая переклассификация и изменение игровых правил.

## Decisions

### Разделить public write и private read

Node runtime сохраняет единственный публично достижимый feedback-маршрут: `POST /api/difficulty-feedback`. Удаляется `GET /api/difficulty-feedback/summary`; любой другой `/api/*` остаётся `404`. Это позволяет игре с любого устройства записать минимальное событие, но исключает browser-доступ к данным. Альтернатива — авторизованный public read API — отвергнута пользователем как излишняя поверхность доступа.

### Production NDJSON — единый источник фактов

Systemd service запускается от `mindbattle` и пишет в `/var/lib/mindbattle/difficulty-feedback.ndjson`, который остаётся вне `/opt/mindbattle`, web-root и rsync deploy scope. CLI-отчёт читает путь, явно переданный оператором через SSH; он не имеет HTTP handler и не создаёт файлы в репозитории. Альтернатива — внешний managed datastore — не нужна для append-only анонимных событий и расширяет зависимости.

### Отчёт ориентирован на v3 и отделяет старые схемы

Новый CLI разбирает NDJSON построчно, дедуплицирует по `eventId`, валидирует v3 против текущего каталога и выводит JSON с total, жалобами, no-complaints, complaint rate, причинами, неизвестными вопросами, повреждёнными строками и распределением catalog revisions. v1/v2 не смешиваются с v3-выводами; они учитываются как historical diagnostics. Свободные заметки не выводятся в агрегатах. Альтернатива — переиспользовать HTTP-store summary — отвергнута, поскольку он поддерживает public API и не является переносимым editor report.

### Обновление каталога не теряет накопленный журнал

При новом catalog revision runtime продолжает хранить старые валидные записи как исторические, а SSH-отчёт показывает их revision и не смешивает с текущим в сигналах. Новый client после deployment отправляет только revision активного bundle. Это лучше, чем ослабить server validation: неверно совмещённые bundle и каталог должны получить явную ошибку и повторить событие после обновления.

### Надёжность и границы состояния

HTTP handler подтверждает событие только после fsync; in-memory очередь сериализует конкурентные append. При сетевой или файловой ошибке client сохраняет уже выбранный feedback в своём snapshot и повторяет тот же `eventId`. Это локальная recovery-механика: успешная запись становится cross-device доступной для SSH-анализа, но незавершённая партия не переносится на другое устройство. Очки, таймеры, seed, command ordering, hidden answers и правила состязания не пересекают persistence boundary.

## Risks / Trade-offs

- [Старый bundle отправляет неактуальную catalog revision] → сервер отвергает его явно; retry остаётся локальным, а deployment публикует bundle и runtime одной версией.
- [Оператор запускает отчёт без доступа к `/var/lib/mindbattle`] → README описывает SSH-команду и required privileged/service-user execution, без ослабления прав каталога.
- [Повреждённая или оборванная NDJSON-строка] → отчёт и store пропускают её и явно считают diagnostic error; append не переписывает прошлые данные.
- [Свободная заметка попадёт в журнал терминала или CI] → агрегированный CLI её не печатает; raw-журнал читается вручную только оператором и не копируется в repo.

## Migration Plan

1. Реализовать private CLI и удалить HTTP summary вместе с её ссылками и healthcheck-зависимостью.
2. Обновить `GAME_SPEC`, canonical specs и deploy documentation; добавить automated API/CLI tests.
3. Выполнить локальный regression check и strict OpenSpec validation.
4. При deploy service restart сохраняет существующий `/var/lib/mindbattle/difficulty-feedback.ndjson`; проверить по SSH, что POST работает, public read даёт `404`, а CLI читает тот же журнал.
5. Rollback: вернуть предыдущий application revision. Журнал не мигрируется и остаётся append-only; отчёт current revision по-прежнему может учитывать старые записи как historical diagnostics.
