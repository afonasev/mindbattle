# Матрица соответствия

Ревизия: a4ee2d8. Это карта реализации и оставшихся gates, а не декларация ручной приёмки.

| ID | Требование | Реализация / проверка |
|---|---|---|
| MENU-STRUCTURE-01 | Главное меню | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-STRUCTURE-02 | Дополнительные маршруты | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-STRUCTURE-03 | Доступность действий | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-INPUT-01 | Три способа управления | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-INPUT-02 | Значение кнопок геймпада | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-INPUT-03 | Единственный получатель ввода | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-INPUT-04 | Защита переходов | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-INPUT-05 | Поля ввода | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-FOCUS-01 | Видимый и осмысленный фокус | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-FOCUS-02 | Восстановление контекста | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-FOCUS-03 | Раскрытие выбранного элемента | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-DEVICE-01 | Переключение устройства | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-DEVICE-02 | Указатель мыши | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-HINTS-01 | Только геймпад | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-HINTS-02 | Подсказка на экранном действии | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-HINTS-03 | Соответствие поведению | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-LAYOUT-01 | Повторяющиеся действия | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-LAYOUT-02 | Экран без прокрутки | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-LAYOUT-03 | Поддерживаемые размеры | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-STATE-01 | Ошибки в визуальном языке игры | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-STATE-02 | Выполняющиеся операции | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| MENU-PAUSE-01 | Игровое меню и полномочия | menuNavigation.ts, menuUi.tsx и menu surfaces; browser keyboard/virtual-pad checks; полный физический проход — pending |
| SETTINGS-BASE-01 | Наследование базового меню | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-ENTRY-01 | Главное и игровое меню | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-CATALOG-01 | Полный применимый каталог | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-GROUPS-01 | Смысловые разделы | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-SCOPE-01 | Предпочтения отдельно от баланса | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-CONTROL-01 | Тип элемента | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-CONTROL-02 | Контракт параметра | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-CONTROL-03 | Область действия | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-PERSIST-01 | Автоматическое применение и сохранение | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-PERSIST-02 | Отложенное применение | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-PERSIST-03 | Ошибки и совместимость | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-DISPLAY-01 | Безопасная смена экрана | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-AUDIO-01 | Громкости вместо отдельного mute | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-AUDIO-02 | Технический тихий запуск | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-RESET-01 | Область сброса | PresentationSettings.tsx, DesktopControls.tsx, storage/audio.ts, display.mjs; unit/native/browser tests; device/audio acceptance — pending |
| SETTINGS-RESET-02 | Shortcut геймпада | N/A: дополнительный shortcut сброса не назначен; обычные screen actions доступны всем устройствам |
| SETTINGS-HELP-01 | Отдельная графическая справка | PresentationSettings.tsx + public/images/controls-devices-v1.png; browser screenshots; физический pad — pending |
| SETTINGS-HELP-02 | Страницы устройств | PresentationSettings.tsx + public/images/controls-devices-v1.png; browser screenshots; физический pad — pending |
| SETTINGS-HELP-03 | Генерируемые изображения | PresentationSettings.tsx + public/images/controls-devices-v1.png; browser screenshots; физический pad — pending |
| SETTINGS-HELP-04 | Только игровое управление | PresentationSettings.tsx + public/images/controls-devices-v1.png; browser screenshots; физический pad — pending |
| SETTINGS-HELP-05 | Точность назначений | PresentationSettings.tsx + public/images/controls-devices-v1.png; browser screenshots; физический pad — pending |
| SETTINGS-HELP-06 | Читаемость и проверка | PresentationSettings.tsx + public/images/controls-devices-v1.png; browser screenshots; физический pad — pending |
| INSTALLER-PACKAGE-01 | Готовая поставка | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-IDENTITY-01 | Единая иконка | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-FLOW-01 | Понятная установка | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-FLOW-02 | Предварительные проверки | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-RIGHTS-01 | Минимальные права | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-TRUST-01 | Подпись и тестовая поставка | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-CONTENT-01 | Полный состав и точка входа | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-CONTENT-02 | Сведения об установке | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-LAUNCH-01 | Штатный запуск | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-DATA-01 | Разделение приложения и данных | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-REINSTALL-01 | Повторная установка | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-REINSTALL-02 | Работающая игра и каналы | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-RECOVERY-01 | Отмена и сбои | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-REMOVE-01 | Удаление | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-ARGS-01 | Параметры и тихий запуск | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-QA-01 | Проверки по изменениям | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| INSTALLER-RELEASE-01 | Публикация без полного регресса | electron-builder.yml, installer.nsh, RELEASE.md; реальная установка/удаление и платформенная приёмка — pending |
| UPDATES-SOURCE-01 | GitHub Releases | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-SELECT-01 | Подходящая версия | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-CHECK-01 | Проверка только при запуске | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-CHECK-02 | Сеть и лимиты | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-CONSENT-01 | Фиксированное поведение без настроек | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-FLOW-01 | Игра и несохранённая работа | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-UI-01 | Состояния в главном меню | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-DOWNLOAD-01 | Отдельная подготовка | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-HISTORY-01 | «Что нового» на языке игры | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-CHANGELOG-01 | Двуязычное описание релиза | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-TRUST-01 | Подлинность и целостность | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-INSTALL-01 | Целостная установка | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-INSTALL-02 | Бесшовное применение | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-DATA-01 | Сохранность данных | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-RECOVERY-01 | Возврат к рабочей версии | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-ARGS-01 | Параметры после обновления | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-RELEASE-01 | Полный и неизменяемый выпуск | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
| UPDATES-QA-01 | Приёмка и публикация | desktop/releases.mjs, updateCheck.mjs, content.mjs, shell.mjs, updater/; Node/Go fixtures; реальная установка N→N+1/аварии — pending |
