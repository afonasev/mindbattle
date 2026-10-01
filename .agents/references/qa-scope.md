# QA scope and evidence

Выбирай gate по изменённым контрактам, потребителям общей зависимости и возможным
последствиям, а не по имени файла. В change записывай выбранный scope, обоснование,
затронутые поверхности и дополнительные tests. При нескольких влияниях объединяй
маршруты; если границу доказать нельзя — `full`. Эта матрица определяет required
checks для change; профильный default `npm run qa` — безопасный full fallback,
а не требование full для каждого изменения.

| Влияние | Обязательный локальный маршрут | Дополнительные gates |
| --- | --- | --- |
| QA tooling/docs без runtime/visible изменений | `npm run qa:tooling` | Маршрут включает Node и Python flow-контракты; реально выполнить каждый изменённый маршрут. Для flow helper дополнительно `python3 tools/test_flow.py` и `python3 -m unittest discover -s tests -p 'test_flow*.py'`. |
| Изолированное представление/текст/layout без изменения правил, state, permissions, timers или input | `npm run qa:ui` | Затронутые browser сценарии вне smoke и screenshots; реальный in-app Browser для visible изменений. |
| Phone/display presentation | `npm run qa:ui` | Snapshot checks не доказывают SSE/privacy. Если меняются роль, snapshot mapping, права/синхронизация — также `qa:network`; физические телефоны при изменении device interaction. |
| Изолированное сетевое взаимодействие с известной границей | `npm run qa:network` + UI при visible изменении | network-domain/room/status, реальные SSE и 12 browser клиентов, restore/departure/privacy. При изменении протокола/authority/timers/full shared state — full. |
| Изолированный input adapter с известной границей | `npm run qa:input` + UI при visible изменении | Keyboard/virtual-gamepad integration и controller tests; физический gamepad отдельно. Изменение общего порядка/neutral gates/permissions — full. |
| Конкретная subsystem без общего критического влияния | Typecheck + явные затронутые Vitest/browser tests с JSON evidence | Content: catalog-full/topics/content и действующие editorial integrity gates. Audio: audio unit/browser tests и audible acceptance. Storage/results/feedback/PWA: собственные unit/browser integration tests; smoke не покрывает эти контракты. |
| Gameplay rules, clocks, scoring, seed/RNG, command ordering, hidden information, общие критические зависимости, неизвестное влияние, зависимости/toolchain | `npm run qa` (full) | Полные units, production build, все browser scenarios. Перед production full, release identity и smoke; production требует отдельного разрешения. |

## Команды и покрытие

```sh
npm run qa:tooling
npm run qa:ui
npm run qa:network
npm run qa:input
npm run qa                              # full default
npm run qa:ui -- --evidence /absolute/durable/path
npm run test:qa-tooling                 # только контрактные tests runner
```

Все маршруты запускают контрактные tooling tests и typecheck. UI unit scope:
solo-ui, network-status, content-answer-notes. UI browser scope: desktop меню и
settings/local setup (1280/1920), mobile 390 menu→solo, classic reveal (0–3
ошибки/accessibility), solo reveal (desktop/360/760) и pause/resume, phone
reveal/standings/veto (360/760, 2/12 игроков), display reveal 12 игроков в обоих
contrast modes. Выборы находятся в `scripts/qaScope.mjs`; отсутствие любого
selector/project делает прогон failed. UI snapshots используют intercepted
payload и не проверяют реальную серверную авторитетность/SSE/privacy.

Network: network-domain/room/status и реальные network feedback, 12 phones с
privacy/bonus/display restore/departure, авторитетные списки тем display/phones
при 1280/1920. Input: adapter/solo-input/application-controller плюс fallback
без Gamepad API, virtual-pad neutral gate/cursor/confirm и D-pad feedback и 3/4 team bonus veto только
1280; это автоматизированная проверка, а не physical acceptance.

Full сохраняет существующие gameplay assertions, clocks и длительности. Пять
существующих исключений второго viewport (virtual-pad и real-time deadline)
показываются как skipped, а не passed; runner разрешает только эти известные
file/title/project исключения. Focused routes не допускают skipped, todo,
flaky, expected failures или нулевые tests. `npm run check` остаётся types +
все unit tests + builds; `npm run test:browser` остаётся самостоятельным
production build + browser gate. `check` не повторяет typecheck внутри build;
самостоятельный `build` по-прежнему проверяет types.

## Изоляция и evidence

`qa` создаёт уникальную run-папку, JSON reports и logs, summary с HEAD, dirty
status/diff hash, Node version, scope, counts, commands/exit codes и wall time.
Dirty evidence относится к HEAD + diff hash; финальное evidence записывай с
clean commit. Отсутствующий/некорректный JSON report — ошибка. Не используй
старые успешные reports. CLI не принимает произвольный grep, который мог бы
тихо сузить gate; дополнительные tests запускай отдельно и сохраняй evidence.

Browser runner запускает собственный Node host на свободном loopback port,
проверяет startup и записывает его время отдельно от Playwright wall time.
У него отдельные временные feedback/results data; он завершает только свой
процесс и удаляет только свои data. Focused использует Vite dev (не проверяет
production bundling/service worker/cache); full использует свежую сборку и
production preview. Установи зависимости в worktree через `npm ci`; симлинк на
чужой node_modules может блокировать шрифты в Vite. Vitest import/transform
время смотри в unit.log: суммы по workers не равны wall time. Не обещай
ускорение относительно full browser без измерения обоих маршрутов.

Tooling-only изменение не меняет игровой артефакт и не требует нового physical
playtest, визуальной приёмки игры, сборки или деплоя. Ручная приёмка отчёта и
точной tooling revision остаётся отдельной. Никакой автоматический gate не
означает human/device/platform acceptance.

## Известный открытый gate на 2026-10-01

`qa:network` обнаружил существующий runtime-дефект: `server/index.mjs`
использует `mindbattle-questions-2026-09-02-r3`, а `src/content/catalog.ts` —
`mindbattle-questions-2026-09-29-quality-wave-3`. `validateFeedbackEvent`
отвергает сетевой feedback с актуальной revision; продолжение после него
остаётся failed. Этот gate и зависящий full не считаются green. Исправление
runtime — отдельный scope; QA tooling не подменяет feedback успешным mock.
Evidence: planning `evidence/focused-qa-routes/network/` и acceptance.md.
