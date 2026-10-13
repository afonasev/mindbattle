Проверил отдельный атом `weather-climate-rain-liquid`. Обнаружил одну точечную проблему: формулировка подходит и под морось — тоже жидкие капли осадков. Захват NOAA различает дождь как капли больше 0,5 мм и морось как капли меньше 0,5 мм. Файлы не менял: текущая инструкция координатора требует read-only. Предлагаю добавить этот порог в вопрос; остальные поля карточки подтверждаются источниками.

Пакет для координатора:

```json
{
  "status": "author_review_complete_prompt_needs_disambiguation",
  "qualityCredit": "none",
  "independentReader": "не проводил эту проверку",
  "scope": {
    "currentId": "weather-climate-rain-liquid",
    "selectedIndex": 0,
    "otherEightSelectedCards": "по ранее сверенным данным совпадают с замороженным baseline",
    "finalSelectedCard": {
      "id": "weather-climate-barometer-pressure",
      "difficulty": "easy",
      "correctIndex": 3
    },
    "currentCardMatchesFrozenBaseline": true,
    "firstTenIdsAndOrderMatchScope": true,
    "currentDifficultyDistribution": {"easy": 40, "medium": 40, "hard": 20}
  },
  "currentCardLiteral": {
    "id": "weather-climate-rain-liquid",
    "difficulty": "easy",
    "prompt": "В прогнозе сказано, что из облака осадки выпадают отдельными жидкими каплями, без снежинок или ледяных частиц. Как называется этот вид осадков?",
    "answers": [
      {"text": "Дождь", "note": "У дождевых капель диаметр больше 0,5 мм."},
      {"text": "Снег", "note": "Снежинки возникают из ледяных кристаллов, которые могут срастаться друг с другом."},
      {"text": "Град", "note": "Мелкие ледяные частицы и переохлаждённые капли соединяются; восходящий поток может снова поднять их, и повторение цикла увеличивает градину."},
      {"text": "Мокрый снег", "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."}
    ],
    "correctIndex": 0,
    "explanation": "Дождь — жидкие капли, которые выпадают из облаков. В отличие от града и снежинок, при дожде вода достигает земли в жидком виде.",
    "source": {
      "title": "NOAA National Weather Service Glossary: Rain",
      "url": "https://forecast.weather.gov/glossary.php?word=RAIN",
      "verifiedAt": "2026-10-13"
    }
  },
  "canonicalBindings": {
    "recipe": "SHA-256 от UTF-8 json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')); без завершающего перевода строки",
    "wholeCardSha256": "665b125caaf703bd62c34234d65f7b44ee1f8f2408b6769f27cdb2413f6bd834",
    "compositePromptOrderedAnswerTextsAndKey": {
      "value": {
        "prompt": "В прогнозе сказано, что из облака осадки выпадают отдельными жидкими каплями, без снежинок или ледяных частиц. Как называется этот вид осадков?",
        "answers": ["Дождь", "Снег", "Град", "Мокрый снег"],
        "correctIndex": 0
      },
      "sha256": "dc9ef375c4d9eaf7a7e8c2178bc6b764f5b42ea5ea3be5a6a9f77b73917bd2e3"
    },
    "difficultySha256": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
    "sourceMetadataSha256": "b92400c79d3cd0c505d61ecd50ccd841fc893bb2b5366db463566fd0e581771b",
    "explanationSha256": "2608fc2313ae508caf28c8e101d1cda68c7c20e9329ea590f57f86cf95728b61",
    "orderedNoteSha256": [
      "c8526be67ac7a8fdc56c991d55517d9181aeaa1af42d28546a9a768cc65f5148",
      "e69ac38c45c20000e0050ae47f9c6fe687d10400537aea091cb3dee635bc63ad",
      "4f675b4e2927939d5d57fc7b525384b16510dc82d14bb47d53a203fb5f8fe51c",
      "72f966328e74969d81ded8127ae939f8eb15573b547b23f3b7569bd3eb06a3a0"
    ],
    "idSha256": "e04d6c635ea3b1206e322b66fc223896c0c15667188c5949376800768411dba5",
    "correctIndexSha256": "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
  },
  "sixEditorialGroups": [
    {
      "group": "prompt + ordered answer texts + key",
      "verdict": "needs prompt disambiguation",
      "source": "NOAA NWS Glossary: Rain and Drizzle",
      "evidence": [
        {
          "body": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/rain.html",
          "bodyBytes": 11482,
          "bodySha256": "69efbae454a31f30fcc240d43e8fe4bb3c1261efb80f2953d8dd24e52c69f246",
          "headers": "sources/rain.headers.txt",
          "headersBytes": 1024,
          "headersSha256": "3f65237803caa15d20c7345652f0fc62ef9311b5044e90b24b377d14a2f34ca7",
          "range": "[4580,4652)",
          "rangeSha256": "ccccabad872b06642361609c165765fb2149eebe433ae761456491960603c40c",
          "quote": "Precipitation that falls to earth in drops more than 0.5 mm in diameter.",
          "fullContext": "[4556,4657), SHA-256 f6dc85a0e9e08b5d105515b6a27a839c16209c8341a946c60a0536486ecdeed1"
        },
        {
          "body": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/sources/drizzle.html",
          "bodyBytes": 2574,
          "bodySha256": "c42aad8a435a1ef55c0b633740cf7652e41c2e2465f33ff793f8c46941d61733",
          "headers": "sources/drizzle.headers.txt",
          "headersBytes": 1069,
          "headersSha256": "a920de6468675da69e85797b06b752308ffe6b1421dd6689f4f1a3abd781e877",
          "range": "[348,457)",
          "rangeSha256": "03f1a48da8443e2caabcfedfd72fb390ea453988f760d8a650523784c076aab7",
          "quote": "Precipitation consisting of numerous minute droplets of water less than 0.5 mm (500 micrometers) in diameter.",
          "fullContext": "[321,462), SHA-256 99ba81b9a4432235331cba8e6f0f0b47b2ea4018abc924392ded17118f26bd86"
        }
      ],
      "editorialReason": "The prompt says liquid drops and excludes snow and ice, but does not distinguish rain from drizzle. Both are liquid precipitation. The answer list makes rain the only available liquid option, yet a diameter threshold would make the prompt itself precise.",
      "proposedPromptForCoordinatorReview": "В прогнозе сказано, что из облака осадки выпадают отдельными жидкими каплями диаметром больше 0,5 мм, без снежинок или ледяных частиц. Как называется этот вид осадков?",
      "changeMade": false
    },
    {
      "group": "explanation",
      "verdict": "factually supported",
      "source": "NWS Rain definition, same capture and range above",
      "editorialReason": "It correctly identifies rain as liquid drops reaching the ground. It does not distinguish drizzle, so the proposed prompt clarification would make the full item more precise."
    },
    {
      "group": "answer note 0: Дождь",
      "verdict": "factually supported and useful",
      "source": "NWS Rain definition, same capture and range above",
      "editorialReason": "The note supplies the exact size criterion missing from the prompt and helps distinguish rain from drizzle."
    },
    {
      "group": "answer note 1: Снег",
      "verdict": "factually supported and useful",
      "source": {
        "url": "https://forecast.weather.gov/glossary.php?word=SNOW",
        "bodyBytes": 11384,
        "bodySha256": "55f252aa2e7060357d8f7c87d78bfa0f65d7a2410ce780ff424154216c29ed6f",
        "headersBytes": 1024,
        "headersSha256": "fbc3123389b959f2421d4e4635ba4df6e40dc914adc5acb252a77ad5daf990d8",
        "supportingRange": "Snow definition [5015,5222), range SHA-256 ba908b4748780faeb8d29b12c520b593cef46ee9daa80978e2f1510bccfa78a7",
        "additionalSnowflakeRange": "[9196,9248), range SHA-256 090e6c02e5201beba1ae8c32f6926a6a3b9bd853050fd646dbdad7e34304b57f",
        "snowflakeContext": "Snowflake An agglomeration of snow crystals falling as a unit.",
        "snowflakeContextRange": "[9167,9253), context SHA-256 b3a16079a6bc9a27ee52784fd65f9fe6d0a84f7ff179629900be8f9c4f608aab"
      },
      "editorialReason": "Snow crystals can aggregate into snowflakes; the note gives the reader a concrete fact about the snow distractor."
    },
    {
      "group": "answer note 2: Град",
      "verdict": "factually supported and useful",
      "source": {
        "title": "NWS Birmingham: Severe Weather Outreach — Hail Formation",
        "url": "https://www.weather.gov/bmx/outreach_svr",
        "bodyBytes": 63376,
        "bodySha256": "a864f1b813ded50a60bed16dcc77d75cebd85020f5cb8b1574c9a9984923c977",
        "headersBytes": 1068,
        "headersSha256": "d81d9d79f420e1d39c9055b5e1c8cc2c0726dd2b877646d956ba94166816e03f",
        "paragraphRange": "[41904,42658)",
        "paragraphSha256": "5193bcfdd34a3538230ec2805e7097bde2b3dd24dfb5c766110bc1d1be522ae6",
        "sourceContext": "The paragraph says small ice particles and supercooled water droplets lifted by a thunderstorm updraft can combine, enter downdrafts, and be recycled above the freezing level; repeated cycles allow hailstones to grow."
      },
      "editorialReason": "The note accurately condenses the source’s hail-growth process and explains why hail is a different precipitation form."
    },
    {
      "group": "answer note 3: Мокрый снег",
      "verdict": "factually supported and useful",
      "source": {
        "url": "https://meteoinfo.ru/forcabout/3891-nast-kpp",
        "bodyBytes": 65113,
        "bodySha256": "2011bcaeffd8e3dc8270da507479a8bdc37d7f37b67b95bd6b570ca6c12f52da",
        "headersBytes": 576,
        "headersSha256": "0729337617d637de4dddad120481b2fddaf9130291414cc3270440525dd3f38f",
        "tableRow": "[39490,39679)",
        "rowSha256": "26c45207fed5e1405770799ebf722d64955f98a54550641a129951a4430b2c92",
        "fullContext": "[39422,39684), SHA-256 c97c3ab34eb016531a5895499c4747440a902b462108cd10bb1354f482f88e3c",
        "normalizedContext": "Мокрый снег Снег и дождь одновременно, но преобладает снег; тающий снег"
      },
      "editorialReason": "The Russian hydrometeorological terminology defines мокрый снег as simultaneous snow and rain with snow predominating, matching the note."
    }
  ],
  "difficultyGroup": {
    "literal": "easy",
    "canonicalSha256": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
    "editorialReason": "Scope fixes this position as easy. The question tests direct identification of a familiar precipitation type from a short description, rather than a multi-step meteorological inference.",
    "scopeBaseline": "Exact scope baseline card for this ID has difficulty easy."
  },
  "sourceMetadataGroup": {
    "literal": {
      "title": "NOAA National Weather Service Glossary: Rain",
      "url": "https://forecast.weather.gov/glossary.php?word=RAIN",
      "verifiedAt": "2026-10-13"
    },
    "canonicalSha256": "b92400c79d3cd0c505d61ecd50ccd841fc893bb2b5366db463566fd0e581771b",
    "editorialReason": "The card metadata points to the NWS Rain glossary page. The captured primary page, its HTTP headers, and cited raw byte range agree with that URL and support the rain definition.",
    "sourceBodyUrlManifest": {
      "httpStatus": 200,
      "contentType": "text/html; charset=UTF-8",
      "captureMethod": "curl -fsSL; body saved without HTML normalization",
      "bodyPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/rain.html",
      "bodyBytes": 11482,
      "bodySha256": "69efbae454a31f30fcc240d43e8fe4bb3c1261efb80f2953d8dd24e52c69f246",
      "headersPath": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/rain.headers.txt",
      "headersBytes": 1024,
      "headersSha256": "3f65237803caa15d20c7345652f0fc62ef9311b5044e90b24b377d14a2f34ca7"
    }
  },
  "sourceAndParsing": {
    "offsets": "Half-open byte ranges into the saved raw HTTP body files.",
    "passageRecipe": "Strict UTF-8 decode; remove HTML tags with regex <[^>]*> replaced by empty string; html.unescape entity references; collapse Unicode whitespace with Python str.split() and join by one ASCII space; no Unicode normalization or text correction.",
    "contextRecipe": "Python HTMLParser(convert_charrefs=True); collect text nodes; add separators at br/p/dt/dd/tr/td/div/li/h1/h2/h3/section boundaries; collapse Unicode whitespace. Raw source ranges are independently hashed."
  },
  "neighborReview": {
    "retrievalBasis": {
      "artifact": "whole-catalog-retrieval.json",
      "artifactSha256": "89b8307d846330bc070ac9841e3195053a118d8f74479663c9fe175bf2ccb722",
      "sourceBaseline": "9e800d7",
      "topicFiles": 110,
      "cards": 11000,
      "topicFilesSha256": "d24f4fbfeb8c91e225ffa68064daf93c6d6eb9efb4c46b3fb9bf60cabe454fea",
      "rainLiquidFamilyCandidateCount": 79,
      "method": "Targeted regex candidates from prompt and ordered answer texts only; candidate generation, not duplicate verdict."
    },
    "closestFullCurrentNeighbors": [
      {
        "id": "weather-climate-snow-crystals",
        "canonicalSha256": "d04ce9ec980b9f7537eaccb63aa5db600bfef3e32043566496aaaca94ff4e9ee",
        "card": {
          "id": "weather-climate-snow-crystals",
          "difficulty": "easy",
          "prompt": "Какие осадки выпадают в виде разветвлённых ледяных кристаллов, часто соединённых в снежинки?",
          "answers": [
            {"text": "Снег", "note": "Снег образуется непосредственно из водяного пара; отдельные кристаллы имеют разветвлённую форму."},
            {"text": "Дождь", "note": "По определениям NWS, дождевые капли имеют диаметр более 0,5 мм, а капли мороси — менее 0,5 мм."},
            {"text": "Град", "note": "Градины обычно представляют собой ледяные шарики или неправильные кусочки льда."},
            {"text": "Мокрый снег", "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."}
          ],
          "correctIndex": 0,
          "explanation": "Снег состоит из ледяных кристаллов, которые часто срастаются в снежинки. Их форма зависит от условий роста в облаке.",
          "source": {"title": "NOAA National Weather Service Glossary: Snow", "url": "https://forecast.weather.gov/glossary.php?word=SNOW", "verifiedAt": "2026-10-13"}
        },
        "comparison": "Same precipitation family and shares distractors, but identifies ice-crystal precipitation rather than liquid rain."
      },
      {
        "id": "weather-climate-hail-ice-balls",
        "canonicalSha256": "7fd98ec0d15e716d252b1ecffb91c6c59ebd1ff471ac0abbd0f27ca57de1ee9b",
        "card": {
          "id": "weather-climate-hail-ice-balls",
          "difficulty": "easy",
          "prompt": "После грозы на земле нашли твёрдые ледяные шарики и комочки. Как называются такие осадки?",
          "answers": [
            {"text": "Град", "note": "NWS определяет град как ледяные шарики или комки диаметром более 5 мм."},
            {"text": "Дождь", "note": "Дождь достигает земли каплями воды диаметром больше 0,5 мм."},
            {"text": "Снег", "note": "Снежинки состоят из ледяных кристаллов, а не из сплошных ледяных комков."},
            {"text": "Мокрый снег", "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."}
          ],
          "correctIndex": 0,
          "explanation": "Град — твёрдые ледяные частицы, выпадающие из кучево-дождевого облака. NWS определяет град как ледяные частицы диаметром более 5 мм.",
          "source": {"title": "NOAA National Weather Service Glossary: Hail", "url": "https://forecast.weather.gov/glossary.php?word=HAIL", "verifiedAt": "2026-10-13"}
        },
        "comparison": "Same precipitation family and distractor set, but identifies solid ice pellets."
      },
      {
        "id": "weather-climate-sleet-mix",
        "canonicalSha256": "264d169b6d60aa5afeb45a70594db835db0a9a40f09faf494f10eefb923dd285",
        "card": {
          "id": "weather-climate-sleet-mix",
          "difficulty": "easy",
          "prompt": "В осадках одновременно присутствуют дождь и снег, причём снег преобладает. Как называется такой вид осадков?",
          "answers": [
            {"text": "Дождь", "note": "Дождь — жидкие осадки; по определению NWS, дождевые капли крупнее 0,5 мм."},
            {"text": "Мокрый снег", "note": "В метеосводке так называют одновременное выпадение снега и дождя, когда преобладает снег."},
            {"text": "Снег", "note": "Снег выпадает в виде ледяных кристаллов, которые часто соединяются в снежинки."},
            {"text": "Град", "note": "Град — ледяные шарики или неправильные кусочки льда, образующиеся в кучево-дождевых облаках."}
          ],
          "correctIndex": 1,
          "explanation": "Росгидромет описывает мокрый снег как одновременное выпадение снега и дождя с преобладанием снега. Если дождь и снег чередуются, применяется отдельная формулировка «снег с дождём».",
          "source": {"title": "Росгидромет / Метеоинфо: Терминология прогнозов и штормовых предупреждений", "url": "https://meteoinfo.ru/forcabout/3891-nast-kpp", "verifiedAt": "2026-10-13"}
        },
        "comparison": "Shares a precipitation name and choice set, but tests mixed precipitation where snow predominates."
      },
      {
        "id": "weather-climate-rain-gauge",
        "canonicalSha256": "13057b5b0fc8755b034dcc3abac792b7fdac534abcc4db6c2d3110d4a550a414",
        "card": {
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
          "source": {"title": "Britannica: Осадкомер", "url": "https://www.britannica.com/technology/rain-gauge", "verifiedAt": "2026-09-02"}
        },
        "comparison": "Uses the word rain but asks for a measurement instrument, not precipitation type."
      },
      {
        "id": "weather-climate-warm-cloud-collision",
        "canonicalSha256": "a82742b1e1b4ebb737cf20cd053e3bef3214e81946003d358d386f55b83462b0",
        "card": {
          "id": "weather-climate-warm-cloud-collision",
          "difficulty": "hard",
          "prompt": "Какой процесс создаёт дождь в тёплом облаке без ледяной фазы?",
          "answers": [
            {"text": "Процесс Бержерона", "note": "Процесс Бержерона переносит водяной пар от переохлаждённых капель к ледяным кристаллам."},
            {"text": "Аккреция", "note": "Аккреция — рост ледяной частицы при намерзании столкнувшихся с ней переохлаждённых капель."},
            {"text": "Коалесценция капель", "note": "Коалесценция — рост облачных капель при столкновениях и слиянии."},
            {"text": "Агрегация кристаллов", "note": "Агрегация — слипание отдельных ледяных кристаллов в крупные снежинки."}
          ],
          "correctIndex": 2,
          "explanation": "Коалесценция — рост облачных капель при столкновениях и слиянии. Крупные капли падают быстрее и собирают мелкие.",
          "source": {"title": "Clouds and Precipitation", "url": "https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf", "verifiedAt": "2026-09-02"}
        },
        "comparison": "Rain is mentioned, but the card tests cloud microphysics rather than naming the resulting precipitation."
      },
      {
        "id": "oceans-seas-precipitation-fall",
        "canonicalSha256": "284f820ff900f0fe4ba99421977882b35d9f578b0a4bfd053aa71af2de83b4e4",
        "card": {
          "id": "oceans-seas-precipitation-fall",
          "difficulty": "easy",
          "prompt": "Как называется выпадение воды из облаков дождём или снегом?",
          "answers": [
            {"text": "Поверхностный сток", "note": "Поверхностный сток движется по земле в ручьи, реки, озёра и океан."},
            {"text": "Замерзание", "note": "Замерзание переводит жидкую воду в твёрдый лёд."},
            {"text": "Испарение", "note": "Испарение превращает жидкую воду в водяной пар."},
            {"text": "Осадки", "note": "Осадки возвращают воду из атмосферы на поверхность Земли."}
          ],
          "correctIndex": 3,
          "explanation": "Осадки возвращают воду из атмосферы на поверхность Земли. Они выпадают в виде дождя, снега, града или мороси.",
          "source": {"title": "NOAA: The Water Cycle", "url": "https://www.noaa.gov/education/resource-collections/freshwater/water-cycle", "verifiedAt": "2026-09-02"}
        },
        "comparison": "The broad hydrological-cycle category includes rain, snow, hail, and drizzle; this card asks for the umbrella term precipitation."
      }
    ],
    "otherManuallyReadFullNeighbors": [
      "weather-climate-convectional-rain",
      "weather-climate-frontal-rain",
      "weather-climate-orographic-rain",
      "weather-climate-rain-shadow",
      "weather-climate-rainbow-refraction",
      "weather-climate-cumulus-puffy",
      "weather-climate-stratus-layer",
      "ecology-environment-acid-rain",
      "ecology-environment-stormwater-runoff"
    ],
    "directInverseSemanticResult": "No exact duplicate found in the reviewed candidates. Related cards ask about rain collection, hail/snow/mixed precipitation, cloud processes, rain-producing mechanisms, rain shadow, or the broad precipitation-cycle concept. They ask different facts. The drizzle ambiguity is a category-coverage issue in the current prompt, not a duplicate-card finding."
  },
  "preservation": {
    "currentCardChange": "None; this atom remains bytewise equal to the frozen baseline card.",
    "evidenceWrites": "None.",
    "tests": "Not run; content-source author review only.",
    "fullSuite": "Not run.",
    "build": "Not run.",
    "commit": "None.",
    "publishOrDeploy": "None.",
    "nextStep": "A human or authorized source editor can add the >0.5 mm criterion to the prompt, preserving ID, order, easy difficulty, and correctIndex 0. Then the corrected atom can enter independent review."
  }
}
```

Исходники подтверждают ответ, пояснение и четыре факта в заметках. Ограничение по мороси — единственная найденная неоднозначность вопроса; поэтому этот атом пока не передаётся как полностью квалифицированный. Другие восемь карточек остаются ожидающими. В рабочем дереве целевой задачи никаких новых правок не делал.

**Следующий шаг:** внести предложенное уточнение порога в вопрос можно только после снятия read-only ограничения координатора. До этого независимую оценку текущей формулировки следует считать ожидающей; quality credit остаётся нулевым.