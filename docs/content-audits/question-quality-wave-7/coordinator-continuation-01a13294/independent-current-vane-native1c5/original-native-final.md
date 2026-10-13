**PASS:** текущая карточка, все 6 групп, easy, метаданные и проверка дублей. Зачёт **+0** до ручного решения координатора.

Следующий шаг: координатор сохраняет полный JSON ниже в Git и выполняет ручную оценку. Файлы и TMP не создавались; actual compactions **1**.

```json
{
  "schema": "mindbattle.weather-vane.native-independent-current.v1",
  "nativeReaderId": "01a131c5-edfb-7b82-8ddf-bd88a8b95597",
  "authorNativeId": "01a1324b-98ce-7852-85aa-f53587883f00",
  "coordinatorId": "01a13294-7d84-7583-930d-02eb1c80eb45",
  "actualCompactions": 1,
  "scope": ["weather-climate-barometer-pressure"],
  "verdict": "PASS_CURRENT_ONE_CARD",
  "qualityCredit": 0,
  "workdir": "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle",
  "sourceWorktreeReadonly": true,
  "filesWritten": [],
  "testsOrBuilds": [],
  "observedHEAD": "6bea69b0f43a8f52894d7be9e45716c7ac65a5ac",
  "currentWholeCard": {
    "id": "weather-climate-barometer-pressure",
    "difficulty": "easy",
    "prompt": "Как называется прибор на метеостанции, который показывает направление, откуда дует ветер?",
    "answers": [
      {
        "text": "Барометр",
        "note": "Барометр измеряет атмосферное давление."
      },
      {
        "text": "Термометр",
        "note": "Термометр измеряет температуру воздуха."
      },
      {
        "text": "Осадкомер",
        "note": "Осадкомер измеряет количество выпавшего дождя."
      },
      {
        "text": "Флюгер",
        "note": "Ветер называют по стороне, откуда он приходит: северный ветер дует с севера."
      }
    ],
    "correctIndex": 3,
    "explanation": "Флюгер показывает направление ветра, а анемометр измеряет его скорость. В метеорологии «северный ветер» означает поток, приходящий с севера.",
    "source": {
      "title": "NOAA JetStream: Origin of Wind",
      "url": "https://www.noaa.gov/jetstream/synoptic/origin-of-wind",
      "verifiedAt": "2026-10-13"
    }
  },
  "wholeCanonicalSHA256": "6d6ab1fbacb53b3b90a95c8c889383bf3e17a968d21c831633a87e9aed171970",
  "hashRecipes": {
    "wholeAndComposite": "SHA256 of UTF8 JSON sorted keys, ensure_ascii=False, compact comma/colon separators, no newline.",
    "scalarGroups": "SHA256 exact scalar UTF8 without JSON quotes or trailing newline.",
    "authorHashDifference": "Author scalar hashes use canonical JSON including quotes; independently declared exact-scalar hashes intentionally differ."
  },
  "currentTopic": {
    "observedSHA256": "29ba8f76ed2065eb33a85358b65369f01cc0791ecb48f059bf2a7525f1737a2d",
    "suppliedLaunchSHA256": "82f4c291ee1b8aaddcb1bf1fdc0b0a6168b431b2ba5c1e98308d5d3939ec135b",
    "intakeSHA256": "29ba8f76ed2065eb33a85358b65369f01cc0791ecb48f059bf2a7525f1737a2d",
    "launchTopicMismatchPreserved": true,
    "cardCanonicalMatchesLaunchAndIntake": true,
    "diskEqualsHEAD": false,
    "other99EqualTo5250100Verified": true,
    "onlyChangedCardVs5250100": "weather-climate-barometer-pressure",
    "interpretation": "Current scoped card matches exact authorized canonical. Topic-byte mismatch and current uncommitted source are disclosed; no whole-topic certification or repair."
  },
  "sixGroups": [
    {
      "group": "prompt-all4-ordered-texts-index-explicitKey",
      "currentLiteral": {
        "prompt": "Как называется прибор на метеостанции, который показывает направление, откуда дует ветер?",
        "orderedAnswerTextStrings": ["Барометр", "Термометр", "Осадкомер", "Флюгер"],
        "correctIndex": 3,
        "keyText": "Флюгер"
      },
      "sha256": "3f95d3f09bee0f58c89d99022420e6f1e2eb8f841249b8fa25948777dfecd3b5",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The full NOAA paragraph expressly assigns direction to a wind vane and speed to an anemometer. Four distinct station instruments form a credible comparison; barometer, thermometer and rain gauge measure different quantities. Key3 is unique; neither the name nor answer appears in the stem.",
      "proofRefs": ["NOAA-origin", "NOAA-vane-speed"]
    },
    {
      "group": "explanation",
      "currentLiteral": "Флюгер показывает направление ветра, а анемометр измеряет его скорость. В метеорологии «северный ветер» означает поток, приходящий с севера.",
      "sha256": "f4f531c9574d452ead070f00255171e9d96edb91d286be287053d087c0541378",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "Two concise sentences distinguish vane direction from anemometer speed and explain the meteorological origin convention. Applying the source's west-wind convention to north is a direct directional example, not an unsupported special fact.",
      "proofRefs": ["NOAA-origin", "NOAA-vane-speed"]
    },
    {
      "group": "note0",
      "currentLiteral": "Барометр измеряет атмосферное давление.",
      "sha256": "49deb486fc55985956a08979433ad55202e1dac750144eab37852ee76a54bc71",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The complete NWS Barometer entry states atmospheric-pressure measurement. The note supplies this distractor's real function, instead of merely denying that it measures direction.",
      "proofRefs": ["NWS-barometer"],
      "variant": "Барометр",
      "index": 0,
      "isKey": false
    },
    {
      "group": "note1",
      "currentLiteral": "Термометр измеряет температуру воздуха.",
      "sha256": "a2a135950b7d27280a3ec9dd2469eed0f5615a380e5152711df236e82e8ca9ca",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The complete NWS Thermometer entry specifies air-temperature measurement. The note gives this selected station instrument a specific positive function.",
      "proofRefs": ["NWS-thermometer"],
      "variant": "Термометр",
      "index": 1,
      "isKey": false
    },
    {
      "group": "note2",
      "currentLiteral": "Осадкомер измеряет количество выпавшего дождя.",
      "sha256": "11c9d899f2184c7672f1aba6d4ce9387a9b953045822ff070bdcd18c25b2dc54",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The complete Rain Gauge entry defines quantity of fallen rain. Russian осадкомер is broader than rain gauge, but the note accurately states its rain-measurement function without excluding other precipitation; no overclaim or alternative key.",
      "proofRefs": ["NWS-rain"],
      "variant": "Осадкомер",
      "index": 2,
      "isKey": false
    },
    {
      "group": "note3",
      "currentLiteral": "Ветер называют по стороне, откуда он приходит: северный ветер дует с севера.",
      "sha256": "f1541f7c880e88427365cf625758b1882a2f9e1f620a439553066869d278eb03",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The note adds the naming convention and north-wind example. The stem already specifies direction from which wind blows, but does not state that wind names refer to their origin or give the north example. This is an additional useful fact beyond prompt/key, not a repetition that a vane indicates direction.",
      "proofRefs": ["NOAA-origin"],
      "variant": "Флюгер",
      "index": 3,
      "isKey": true
    }
  ],
  "difficulty": {
    "currentLiteral": "easy",
    "scalarSHA256": "97c10efe01d5c9c88704a12d361d8429b3a6aa2412290a0773109d5d2d603d5e",
    "verdict": "PASS",
    "reason": "Familiar station-instrument function recognition, one direct correspondence with plausible neighboring instruments; no dates, calculation or specialist inference. Easy is substantively justified, not accepted merely because frozen."
  },
  "sourceMetadata": {
    "currentLiteral": {
      "title": "NOAA JetStream: Origin of Wind",
      "url": "https://www.noaa.gov/jetstream/synoptic/origin-of-wind",
      "verifiedAt": "2026-10-13"
    },
    "canonicalSHA256": "91cecdb634ce48951920708f72928b2c33eee6efb6d572c7ca554b7d395e47c4",
    "verdict": "PASS",
    "reason": "Original HTML title Origin of Wind | National Oceanic and Atmospheric Administration matches NOAA JetStream subject and exact capture URL. verifiedAt is capture/verification date, not a fresh-network claim. The linked page supports direction, speed contrast and origin naming; NWS originals independently support the distractor functions."
  },
  "sources": {
    "noaa": {
      "url": "https://www.noaa.gov/jetstream/synoptic/origin-of-wind",
      "bodyPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/weather-origin-wind-full-range-assembled.body",
      "bodyBytes": 120647,
      "bodySHA256": "f2b563bc770505e59b8726990598c38335c094dc4a4a3f03e8674351f54565e1",
      "manifestPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/weather-origin-wind-full-range-manifest.json",
      "manifestSHA256": "f4b54e63b874f3431006fa80be06f34f1be493830402fd2eb90264b988da4656",
      "originalPreservationCommit": "6eadc87",
      "capture": "15 contiguous HTTP206 responses, identical ETag \"1791886232\", assembled exact120647bytes; not a single200 response.",
      "rangeBodyAndHeadersVerification": "For all15: expected SHA/bytes in original manifest matched disk and HEAD Git; raw header status206, Content-Range start/end/120647 and ETag independently checked; concatenate original bodies equals assembled body and Git6eadc87.",
      "coverage": [
        [0, 8191],
        [8192, 16383],
        [16384, 24575],
        [24576, 32767],
        [32768, 40959],
        [40960, 49151],
        [49152, 57343],
        [57344, 65535],
        [65536, 73727],
        [73728, 81919],
        [81920, 90111],
        [90112, 98303],
        [98304, 106495],
        [106496, 114687],
        [114688, 120646]
      ],
      "personallyRead": "Full relevant article prose paragraphs81903..94868, including full wind-origin and vane/anemometer paragraphs and surrounding examples, pressure/force context.",
      "contexts": [
        {
          "id": "NOAA-origin",
          "rawByteRange": [81903, 82225],
          "rangeSHA256": "0f08670de88fbef3686dd568fd5ac58a76fbafbc440d13822370c9ccefc0447c",
          "fullNormalizedParagraph": "Wind is simply air in motion. Usually in meteorology, when we are talking about the wind it is the horizontal speed and direction we are concerned about. For example, if you hear a report of a west wind at 15 mph (24 km/h) that means the horizontal winds will be coming FROM the west at that speed."
        },
        {
          "id": "NOAA-vane-speed",
          "rawByteRange": [83084, 83370],
          "rangeSHA256": "4461512126a1f694eeb0900cfd4b38e256fd9b62a7a7861fe54b37ba51a2061b",
          "fullNormalizedParagraph": "Although we cannot actually see the air moving we can measure its motion by the force that it applies on objects. We use a wind vane to indicate the wind's direction and an anemometer to measure the wind's speed. But even without those instruments we can determine the direction."
        },
        {
          "id": "NOAA-adjacent-examples",
          "rawByteRange": [83372, 83606],
          "rangeSHA256": "12699039292dbab7123d3288568cf8a3cb1c3a8d1163be8148e2054aaa922796",
          "fullNormalizedParagraph": "For example, a flag points in the opposite direction of the wind. The wind blows leaves opposite the direction from which the wind is blowing. Airplanes taking off and landing at airports will be into the direction of the wind."
        }
      ]
    },
    "nws": [
      {
        "id": "NWS-barometer",
        "bodyPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/barometer.html",
        "bodyBytes": 2582,
        "bodySHA256": "9939f7960cdeab4dbd7775282cbac7d52cd9fb9b9d67181b3ee8cc6bd08bbbbc",
        "headersPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/barometer.headers.txt",
        "headersBytes": 1023,
        "headersSHA256": "e3d73fdb00982c4fff4a78adf8a4c5f551bf7f511b00d3d5e86cd6a129d3e789",
        "url": "https://forecast.weather.gov/glossary.php?word=BAROMETER",
        "fullContextRange": [565, 648],
        "rangeSHA256": "95119fc3c87510cebd09b8e158388ece7124bd11fdd0f774847a5350f6eafa7f",
        "fullContextNormalized": "Barometer An instrument that measures atmospheric pressure.",
        "diskHEADGitExact": true
      },
      {
        "id": "NWS-thermometer",
        "bodyPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/thermometer.html",
        "bodyBytes": 2092,
        "bodySHA256": "9e87f77f36f662b5eb022afef680a72571c38d4c2cda9e2655331959412a426b",
        "headersPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/thermometer.headers.txt",
        "headersBytes": 1023,
        "headersSHA256": "072f79517b64d3d7bfdbf5e1241187220ba8fdc56af27771250bee64f461fe83",
        "url": "https://forecast.weather.gov/glossary.php?word=THERMOMETER",
        "fullContextRange": [321, 401],
        "rangeSHA256": "4772efa8380efd0827b57aa4c0e409e68e21454c8c59ca47f3374e8000515437",
        "fullContextNormalized": "Thermometer An instrument for measuring air temperature.",
        "diskHEADGitExact": true
      },
      {
        "id": "NWS-rain",
        "bodyPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/rain.html",
        "bodyBytes": 11482,
        "bodySHA256": "69efbae454a31f30fcc240d43e8fe4bb3c1261efb80f2953d8dd24e52c69f246",
        "headersPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/rain.headers.txt",
        "headersBytes": 1024,
        "headersSHA256": "3f65237803caa15d20c7345652f0fc62ef9311b5044e90b24b377d14a2f34ca7",
        "url": "https://forecast.weather.gov/glossary.php?word=RAIN",
        "fullContextRange": [4995, 5095],
        "rangeSHA256": "c0ae7a04f362c26202a728d62ddbae5fb4cfaa71018f7ceec6d7e056e796f43f",
        "fullContextNormalized": "Rain Gauge An instrument for measuring the quantity of rain that has fallen.",
        "diskHEADGitExact": true
      }
    ],
    "parserRecipe": "Python HTMLParser(convert_charrefs=True) on exact original UTF8 full enclosing paragraph/entry; join text nodes with spaces then collapse Unicode whitespace. Source-context ranges zero-based, end exclusive; SHA256 applies to original slice before decoding. Full original NWS bodies read; navigation/style content excluded from factual use."
  },
  "catalog": {
    "count": 11000,
    "retrievalQueries": {
      "direct": "флюгер|направлени.{0,50}ветр|направлени.{0,50}ветер",
      "inverse": "ветр.{0,50}направлени|ветер.{0,50}направлени|ветр.{0,50}откуда|ветер.{0,50}откуда",
      "semantic": "метеостанци|барометр|анемометр|осадкомер|рыскани"
    },
    "retrievalResults": {
      "direct": ["energy-power-yaw-turns-nacelle", "weather-climate-barometer-pressure"],
      "inverse": [],
      "semantic": [
        "aviation-dutch-roll",
        "energy-power-yaw-turns-nacelle",
        "inventions-technology-ext-barometer-torricelli",
        "ships-navigation-yaw-motion",
        "weather-climate-thermometer-temperature",
        "weather-climate-barometer-pressure",
        "weather-climate-anemometer-speed",
        "weather-climate-rain-gauge"
      ]
    },
    "all11000ManuallyRead": false,
    "fullRelevantManualCount": 9,
    "neighbors": [
      {
        "id": "weather-climate-thermometer-temperature",
        "fullCurrentCard": {
          "id": "weather-climate-thermometer-temperature",
          "difficulty": "easy",
          "prompt": "Какой прибор на метеостанции защищают от прямого солнечного нагрева, чтобы его показания не искажались?",
          "answers": [
            {"text": "Барометр", "note": "Барометр измеряет атмосферное давление, а не степень нагрева воздуха."},
            {"text": "Анемометр", "note": "Анемометр измеряет скорость ветра."},
            {"text": "Осадкомер", "note": "Осадкомер собирает и измеряет количество выпавших осадков."},
            {"text": "Термометр", "note": "На метеостанции термометр защищают от прямого солнца, осадков и конденсата, сохраняя вентиляцию воздуха."}
          ],
          "correctIndex": 3,
          "explanation": "Термометр измеряет температуру воздуха. На метеостанции его размещают так, чтобы солнечное излучение не нагревало прибор напрямую.",
          "source": {
            "title": "NOAA National Weather Service Glossary: Thermometer",
            "url": "https://forecast.weather.gov/glossary.php?word=THERMOMETER",
            "verifiedAt": "2026-10-13"
          }
        },
        "canonicalSHA256": "76722c4575400409809cffea041b267a274c416f7d3d3793b8ba775977aac6cd",
        "sourceEditorialCertificationOfForeignCard": false,
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Thermometer exposure/protection and temperature differ from vane direction; shared station vocabulary is not duplication."
      },
      {
        "id": "weather-climate-anemometer-speed",
        "fullCurrentCard": {
          "id": "weather-climate-anemometer-speed",
          "difficulty": "easy",
          "prompt": "Каким прибором измеряют скорость ветра?",
          "answers": [
            {"text": "Анемометр", "note": "Анемометр измеряет скорость ветра."},
            {"text": "Термометр", "note": "Термометр измеряет температуру воздуха или другого тела."},
            {"text": "Барометр", "note": "Барометр измеряет атмосферное давление."},
            {"text": "Осадкомер", "note": "Осадкомер собирает и измеряет количество выпавших жидких осадков."}
          ],
          "correctIndex": 0,
          "explanation": "Анемометр измеряет скорость ветра. Чашечный прибор вращается тем быстрее, чем сильнее ветер.",
          "source": {
            "title": "Britannica: Анемометр",
            "url": "https://www.britannica.com/technology/anemometer",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "f9024dce586858daf301a291c3c9ad531169a234d40a0a416154ed21e0766ec4",
        "sourceEditorialCertificationOfForeignCard": false,
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Anemometer speed and vane direction are distinct measured quantities, not inverse versions of one fact."
      },
      {
        "id": "weather-climate-rain-gauge",
        "fullCurrentCard": {
          "id": "weather-climate-rain-gauge",
          "difficulty": "easy",
          "prompt": "Каким прибором измеряют количество дождя?",
          "answers": [
            {"text": "Осадкомер", "note": "Осадкомер собирает и измеряет количество выпавших жидких осадков."},
            {"text": "Термометр", "note": "Термометр измеряет температуру воздуха или другого тела."},
            {"text": "Барометр", "note": "Барометр измеряет атмосферное давление."},
            {"text": "Анемометр", "note": "Анемометр измеряет скорость ветра."}
          ],
          "correctIndex": 0,
          "explanation": "Осадкомер собирает и измеряет количество выпавших жидких осадков. Результат обычно выражают высотой слоя воды в миллиметрах.",
          "source": {
            "title": "Britannica: Осадкомер",
            "url": "https://www.britannica.com/technology/rain-gauge",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "13057b5b0fc8755b034dcc3abac792b7fdac534abcc4db6c2d3110d4a550a414",
        "sourceEditorialCertificationOfForeignCard": false,
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Rain quantity differs from wind direction; matching distractor instruments do not make prompts equivalent."
      },
      {
        "id": "weather-climate-breeze-gentle",
        "fullCurrentCard": {
          "id": "weather-climate-breeze-gentle",
          "difficulty": "easy",
          "prompt": "Как называется слабый местный ветер между морем и сушей?",
          "answers": [
            {"text": "Ураган", "note": "Ураган — мощный тропический циклон Атлантики или восточной части Тихого океана."},
            {"text": "Торнадо", "note": "Торнадо — быстро вращающийся столб воздуха, связанный с грозовым облаком и землёй."},
            {"text": "Бриз", "note": "Бриз — местный ветер; морской бриз днём дует с воды на сушу."},
            {"text": "Муссон", "note": "Муссон — сезонная система ветров, меняющая направление между летом и зимой."}
          ],
          "correctIndex": 2,
          "explanation": "Бриз — местный ветер; морской бриз днём дует с воды на сушу. Направление меняется из-за разной скорости нагрева воды и земли.",
          "source": {
            "title": "Britannica: Бриз",
            "url": "https://www.britannica.com/science/breeze",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "8d5a3117ad20c2c631b2c34004646f98fea7bb1bda136ac3dce156355eabf822",
        "sourceEditorialCertificationOfForeignCard": false,
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Breeze names a local wind phenomenon; it does not identify an instrument or reverse the direction/vane relation."
      },
      {
        "id": "weather-climate-pressure-air-weight",
        "fullCurrentCard": {
          "id": "weather-climate-pressure-air-weight",
          "difficulty": "easy",
          "prompt": "Как называется сила, с которой воздух давит на единицу площади?",
          "answers": [
            {"text": "Влажность", "note": "Влажность характеризует содержание водяного пара в воздухе."},
            {"text": "Атмосферное давление", "note": "Атмосферное давление создаётся весом столба воздуха над поверхностью."},
            {"text": "Температура воздуха", "note": "Температура воздуха показывает степень его нагретости."},
            {"text": "Видимость", "note": "Метеорологическая видимость — наибольшее расстояние уверенного распознавания объектов."}
          ],
          "correctIndex": 1,
          "explanation": "Атмосферное давление создаётся весом столба воздуха над поверхностью. С высотой оно обычно уменьшается.",
          "source": {
            "title": "Britannica: Атмосферное давление",
            "url": "https://www.britannica.com/science/atmospheric-pressure",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "ffe459f7a0dcdd72ede2a6a15ee9b68243e69678ab35eaaa6fc9b05cc426e544",
        "sourceEditorialCertificationOfForeignCard": false,
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Atmospheric-pressure definition differs from instrument identification for wind direction."
      },
      {
        "id": "energy-power-yaw-turns-nacelle",
        "fullCurrentCard": {
          "id": "energy-power-yaw-turns-nacelle",
          "difficulty": "medium",
          "prompt": "Какой механизм ориентирует турбину по изменившемуся направлению ветра?",
          "answers": [
            {"text": "Ротор", "note": "Ротор ветротурбины включает ступицу и лопасти, забирающие энергию потока."},
            {"text": "Гондола", "note": "Гондола на вершине башни содержит вал, генератор и другое оборудование."},
            {"text": "Система рыскания", "note": "Система рыскания поворачивает гондолу горизонтально, направляя ротор навстречу ветру."},
            {"text": "Башня", "note": "Башня поднимает ротор в более сильный и ровный воздушный поток."}
          ],
          "correctIndex": 2,
          "explanation": "Система рыскания поворачивает гондолу горизонтально, направляя ротор навстречу ветру. Датчик направления подаёт сигнал приводам.",
          "source": {
            "title": "U.S. Department of Energy",
            "url": "https://www.energy.gov/cmei/systems/explore-wind-turbine-text-version",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "6af2b7f8d85d2a8528a250a6aeda01d2bfd0a10ebebe8e01fba757fa4410eae6",
        "sourceEditorialCertificationOfForeignCard": false,
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Turbine yaw system actively orients a nacelle; a vane indicates direction. Related wind vocabulary does not equate machinery and measurement."
      }
    ],
    "additionalFullCandidates": [
      {
        "id": "aviation-dutch-roll",
        "fullCurrentCard": {
          "id": "aviation-dutch-roll",
          "difficulty": "hard",
          "prompt": "Как называется боковое колебание, которое на стреловидном самолёте подавляет демпфер рыскания?",
          "answers": [
            {"text": "Угол гроба", "note": "«Угол гроба» — высотный режим, где запас между низкоскоростным и высокоскоростным срывом очень мал."},
            {"text": "Голландский шаг", "note": "Голландский шаг — связанное колебание по рысканию и крену."},
            {"text": "Затягивание в пикирование", "note": "Затягивание в пикирование — тенденция носа опускаться при смещении центра давления назад на околозвуке."},
            {"text": "Фугоида", "note": "Фугоида — медленное продольное колебание скорости и высоты при малом изменении угла атаки."}
          ],
          "correctIndex": 1,
          "explanation": "Голландский шаг — связанное колебание по рысканию и крену. Нос движется из стороны в сторону вместе с раскачкой крыльев.",
          "source": {
            "title": "SKYbrary",
            "url": "https://skybrary.aero/articles/dutch-roll",
            "verifiedAt": "2026-09-02"
          }
        },
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Coupled aircraft yaw/roll oscillation, unrelated to identifying a weather-station vane."
      },
      {
        "id": "inventions-technology-ext-barometer-torricelli",
        "fullCurrentCard": {
          "id": "inventions-technology-ext-barometer-torricelli",
          "difficulty": "easy",
          "prompt": "Какой прибор измеряет атмосферное давление?",
          "answers": [
            {"text": "Барометр", "note": "Барометр измеряет атмосферное давление."},
            {"text": "Термометр", "note": "Термометр измеряет температуру."},
            {"text": "Гигрометр", "note": "Гигрометр измеряет влажность воздуха."},
            {"text": "Анемометр", "note": "Анемометр измеряет скорость ветра."}
          ],
          "correctIndex": 0,
          "explanation": "Барометр измеряет атмосферное давление. Первый ртутный барометр создал Эванджелиста Торричелли.",
          "source": {
            "title": "Britannica: Evangelista Torricelli",
            "url": "https://www.britannica.com/biography/Evangelista-Torricelli",
            "verifiedAt": "2026-09-02"
          }
        },
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Pressure-to-barometer identification duplicated the former target; the current target tests direction-to-vane and is distinct."
      },
      {
        "id": "ships-navigation-yaw-motion",
        "fullCurrentCard": {
          "id": "ships-navigation-yaw-motion",
          "difficulty": "medium",
          "prompt": "Как называется поворот носа влево и вправо вокруг вертикальной оси?",
          "answers": [
            {"text": "Бортовая качка", "note": "Бортовая качка — вращение вокруг продольной оси судна."},
            {"text": "Рыскание", "note": "Рыскание — вращение вокруг вертикальной оси судна."},
            {"text": "Килевая качка", "note": "Килевая качка — вращение вокруг поперечной оси."},
            {"text": "Вертикальная качка", "note": "Вертикальная качка перемещает судно вдоль вертикальной оси без обязательного наклона."}
          ],
          "correctIndex": 1,
          "explanation": "Рыскание — вращение вокруг вертикальной оси судна. Оно меняет курс и требует коррекции рулём.",
          "source": {
            "title": "britannica.com: Рыскание",
            "url": "https://www.britannica.com/technology/ship",
            "verifiedAt": "2026-09-02"
          }
        },
        "fullCurrentLiteralPersonallyRead": true,
        "relationVerdict": "DISTINCT",
        "independentReason": "Ship rotation about its vertical axis, not a wind-direction instrument."
      }
    ],
    "dedupVerdict": "PASS no direct or inverse equivalent of current direction-to-vane question among retrieved relevant full neighbors. Shared wrong-note facts are supporting knowledge, not equivalent primary prompts."
  },
  "provenance": {
    "authorPackages": "5250100 plus supplement7249780; intake is mechanical only; author grades not inherited.",
    "actualNativeIdentity": "Existing actual reader01a131c5, different from author01a1324b; not derived from an environment label.",
    "executed": [
      "Read original author payload and supplement for literal/source paths only.",
      "Readonly Python raw-source extraction and complete relevant NOAA/NWS primary-context reads.",
      "Readonly Python checks all15 raw range bodies and headers, SHA/bytes, Content-Range/ETag/HEAD Git, assembled bodyGit6eadc87.",
      "Readonly Python parses11000 current cards and independent direct/inverse/semantic candidate retrieval; personally read9full current neighbors.",
      "Readonly Python exact card/composite/scalar hashes, current topic hash, other99 comparison to5250100, metadata title, Git status.",
      "task-cleanup.md read before closure."
    ],
    "writes": "None, including no temp/Git/index/source/metadata/counter writes.",
    "audio": "No game/browser/Unity process launched; checks had no sound output; system volume untouched.",
    "ownedProcesses": "Only synchronous completed Python/read commands; no background process/resource created.",
    "foreignStatus": " M docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-fresh-rework19/sources/newadvent-rule-benedict.html\n M src/content/topics/physics.json\n M src/content/topics/weather-climate.json\n",
    "ignoredStatus": " M docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-fresh-rework19/sources/newadvent-rule-benedict.html\n M src/content/topics/physics.json\n M src/content/topics/weather-climate.json\n!! docs/content-audits/question-quality-wave-6/__pycache__/\n!! docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-remaining23/__pycache__/\n!! docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle23-current/__pycache__/\n!! node_modules/\n",
    "priorTmpRoots": "Not recreated."
  },
  "counts": {
    "groups": 6,
    "sourcePASS": 6,
    "editorialPASS": 6,
    "orderedNotes": 4,
    "difficultyPASS": 1,
    "metadataPASS": 1,
    "newCredit": 0
  },
  "handoff": {
    "nextStep": "Coordinator opaque-preserves this complete native JSON/final payload in durable Git, verifies current binding and performs manual adjudication before any increment.",
    "archiveNow": false,
    "reason": "The new native receipt is returned in this chat without filesystem writes; durable coordinator preservation and manual gate pending.",
    "cleanupDebt": "No own TMP created; nothing to delete. Source and foreign resources remain untouched."
  }
}
```