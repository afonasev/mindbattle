Авторский приоритетный Snow corrective выполнен read-only; в primary checkout ничего не менял. Проверен owned worktree /Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle, branch codex/question-quality-wave-6, HEAD 90fa307db3c888c3b1112f9a9c86083d7a1b08c2. Текущий weather file: 173826 bytes, SHA-256 6a34b95224f9bc8758979098aaf099ef13ef7f80148793dc45f92a6d9e136597; исходный Snow card SHA d04ce9ec980b9f7537eaccb63aa5db600bfef3e32043566496aaaca94ff4e9ee совпал со scope.

Snow авторская рекомендация, только изменение prompt; exact ID/order/difficulty/key/options/explanation/notes/source сохраняются:
{
  "id":"weather-climate-snow-crystals",
  "difficulty":"easy",
  "prompt":"Какая форма осадков выпадает в виде множества отдельных ледяных кристаллов?",
  "answers":[
    {"text":"Снег","note":"Снег образуется непосредственно из водяного пара; отдельные кристаллы имеют разветвлённую форму."},
    {"text":"Дождь","note":"По определениям NWS, дождевые капли имеют диаметр более 0,5 мм, а капли мороси — менее 0,5 мм."},
    {"text":"Град","note":"Градины обычно представляют собой ледяные шарики или неправильные кусочки льда."},
    {"text":"Мокрый снег","note":"Мокрый снег — снег и дождь одновременно, причём преобладает снег."}
  ],
  "correctIndex":0,
  "explanation":"Снег состоит из ледяных кристаллов, которые часто срастаются в снежинки. Их форма зависит от условий роста в облаке.",
  "source":{"title":"NOAA National Weather Service Glossary: Snow","url":"https://forecast.weather.gov/glossary.php?word=SNOW","verifiedAt":"2026-10-13"}
}
Новый canonical card SHA-256: a38684312bcf86e7cafd6884e0c546c8208e388f48bf887ad76b42e4c5844f4f. Recipe: SHA-256 UTF-8 json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')); no trailing newline. Six literal group values/hashes:
prompt+ordered answer texts+key (object {prompt, answers:[texts in order], correctIndex}): 9d7d72211e69f3cb0dd230dbe64e2f0f2a072e4b81d36690797cf83589b1e765
explanation (JSON scalar): 8529c59d6ad892e0e0da68dd95edeca86f46fd2ad95298139fdf162ac00803f0
answer notes 0..3 as JSON string scalar hashes, in order: 1b46b4985f038349dc169b9b0215063b026abba48e5e5071443f589672d1074a; f492e27205917acd87f1b1c028192a20f9406c7f09ff7b9a90ca5e525e7f19b1; 3ebc47162e7434db1a2f4e1f187bd2e50ed3698cf676a847d2d09b81b0a9383f; 72f966328e74969d81ded8127ae939f8eb15573b547b23f3b7569bd3eb06a3a0.
Auxiliary metadata hashes: difficulty 3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703; full source metadata 41a4a524449535462df3124c95e8b3a9b4ca0bb58cda12d84798fea933eb35af.

Six independent editorial reasons: (1) stem removes the direct Russian lexical/root cue “снежинки” while directly testing the definition; snow is crystal precipitation, rain liquid drops, hail pellets/balls, wet snow rain-snow mixture. (2) explanation is supported by NWS snow definition and NWS cloud-development capture on ice crystal arms/aggregation. (3) keyed note adds direct vapor deposition and branching, both in NWS snow definition beyond answer label. (4) rain note distinguishes NWS drop threshold (&gt;0.5 mm) from drizzle (&lt;0.5 mm); supported by saved NWS Rain and Drizzle sources. (5) hail note agrees with saved NWS Hail definition of ice pellets/balls. (6) wet-snow note agrees with saved Meteoinfo Russian terminology row: simultaneous rain and snow, snow predominates, with thawing snow synonym.
Difficulty stays easy: familiar direct recognition, no computation or specialist inference. Source metadata stays unchanged: saved exact NWS Snow glossary source is directly authoritative for key and verifiedAt already matches this saved capture. No other field needs changing.

