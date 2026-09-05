## Context

См. `proposal.md`. React/Vite-клиент уже хранит настройки и соло-снимок в localStorage, а `SoloController` ожидает успешной записи feedback до continuation. Текущие production-ресурсы получают content-hash, поэтому ручной статический service worker не может надёжно precache-ить актуальный bundle.

## Goals / Non-Goals

**Goals:**

- Установить mobile PWA поверх существующего Vite bundle, не затрагивая доменное состояние и seed.
- Сделать mobile меню и соло-экраны touch-first, сохраняя desktop-classic UI.
- Доставлять только минимальный feedback event из локальной очереди и безопасно применять обновления.

**Non-Goals:**

- Не удалять и не переделывать classic-v1, не добавлять сетевой матч, аккаунты, push-уведомления или background sync API.
- Не менять каталог, авторитетные часы, scoring, randomness или аудио-политику.

## Decisions

### Генерируемый precache service worker

Используется `vite-plugin-pwa` с Workbox `generateSW`: он получает список фактических hashed Vite-ассетов на build и precache-ит shell, каталог, локальную иконку и аудио. Это надёжнее hand-written списка путей и не требует внешних runtime-запросов. Навигация возвращает cached `index.html`; runtime cache обслуживает same-origin static assets.

Альтернатива — собственный service worker в `public/` — отклонена: он не узнаёт имена production bundle без дополнительной build-интеграции.

### Отложенное обновление

Регистрация PWA сообщает UI о waiting worker. Приложение предлагает «Обновить» только в меню либо после завершения забега; нажатие отправляет `SKIP_WAITING`, ждёт `controllerchange` и перезагружает страницу. Во время любой активной solo-фазы waiting worker не активируется через UI. Это сохраняет сериализованный соло-снимок и не изменяет авторитетные часы.

### Очередь feedback принадлежит presentation/persistence слою

`QueuedDifficultyFeedbackSink` оборачивает существующий HTTP sink. При ошибке сети он сохраняет сам `DifficultyFeedbackEvent` в отдельном versioned localStorage ключе и возвращает успешный результат controller-у, чтобы тот мог продолжить flow. При запуске и `online` очередь последовательно отправляется; запись удаляется только после успеха. Дедупликация по `eventId` предотвращает дубликат. Ни domain state, ни serializer матча не импортируют этот слой.

Альтернатива — менять `SoloController` и его авторитетные переходы — отклонена: доставка feedback не является игровым правилом.

### Mobile UI является CSS-слоем

`MenuScreen` вычисляет mobile layout через CSS, а classic configuration получает класс, который скрывается только в media-query. `start` недоступен pointer-пользователю на mobile, однако не удаляется из desktop DOM-потока. Соло использует одну mobile media-query для рамки, header, topic/risk actions и answer cross; DOM-команды и pointer handlers остаются прежними.

### Версионная совместимость и rollback

У deploy новая precache-ревизия устанавливается рядом со старой. Если новый bundle ломается, rollback deploy создаёт следующую корректную ревизию, которую установленный клиент также обнаружит. Старые offline cache удаляет Workbox после успешной активации. Очередь feedback версионируется и при повреждении безопасно очищается изолированно.

## Risks / Trade-offs

- [Cache увеличивает первый install] → precache ограничивается необходимыми локальными игровыми ресурсами и проверяется размером production build.
- [Ожидающее обновление остаётся незаметным] → видимый banner в safe state и проверка registration при возвращении фокуса.
- [Повтор feedback после timeout может быть уже принят сервером] → сохраняется исходный `eventId`, а серверная идемпотентность остаётся источником истины.
- [CSS скрытие не является security boundary] → требование ограничивает mobile UX, не утверждает запрет программного вызова classic API.

## Migration Plan

1. Deploy build с manifest и service worker; первое online-открытие устанавливает PWA и precache.
2. Уже открытый клиент получает waiting worker и применяет его только через safe-state action.
3. При rollback deploy публикует новую корректную worker-ревизию; пользователь не переустанавливает приложение.
