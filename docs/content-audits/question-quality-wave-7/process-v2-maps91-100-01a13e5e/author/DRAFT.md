# Author draft: maps-cartography 91–100

Baseline: `6d679c25615ed1a8a582fbc57113cb36d8be0a5f`. Exact preimage matched all ten cards in the baseline and CURRENT catalog.

## Proposed status

- 91 `maps-cartography-direction-distortion` — FIX; Ученик переносит проекционное свойство на задачу полярной навигационной карты и ограничивает его именно центром; четыре свойства нужно различить по области действия.
- 92 `maps-cartography-generalization-select` — FIX; Задача требует применить два независимых преобразования к слою и соблюсти третье ограничение — не разрушить связность; это содержательное применение генерализации, а не воспроизведение определения.
- 93 `maps-cartography-classification-groups` — FIX; Нужно выбрать классификацию по одновременно заданным ширине диапазона и равному числу классов, отделив её от квантилей и естественных границ; это практическая настройка тематической карты.
- 94 `maps-cartography-symbolization-style` — FIX; Пользователь должен сопоставить тип измерения (категориальный) с методом символизации и отличить его от количественного кодирования; это реальное решение дизайна тематического слоя.
- 95 `maps-cartography-label-placement` — FIX; Ситуация требует настроить очередность и разрешение столкновений одновременно, а также предсказать действие движка для низкоприоритетной подписи; это практическая картографическая настройка.
- 96 `maps-cartography-dangling-node` — FIX; Нужно применить два самостоятельных условия: выбрать линейное правило связности и отделить разрешённые тупики от незапланированного окончания; одного знания термина dangle недостаточно.
- 97 `maps-cartography-graticule` — FIX; Решение требует различить две независимые вещи: полные линии географической сетки и граничные засечки; дополнительно выбрать правильный компонент карты, а не только название системы координат.
- 98 `maps-cartography-neatline` — FIX; Нужно отличить географическую границу данных от физической рамки map frame и от подписей координат, затем применить нужное оформление; это два независимых ограничения задачи макета.
- 99 `maps-cartography-tic-mark` — FIX; Кандидат должен соотнести требование «только отметки на границе» с компонентом рисок и отвергнуть три соседних, но функционально разные компонента карты; это применение компонентной структуры.
- 100 `maps-cartography-declination-diagram` — FIX; Ученик должен различить ориентирующее схематическое изображение и три похожих элемента рамки/координатной сетки, а затем верно интерпретировать три типа севера и углы между ними.

## Evidence and limits

- Full captured source bodies, provenance, byte hashes, locators, six-group hashes, four answer/note rationales, and difficulty bases are in the adjacent JSON files.
- SourceRegister points to shared full contexts in place; common USGS PDFs and earlier ArcGIS captures are not duplicated.
- Peer snapshot separates CURRENT cards from 71–75 author-cycle1 proposals. All comparisons use exact proposed text.
- Quality credit remains zero pending coordinator application and independent review.
- No catalog, planning, claim, index, staging, commit, runtime, test, build, or deployment action was performed.
