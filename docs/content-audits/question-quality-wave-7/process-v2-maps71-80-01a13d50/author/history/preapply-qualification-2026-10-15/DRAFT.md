# Авторский пакет: картография, source order 71–80

Baseline `ae703cae08757ee1b4b5c6aa8acaabed91e9c850`; ровно десять заданных ID, `topicId`, `sourceOrder`, `difficulty` и `correctIndex` сохранены. Quality credit: 0.

Статусы: FIX — 71–77; HOLD — 78–80. Пять hard-вопросов перестроены в прикладные решения по двум projection constraints, правилу сплошной полигональной поверхности и направлениям Trim/Extend. Два лёгких contour-вопроса сохранили короткий уровень и получили полезные самостоятельные заметки.

Ортографическая, Lambert azimuthal, оба Esri topology и ранее сохранённые GeographicLib/Esri projection contexts восстановлены/read полностью, с provenance, coverage, byte SHA и exact locators в `sources/` и `sourceproof.json`. Для hill/valley прочитаны сохранённые USGS и OS первичные материалы.

`peer-snapshot.json` содержит все десять exact target current/proposed versions и whole-card/hash records из hard5 terminal, medium9 certified, scale/grid new3, prepared GIS6 cycle1 и historical2 CURRENT. Для каждого target записан направленный inbound/outbound смысловой риск.

HOLD для atlas/globe/wall-map: в доступном source set нет полного пригодного primary контекста для всех утверждений вариантов и заметок. Точные запросы перечислены в `needed-evidence.json`. Статус FIX означает авторскую правку, не независимую приёмку. В Git и каталог не писалось; тесты, runtime, build и audio не запускались.
