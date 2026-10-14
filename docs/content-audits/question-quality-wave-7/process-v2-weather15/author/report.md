# Авторская проверка: Weather/Climate, 15 карточек

Source baseline: `069743068e800cca9a703c6c8621c3c1fcedb3e4`; repository HEAD был `8430a70541f7aa5d74b385f0741d3b79477a36f9`. Ровно 15 ID из `preimage.json`; ID, topic/order, difficulty и correctIndex сохранены.

## Статусы

- FIX: tropical depression, tropical storm, hurricane, orographic rain, rain shadow, humidity, pressure, Koppen A/B/C/E — 11 карточек.
- HOLD: cirrus, cumulonimbus, climate long term, frontal rain — 4 карточки. По каждой HOLD запись содержит точный недостающий факт и действие в `candidate.json`; они не блокируют FIX.

## Источники

Проверены сохранённые bodies из Git: NWS Key Glossary, NWS Basic Fronts, NOAA Ocean Service windward/leeward, NOAA NESDIS climate types, NOAA JetStream climate zones и NOAA rain-shadow PDF. SHA-256 и размеры сверены с source index. Для NOAA climate zones commit:path из индекса недоступен, поэтому прочитан указанный git blob `4f89c317db15aee4c6362f60b38d87694cc7fe38`; длина и SHA совпали с индексом.

PDF прочитан через bundled `pypdf` без новой загрузки: 22 страницы. Страница 2 прямо описывает осадки на наветренной стороне и сухой воздух, спускающийся по другой стороне. NWS Glossary независимо определяет rain shadow как сухую подветренную сторону с малым/нулевым количеством осадков.

## Сверки

Manifest включает beforeCard/beforeHash, proposedCard/afterHash, шесть literal-групп с SHA-256, конкретные sourceReasons/editorialReason, sourceLocators, defects и neighborReview. Frozen-инварианты проверены. Локальная проверка JSON, хешей literal-групп/карточек, frozen-полей и пробелов пройдена. Runtime, full QA, build и deploy не запускались.

Следующий исполнитель: координатор exact-applies только 11 FIX-карточек, затем передаёт их независимому CURRENT-reader; 4 HOLD остаются с конкретными действиями в manifest. Авторский FIX не является независимой проверкой или приёмкой CURRENT.