Saved-source binding: exact body paths, bytes/SHA and headers are in the shared first10 manifest docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/source-manifest.json. Snow body 11384 / 55f252aa2e7060357d8f7c87d78bfa0f65d7a2410ce780ff424154216c29ed6f; headers 1024 / fbc3123389b959f2421d4e4635ba4df6e40dc914adc5acb252a77ad5daf990d8. NWS cloud-development body 46017 / e1bc3c932198a78331ce8b54352109d47d0cc0e1decd155a474be392ba06beda; headers 1159 / 1aa07a4b75bd660ee16b27ccdc7b97614a740a20d3105ee86ec49ec005078efb. NWS Hail body 4421 / baa563a27c65783316ff4bdc6eae9b85e0d9a9166ca8cbecb73e8af522792499. Rain body 11482 / 69efbae454a31f30fcc240d43e8fe4bb3c1261efb80f2953d8dd24e52c69f246. Meteoinfo body 65113 / 2011bcaeffd8e3dc8270da507479a8bdc37d7f37b67b95bd6b5706a1c12f52da. Saved source passages v2 records half-open raw offsets, raw/context hashes, and exact whitespace-normalization recipes; Snow definition raw bytes 5015..5222 hash ba908b4748780faeb8d29b12c520b593cef46ee9daa80978e2f1510bccfa78a7, context hash 0561c00d6a4cc24ee6a10355ebddf074510c1a17292b60681a94dc1c974b3290. Crystal-growth passage context hash c2354a36674beada107cdd2ef7651e44030f93882efbfdd7c8a9baed31ae0d2d; exact source object in saved source-passages-v2.json.

Full 29 neighbor objects can be referenced from saved full native original docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13619/weather9-authorff-original/original-native-payload.json and supplement docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13619/weather9-authorff-supplements/native-385-payload.json; Snow target-specific saved comparison is in native-385-payload.json. That comparison covers Bergeron/riming (microphysical processes), cirrus/cumulus/cumulonimbus/stratus (cloud types), warm-cloud collision (rain formation), oceans-seas precipitation (broad category), plus selected rain/hail/wet-snow contrasts. I verified current raw file hash and all 90 protected other-card hashes: all match. Proposed target only changes prompt. No file writes, apply, separate reader, or credit: independent current-card reader remains pending; qualityCredit 0.

Next10 author continuation: scope exact 10 targets all match their frozen canonical SHA; 90 protected neighbors also unchanged. However there are no corresponding captured primary body/header artifacts in the saved weather-climate source package; only first10 precipitation sources are present. I therefore did not fabricate a full native/evidence-qualified packet or use network/recapture. Concrete proof gaps to resolve from saved first-full bodies:
- dew-point: https://en.wikipedia.org/wiki/dew_point (prefer a saved NOAA/NWS primary page); verify what dew point says about water-vapor content and whether “absolute content” is accurate.
- relative humidity: https://www.britannica.com/science/relative-humidity; verify percent-of-saturation and the constant-moisture cooling statement.
- wet bulb: https://www.britannica.com/technology/psychrometer; verify wet wick evaporation and psychrometer paired readings.
- heat index: https://en.wikipedia.org/wiki/heat_index (prefer saved NWS Heat Index primary page); verify apparent temperature from heat plus humidity and evaporative-cooling wording.
- adiabatic cooling: https://www.britannica.com/science/adiabatic-lapse-rate; verify unsaturated parcel expansion/cooling on ascent.
- inversion: https://www.britannica.com/science/temperature-inversion; verify temperature increasing with altitude within inversion.
- convection: https://www.britannica.com/science/convection; verify vertical heat transfer and buoyancy wording.
- subsidence: https://www.britannica.com/science/anticyclone; verify sinking-air compression/warming/drying and clearing.
- cyclone: https://www.britannica.com/science/cyclone-meteorology; verify low pressure, convergence/ascent, precipitation association, and Northern-Hemisphere rotation statement.
- anticyclone: https://www.britannica.com/science/anticyclone; verify high-pressure, subsidence/divergence, stable-clear-weather and Northern-Hemisphere rotation.
Potential precise issue to qualify first: dew point “absolute moisture content” may overstate a temperature metric as absolute humidity. No next10 text is proposed as verified yet.