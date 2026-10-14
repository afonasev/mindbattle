# Авторский пакет: Weather × 20

Baseline commit: `069743068e800cca9a703c6c8621c3c1fcedb3e4`. Проверено: ID, тема, порядок ответов, difficulty и correctIndex сохранены. Канонические hashes вычислены как sorted compact UTF-8 JSON с Unicode.

Все 20 карточек получили адресный `FIX`: обновлены содержательные заметки и объяснения, уточнены диагностические формулировки и заменены неподходящие вторичные ссылки. Для 12 использованных индексированных первичных контекстов считаны сами immutable bodies и сверены byte count/SHA-256; Git refs, которых нет в checkout, разрешены через `git cat-file blob` из общего object store. В частности, NOAA climate-zones body прочитан по blob `4f89c317db15aee4c6362f60b38d87694cc7fe38`, его SHA/bytes совпали с индексом; тело не скачивалось повторно. Для NOAA JetStream Weather Satellites и Met Office Climate Zones сохранены полные HTML bodies и HTTP response headers в `author/sources/`. Ответы пришли порциями HTTP 206 после ограничения обычной загрузки до 12 288 байт; диапазоны покрывают полный размер ответов, ETag NOAA не менялся. Размеры, SHA-256, ETag/Last-Modified и карта locator-ов записаны в `author/sources/manifest.json`. Сами сохранённые тела прочитаны по нужным разделам. NWS weather-satellite glossary query не содержал определения, поэтому NOAA JetStream является официальной альтернативой для спутников.

## Итоги
- `weather-climate-trade-winds-tropics` — FIX; after `993b24ca9d22d8713ea32f22a61a29bdcefa6430d3df66e3b33d9a9d1823d859`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-westerlies-midlat` — FIX; after `0024be25f045cb5f1034855895c31a2dd823191e428b9861196d43082e95acba`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-polar-easterlies` — FIX; after `1d1016c235d5aa28847b8481bba999987a252a8c7efd94a629f0dfd3bebcf247`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-cin-cap` — FIX; after `96c3500b56dffe1870d083d0bc7924f9a8f88d019c39c670f1cb6816a09e6109`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-lifted-index` — FIX; after `7ca9b428ba8fb1ac7f60f24ab1b6f855f579ee0cd5d24ed08bce1ebf39fff960`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-helicity-rotation` — FIX; after `0efe0aaab6fc99f035dae088d5f4d65fb4a880324aa0135791fcbbe182f9cb29`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-warm-cloud-collision` — FIX; after `4effa44307539cfd41c2262d72a42cf7cf3940e92aa367a7b503f43c9860a850`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-bergeron-ice` — FIX; after `48f0a289114c236050ea63c2c56f8b2fccdd4ba2db2bf6ad5bd6daeb4c7e7068`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-desert-dry` — FIX; after `6c0df9437f5f272f7ed0229ebdfbe525f009bd5c953c7c3dd4fc863a928b1c1a`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-polar-cold` — FIX; after `c2fe012bbafe42387ba7029bdd82bbc631dedf0d7e3ea43e7a918d1828a28ff7`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-warm-front-symbol` — FIX; after `bafd89f5061fd2bceb14c219417d782b0b8cb43f81bf785cb679df0368874e51`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-cold-front-symbol` — FIX; after `54b25612ce75a50cad98b85d4feea0295475b9a76dea1e50a0ac82b60d90fac1`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-stationary-front` — FIX; after `b218d139e0ca92d1861c28fb392d74e257fc065d94fea19fd997fa8d22913d11`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-occluded-front` — FIX; after `eb8d402ae939e0d6d66131d6ff37bd5eeac9df4eff0a8393f7b9917f2def4097`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-cumulus-puffy` — FIX; after `44c7db67db0e52dbffeef0a3098417b4609165495496265cb433d5b7024c0c68`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-stratus-layer` — FIX; after `cc152e7740cbdc8a44fcaf19a68428747fc9cf731c65da4c74e76556381bc017`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-radar-precipitation` — FIX; after `d409094dbda5ffb8f54e2019be5bdbd847e181ad1e3832a924b603339b45ad2a`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-radiosonde-balloon` — FIX; after `8e3cd306a908a8c66068ee0d64b3af08972ddd7a8e04ae07b15a1f2d7a4c3fb6`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-ceilometer-cloud-base` — FIX; after `8179b1f02e49353c3b45b4b2272f5ca08fca3d4ba5cf5113e045ef93c171f55a`; соседние карточки просмотрены по смысловым кластерам.
- `weather-climate-satellite-clouds` — FIX; after `389ae040692f11d2768bb93f80dd80073f5422f15cdeb9e75e66923d49bcd7f5`; соседние карточки просмотрены по смысловым кластерам.

## Ограничения источников

- NOAA JetStream satellites body: `author/sources/noaa-weather-satellites.body`; Met Office climate zones body: `author/sources/metoffice-climate-zones.body`. Полные headers, размеры и SHA-256 — в `author/sources/manifest.json`.
- В карточке про радар вопрос ограничен доплеровской радиальной скоростью и картированием отражений; это точнее исходного широкого «движения зон осадков».
- Предложение не применено к каталогу и не является независимым review.
