# Публикация Mindbattle

Каноническая инструкция для сайта, установщиков и обновлений установленной игры. Исходники и установщики публикуются в публичном репозитории [afonasev/mindbattle](https://github.com/afonasev/mindbattle). Публикация требует разрешения пользователя на соответствующую среду; сборка, Git push и запись этой инструкции сами по себе его не дают.

## Что публикуем

| Изменение | Подготовка | Публикация |
|---|---|---|
| Сайт / PWA | `npm run build` (включён в deploy) | `make deploy` |
| Игра, вопросы, JS/CSS, музыка и другие content-ассеты для установленной игры | `npm run desktop:content` | `bash scripts/desktop/publish.sh content` |
| Electron, main/preload, native updater или другие файлы оболочки | Новая `shellVersion`, content, оба установщика и `npm run desktop:shell` | `publish.sh content`, `publish.sh shell`, `publish.sh installers` |
| Только оформление / поведение установщика | Новая `shellVersion`, content, оба установщика и `npm run desktop:catalog` | `publish.sh installers`; shell/content отдельно, если они входят в разрешённую поставку |

`make deploy` не собирает и не публикует desktop-дистрибутивы. GitHub Release с установщиками не обновляет content/shell каналы автоматически. Для выпуска игры одновременно на сайте и установленным клиентам нужны обе соответствующие публикации. Обычная правка игры не требует пересборки установщиков.

## Где находятся версии и файлы

- `package.json` → `version`: версия самой игры. Публикационный build добавляет идентификатор содержимого; UI показывает номер без хэша.
- `desktop/config.json` → `shellVersion`: версия оболочки и установщиков. Для нового комплекта увеличивай её; это же номер тега `v<shellVersion>`. Не переиспользуй опубликованный тег для других бинарников.
- Windows: `Mindbattle-<shellVersion>.exe`; macOS: `Mindbattle-<shellVersion>-mac-universal.dmg` (Intel + Apple Silicon).
- `desktop-release/installers/downloads.json`: каталог с версиями, HTTPS GitHub URLs, размерами и SHA-256 для обеих ОС.
- GitHub Releases хранит версионные установщики. На VPS `/var/lib/mindbattle-desktop/installers/current` хранится только каталог; EXE/DMG туда больше не загружаются.
- Подписанные content и shell обновления остаются на VPS в `/var/lib/mindbattle-desktop/{content,shell}/current`. Их нельзя удалять при очистке установщиков. Эти данные находятся вне `/opt/mindbattle` и области `rsync --delete` web-deploy.

## Подготовка выпуска

1. Работай в worktree/ветке своей задачи. Обнови нужную версию, проверь согласованный scope, текущие Git refs и опубликованные каталоги. Сохрани чужие изменения.
2. Нужны Node из `package.json`, `npm ci`, SSH-профиль `gfe`, `rsync` и авторизованный `gh` с правом писать Releases в `afonasev/mindbattle`. Для сборки обоих установщиков на macOS нужны Go и `lipo` (native helper), несколько ГБ свободного места.
3. Используй существующий Ed25519 private key вне репозитория, совпадающий с `desktop/content-public.pem`. Не выводи ключ и не клади его в Git, артефакты или VPS web-root. `npm run desktop:key` предназначен только для первого создания ключа; новый ключ не заменяет pin существующих установок.
4. Задай один UTC timestamp для всего выпуска **до** `desktop:content` и повторно используй его при web-deploy. Иначе offline-игра покажет «Ещё не опубликована» или даты сайта и установщика разойдутся.

```sh
set -euo pipefail
export MINDBATTLE_CONTENT_KEY=/secure/path/content-signing.pem
export MINDBATTLE_PUBLISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# DEPLOY_HOST при необходимости меняет SSH-профиль; по умолчанию gfe.
gh auth status
ssh -o BatchMode=yes "${DEPLOY_HOST:-gfe}" true
npm ci
npm run check
npm run test:desktop
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

Публикация content/shell отдельно проверяет объекты и монотонность sequence, переключает `current` под lock и удаляет предыдущий завершённый релиз этого канала. Клиентская last-good/rollback копия независима от retention сервера.

Для каждого выпуска подготовь актуальные release notes с его изменениями и ограничениями приёмки. Сейчас `publish-github.mjs` использует фиксированный текст про Windows-установщик; он не описывает автоматически будущие изменения. После успешной публикации обнови описание из подготовленного файла:

```sh
# Подставь существующий файл с описанием именно этого выпуска.
version="$(node -p 'JSON.parse(require("fs").readFileSync("desktop/config.json", "utf8")).shellVersion')"
gh release edit "v${version}" --repo afonasev/mindbattle --notes-file /absolute/path/release-notes.md
```

## Если публикация прервалась

- Повтори `publish.sh installers` с той же ревизией и **теми же файлами/каталогом**: отсутствующие assets будут загружены, существующие — проверены. Путь повторения работает, пока релиз присутствует среди последних 100 записей GitHub API, которые читает скрипт.
- Несовпадение хэша/размера останавливает публикацию; скрипт не перезаписывает существующий asset. Не обходи проверку и не удаляй рабочие VPS-файлы вручную.
- Если пришлось пересобрать ещё не опубликованный **собственный draft**, проверь его статус/владение и удали только его устаревшие assets, затем заново создай каталог и повтори публикацию. Опубликованный релиз сохраняй; для изменённых бинарников увеличь версию.
- GitHub и VPS не являются одной транзакцией: при сбое серверной проверки релиз может уже быть публичным, а VPS продолжит отдавать прежний каталог. Исправь причину и повтори публикацию тех же проверенных файлов. До переключения `current` старый каталог и дистрибутивы сохраняются.
- Для content/shell после уже успешной активации та же sequence не принимается повторно. Сначала прочитай текущий manifest; новый выпуск требует большей sequence.

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

Для desktop-релиза прочитай каталог обратно, сравни версию/URLs/размеры/SHA-256 с локальным, проверь публичное скачивание обеих ОС и отсутствие EXE/DMG в VPS installer-каталоге. После content/shell публикации отдельно проверь соответствующие `/desktop/content/latest.json` и `/desktop/shell/{darwin-universal,win32-x64}/latest.json`. В браузере проверь ссылку своей ОС; уже открытая PWA может сначала предложить применить загруженное обновление. Мобильная PWA не показывает desktop-download.

## Установка и ручная приёмка

Windows: установка для всех пользователей в Program Files с UAC, без страницы выбора user/system; путь можно менять. На последнем экране вместе стоят отмеченные галочки запуска и создания ярлыка. Ярлык создаётся в Public Desktop, с иконкой игры; запуск выполняется для обычного пользователя. Проверь реальные opt-in/opt-out, иконку EXE/ярлыка/панели задач, запуск и удаление ярлыка при uninstall.

macOS: скопируй universal app из DMG в подходящую папку приложений; проверь запуск и иконку. Текущие установщики без developer-сертификатов/notarization. Packaging и cross-compilation не заменяют реальную установку на Windows/macOS, offline-play с физическим вводом, повторный запуск и N→N+1 с сохранением профиля. Физические проверки телефонов нужны при изменении соответствующего взаимодействия.

Content updater пишет в userData и работает при защищённой установке. Native shell updater требует writable installation и не повышает права; в защищённой Program Files обновление оболочки может потребовать нового установщика. DMG/translocation, недоступный путь, неисправимое повреждение или потеря питания во время замены также могут потребовать ручного восстановления. Не удаляй backup/journal незавершённой recovery-транзакции.

## Завершение выпуска

Запиши в shared planning change исходную ревизию, GitHub tag/URLs, каталог с хэшами, manifests, checks/smoke и отдельно pending human/platform acceptance. Сохрани необходимые screenshots и точные артефакты для приёмки; проверенный опубликованный GitHub asset с хэшем может быть постоянной копией установщика.

Прочитай `~/.codex/references/task-cleanup.md`. Удали только принадлежащие задаче staging/build-копии, временные логи/профили и dev-серверы после сохранения доказательств. Проверь Git/status, интеграцию и владельцев перед удалением worktree; чужие ресурсы сохраняй. Заверши технический lifecycle через helper `finalize`; без явной приёмки результат остаётся `awaiting-acceptance`, а архивирование требует отдельного разрешения и gates.
