## MODIFIED Requirements

### Requirement: Локальный browser-клиент работает с локальным feedback backend

Система SHALL предоставлять browser-клиент и Node runtime, обслуживающий статические ресурсы и same-origin difficulty-feedback API. В локальном запуске runtime и клиент могут находиться на одной машине; в production browser-клиент на любом устройстве SHALL отправлять анонимное v3-событие только в same-origin `POST` production runtime. Клиент MUST не использовать аккаунты, внешнюю аналитику, телеметрию, device-идентификаторы или запросы к origin, отличному от origin приложения. Production runtime MUST не предоставлять browser-клиенту или посетителю HTTP-доступ к feedback-журналу, его агрегатам либо редакторскому отчёту.

#### Scenario: Запуск локального приложения
- **WHEN** пользователь запускает поддерживаемую локальную команду и открывает клиент в desktop Chromium
- **THEN** один локальный runtime обслуживает клиент, API оценки и доступ к серверному файлу без обращения к внешним runtime-сервисам

#### Scenario: Production build локального прототипа
- **WHEN** разработчик выполняет production build
- **THEN** система создаёт browser bundle и запускаемый Node runtime, способный обслужить bundle и принимать same-origin запись анонимного feedback без выдачи журнала или агрегатов по HTTP

#### Scenario: Внешний runtime-запрос
- **WHEN** клиент пытается обратиться к origin, отличному от origin локального приложения
- **THEN** такой запрос не является частью поддерживаемого игрового потока
