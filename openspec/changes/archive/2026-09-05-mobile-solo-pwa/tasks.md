## 1. Контракт и PWA-основа

- [x] 1.1 Синхронизировать `docs/GAME_SPEC.md` с утверждёнными mobile solo-first и PWA-решениями; проверить, что desktop classic и правила `solo-endless-v1` описаны без противоречий.
- [x] 1.2 Добавить manifest, существующую иконку и production service worker с precache; проверить production build и manifest/service-worker ресурсы в `dist`.
- [x] 1.3 Добавить контролируемое уведомление о waiting-обновлении и безопасное применение; покрыть UI/registration unit-тестом либо browser-сценарием без авто-reload активного соло-забега.

## 2. Офлайн feedback

- [x] 2.1 Реализовать versioned локальную очередь минимальных feedback-событий с дедупликацией `eventId`; покрыть unit-тестами добавление, повреждённые данные и успешное удаление.
- [x] 2.2 Обернуть same-origin feedback sink, чтобы офлайн-ошибка не блокировала continuation, а повторная доставка выполнялась при запуске и `online`; проверить unit-тестом порядок и приватный payload.

## 3. Телефонный соло-опыт

- [x] 3.1 Сделать mobile viewport solo-first: скрыть classic setup и его запуск только до 760 CSS-пикселей, сохранив desktop classic; проверить browser-сценариями 390 и 1280 CSS-пикселей.
- [x] 3.2 Адаптировать соло-меню, тему, риск, вопрос и результаты под 360–760 CSS-пикселей с touch-целями от 44 CSS-пикселей и без горизонтального overflow; проверить реальным browser phone playtest с выключенным звуком и актуальным screenshot.

## 4. Интеграционная проверка и доставка

- [x] 4.1 Выполнить `npm run check`, production PWA/browser-проверки и `openspec validate mobile-solo-pwa --strict`; зафиксировать краткое доказательство результатов.
- [x] 4.2 Проверить staged scope и `git diff --cached --check`, создать отдельный commit change и только затем архивировать completed change через `openspec archive mobile-solo-pwa`.
