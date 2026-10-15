# Публикация Mindbattle

Каноническая инструкция для сайта, установщиков и обновлений установленной игры. Исходники и установщики публикуются в публичном репозитории [afonasev/mindbattle](https://github.com/afonasev/mindbattle). Публикация требует разрешения пользователя на соответствующую среду; сборка, Git push и запись этой инструкции сами по себе его не дают.

## Что публикуем

| Изменение | Подготовка | Публикация |
|---|---|---|
| Сайт / PWA | `npm run build` (включён в deploy) | `make deploy` |
| Игра, вопросы, JS/CSS, музыка и другие content-ассеты для установленной игры | `npm run desktop:content` | `bash scripts/desktop/publish.sh content` (GitHub Releases + Pages) |
| Electron, main/preload, native updater или другие файлы оболочки | Новая `shellVersion`, content, оба установщика и `npm run desktop:shell` | `publish.sh content`, `publish.sh shell`, `publish.sh installers` |
| Только оформление / поведение установщика | Новая `shellVersion`, content, оба установщика и `npm run desktop:catalog` | `publish.sh installers`; shell/content отдельно, если они входят в разрешённую поставку |

`make deploy` не собирает и не публикует desktop-дистрибутивы. GitHub Release с установщиками не обновляет content/shell каналы автоматически. Для выпуска игры одновременно на сайте и установленным клиентам нужны обе соответствующие публикации. Обычная правка игры не требует пересборки установщиков.

## Где находятся версии и файлы

- `package.json` → `version`: версия самой игры. Публикационный build добавляет идентификатор содержимого; UI показывает номер без хэша. Готовая кнопка «Обновить» выделена тёплым оттенком и показывает версию и дату именно подготовленного обновления; даты current/latest для её подписи не используются.
- `desktop/config.json` → `shellVersion`: версия оболочки и установщиков. Для нового комплекта увеличивай её; это же номер тега `v<shellVersion>`. Не переиспользуй опубликованный тег для других бинарников.
- Windows: `Mindbattle-<shellVersion>.exe`; macOS: `Mindbattle-<shellVersion>-mac-universal.dmg` (Intel + Apple Silicon).
- `desktop-release/installers/downloads.json`: каталог с версиями, HTTPS GitHub URLs, размерами и SHA-256 для обеих ОС.
- GitHub Releases хранит версионные установщики. На VPS `/var/lib/mindbattle-desktop/installers/current` хранится только каталог; EXE/DMG туда больше не загружаются.
- Новые подписанные content и shell обновления хранятся в GitHub Releases (`content-<sequence>`, `shell-<sequence>`); публичные manifests — на `https://afonasev.github.io/mindbattle/desktop/{content,shell}/...`. Ветка `desktop-updates` хранит только manifests и является source GitHub Pages (`/`, branch deployment). Старые VPS feeds нельзя удалять до завершения перехода установленных клиентов.

## Подготовка выпуска

1. Работай в worktree/ветке своей задачи. Обнови нужную версию, проверь согласованный scope, текущие Git refs и опубликованные каталоги. Сохрани чужие изменения.
2. Нужны Node из `package.json`, `npm ci` и авторизованный `gh` с правом писать Releases/Pages в `afonasev/mindbattle`, Git push в `origin`. Для web, каталога установщиков и однократной legacy-публикации нужны SSH-профиль `gfe` и `rsync`. Для сборки обоих установщиков на macOS нужны Go и `lipo` (native helper), несколько ГБ свободного места.
3. Используй существующий Ed25519 private key вне репозитория, совпадающий с `desktop/content-public.pem`. Не выводи ключ и не клади его в Git, артефакты или VPS web-root. `npm run desktop:key` предназначен только для первого создания ключа; новый ключ не заменяет pin существующих установок.
4. Задай один UTC timestamp для всего выпуска **до** `desktop:content` и повторно используй его при web-deploy. Дата попадёт в game-version.json, signed content/shell payload и waiting PWA worker. GitHub publication отклоняет payload без валидной даты; старые offline/legacy manifests без даты читаются, но UI не выдумывает время публикации. Без timestamp offline-игра покажет «Ещё не опубликована».

```sh
set -euo pipefail
export MINDBATTLE_CONTENT_KEY=/secure/path/content-signing.pem
export MINDBATTLE_PUBLISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# DEPLOY_HOST при необходимости меняет SSH-профиль; по умолчанию gfe.
gh auth status
ssh -o BatchMode=yes "${DEPLOY_HOST:-gfe}" true
npm ci
npm run typecheck
# Выполните affected tests по diff; полный прогон — только по отдельной команде человека.
```

`MINDBATTLE_CONTENT_SEQUENCE` и `MINDBATTLE_SHELL_SEQUENCE` по умолчанию берутся из текущего времени. Новая sequence должна быть выше опубликованной; проверяй часы и актуальный manifest перед публикацией. Явное значение задавай только при необходимости, не откатывай счётчик.

## Новый комплект установщиков

После изменения `shellVersion` подготовь актуальную offline-игру, затем последовательно собери обе платформы. Не редактируй исходники и не запускай другие сборки в этом же worktree во время packaging.

```sh
npm run desktop:content
npm run desktop:mac
npm run desktop:win
npm run desktop:catalog
node scripts/desktop/verify-release.mjs installers
npm run desktop:smoke
# Если выпускается новая оболочка для обновления существующих установок:
npm run desktop:shell
node scripts/desktop/verify-release.mjs shell
```

`desktop:content` создаёт `desktop/bundle` и `desktop-release/content`. Установщики содержат именно этот bundle. Команды packaging обновляют main/preload/helper из исходников перед сборкой. После изменения содержимого, даты публикации или packaged-файлов пересобери затронутые артефакты и заново создай каталог. После изменения runtime файлов нужен новый shell manifest.

Проверки выбирай по затронутому поведению: для ссылки скачивания есть `tests/browser/github-download.spec.ts`; изменения игровой логики требуют проектных game-QA gates. `desktop:smoke` проверяет офлайн-запуск, сохранения, display-настройки и подписанное content-обновление с отдельным профилем. Для механизма shell-обновления `node scripts/desktop/smoke-shell.mjs` проверяет packaged macOS N→N+1 и восстановление после неуспешного старта; это не Windows acceptance. Все обычные QA запускай без звука.

До внешней публикации сохрани проверенные исходники в Git, отправь feature-ветку, интегрируй и отправь `main`, проверь удалённые SHA. Публикуй из чистого checkout этой проверенной ревизии. `publish-github.mjs` привязывает новый draft/tag к `HEAD`; не запускай его из постороннего checkout. Собранные файлы и их происхождение должны соответствовать записанной ревизии.

## Публикация и её порядок

Команды ниже выполняются только для каналов, включённых в разрешённую поставку. Для полного выпуска оболочки нужны все три desktop-канала; для installer-only выпуска достаточно `installers`.

```sh
# Подготовленное игровое содержимое для существующих установок:
bash scripts/desktop/publish.sh content
# Подготовленная новая оболочка, если она входит в выпуск:
bash scripts/desktop/publish.sh shell
# Новый комплект установщиков и ссылка лендинга:
bash scripts/desktop/publish.sh installers
# Сайт/PWA, если они входят в выпуск; сохраняет экспортированный timestamp:
make deploy
```

`publish.sh installers` — основной способ публикации установщиков. Не заменяй его ручной загрузкой на VPS или одиночным `gh release upload`:

1. Проверяет локальные EXE/DMG по каталогу.
2. Создаёт/находит GitHub draft `v<shellVersion>`, загружает недостающие assets обеих ОС, проверяет GitHub digest SHA-256 и размер. Draft-файлы определяются по имени: до публикации GitHub использует временный `untagged-*` URL.
3. Публикует проверенный релиз и помечает его latest.
4. Передаёт на VPS только `downloads.json`. VPS скачивает публичные GitHub assets и проверяет размер и SHA-256 ещё раз.
5. Под lock атомарно переключает `current`, затем удаляет предыдущие installer-каталоги и payloads. Лендинг выбирает ссылку своей ОС из `/desktop/downloads.json`.

Публикация content/shell не использует SSH/VPS. `publish-updates.mjs`:

1. Требует чистую ревизию, совпадающую с `origin/main`, проверяет подписи и каждый локальный объект. Обе shell-платформы имеют одну sequence. Подписанный `objectBaseUrl` привязан к своему каналу/sequence в `afonasev/mindbattle`.
2. Читает ветку `desktop-updates`, проверяет предыдущие manifests и sequence. Равная sequence допустима только для идентичных payload при повторе; меньшая и изменённая равная запрещены. Другая существующая конфигурация Pages останавливает публикацию до изменения Releases.
3. Создаёт draft/prerelease `content-<sequence>` или `shell-<sequence>` на текущем commit. Загружает объекты по SHA-256 и копии подписанных manifests. Проверяет digest/size GitHub каждого asset. Не перезаписывает assets и не дополняет уже опубликованный неполный релиз. Превышение лимита GitHub 1000 assets останавливает публикацию.
4. Публикует проверенный релиз, не меняя latest установщиков. Коммитит только metadata в `desktop-updates`, отправляет без force; конкурентное изменение ветки вызывает безопасный отказ. При первом выпуске создаёт Pages с этой веткой, не заменяя чужой source/domain.
5. Ожидает точного публичного readback manifests на Pages (до пяти минут). Timeout означает pending publication/readback, а не успешную поставку. Повтор использует те же подготовленные bytes.

Старые Releases/объекты сохраняются для last-good/rollback и клиентов, скачивающих прежний manifest. Автоматической очистки этих объектов нет. Private key никогда не загружается в GitHub; Pages содержит только подписанные metadata. GitHub redirects разрешены только HTTPS в этом репозитории и на разрешённых release CDN; подпись и hash/size остаются обязательными.

### Переход существующих установок

`desktop/config.json` разделяет `origin` сетевой игры и `updateOrigin` обновлений. Начиная с подготовленной оболочки 1.0.5 проверки идут на Pages. **Content-обновление не меняет main/preload старой оболочки**.

После отдельной команды собрать/опубликовать переход:

1. Соберите content и оба установщика с 1.0.5, затем shell; выполняйте affected проверки и настоящую N→N+1 приёмку.
2. Опубликуйте content и shell через обычные GitHub команды и дождитесь readback обоих каналов.
3. Явно выполните `bash scripts/desktop/publish.sh legacy-shell`: тот же подписанный shell и его объекты однократно публикуются на старый VPS feed. Legacy клиенты игнорируют дополнительное подписанное поле objectBaseUrl и скачивают переходную оболочку по своему старому маршруту. Новая оболочка после перезапуска использует GitHub.
4. Опубликуйте установщики обычной командой. Если старый клиент вообще не может достучаться до VPS, установите новую версию поверх существующей с сохранением профиля.

Новые content/shell выпуски после перехода требуют только GitHub. VPS остаётся для сайта, сетевых комнат/статистики и каталога скачивания на старом лендинге; его старые feeds пока сохраняются для ещё не обновившихся установок.

Content/shell и installer Releases получают двуязычное player-facing описание из `scripts/desktop/release-notes.mjs`. Генератор выбирает версионируемые fragments `docs/desktop/release-changes/*.json`, введённые Git-коммитами после предыдущего тега своего канала (для первого выпуска — всю историю). Каждая запись содержит одинаковый смысл RU/EN и категорию added/improved/fixed. Пустые категории опускаются. Отсутствие reviewed fragments останавливает публикацию: фиксированный текст или список commit subjects не заменяют changelog. В описание включены ограничения неподписанной test-поставки и штатный способ запуска. Перед публикацией прочитайте результат `node scripts/desktop/release-notes.mjs content` (либо shell/installer).

## Если публикация прервалась

- Повтори `publish.sh installers` с той же ревизией и **теми же файлами/каталогом**: отсутствующие assets будут загружены, существующие — проверены. Путь повторения работает, пока релиз присутствует среди последних 100 записей GitHub API, которые читает скрипт.
- Несовпадение хэша/размера останавливает публикацию; скрипт не перезаписывает существующий asset. Не обходи проверку и не удаляй рабочие VPS-файлы вручную.
- Если пришлось пересобрать ещё не опубликованный **собственный draft**, проверь его статус/владение и удали только его устаревшие assets, затем заново создай каталог и повтори публикацию. Опубликованный релиз сохраняй; для изменённых бинарников увеличь версию.
- GitHub и VPS не являются одной транзакцией: при сбое серверной проверки релиз может уже быть публичным, а VPS продолжит отдавать прежний каталог. Исправь причину и повтори публикацию тех же проверенных файлов. До переключения `current` старый каталог и дистрибутивы сохраняются.
- Для GitHub content/shell повтор тех же payload/sequence идемпотентен, опубликованные assets неизменяемы. Новый payload требует большей sequence; shell требует также большей shellVersion для существующих клиентов. Legacy VPS activation по-прежнему не принимает ту же sequence повторно.

## Проверки после публикации

```sh
version="$(node -p 'JSON.parse(require("fs").readFileSync("desktop/config.json", "utf8")).shellVersion')"
gh release view "v${version}" --repo afonasev/mindbattle
curl -fsS https://mindbattle.afonasev.tech/desktop/downloads.json
curl -fsSI https://mindbattle.afonasev.tech/
curl -fsS https://mindbattle.afonasev.tech/network >/dev/null
bash scripts/checkReleaseIdentity.sh
MINDBATTLE_TEST_ORIGIN=https://mindbattle.afonasev.tech node scripts/testNetworkApi.mjs
```

Для web-deploy проверь совпадение локального и серверного bundle через `checkReleaseIdentity.sh`, опубликованную дату в HTML и загрузку меню. Эта hash-проверка относится только к `server-dist/network.js`; она не доказывает целостность установщиков или всех web-ассетов.

Для desktop-релиза прочитай каталог обратно, сравни версию/URLs/размеры/SHA-256 с локальным, проверь публичное скачивание обеих ОС и отсутствие EXE/DMG в VPS installer-каталоге. После content/shell публикации отдельно проверь соответствующие `https://afonasev.github.io/mindbattle/desktop/content/latest.json` и `https://afonasev.github.io/mindbattle/desktop/shell/{darwin-universal,win32-x64}/latest.json`, а также подписанные объекты GitHub Releases. При legacy-shell отдельно прочитайте старый VPS feed. В браузере проверь ссылку своей ОС; уже открытая PWA может сначала предложить применить загруженное обновление. Мобильная PWA не показывает desktop-download.

## Установка и ручная приёмка

Windows: установка для всех пользователей в Program Files с UAC, без страницы выбора user/system; путь можно менять. На последнем экране вместе стоят отмеченные галочки запуска и создания ярлыка. Ярлык создаётся в Public Desktop, с иконкой игры; запуск выполняется для обычного пользователя. Проверь реальные opt-in/opt-out, иконку EXE/ярлыка/панели задач, запуск и удаление ярлыка при uninstall.

macOS: скопируй universal app из DMG в подходящую папку приложений; проверь запуск и иконку. Текущие установщики без developer-сертификатов/notarization. Packaging и cross-compilation не заменяют реальную установку на Windows/macOS, offline-play с физическим вводом, повторный запуск и N→N+1 с сохранением профиля. Физические проверки телефонов нужны при изменении соответствующего взаимодействия.

Content updater пишет в userData и работает при защищённой установке. Начиная с подготовленной оболочки 1.0.6 файловый helper при необходимости запрашивает UAC/системное подтверждение macOS; broker и игра остаются обычными процессами пользователя. Обновление не открывает обычный мастер установки. Реальные системные запросы и работа в защищённой установке требуют отдельной приёмки. DMG/translocation, недоступный путь, неисправимое повреждение или потеря питания во время замены также могут потребовать ручного восстановления. Не удаляй backup/journal незавершённой recovery-транзакции.

## Завершение выпуска

Запиши в shared planning change исходную ревизию, GitHub tag/URLs, каталог с хэшами, manifests, checks/smoke и отдельно pending human/platform acceptance. Сохрани необходимые screenshots и точные артефакты для приёмки; проверенный опубликованный GitHub asset с хэшем может быть постоянной копией установщика.

Прочитай `~/.codex/references/task-cleanup.md`. Удали только принадлежащие задаче staging/build-копии, временные логи/профили и dev-серверы после сохранения доказательств. Проверь Git/status, интеграцию и владельцев перед удалением worktree; чужие ресурсы сохраняй. Заверши технический lifecycle через helper `finalize`; без явной приёмки результат остаётся `awaiting-acceptance`, а архивирование требует отдельного разрешения и gates.

## Автоматическая проверка

Оболочка 1.0.6 делает один GitHub API discovery после открытия окна, с ETag-кешем. Ни таймера, ни online-retry, ни ручной проверки в сессии нет. Ошибка сообщает, что следующая попытка будет при новом запуске. «Обновить» начинает выбранный download, доступны прогресс/отмена/retry; перед матчем загрузка и история останавливаются. Готовый пакет применяется при следующем обычном запуске либо по «Перезапустить» в безопасном меню. «Что нового» доступно независимо от новой версии: до 8 последних релизов плюс установленная. Новый content использует bridge=2 и требует shell >=1.0.6: прежние оболочки не должны получать новый UI/API через content-only публикацию. Pages feeds сохраняются для перехода legacy клиентов; новые стабильные releases не помечаются prerelease. Точное подключение и 30 OPT: [CONNECTION.md](../template-alignment/CONNECTION.md).

Тихий запуск установленной игры: `/Applications/Mindbattle.app/Contents/MacOS/Mindbattle -muted`; Windows PowerShell: `& 'C:\Program Files\Mindbattle\Mindbattle.exe' -muted`. Из исходников: `npm run desktop:start -- -muted`; старый `--muted` остаётся alias. Автоматические browser checks используют `?muted=1` и Chromium `--mute-audio` до autoplay. При обновлении сохраняются CLI-аргументы и профиль. Новое имя Windows-пакета: `Mindbattle-<version>-win-x64.exe`.
