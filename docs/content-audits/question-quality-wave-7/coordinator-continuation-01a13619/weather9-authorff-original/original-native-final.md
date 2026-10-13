Авторская проверка девяти карточек завершена. Живой каталог и сохранённые доказательства не менялись. Все девять текущих карточек совпали с переданными canonical SHA; все остальные 91 карточка погодного файла совпали со снимком baseline.

Предлагаю два локальных текстовых изменения для редакторского рассмотрения:

- В Rain уточнить порог капель и заменить справку правильного ответа на отдельное различие с моросью. NWS задаёт дождь как капли больше 0,5 мм, а морось — меньше 0,5 мм.
- В Sleet заменить справку правильного ответа на дополнительный синоним из таблицы Росгидромета — «тающий снег».

Ниже — авторский пакет. `qualityCredit` остаётся нулевым; независимое чтение не запускалось.

```json
{
  "status": "author_review_complete_pending_independent_reader",
  "qualityCredit": "none",
  "independentReaderVerdict": "pending",
  "hashRecipe": "SHA-256 UTF-8 json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')); no trailing newline.",
  "binding": {
    "worktree": "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle",
    "branch": "codex/question-quality-wave-6",
    "head": "0c67c955bb7eb3982985e981b5083a0aa7859003",
    "primaryCheckoutWasReadOrChanged": false,
    "weatherFile": {
      "path": "src/content/topics/weather-climate.json",
      "bytes": 173868,
      "sha256": "29ba8f76ed2065eb33a85358b65369f01cc0791ecb48f059bf2a7525f1737a2d",
      "selectedCardCount": 9,
      "totalCardCount": 100
    },
    "selectedOrderAndSlots": [
      ["weather-climate-rain-liquid", 0, "easy", 0],
      ["weather-climate-snow-crystals", 1, "easy", 0],
      ["weather-climate-hail-ice-balls", 2, "easy", 0],
      ["weather-climate-sleet-mix", 3, "easy", 1],
      ["weather-climate-fog-ground-cloud", 4, "easy", 1],
      ["weather-climate-dew-condensation", 5, "easy", 1],
      ["weather-climate-frost-ice", 6, "easy", 2],
      ["weather-climate-cloud-droplets", 7, "easy", 2],
      ["weather-climate-thermometer-temperature", 8, "easy", 3]
    ],
    "other91MatchSnapshot": true,
    "protectedWindVaneCardSha256": "6d6ab1fbacb53b3b90a95c8c889383bf3e17a968d21c831633a87e9aed171970",
    "protectedWindVaneCardChanged": false
  },
  "cards": [
    {
      "id": "weather-climate-rain-liquid",
      "currentSha256": "665b125caaf703bd62c34234d65f7b44ee1f8f2408b6769f27cdb2413f6bd834",
      "proposedSha256": "218d21b424b807679c1a321bd52b4cb9a3ffd6d0c314ad5268fc1e2ea1edbeb8",
      "currentCard": {
        "id": "weather-climate-rain-liquid",
        "difficulty": "easy",
        "prompt": "В прогнозе сказано, что из облака осадки выпадают отдельными жидкими каплями, без снежинок или ледяных частиц. Как называется этот вид осадков?",
        "answers": [
          {
            "text": "Дождь",
            "note": "У дождевых капель диаметр больше 0,5 мм."
          },
          {
            "text": "Снег",
            "note": "Снежинки возникают из ледяных кристаллов, которые могут срастаться друг с другом."
          },
          {
            "text": "Град",
            "note": "Мелкие ледяные частицы и переохлаждённые капли соединяются; восходящий поток может снова поднять их, и повторение цикла увеличивает градину."
          },
          {
            "text": "Мокрый снег",
            "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."
          }
        ],
        "correctIndex": 0,
        "explanation": "Дождь — жидкие капли, которые выпадают из облаков. В отличие от града и снежинок, при дожде вода достигает земли в жидком виде.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Rain",
          "url": "https://forecast.weather.gov/glossary.php?word=RAIN",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": {
        "id": "weather-climate-rain-liquid",
        "difficulty": "easy",
        "prompt": "Как называются жидкие осадки из капель диаметром более 0,5 мм, падающих из облака?",
        "answers": [
          {
            "text": "Дождь",
            "note": "Морось отличается более мелкими каплями диаметром менее 0,5 мм."
          },
          {
            "text": "Снег",
            "note": "Снежинки возникают из ледяных кристаллов, которые могут срастаться друг с другом."
          },
          {
            "text": "Град",
            "note": "Мелкие ледяные частицы и переохлаждённые капли соединяются; восходящий поток может снова поднять их, и повторение цикла увеличивает градину."
          },
          {
            "text": "Мокрый снег",
            "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."
          }
        ],
        "correctIndex": 0,
        "explanation": "Дождь — жидкие капли, которые выпадают из облаков. В отличие от града и снежинок, при дожде вода достигает земли в жидком виде.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Rain",
          "url": "https://forecast.weather.gov/glossary.php?word=RAIN",
          "verifiedAt": "2026-10-13"
        }
      },
      "groupReasons": [
        ["prompt + ordered answers + key", ["rain", "snow", "hail", "russian-wet-snow-definition"], "Порог NWS однозначно отделяет дождь от мороси. Снег, град и мокрый снег описывают отличные от жидкого дождя формы осадков."],
        ["explanation", ["rain", "snow", "hail"], "NWS определяет дождь как выпадающие жидкие капли; сохранённые глоссарии снега и града подтверждают контраст фаз."],
        ["note 0, keyed Rain", ["drizzle-size-threshold"], "Справка даёт полезное различие: у мороси капли меньше 0,5 мм, то есть факт не дублирует предложенный порог дождя."],
        ["note 1, Snow", ["snow", "snowflake"], "NWS описывает снежинки как агрегаты кристаллов, падающие единым целым."],
        ["note 2, Hail", ["hail-formation-recycling-growth"], "Сохранённый полный абзац NWS описывает соединение ледяных частиц и переохлаждённых капель и повторное поднятие восходящим потоком."],
        ["note 3, Wet snow", ["russian-wet-snow-definition"], "Официальная русская строка определяет мокрый снег как одновременный дождь и снег с преобладанием снега."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "После уточнения размера капель это прямое распознавание общеизвестной формы осадков без вычисления."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Rain",
          "url": "https://forecast.weather.gov/glossary.php?word=RAIN",
          "verifiedAt": "2026-10-13"
        },
        "reason": "URL и сохранённый первичный текст NWS относятся к глоссарной статье Rain; страница прямо задаёт размер капель."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "3bab5f44cebda0374de3ba67b8e83e6c9e5bccb3c8560c51d4ad6cc456bce3d0",
        "explanation": "2608fc2313ae508caf28c8e101d1cda68c7c20e9329ea590f57f86cf95728b61",
        "orderedNotes": [
          "fc3fdbf750d3336cc36806fe6e79a6f8461d862ec91d4fa803a90caf29214102",
          "e69ac38c45c20000e0050ae47f9c6fe687d10400537aea091cb3dee635bc63ad",
          "4f675b4e2927939d5d57fc7b525384b16510dc82d14bb47d53a203fb5f8fe51c",
          "72f966328e74969d81ded8127ae939f8eb15573b547b23f3b7569bd3eb06a3a0"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "b92400c79d3cd0c505d61ecd50ccd841fc893bb2b5366db463566fd0e581771b"
      }
    },
    {
      "id": "weather-climate-snow-crystals",
      "currentSha256": "d04ce9ec980b9f7537eaccb63aa5db600bfef3e32043566496aaaca94ff4e9ee",
      "proposedSha256": "d04ce9ec980b9f7537eaccb63aa5db600bfef3e32043566496aaaca94ff4e9ee",
      "currentCard": {
        "id": "weather-climate-snow-crystals",
        "difficulty": "easy",
        "prompt": "Какие осадки выпадают в виде разветвлённых ледяных кристаллов, часто соединённых в снежинки?",
        "answers": [
          {
            "text": "Снег",
            "note": "Снег образуется непосредственно из водяного пара; отдельные кристаллы имеют разветвлённую форму."
          },
          {
            "text": "Дождь",
            "note": "По определениям NWS, дождевые капли имеют диаметр более 0,5 мм, а капли мороси — менее 0,5 мм."
          },
          {
            "text": "Град",
            "note": "Градины обычно представляют собой ледяные шарики или неправильные кусочки льда."
          },
          {
            "text": "Мокрый снег",
            "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."
          }
        ],
        "correctIndex": 0,
        "explanation": "Снег состоит из ледяных кристаллов, которые часто срастаются в снежинки. Их форма зависит от условий роста в облаке.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Snow",
          "url": "https://forecast.weather.gov/glossary.php?word=SNOW",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["snow", "hail", "russian-wet-snow-definition"], "Разветвлённые кристаллы и снежинки соответствуют снегу; дождь, град и мокрый снег описывают другие формы осадков."],
        ["explanation", ["snow", "snow-crystal-growth"], "NWS определяет снег как ледяные кристаллы, часто соединённые в снежинки; сохранённый учебный абзац объясняет ветвление и рост кристаллов в облаке."],
        ["note 0, keyed Snow", ["snow", "snow-crystal-growth"], "Образование непосредственно из пара и ветвление — факты о росте кристалла сверх самого названия ответа."],
        ["note 1, Rain", ["rain", "drizzle-size-threshold"], "Две размерные границы NWS различают дождевые и моросящие капли."],
        ["note 2, Hail", ["hail"], "Глоссарий определяет град как ледяные шарики или неправильные ледяные комки."],
        ["note 3, Wet snow", ["russian-wet-snow-definition"], "Русская терминологическая таблица подтверждает одновременное выпадение дождя и снега с преобладанием снега."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Это знакомое прямое распознавание снега по кристаллам и снежинкам, без редкой терминологии или вычислений."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Snow",
          "url": "https://forecast.weather.gov/glossary.php?word=SNOW",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённая NWS страница Snow подтверждает ключ; отдельный сохранённый учебный текст NWS поддерживает сведения о росте кристаллов."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "2f33fa46f112bfa918b97cfe0374e1a8047cefb558c2d33a88177f79b71defbf",
        "explanation": "8529c59d6ad892e0e0da68dd95edeca86f46fd2ad95298139fdf162ac00803f0",
        "orderedNotes": [
          "1b46b4985f038349dc169b9b0215063b026abba48e5e5071443f589672d1074a",
          "f492e27205917acd87f1b1c028192a20f9406c7f09ff7b9a90ca5e525e7f19b1",
          "3ebc47162e7434db1a2f4e1f187bd2e50ed3698cf676a847d2d09b81b0a9383f",
          "72f966328e74969d81ded8127ae939f8eb15573b547b23f3b7569bd3eb06a3a0"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "41a4a524449535462df3124c95e8b3a9b4ca0bb58cda12d84798fea933eb35af"
      }
    },
    {
      "id": "weather-climate-hail-ice-balls",
      "currentSha256": "7fd98ec0d15e716d252b1ecffb91c6c59ebd1ff471ac0abbd0f27ca57de1ee9b",
      "proposedSha256": "7fd98ec0d15e716d252b1ecffb91c6c59ebd1ff471ac0abbd0f27ca57de1ee9b",
      "currentCard": {
        "id": "weather-climate-hail-ice-balls",
        "difficulty": "easy",
        "prompt": "После грозы на земле нашли твёрдые ледяные шарики и комочки. Как называются такие осадки?",
        "answers": [
          {
            "text": "Град",
            "note": "NWS определяет град как ледяные шарики или комки диаметром более 5 мм."
          },
          {
            "text": "Дождь",
            "note": "Дождь достигает земли каплями воды диаметром больше 0,5 мм."
          },
          {
            "text": "Снег",
            "note": "Снежинки состоят из ледяных кристаллов, а не из сплошных ледяных комков."
          },
          {
            "text": "Мокрый снег",
            "note": "Мокрый снег — снег и дождь одновременно, причём преобладает снег."
          }
        ],
        "correctIndex": 0,
        "explanation": "Град — твёрдые ледяные частицы, выпадающие из кучево-дождевого облака. NWS определяет град как ледяные частицы диаметром более 5 мм.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Hail",
          "url": "https://forecast.weather.gov/glossary.php?word=HAIL",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["hail", "snow", "russian-wet-snow-definition"], "Твёрдые ледяные шарики после грозы описывают град; снег — кристаллы, мокрый снег — смесь фаз, дождь — жидкие капли."],
        ["explanation", ["hail"], "Сохранённый NWS глоссарий прямо связывает град с кучево-дождевыми облаками и частицами льда более 5 мм."],
        ["note 0, keyed Hail", ["hail"], "Размерный критерий NWS добавляет проверяемую границу к узнаваемому примеру."],
        ["note 1, Rain", ["rain"], "Порог NWS для дождевых капель отличает жидкую форму от градин."],
        ["note 2, Snow", ["snow", "snowflake"], "Снежинки состоят из кристаллов и не являются сплошными ледяными комками."],
        ["note 3, Wet snow", ["russian-wet-snow-definition"], "Русский официальный термин описывает совместное выпадение дождя и снега, не градины."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Ледяные шарики после грозы — широко узнаваемый пример града; размерный порог остаётся дополнительной справкой."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Hail",
          "url": "https://forecast.weather.gov/glossary.php?word=HAIL",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённая NWS Hail страница подтверждает ключевую форму и порог; Rain, Snow и Meteoinfo capture поддерживают пояснения вариантов."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "4f4e447610a1a3afa4853e61d39ad2f4456b390014204f32e9bf0ae1181dc9d4",
        "explanation": "66e8c901eb9dea8df98a2e2c052346d2b1cd46ffbf77fd7ace3733d3905a14f7",
        "orderedNotes": [
          "73e45e126c00bab6c6b133154b4dc3c01882ff841669b7dd948c40ae29284c10",
          "0fc0ab98b7da46ecf1ed766e91e1b1eb25d075c80b327b3bde95f8d9628ea120",
          "53eb3b5e495f89c69f40bec17cf334337c07ef5331316c784de5d5def849221b",
          "72f966328e74969d81ded8127ae939f8eb15573b547b23f3b7569bd3eb06a3a0"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "5a943db9e6823b2adec39540cccc6330e15f091b9d006f3118e970f71844dcd4"
      }
    },
    {
      "id": "weather-climate-sleet-mix",
      "currentSha256": "264d169b6d60aa5afeb45a70594db835db0a9a40f09faf494f10eefb923dd285",
      "proposedSha256": "d85914aded7b14dc90c7592b9710af06d8d29cb093f5a795d5b3e41576edab53",
      "currentCard": {
        "id": "weather-climate-sleet-mix",
        "difficulty": "easy",
        "prompt": "В осадках одновременно присутствуют дождь и снег, причём снег преобладает. Как называется такой вид осадков?",
        "answers": [
          {
            "text": "Дождь",
            "note": "Дождь — жидкие осадки; по определению NWS, дождевые капли крупнее 0,5 мм."
          },
          {
            "text": "Мокрый снег",
            "note": "В метеосводке так называют одновременное выпадение снега и дождя, когда преобладает снег."
          },
          {
            "text": "Снег",
            "note": "Снег выпадает в виде ледяных кристаллов, которые часто соединяются в снежинки."
          },
          {
            "text": "Град",
            "note": "Град — ледяные шарики или неправильные кусочки льда, образующиеся в кучево-дождевых облаках."
          }
        ],
        "correctIndex": 1,
        "explanation": "Росгидромет описывает мокрый снег как одновременное выпадение снега и дождя с преобладанием снега. Если дождь и снег чередуются, применяется отдельная формулировка «снег с дождём».",
        "source": {
          "title": "Росгидромет / Метеоинфо: Терминология прогнозов и штормовых предупреждений",
          "url": "https://meteoinfo.ru/forcabout/3891-nast-kpp",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": {
        "id": "weather-climate-sleet-mix",
        "difficulty": "easy",
        "prompt": "В осадках одновременно присутствуют дождь и снег, причём снег преобладает. Как называется такой вид осадков?",
        "answers": [
          {
            "text": "Дождь",
            "note": "Дождь — жидкие осадки; по определению NWS, дождевые капли крупнее 0,5 мм."
          },
          {
            "text": "Мокрый снег",
            "note": "В справочнике Росгидромета мокрый снег также назван тающим снегом."
          },
          {
            "text": "Снег",
            "note": "Снег выпадает в виде ледяных кристаллов, которые часто соединяются в снежинки."
          },
          {
            "text": "Град",
            "note": "Град — ледяные шарики или неправильные кусочки льда, образующиеся в кучево-дождевых облаках."
          }
        ],
        "correctIndex": 1,
        "explanation": "Росгидромет описывает мокрый снег как одновременное выпадение снега и дождя с преобладанием снега. Если дождь и снег чередуются, применяется отдельная формулировка «снег с дождём».",
        "source": {
          "title": "Росгидромет / Метеоинфо: Терминология прогнозов и штормовых предупреждений",
          "url": "https://meteoinfo.ru/forcabout/3891-nast-kpp",
          "verifiedAt": "2026-10-13"
        }
      },
      "groupReasons": [
        ["prompt + ordered answers + key", ["russian-wet-snow-definition", "russian-snow-rain-definition", "rain", "snow", "hail"], "Официальная строка описывает смесь с преобладанием снега. Дождь, кристаллический снег и град имеют иные состояния/состав."],
        ["explanation", ["russian-wet-snow-definition", "russian-snow-rain-definition"], "Таблица разносит одновременный мокрый снег и чередование снега с дождём по двум терминам."],
        ["note 0, Rain", ["rain"], "NWS подтверждает размер дождевых капель больше 0,5 мм."],
        ["note 1, keyed Wet snow", ["russian-wet-snow-definition"], "Строка Росгидромета добавляет отдельное наименование «тающий снег» сверх признаков в вопросе и ключе."],
        ["note 2, Snow", ["snow"], "NWS определяет снег через кристаллы льда и снежинки."],
        ["note 3, Hail", ["hail"], "NWS определяет град как ледяные шарики или комки из кучево-дождевых облаков."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Описание сразу называет две фазы и какая преобладает; это знакомый термин прогноза без расчёта."
      },
      "sourceMetadata": {
        "literal": {
          "title": "Росгидромет / Метеоинфо: Терминология прогнозов и штормовых предупреждений",
          "url": "https://meteoinfo.ru/forcabout/3891-nast-kpp",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённый первичный русскоязычный справочник содержит точные определения мокрого снега и чередования снега с дождём."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "fd9700273ea8efb44f93f938fdfe9728c1b65a9a90ed887928e1b0a043e35c3a",
        "explanation": "a3bfda36c31038f729f0de818c670ea11bbe02ae8c99082e74b0bb0599a2dfb5",
        "orderedNotes": [
          "b60b374d7594ec269a6a6839d42957b23967981eaed64070d656b000ca0c26bb",
          "812b4ac06bcc981560273a8ff99fa834d8a3c1fad81eba4f3a73dd6dfb350b6b",
          "4f1c24c4586c8d951b6a70c8b364984f97bfce0b3141f5253fb223f3c1a92257",
          "98ea1059c525d4488a97ae54066219d2d64046d1447421c951b9234d3ee95d7e"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "c42d2a41d94af6a4598a812f376953f4e101225f0930ce9a0ba663cb0ef41d59"
      }
    },
    {
      "id": "weather-climate-fog-ground-cloud",
      "currentSha256": "a2325a7fe401ec810ab6db5677630148b1021c39fc3734b2e5f83b43d4c77916",
      "proposedSha256": "a2325a7fe401ec810ab6db5677630148b1021c39fc3734b2e5f83b43d4c77916",
      "currentCard": {
        "id": "weather-climate-fog-ground-cloud",
        "difficulty": "easy",
        "prompt": "После ясной прохладной ночи воздух у земли помутнел, а предметы вдали стали плохо различимы. Как называется это явление?",
        "answers": [
          {
            "text": "Роса",
            "note": "Роса оседает жидкими каплями на предметах у земли, а не остаётся взвешенной в воздухе."
          },
          {
            "text": "Туман",
            "note": "При тумане капли взвешены у поверхности; NWS отмечает опасное снижение видимости до четверти мили и менее."
          },
          {
            "text": "Иней",
            "note": "Иней — кристаллы льда на охлаждённых предметах, а не взвесь жидких капель."
          },
          {
            "text": "Облако",
            "note": "Облако состоит из водяных капель или ледяных частиц выше земной поверхности."
          }
        ],
        "correctIndex": 1,
        "explanation": "Ночью земля теряет тепло и охлаждает прилегающий влажный воздух. Когда он достигает точки росы, в нём образуются капли тумана.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Fog",
          "url": "https://forecast.weather.gov/glossary.php?word=FOG",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["fog", "radiation-fog", "radiation-fog-context", "fog-cloud-altitude-context", "cloud"], "Влага у поверхности и ухудшение видимости соответствуют туману; роса и иней оседают на поверхностях, облако находится выше."],
        ["explanation", ["radiation-fog-context", "radiation-fog"], "NWS описывает ночное охлаждение поверхности и прилегающего влажного воздуха до насыщения с образованием капель."],
        ["note 0, Dew", ["dew"], "Роса конденсируется на предметах у земли, а не остаётся взвешенной в воздухе."],
        ["note 1, keyed Fog", ["fog", "fog-visibility-threshold"], "Глоссарий NWS связывает туман с каплями у земной поверхности и порогом видимости для Dense Fog Advisory."],
        ["note 2, Frost", ["frost", "hoar-frost"], "Иней осаждает кристаллы на холодные поверхности, в отличие от жидких капель тумана."],
        ["note 3, Cloud", ["cloud", "fog-cloud-altitude-context"], "NWS отличает облако от тумана высотой расположения видимых капель/частиц."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Помутнение воздуха у земли после прохладной ночи — знакомый непосредственный признак тумана."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Fog",
          "url": "https://forecast.weather.gov/glossary.php?word=FOG",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённая NWS Fog статья подтверждает капли у поверхности и видимость; сохранённая NWS учебная страница поддерживает образование ночного тумана."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "84bf55e92f19ab1db7ae3f835c59f93f2a9ce01d7d18e2b2903805a827e71994",
        "explanation": "3fda16b216ed25c7fb7b3e94bfac96a27c88e2431a6661c601d03dcb94aaed02",
        "orderedNotes": [
          "6e4c3ba9d5e6a49a335c026f6adeb9a7e54b95993f4a736c9be811cc5f1fdb52",
          "bb5d025d3003c997bd252eabbe4e5724e7550d2e2a546f1efcfe3b94c1e924a1",
          "cc75e671dcc8e9e8392e55de7a6bd502291d2b00a98360e359ba85a3e74cfce4",
          "bc9f761cc21199689f7f106e8c5097ff3c995513f9bd853d3db0539888b42408"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "9037ae86528a022459d5a9137786a06e2e6816590427482e2ace1b10518c61d3"
      }
    },
    {
      "id": "weather-climate-dew-condensation",
      "currentSha256": "a276d1e499db720aa52551c21d7da55cc5cc4b75d55f7adddacbf3b42e2c943d",
      "proposedSha256": "a276d1e499db720aa52551c21d7da55cc5cc4b75d55f7adddacbf3b42e2c943d",
      "currentCard": {
        "id": "weather-climate-dew-condensation",
        "difficulty": "easy",
        "prompt": "После ясной ночи на листьях появились жидкие капли, хотя дождя не было. Как называется эта влага?",
        "answers": [
          {
            "text": "Туман",
            "note": "Туман — капли воды, остающиеся во взвешенном состоянии в приземном воздухе."
          },
          {
            "text": "Роса",
            "note": "Роса конденсируется на предметах у земли, когда их поверхность охлаждается ниже точки росы."
          },
          {
            "text": "Иней",
            "note": "Иней образуется на достаточно холодных поверхностях в виде кристаллов льда, а не жидких капель."
          },
          {
            "text": "Облако",
            "note": "Облако — капли воды или частицы льда, находящиеся в атмосфере выше земной поверхности."
          }
        ],
        "correctIndex": 1,
        "explanation": "Роса — влага, сконденсировавшаяся на предметах у поверхности земли. Она появляется, когда поверхность охлаждается до точки росы.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Dew",
          "url": "https://forecast.weather.gov/glossary.php?word=DEW",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["dew", "fog", "frost", "cloud"], "Капли лежат на листьях после ночи без дождя; туман и облако остаются во взвеси, иней — лёд на поверхности."],
        ["explanation", ["dew"], "NWS определяет росу как влагу, сконденсировавшуюся на предметах у земли после охлаждения ниже точки росы."],
        ["note 0, Fog", ["fog"], "Туман состоит из капель, подвешенных в приземном воздухе."],
        ["note 1, keyed Dew", ["dew"], "Порог точки росы объясняет конденсацию жидкости на охлаждённой поверхности."],
        ["note 2, Frost", ["frost"], "Иней образует кристаллы льда на достаточно холодной поверхности, что отличает его от жидких капель."],
        ["note 3, Cloud", ["cloud"], "Глоссарий NWS помещает облачные капли и частицы льда в атмосферу над поверхностью Земли."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Жидкие капли на листьях после сухой ночи — знакомый непосредственный пример росы."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Dew",
          "url": "https://forecast.weather.gov/glossary.php?word=DEW",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённый NWS Dew глоссарий напрямую поддерживает ключ и объяснение; Fog, Frost и Cloud captures поддерживают различия."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "e2f0bdd98de3c2e1f0c0404424653d328157764c6c0e71d003b95f9460069ce9",
        "explanation": "3396c2014261c6afed10d7ce06cfe371e86ecbc034ec759e6cace4e11068fa61",
        "orderedNotes": [
          "0511ab0a4560ae3d7c8757184ba9951eed9b8574bffa7f40d6194b584878cda4",
          "c12b35af1cb00b9c6678658249692efbe8ef2a2b8aa08edf90b5aae4d45ccdbb",
          "8f45533bbc501ecabca0d52d9f7045769bddf4e9b8d5dfdcdb69272649e7bbec",
          "5076da821e1bbe8e7f5c91448b2fe2537e73b8b89cf3e36026008c18e07967d1"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "8557a9bd816f5fe26784e5a1d7fe4e3fe44f272dbd5c0163ce0eb90396a17f89"
      }
    },
    {
      "id": "weather-climate-frost-ice",
      "currentSha256": "03241147bc1d7290e63504901fa1178d27cc1282b25f64e68380f85a97fdd28f",
      "proposedSha256": "03241147bc1d7290e63504901fa1178d27cc1282b25f64e68380f85a97fdd28f",
      "currentCard": {
        "id": "weather-climate-frost-ice",
        "difficulty": "easy",
        "prompt": "На траве после холодной ночи видны тонкие белые кристаллы льда. Как называется такой налёт?",
        "answers": [
          {
            "text": "Туман",
            "note": "Туман — взвесь водяных капель у поверхности; при низкой температуре он может состоять из ледяных частиц."
          },
          {
            "text": "Роса",
            "note": "Роса — влага, сконденсировавшаяся на предметах у земли ниже точки росы."
          },
          {
            "text": "Иней",
            "note": "Иней может выглядеть как чешуйки, иглы, перья или веера; поверхность при этом охлаждается ниже 0 °C."
          },
          {
            "text": "Облако",
            "note": "Облако — видимая совокупность капель воды или частиц льда, удерживающихся в атмосфере."
          }
        ],
        "correctIndex": 2,
        "explanation": "Иней — тонкие кристаллы льда на траве и других поверхностях. Для его образования поверхность должна охладиться ниже точки замерзания.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Frost",
          "url": "https://forecast.weather.gov/glossary.php?word=FROST",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["frost", "hoar-frost", "dew", "fog", "cloud"], "Тонкие кристаллы на траве — отложение на поверхности; роса жидкая, туман и облако взвешены в воздухе."],
        ["explanation", ["frost", "hoar-frost"], "NWS определяет тонкие кристаллы на земле и поверхностях и связывает их с охлаждением ниже точки замерзания."],
        ["note 0, Fog", ["fog", "ice-fog"], "NWS различает водяной туман и ледяной туман как взвешенные частицы; это не налёт кристаллов на траве."],
        ["note 1, Dew", ["dew"], "Роса — сконденсированная влага на предметах, а не кристаллический иней."],
        ["note 2, keyed Frost", ["frost", "hoar-frost"], "Формы чешуек, игл, перьев и вееров и условие ниже 0 °C добавляют различительные признаки."],
        ["note 3, Cloud", ["cloud"], "Облако — совокупность частиц в атмосфере, тогда как вопрос описывает осадок на поверхности."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Белые кристаллы льда на траве после холодной ночи — непосредственный знакомый признак инея."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Frost",
          "url": "https://forecast.weather.gov/glossary.php?word=FROST",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённый NWS Frost глоссарий подтверждает форму инея и температурный признак; Fog и Dew captures поддерживают дистракторы."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "fcd6563ec6bdea2770128d7e689467d9dddb3f72bcab7017228e96f362ee683f",
        "explanation": "1693c67ea1c6ffe1135c86cd9326584e400dd542e9e12c93c8dda0533a7786cb",
        "orderedNotes": [
          "d1d81413d9613931505ca26a4aae180e497acab22caa2bc8e8615948a7a4ae0c",
          "a9ecb768c440147f7679d239d3e2a4e5dba0fe277dbcb6250c9be20c8ae25dad",
          "1e4720a7936c707850a842c24c8846d6b97d63b7ad0d6a7297d4535862a41f06",
          "3b4f01acfae929a001705b23de9539a8c60e798187a71ce2978268727661736d"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "8207ed525b8803af3d0b4f26f6109010e9e6da48aa37bfc333a8296bbd79a774"
      }
    },
    {
      "id": "weather-climate-cloud-droplets",
      "currentSha256": "559c3430a6bf702bd429c95cf6eefa5af6d2d3248931efbcdb9aaabee8e1c626",
      "proposedSha256": "559c3430a6bf702bd429c95cf6eefa5af6d2d3248931efbcdb9aaabee8e1c626",
      "currentCard": {
        "id": "weather-climate-cloud-droplets",
        "difficulty": "easy",
        "prompt": "После подъёма влажного воздуха в небе на высоте появились видимые капли воды или кристаллы льда. Как называется это скопление?",
        "answers": [
          {
            "text": "Туман",
            "note": "Туман — капли воды или льда в воздухе у самой земной поверхности; основное различие с облаком — высота."
          },
          {
            "text": "Роса",
            "note": "Роса оседает на близких к земле предметах, а не образует взвесь в свободном воздухе."
          },
          {
            "text": "Облако",
            "note": "Облачные капли настолько малы, что восходящие потоки воздуха могут долго удерживать их во взвешенном состоянии."
          },
          {
            "text": "Иней",
            "note": "Иней — кристаллы, осевшие непосредственно на холодную поверхность."
          }
        ],
        "correctIndex": 2,
        "explanation": "Капли облака настолько малы, что долго остаются во взвешенном состоянии в воздухе. Восходящие потоки помогают удерживать их над землёй.",
        "source": {
          "title": "NOAA National Weather Service: Cloud Development",
          "url": "https://www.weather.gov/source/zhu/ZHU_Training_Page/clouds/cloud_development/clouds.htm",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["cloud", "cloud-definition-context", "cloud-formation-context", "fog-cloud-altitude-context"], "Высотное скопление видимых капель или кристаллов соответствует облаку; туман расположен у поверхности, роса и иней оседают на предметах."],
        ["explanation", ["cloud-suspension-context"], "NWS объясняет долгое взвешенное состояние малым размером капель и восходящими потоками."],
        ["note 0, Fog", ["fog", "fog-cloud-altitude-context"], "Глоссарий и учебный текст NWS определяют туман у поверхности и отличают его от облака высотой."],
        ["note 1, Dew", ["dew"], "Роса конденсируется на предметах у земли, а не образует свободно взвешенное облако."],
        ["note 2, keyed Cloud", ["cloud-suspension-context"], "Сохранённый учебный контекст описывает сопротивление воздуха и поддержку восходящими потоками."],
        ["note 3, Frost", ["hoar-frost"], "Иней — кристаллы, осевшие на холодных предметах, а не частицы в атмосфере."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Это знакомое облако; стем прямо даёт сцену и высоту, отделяющие его от тумана и поверхностных отложений."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service: Cloud Development",
          "url": "https://www.weather.gov/source/zhu/ZHU_Training_Page/clouds/cloud_development/clouds.htm",
          "verifiedAt": "2026-10-13"
        },
        "reason": "Сохранённая NWS учебная страница поддерживает образование и взвесь облаков; словарные captures подтверждают контрасты."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "bd8978afa2a001ce4cc6227cb3fcb1f52da26c118f8453ee0876cb3e1ca1672b",
        "explanation": "c2ac19bda720a42888a213cb5422961d6dd7ed06f668dcae47b13cfb768c9755",
        "orderedNotes": [
          "ae76df1cc175560b0c008f2ce4455bea85f40e1d938dcc6d5ecdfec6fe32162d",
          "5f2a50f6c83b2defde7e5b03cbfc6a9b1e3dd6d0f315276a6726d68f6c772bf1",
          "e9e7a85cdd013460c84bacfbd580df392498bbf806ef85f2d61dba785f35753b",
          "144c0000387930b70dc35d85ff020869cc015a1fbad13b8e43c784ede485bf9b"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "630fc0f709c0a901fb5c83c8716c99defee5e12abf718dc800b87d457de876eb"
      }
    },
    {
      "id": "weather-climate-thermometer-temperature",
      "currentSha256": "76722c4575400409809cffea041b267a274c416f7d3d3793b8ba775977aac6cd",
      "proposedSha256": "76722c4575400409809cffea041b267a274c416f7d3d3793b8ba775977aac6cd",
      "currentCard": {
        "id": "weather-climate-thermometer-temperature",
        "difficulty": "easy",
        "prompt": "Какой прибор на метеостанции защищают от прямого солнечного нагрева, чтобы его показания не искажались?",
        "answers": [
          {
            "text": "Барометр",
            "note": "Барометр измеряет атмосферное давление, а не степень нагрева воздуха."
          },
          {
            "text": "Анемометр",
            "note": "Анемометр измеряет скорость ветра."
          },
          {
            "text": "Осадкомер",
            "note": "Осадкомер собирает и измеряет количество выпавших осадков."
          },
          {
            "text": "Термометр",
            "note": "На метеостанции термометр защищают от прямого солнца, осадков и конденсата, сохраняя вентиляцию воздуха."
          }
        ],
        "correctIndex": 3,
        "explanation": "Термометр измеряет температуру воздуха. На метеостанции его размещают так, чтобы солнечное излучение не нагревало прибор напрямую.",
        "source": {
          "title": "NOAA National Weather Service Glossary: Thermometer",
          "url": "https://forecast.weather.gov/glossary.php?word=THERMOMETER",
          "verifiedAt": "2026-10-13"
        }
      },
      "proposedCard": "unchanged; identical to currentCard",
      "groupReasons": [
        ["prompt + ordered answers + key", ["instrument-shelter", "thermometer", "barometer", "anemometer", "rain-gauge"], "Термометр измеряет температуру; в вопросе описано, зачем его помещают в защитный экран. Другие приборы измеряют давление, ветер и количество осадков."],
        ["explanation", ["thermometer", "instrument-shelter"], "NWS определяет термометр как прибор для измерения температуры воздуха, а экран — как защиту от прямого солнца."],
        ["note 0, Barometer", ["barometer"], "NWS связывает барометр с атмосферным давлением, а не температурой."],
        ["note 1, Anemometer", ["anemometer"], "NWS определяет анемометр как прибор для измерения скорости ветра."],
        ["note 2, Rain gauge", ["rain-gauge"], "NWS определяет осадкомер как прибор для измерения количества дождя."],
        ["note 3, keyed Thermometer", ["instrument-shelter"], "Полная строка NWS добавляет осадки, конденсат и достаточную вентиляцию к защите от прямого солнца."]
      ],
      "difficulty": {
        "value": "easy",
        "reason": "Это прямой вопрос о знакомом измерительном приборе; назначение защиты от солнца сказано явно."
      },
      "sourceMetadata": {
        "literal": {
          "title": "NOAA National Weather Service Glossary: Thermometer",
          "url": "https://forecast.weather.gov/glossary.php?word=THERMOMETER",
          "verifiedAt": "2026-10-13"
        },
        "reason": "NWS Thermometer подтверждает измеряемую величину; отдельная сохранённая NWS Instrument Shelter строка обосновывает защиту и вентиляцию."
      },
      "hashes": {
        "compositePromptOrderedAnswerTextsAndKey": "ae44f1df3a57ee7d0830b88ffc42f904a372cbb43a8533e95507f4efd936389a",
        "explanation": "0e3bce7c4d81b376e0270f556526782c4c6301a2e505ca6624ec16eb9e714303",
        "orderedNotes": [
          "5678225c7da637a294fb3258c39d8bef11346f656cd85678f48d8d23da75e92e",
          "8ea8ea2f1b6f374b5ea3a753c625b8b61de6bc1dffa9664bd5336eba83338ba0",
          "73273a54056ed8ae0dff7ae6e2ff91f390f641842733576d1aa216dd1f6f0646",
          "9c1b8e5ed437a4b8d1254a913bdf291eb771ded2eeb85a96dfd7b1efb70ae631"
        ],
        "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
        "sourceMetadata": "8663b22f98825aba6ddbde3ca68d87cae6511f47d701d8c26ceea1df5f737511"
      }
    }
  ],
  "sharedSourceArtifacts": {
    "sourcePassages": {
      "path": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/source-passages-v2.json",
      "bytes": 95950,
      "sha256": "c4ed39b332476ba84f4fbce1c237834604756dfc429922f2a125d18e7d395ec3"
    },
    "sourceManifest": {
      "path": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/source-manifest-v2.json",
      "bytes": 23138,
      "sha256": "c5d8b97ca5adf3a8a38fb71270e6134169381cbf1a3ec578e580eeb96ee830ea",
      "originalFirstCaptureManifest": {
        "path": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/source-manifest.json",
        "bytes": 14668,
        "sha256": "443001980de47c6f916d2483028d5ed056b2984a4522b0c284cf75b2cfb880f1"
      },
      "gitBinding": "Prior captured source package commit 0a85b4644dd222e6e59892f944c51c726248abd1; current reviewed checkout HEAD 0c67c955bb7eb3982985e981b5083a0aa7859003. Targeted source paths were clean in the reviewed checkout."
    },
    "sourceBodiesAndHeaders": [
      ["NWS_RAIN", "https://forecast.weather.gov/glossary.php?word=RAIN", "sources/rain.html", 11482, "69efbae454a31f30fcc240d43e8fe4bb3c1261efb80f2953d8dd24e52c69f246", "sources/rain.headers.txt", 1024, "3f65237803caa15d20c7345652f0fc62ef9311b5044e90b24b377d14a2f34ca7"],
      ["NWS_SNOW", "https://forecast.weather.gov/glossary.php?word=SNOW", "sources/snow.html", 11384, "55f252aa2e7060357d8f7c87d78bfa0f65d7a2410ce780ff424154216c29ed6f", "sources/snow.headers.txt", 1024, "fbc3123389b959f2421d4e4635ba4df6e40dc914adc5acb252a77ad5daf990d8"],
      ["NWS_HAIL", "https://forecast.weather.gov/glossary.php?word=HAIL", "sources/hail.html", 4421, "baa563a27c65783316ff4bdc6eae9b85e0d9a9166ca8cbecb73e8af522792499", "sources/hail.headers.txt", 1023, "f8847469bc3ddbfcf333905dc186118323945c982b5ba0be3a3573e1b23d7e2e"],
      ["NWS_SLEET", "https://forecast.weather.gov/glossary.php?word=SLEET", "sources/sleet.html", 2581, "3a2642df21eb8251675f055a7828bff7ae15b8460dd9d0de465c0b722587539a", "sources/sleet.headers.txt", 1023, "f29cd3dc21d90279c257fb8f4102104038ad3cca0d2552ddef65f9e293425e41"],
      ["NWS_FOG", "https://forecast.weather.gov/glossary.php?word=FOG", "sources/fog.html", 6202, "54ea1f171112f0966f01de788289903b0b08c279b16a78ac12cbb494b524ff12", "sources/fog.headers.txt", 1023, "fda4eabf63d8bc4668a017cdf2355017799f1399dc94d2cef4b08af4ac9420ea"],
      ["NWS_DEW", "https://forecast.weather.gov/glossary.php?word=DEW", "sources/dew.html", 3225, "d35f3cf581e1d556dbb3e9319674528e1383d7d928081649784e8ad4cb8210e3", "sources/dew.headers.txt", 1023, "a6fdb374de62d62af829e0b825dc8e2a301cce556407b208a032c356180cadde"],
      ["NWS_FROST", "https://forecast.weather.gov/glossary.php?word=FROST", "sources/frost.html", 3729, "f10ff11f4b19f31155ec323ca06cc2b92183a23317757dd03a881fee2e71e8d3", "sources/frost.headers.txt", 1023, "146706243ae6861f2f85937845e3a0bc52dfc0c34b09758a35076b26921fe7cb"],
      ["NWS_CLOUD", "https://forecast.weather.gov/glossary.php?word=CLOUD", "sources/cloud.html", 11815, "b9cca63aa1dbab0fc28b913c9bc8b72dd7857da173025beb3fc3ce0187b78be1", "sources/cloud.headers.txt", 1024, "b684c96ad0c6c24c8fced6759079c2cd7fdbfd2960d8ea32b55b6c47375daa8f"],
      ["NWS_THERMOMETER", "https://forecast.weather.gov/glossary.php?word=THERMOMETER", "sources/thermometer.html", 2092, "9e87f77f36f662b5eb022afef680a72571c38d4c2cda9e2655331959412a426b", "sources/thermometer.headers.txt", 1023, "072f79517b64d3d7bfdbf5e1241187220ba8fdc56af27771250bee64f461fe83"],
      ["NWS_BAROMETER", "https://forecast.weather.gov/glossary.php?word=BAROMETER", "sources/barometer.html", 2582, "9939f7960cdeab4dbd7775282cbac7d52cd9fb9b9d67181b3ee8cc6bd08bbbbc", "sources/barometer.headers.txt", 1023, "e3d73fdb00982c4fff4a78adf8a4c5f551bf7f511b00d3d5e86cd6a129d3e789"],
      ["NWS_ANEMOMETER", "https://forecast.weather.gov/glossary.php?word=ANEMOMETER", "sources/anemometer.html", 2102, "40993360925e0dd6bb4e3302a1579f310e39247c44fc11ae2c835e3c22bb3b84", "sources/anemometer.headers.txt", 1023, "d8ce4ab853441742ef2f7ff1c27e903a6bd9a78fcf2b451f957530b89e987bc9"],
      ["NWS_INSTRUMENT_SHELTER", "https://forecast.weather.gov/glossary.php?word=INSTRUMENTSHELTER", "sources/instrument-shelter.html", 2256, "e9112eca1594c11843118b07fb63749e11d6949f1fcb651f6d296dcab9201fde", "sources/instrument-shelter.headers.txt", 1023, "aac7ffcd9abf0ac7de224651c2c92221fbf9833e0e93ddf949bf11c9cec08e10"],
      ["NWS_CLOUD_DEVELOPMENT", "https://www.weather.gov/source/zhu/ZHU_Training_Page/clouds/cloud_development/clouds.htm", "sources/cloud-development.html", 46017, "e1bc3c932198a78331ce8b54352109d47d0cc0e1decd155a474be392ba06beda", "sources/cloud-development.headers.txt", 1159, "1aa07a4b75bd660ee16b27ccdc7b97614a740a20d3105ee86ec49ec005078efb"],
      ["METEINFO_PRECIP", "https://meteoinfo.ru/forcabout/3891-nast-kpp", "sources/meteoinfo-precip-terms.html", 65113, "2011bcaeffd8e3dc8270da507479a8bdc37d7f37b67b95bd6b5706a1c12f52da", "sources/meteoinfo-precip-terms.headers.txt", 576, "0729337617d637de4dddad120481b2fddaf9130291414cc3270440525dd3f38f"],
      ["MET_OFFICE_SLEET", "https://weather.metoffice.gov.uk/learn-about/weather/types-of-weather/snow/sleet", "sources/metoffice-sleet.html", 84441, "d64d802547b0dbd569c683e0525150cab914008da3a83946076a24dead3ac009", "sources/metoffice-sleet.headers.txt", 750, "08fe9bbcd1baed77205ee0d2799a66f09b42bd13c000c6f69b295f223303cfe0"],
      ["NWS_DRIZZLE", "https://forecast.weather.gov/glossary.php?word=DRIZZLE", "first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/sources/drizzle.html", 2574, "c42aad8a435a1ef55c0b633740cf7652e41c2e2465f33ff793f8c46941d61733", "first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/sources/drizzle.headers.txt", 1069, "a920de6468675da69e85797b06b752308ffe6b1421dd6689f4f1a3abd781e877"],
      ["NWS_HAIL_FORMATION", "https://www.weather.gov/bmx/outreach_svr", "first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/sources/hail-formation.html", 63376, "a864f1b813ded50a60bed16dcc77d75cebd85020f5cb8b1574c9a9984923c977", "first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/sources/hail-formation.headers.txt", 1068, "d81d9d79f420e1d39c9055b5e1c8cc2c0726dd2b877646d956ba94166816e03f"]
    ],
    "rangeAndContextVerification": {
      "checkedPassageCount": 30,
      "checkedSourceBodyCount": 17,
      "rawAndContextRangeByteCountsAndHashesMatch": true,
      "normalization": "Strict UTF-8; HTML text extraction; whitespace collapse only; no Unicode normalization or text correction."
    }
  },
  "neighborReview": {
    "fullCurrentNeighborArtifact": {
      "path": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a13201-b8c6-7e31-947a-e96b214d8117/manual-neighbor-review-v2.json",
      "sha256": "fe64a7a760aaecb2f51b7b37d02fd0270585635ee7b0b19517a13b60ae23bbdc",
      "count": 29
    },
    "comparison": "Все 29 полных соседских объектов сопоставлены с живым каталогом по ID; все объекты совпали целиком. В наборе есть близкие тематические карточки о дождевых процессах, количестве дождя, осадках, облаках, тумане, влажности и приборах. Среди девяти рассматриваемых карточек явных дублей не обнаружено: дождь/снег/град/мокрый снег различаются фазой; туман/облако — высотой; роса/иней — состоянием осадка на поверхности; термометр — измерением температуры и защитой от солнца.",
    "unrelatedExistingFinding": "В соседском пакете отмечена потенциальная близость двух вопросов о барометре; это отдельный вопрос вне девятикарточного scope. Карточка weather-climate-barometer-pressure с зафиксированным SHA сохранена без изменений."
  },
  "neighborObjects": [
    {
      "id": "weather-climate-anemometer-speed",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Same station instrument family but measures wind speed, not temperature or pressure.",
      "fullCurrentNeighborCard": {
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
        "source": {"title": "Britannica: Анемометр", "url": "https://www.britannica.com/technology/anemometer", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "f9024dce586858daf301a291c3c9ad531169a234d40a0a416154ed21e0766ec4"
    },
    {
      "id": "weather-climate-bergeron-ice",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Cloud microphysics transferring vapor to ice crystals; not naming precipitation or device.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-bergeron-ice",
        "difficulty": "hard",
        "prompt": "Какой процесс роста осадков действует в смешанном облаке ниже 0 °C?",
        "answers": [
          {"text": "Коалесценция капель", "note": "Коалесценция — рост облачных капель при столкновениях и слиянии."},
          {"text": "Аккреция", "note": "Аккреция — рост ледяной частицы при намерзании столкнувшихся с ней переохлаждённых капель."},
          {"text": "Агрегация кристаллов", "note": "Агрегация — слипание отдельных ледяных кристаллов в крупные снежинки."},
          {"text": "Процесс Бержерона", "note": "Процесс Бержерона переносит водяной пар от переохлаждённых капель к ледяным кристаллам."}
        ],
        "correctIndex": 3,
        "explanation": "Процесс Бержерона переносит водяной пар от переохлаждённых капель к ледяным кристаллам. Давление насыщенного пара над льдом ниже, чем над водой.",
        "source": {"title": "Bergeron process - Wikipedia", "url": "https://en.wikipedia.org/wiki/Bergeron_process", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "a06504d781bdd01d2eabcf4345e7692258901556e0a184bf25e1abe5ee603544"
    },
    {
      "id": "weather-climate-cirrus-feathery",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Cloud taxonomy from high thin shape, unlike cloud formation or near-ground fog.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-cirrus-feathery",
        "difficulty": "easy",
        "prompt": "Какие облака выглядят как тонкие белые перья высоко в небе?",
        "answers": [
          {"text": "Перистые облака", "note": "Перистые облака — высокие тонкие волокнистые облака из ледяных кристаллов."},
          {"text": "Кучевые облака", "note": "Кучевые облака имеют отдельные плотные белые вершины и относительно плоское основание."},
          {"text": "Слоистые облака", "note": "Слоистые облака образуют низкий ровный серый слой."},
          {"text": "Кучево-дождевые облака", "note": "Кучево-дождевые облака развиваются вертикально и несут ливни, грозы и иногда град."}
        ],
        "correctIndex": 0,
        "explanation": "Перистые облака — высокие тонкие волокнистые облака из ледяных кристаллов. Они могут быть ранним признаком приближения тёплого фронта.",
        "source": {"title": "Britannica: Перистые облака", "url": "https://www.britannica.com/science/cirrus-cloud", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "1ad5c9640ccd4133b55e2f4ca531a57b9619002d47d909e00ef2ffe43a1f2e00"
    },
    {
      "id": "weather-climate-convectional-rain",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "A cause/type of rain (local convective lift), not a name for liquid precipitation.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-convectional-rain",
        "difficulty": "medium",
        "prompt": "Какой тип осадков часто даёт короткий летний ливень после жаркого дня?",
        "answers": [
          {"text": "Конвективные осадки", "note": "Конвективные осадки возникают при быстром подъёме локально нагретого влажного воздуха."},
          {"text": "Орографические осадки", "note": "Орографические осадки выпадают при подъёме влажного воздуха по склону горы."},
          {"text": "Дождевая тень", "note": "Дождевая тень — сухая область за горным хребтом на подветренной стороне."},
          {"text": "Фронтальные осадки", "note": "Фронтальные осадки возникают при подъёме тёплого воздуха над более холодной воздушной массой."}
        ],
        "correctIndex": 0,
        "explanation": "Конвективные осадки возникают при быстром подъёме локально нагретого влажного воздуха. Они связаны с кучево-дождевыми облаками.",
        "source": {"title": "Precipitation types - Wikipedia", "url": "https://en.wikipedia.org/wiki/Precipitation_types#Convectional", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "570e3b49a91573d522bf581093d605aeec8284d9f626f975e4df30c936cdf127"
    },
    {
      "id": "weather-climate-cumulonimbus-storm",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Storm-cloud identification, context for hail but not the precipitation type itself.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-cumulonimbus-storm",
        "difficulty": "easy",
        "prompt": "Из каких облаков обычно развивается гроза?",
        "answers": [
          {"text": "Кучево-дождевые облака", "note": "Кучево-дождевые облака развиваются вертикально и несут ливни, грозы и иногда град."},
          {"text": "Кучевые облака", "note": "Кучевые облака имеют отдельные плотные белые вершины и относительно плоское основание."},
          {"text": "Слоистые облака", "note": "Слоистые облака образуют низкий ровный серый слой."},
          {"text": "Перистые облака", "note": "Перистые облака — высокие тонкие волокнистые облака из ледяных кристаллов."}
        ],
        "correctIndex": 0,
        "explanation": "Кучево-дождевые облака развиваются вертикально и несут ливни, грозы и иногда град. Их вершина часто распластывается в форме наковальни.",
        "source": {"title": "NOAA NESDIS — What Are the Different Types of Clouds?", "url": "https://www.nesdis.noaa.gov/about/k-12-education/atmosphere/what-are-the-different-types-of-clouds", "verifiedAt": "2026-09-04"}
      },
      "neighborCardSha256": "6bf9e4b790594465d6eea0fd5054c5edd86ff63be95cae57e5f0e9109794c311"
    },
    {
      "id": "weather-climate-cumulus-puffy",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Cloud shape taxonomy, adjacent but different from the cloud aggregate question.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-cumulus-puffy",
        "difficulty": "easy",
        "prompt": "Какие облака напоминают белые хлопья или башни?",
        "answers": [
          {"text": "Слоистые облака", "note": "Слоистые облака образуют низкий ровный серый слой."},
          {"text": "Перистые облака", "note": "Перистые облака — высокие тонкие волокнистые облака из ледяных кристаллов."},
          {"text": "Кучево-дождевые облака", "note": "Кучево-дождевые облака развиваются вертикально и несут ливни, грозы и иногда град."},
          {"text": "Кучевые облака", "note": "Кучевые облака имеют отдельные плотные белые вершины и относительно плоское основание."}
        ],
        "correctIndex": 3,
        "explanation": "Кучевые облака имеют отдельные плотные белые вершины и относительно плоское основание. При слабом развитии они часто сопровождают хорошую погоду.",
        "source": {"title": "Britannica: Кучевые облака", "url": "https://www.britannica.com/science/cumulus-cloud", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "b2188f16f3a836cd5c0068fd0fc9d7acc2fbb10a3995fdfc986b3d0133f52be6"
    },
    {
      "id": "weather-climate-cyclone-low",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "A pressure/weather system and possible source of clouds; not barometer measurement.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-cyclone-low",
        "difficulty": "easy",
        "prompt": "Какая система давления чаще приносит облака и осадки в умеренных широтах?",
        "answers": [
          {"text": "Антициклон", "note": "Антициклон — область высокого давления с опускающимся воздухом и расходящимися ветрами."},
          {"text": "Ложбина", "note": "Барическая ложбина — вытянутая область сравнительно низкого давления."},
          {"text": "Гребень", "note": "Барический гребень — вытянутая область сравнительно высокого давления."},
          {"text": "Циклон", "note": "Циклон — область пониженного давления с восходящим воздухом и сходящимися у поверхности ветрами."}
        ],
        "correctIndex": 3,
        "explanation": "Циклон — область пониженного давления с восходящим воздухом и сходящимися у поверхности ветрами. В Северном полушарии ветры вокруг неё закручиваются против часовой стрелки.",
        "source": {"title": "Britannica: Циклон", "url": "https://www.britannica.com/science/cyclone-meteorology", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "dda0392ca588c7610b50a71f80d1d2d256bd8258cc821a5557780ab8072ef1d2"
    },
    {
      "id": "weather-climate-dew-point-saturation",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Moisture saturation indicator related to dew but not liquid drops deposited on leaves.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-dew-point-saturation",
        "difficulty": "medium",
        "prompt": "Какой показатель прямо отражает абсолютное содержание влаги в воздухе?",
        "answers": [
          {"text": "Точка росы", "note": "Точка росы — температура, до которой воздух нужно охладить для насыщения водяным паром."},
          {"text": "Относительная влажность", "note": "Относительная влажность сравнивает фактическое содержание пара с максимально возможным при данной температуре."},
          {"text": "Температура мокрого термометра", "note": "Температура мокрого термометра понижается из-за испарения воды с влажной оболочки датчика."},
          {"text": "Индекс жары", "note": "Индекс жары оценивает ощущаемую температуру по сочетанию жары и влажности."}
        ],
        "correctIndex": 0,
        "explanation": "Точка росы — температура, до которой воздух нужно охладить для насыщения водяным паром. Чем она ближе к температуре воздуха, тем выше относительная влажность.",
        "source": {"title": "dew point - Wikipedia", "url": "https://en.wikipedia.org/wiki/dew_point", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "63d34eb2ab780beead6ac290e0fe467080d19df0fd437a7ad05e61263c051b18"
    },
    {
      "id": "weather-climate-frontal-rain",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Rain caused by frontal lift, distinct from naming rain.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-frontal-rain",
        "difficulty": "medium",
        "prompt": "Какие осадки сопровождают прохождение атмосферного фронта?",
        "answers": [
          {"text": "Фронтальные осадки", "note": "Фронтальные осадки возникают при подъёме тёплого воздуха над более холодной воздушной массой."},
          {"text": "Орографические осадки", "note": "Орографические осадки выпадают при подъёме влажного воздуха по склону горы."},
          {"text": "Дождевая тень", "note": "Дождевая тень — сухая область за горным хребтом на подветренной стороне."},
          {"text": "Конвективные осадки", "note": "Конвективные осадки возникают при быстром подъёме локально нагретого влажного воздуха."}
        ],
        "correctIndex": 0,
        "explanation": "Фронтальные осадки возникают при подъёме тёплого воздуха над более холодной воздушной массой. Их длительность зависит от типа и скорости фронта.",
        "source": {"title": "Rain", "url": "https://weather.metoffice.gov.uk/learn-about/weather/types-of-weather/rain", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "81e62e1be393e6c1fa7b697e7c2e7ef47202470dd7f4ce35fbf62b799c448f24"
    },
    {
      "id": "weather-climate-heat-index-feels",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Perceived heat index influenced by humidity, distinct from thermometer use.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-heat-index-feels",
        "difficulty": "medium",
        "prompt": "Какой индекс показывает, насколько жарко ощущается при высокой влажности?",
        "answers": [
          {"text": "Точка росы", "note": "Точка росы — температура, до которой воздух нужно охладить для насыщения водяным паром."},
          {"text": "Индекс жары", "note": "Индекс жары оценивает ощущаемую температуру по сочетанию жары и влажности."},
          {"text": "Относительная влажность", "note": "Относительная влажность сравнивает фактическое содержание пара с максимально возможным при данной температуре."},
          {"text": "Температура мокрого термометра", "note": "Температура мокрого термометра понижается из-за испарения воды с влажной оболочки датчика."}
        ],
        "correctIndex": 1,
        "explanation": "Индекс жары оценивает ощущаемую температуру по сочетанию жары и влажности. Влажность замедляет испарительное охлаждение тела.",
        "source": {"title": "heat index - Wikipedia", "url": "https://en.wikipedia.org/wiki/heat_index", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "b4d000d0796563b90806d0b775b1b3ae49aa65be9d24d539b8e2e9e005a32740"
    },
    {
      "id": "weather-climate-orographic-rain",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Terrain-driven precipitation process, not precipitation identity.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-orographic-rain",
        "difficulty": "medium",
        "prompt": "Какие осадки усиливаются на наветренном склоне горного хребта?",
        "answers": [
          {"text": "Дождевая тень", "note": "Дождевая тень — сухая область за горным хребтом на подветренной стороне."},
          {"text": "Конвективные осадки", "note": "Конвективные осадки возникают при быстром подъёме локально нагретого влажного воздуха."},
          {"text": "Фронтальные осадки", "note": "Фронтальные осадки возникают при подъёме тёплого воздуха над более холодной воздушной массой."},
          {"text": "Орографические осадки", "note": "Орографические осадки выпадают при подъёме влажного воздуха по склону горы."}
        ],
        "correctIndex": 3,
        "explanation": "Орографические осадки выпадают при подъёме влажного воздуха по склону горы. Подъём охлаждает воздух до насыщения.",
        "source": {"title": "Britannica: Орографические осадки", "url": "https://www.britannica.com/science/orographic-precipitation", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "d0fdcbd1a017490753958a16b3db8633d39af38bd52bf1a71a849a4a10970504"
    },
    {
      "id": "weather-climate-rain-gauge",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Measures quantity of rainfall, not type of precipitation.",
      "fullCurrentNeighborCard": {
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
      "neighborCardSha256": "13057b5b0fc8755b034dcc3abac792b7fdac534abcc4db6c2d3110d4a550a414"
    },
    {
      "id": "weather-climate-rain-shadow",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Dry region on a lee slope, not a falling precipitation form.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-rain-shadow",
        "difficulty": "medium",
        "prompt": "Как называется засушливая зона за горами, где воздух опускается и нагревается?",
        "answers": [
          {"text": "Орографические осадки", "note": "Орографические осадки выпадают при подъёме влажного воздуха по склону горы."},
          {"text": "Конвективные осадки", "note": "Конвективные осадки возникают при быстром подъёме локально нагретого влажного воздуха."},
          {"text": "Фронтальные осадки", "note": "Фронтальные осадки возникают при подъёме тёплого воздуха над более холодной воздушной массой."},
          {"text": "Дождевая тень", "note": "Дождевая тень — сухая область за горным хребтом на подветренной стороне."}
        ],
        "correctIndex": 3,
        "explanation": "Дождевая тень — сухая область за горным хребтом на подветренной стороне. Она образуется после потери влаги на наветренном склоне.",
        "source": {"title": "Britannica: Дождевая тень", "url": "https://www.britannica.com/science/rain-shadow", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "a939a53a7890962477e16786d0a9d934517a1930f70f3b9700db93da29c94be0"
    },
    {
      "id": "weather-climate-rainbow-refraction",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Optical effect from sunlight and drops; not rain classification.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-rainbow-refraction",
        "difficulty": "easy",
        "prompt": "Как называется цветная дуга, видимая напротив Солнца после дождя?",
        "answers": [
          {"text": "Молния", "note": "Молния — мощный электрический разряд в атмосфере."},
          {"text": "Радуга", "note": "Радуга возникает из-за преломления, отражения и разложения света в каплях воды."},
          {"text": "Гром", "note": "Гром — звук от быстрого расширения воздуха, нагретого каналом молнии."},
          {"text": "Полярное сияние", "note": "Полярное сияние создают заряженные частицы, возбуждающие газы верхней атмосферы."}
        ],
        "correctIndex": 1,
        "explanation": "Радуга возникает из-за преломления, отражения и разложения света в каплях воды. Каждая капля отклоняет свет разных цветов под немного разными углами.",
        "source": {"title": "Britannica: Радуга", "url": "https://www.britannica.com/science/rainbow-atmospheric-phenomenon", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "f6d46126066f81441abae31291f0cd5f89306b04ddff166ad49125340dcbd852"
    },
    {
      "id": "weather-climate-relative-humidity-ratio",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Ratio measuring moisture, not dew or instrument shelter use.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-relative-humidity-ratio",
        "difficulty": "medium",
        "prompt": "Какой показатель выражают в процентах от насыщения?",
        "answers": [
          {"text": "Относительная влажность", "note": "Относительная влажность сравнивает фактическое содержание пара с максимально возможным при данной температуре."},
          {"text": "Точка росы", "note": "Точка росы — температура, до которой воздух нужно охладить для насыщения водяным паром."},
          {"text": "Температура мокрого термометра", "note": "Температура мокрого термометра понижается из-за испарения воды с влажной оболочки датчика."},
          {"text": "Индекс жары", "note": "Индекс жары оценивает ощущаемую температуру по сочетанию жары и влажности."}
        ],
        "correctIndex": 0,
        "explanation": "Относительная влажность сравнивает фактическое содержание пара с максимально возможным при данной температуре. При охлаждении воздуха без потери влаги он возрастает.",
        "source": {"title": "Britannica: Относительная влажность", "url": "https://www.britannica.com/science/relative-humidity", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "b14925b2f1280881cc586cc9b253291ccbe87e4ca09e13d6e3077928aa2ab80e"
    },
    {
      "id": "weather-climate-riming-supercooled",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Ice accretion process on crystals, unlike identifying snow or hail.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-riming-supercooled",
        "difficulty": "hard",
        "prompt": "Как называется рост снежинки при намерзании столкнувшихся с ней переохлаждённых капель?",
        "answers": [
          {"text": "Аккреция", "note": "Аккреция — рост ледяной частицы при намерзании столкнувшихся с ней переохлаждённых капель."},
          {"text": "Коалесценция капель", "note": "Коалесценция — рост облачных капель при столкновениях и слиянии."},
          {"text": "Процесс Бержерона", "note": "Процесс Бержерона переносит водяной пар от переохлаждённых капель к ледяным кристаллам."},
          {"text": "Агрегация кристаллов", "note": "Агрегация — слипание отдельных ледяных кристаллов в крупные снежинки."}
        ],
        "correctIndex": 0,
        "explanation": "Аккреция происходит, когда переохлаждённые капли сталкиваются со снежным кристаллом и замерзают на нём. В отличие от агрегации, здесь присоединяются жидкие капли, а не другие кристаллы.",
        "source": {"title": "Всемирная метеорологическая организация — Глоссарий Международного атласа облаков", "url": "https://cloudatlas.wmo.int/ru/glossary.html", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "154b30424956689b3925f6ff0e2cf9c9fbf41c2df0bd4a8a9b6a00f19b30cc43"
    },
    {
      "id": "weather-climate-stratus-layer",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Cloud shape taxonomy, not cloud/fog formation.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-stratus-layer",
        "difficulty": "easy",
        "prompt": "Какие облака закрывают небо сплошной низкой пеленой?",
        "answers": [
          {"text": "Кучевые облака", "note": "Кучевые облака имеют отдельные плотные белые вершины и относительно плоское основание."},
          {"text": "Перистые облака", "note": "Перистые облака — высокие тонкие волокнистые облака из ледяных кристаллов."},
          {"text": "Кучево-дождевые облака", "note": "Кучево-дождевые облака развиваются вертикально и несут ливни, грозы и иногда град."},
          {"text": "Слоистые облака", "note": "Слоистые облака образуют низкий ровный серый слой."}
        ],
        "correctIndex": 3,
        "explanation": "Слоистые облака образуют низкий ровный серый слой. Из них может выпадать морось.",
        "source": {"title": "Stratus cloud - Wikipedia", "url": "https://en.wikipedia.org/wiki/Stratus_cloud", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "1ee53542292d7a3073ac04ae99e0b52e642ef464cf9143d2c131c694fca2a614"
    },
    {
      "id": "weather-climate-visibility-distance",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Fog-related outcome metric; it asks a distance measure rather than naming fog.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-visibility-distance",
        "difficulty": "easy",
        "prompt": "Как называется расстояние, на котором можно различить объект сквозь туман или осадки?",
        "answers": [
          {"text": "Влажность", "note": "Влажность характеризует содержание водяного пара в воздухе."},
          {"text": "Атмосферное давление", "note": "Атмосферное давление создаётся весом столба воздуха над поверхностью."},
          {"text": "Видимость", "note": "Метеорологическая видимость — наибольшее расстояние уверенного распознавания объектов."},
          {"text": "Температура воздуха", "note": "Температура воздуха показывает степень его нагретости."}
        ],
        "correctIndex": 2,
        "explanation": "Метеорологическая видимость — наибольшее расстояние уверенного распознавания объектов. Её ухудшают капли, кристаллы, пыль и дым.",
        "source": {"title": "Britannica: Видимость", "url": "https://www.britannica.com/science/visibility-meteorology", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "6212a64d178361c8cc9c20b4ca63373de0a65e385a197a5b0752d02e721935af"
    },
    {
      "id": "weather-climate-warm-cloud-collision",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Warm-cloud microphysics producing rain, not naming rain.",
      "fullCurrentNeighborCard": {
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
      "neighborCardSha256": "a82742b1e1b4ebb737cf20cd053e3bef3214e81946003d358d386f55b83462b0"
    },
    {
      "id": "weather-climate-wet-bulb-evaporation",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "Humidity measurement using a wet-bulb thermometer, not temperature or barometric pressure.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-wet-bulb-evaporation",
        "difficulty": "medium",
        "prompt": "Какой показатель используют вместе с сухим термометром для определения влажности?",
        "answers": [
          {"text": "Температура мокрого термометра", "note": "Температура мокрого термометра понижается из-за испарения воды с влажной оболочки датчика."},
          {"text": "Точка росы", "note": "Точка росы — температура, до которой воздух нужно охладить для насыщения водяным паром."},
          {"text": "Относительная влажность", "note": "Относительная влажность сравнивает фактическое содержание пара с максимально возможным при данной температуре."},
          {"text": "Индекс жары", "note": "Индекс жары оценивает ощущаемую температуру по сочетанию жары и влажности."}
        ],
        "correctIndex": 0,
        "explanation": "Температура мокрого термометра понижается из-за испарения воды с влажной оболочки датчика. Во влажном воздухе разность показаний двух термометров мала.",
        "source": {"title": "Britannica: Температура мокрого термометра", "url": "https://www.britannica.com/technology/psychrometer", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "dbc9ab51373bf9477974af4705d5a8020765c8c17c3e98609a5a7006e4d169b4"
    },
    {
      "id": "weather-climate-weather-current",
      "file": "src/content/topics/weather-climate.json",
      "relationshipJudgment": "General atmospheric state, broader than a selected phenomenon.",
      "fullCurrentNeighborCard": {
        "id": "weather-climate-weather-current",
        "difficulty": "easy",
        "prompt": "Как называется состояние воздуха сегодня: температура, ветер, облачность и осадки?",
        "answers": [
          {"text": "Прогноз погоды", "note": "Прогноз погоды — научно обоснованное предсказание будущего состояния атмосферы."},
          {"text": "Климат", "note": "Климат — многолетний характер погоды и её изменчивости в определённом регионе."},
          {"text": "Сезон", "note": "Сезон — часть года с характерными условиями освещения и погоды."},
          {"text": "Погода", "note": "Погода — текущее состояние атмосферы в конкретном месте и времени."}
        ],
        "correctIndex": 3,
        "explanation": "Погода — текущее состояние атмосферы в конкретном месте и времени. Она может заметно меняться в течение часов.",
        "source": {"title": "Britannica: Погода", "url": "https://www.britannica.com/science/weather-state-of-atmosphere", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "b3dc744ce6a5ce62af5cdd710af4aff5f6d0749f8b692d8933cad78fecc84426"
    },
    {
      "id": "oceans-seas-precipitation-fall",
      "file": "src/content/topics/oceans-seas.json",
      "relationshipJudgment": "Water cycle return of water from clouds, broader than a precipitation type.",
      "fullCurrentNeighborCard": {
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
      "neighborCardSha256": "284f820ff900f0fe4ba99421977882b35d9f578b0a4bfd053aa71af2de83b4e4"
    },
    {
      "id": "ecology-environment-acid-rain",
      "file": "src/content/topics/ecology-environment.json",
      "relationshipJudgment": "Acidity/chemical composition, not ordinary rain identification.",
      "fullCurrentNeighborCard": {
        "id": "ecology-environment-acid-rain",
        "difficulty": "easy",
        "prompt": "Как называют осадки с повышенной кислотностью из-за оксидов серы и азота?",
        "answers": [
          {"text": "Световое загрязнение", "note": "Световое загрязнение изменяет естественную темноту ночи."},
          {"text": "Тепловое загрязнение", "note": "Тепловое загрязнение изменяет температурный режим водоёма."},
          {"text": "Кислотные осадки", "note": "Кислотные осадки образуются, когда соединения серы и азота превращаются в атмосфере в кислоты."},
          {"text": "Загрязнение воздуха", "note": "Загрязнение воздуха возникает, когда вредные вещества попадают в атмосферу в опасных концентрациях."}
        ],
        "correctIndex": 2,
        "explanation": "Кислотные осадки образуются, когда соединения серы и азота превращаются в атмосфере в кислоты. Они подкисляют воды и почвы.",
        "source": {"title": "EPA: Кислотные осадки", "url": "https://www.epa.gov/acidrain/what-acid-rain", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "d242e4e5f158e07ee1bad525029fd1e159e4916f64493cab6a6d3026f504d0cb"
    },
    {
      "id": "ecology-environment-stormwater-runoff",
      "file": "src/content/topics/ecology-environment.json",
      "relationshipJudgment": "Surface flow after precipitation, a downstream consequence.",
      "fullCurrentNeighborCard": {
        "id": "ecology-environment-stormwater-runoff",
        "difficulty": "medium",
        "prompt": "Как называется вода, стекающая по поверхности после дождя и переносящая загрязнители?",
        "answers": [
          {"text": "Сточные воды", "note": "Сточные воды образуются после бытового, промышленного или другого использования воды."},
          {"text": "Ливневый сток", "note": "Ливневый сток течёт по крышам, дорогам и почве после осадков."},
          {"text": "Сельскохозяйственный сток", "note": "Сельскохозяйственный сток переносит с полей питательные вещества, осадки и микроорганизмы."},
          {"text": "Приземный озон", "note": "Приземный озон — вторичный загрязнитель, образующийся в фотохимических реакциях."}
        ],
        "correctIndex": 1,
        "explanation": "Ливневый сток течёт по крышам, дорогам и почве после осадков. Он может переносить масло, мусор и питательные вещества в водоёмы.",
        "source": {"title": "EPA: Ливневый сток", "url": "https://www.epa.gov/npdes/stormwater-discharges-municipal-sources", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "7de4efb25043153dd0872e97ab107259f2be518721b0ee8573d2c25d2543cdde"
    },
    {
      "id": "inventions-technology-thermometer-temperature",
      "file": "src/content/topics/inventions-technology.json",
      "relationshipJudgment": "The general inverse temperature-thermometer relation; current target stem asks a weather-station shelter use.",
      "fullCurrentNeighborCard": {
        "id": "inventions-technology-thermometer-temperature",
        "difficulty": "easy",
        "prompt": "Какую величину измеряет термометр?",
        "answers": [
          {"text": "Скорость", "note": "Скорость показывает изменение положения за единицу времени и измеряется, например, в метрах в секунду."},
          {"text": "Давление", "note": "Давление — скалярная интенсивная физическая величина, характеризующая способность сплошной среды совершать работу при изменении объёма."},
          {"text": "Температуру", "note": "Термометр предназначен для измерения температуры."},
          {"text": "Влажность", "note": "Влажность — показатель содержания воды в физических телах или средах."}
        ],
        "correctIndex": 2,
        "explanation": "Термометр предназначен для измерения температуры. Разные модели используют расширение жидкости, электрические датчики или другие физические эффекты.",
        "source": {"title": "Encyclopaedia Britannica: Thermometer", "url": "https://www.britannica.com/technology/thermometer", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "f1d7b82789177880831545dfecdab09416284130d22c235a6f3da5ebaf818f6f"
    },
    {
      "id": "inventions-technology-ext-barometer-torricelli",
      "file": "src/content/topics/inventions-technology.json",
      "relationshipJudgment": "Same barometer/atmospheric-pressure fact and nearly same prompt; material unresolved duplicate, unrelated to the nine selected stems.",
      "fullCurrentNeighborCard": {
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
        "source": {"title": "Britannica: Evangelista Torricelli", "url": "https://www.britannica.com/biography/Evangelista-Torricelli", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "32f8c6848ae03429e6dbbaa81a06df6147e2a25837d08dbd4d9eba236f1bdcca"
    },
    {
      "id": "laboratories-measurement-hygrometer-humidity",
      "file": "src/content/topics/laboratories-measurement.json",
      "relationshipJudgment": "Adjacent weather instrument but measures humidity, not pressure/temperature.",
      "fullCurrentNeighborCard": {
        "id": "laboratories-measurement-hygrometer-humidity",
        "difficulty": "easy",
        "prompt": "Каким прибором проверяют влажность в помещении?",
        "answers": [
          {"text": "Термометр", "note": "Термометр измеряет температуру по изменению физического свойства чувствительного элемента."},
          {"text": "Гигрометр", "note": "Гигрометр измеряет влажность воздуха."},
          {"text": "Барометр", "note": "Барометр измеряет атмосферное давление."},
          {"text": "Анемометр", "note": "Анемометр измеряет скорость воздушного потока."}
        ],
        "correctIndex": 1,
        "explanation": "Гигрометр измеряет влажность воздуха. Электронные датчики часто реагируют изменением электрических свойств.",
        "source": {"title": "Encyclopaedia Britannica", "url": "https://www.britannica.com/technology/hygrometer", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "c420294b58bf8ca1092a24d42d9ab72f2a007aba511075db88dadb2ea5ba2f27"
    },
    {
      "id": "laboratories-measurement-calibration-reference",
      "file": "src/content/topics/laboratories-measurement.json",
      "relationshipJudgment": "Metrology calibration of a thermometer, not choosing an instrument for weather reading.",
      "fullCurrentNeighborCard": {
        "id": "laboratories-measurement-calibration-reference",
        "difficulty": "medium",
        "prompt": "Как называется сравнение термометра с прослеживаемым эталоном?",
        "answers": [
          {"text": "Калибровка", "note": "Калибровка устанавливает связь показаний прибора с известными значениями эталона."},
          {"text": "Метрологическая прослеживаемость", "note": "Прослеживаемость связывает результат с эталоном документированной непрерывной цепью калибровок."},
          {"text": "Стандартный образец", "note": "Стандартный образец имеет установленные значения свойств и служит для проверки методов."},
          {"text": "Неопределённость измерения", "note": "Неопределённость количественно характеризует обоснованный диапазон значений измеряемой величины."}
        ],
        "correctIndex": 0,
        "explanation": "Калибровка устанавливает связь показаний прибора с известными значениями эталона. Результат не всегда включает регулировку прибора.",
        "source": {"title": "NIST", "url": "https://www.nist.gov/calibrations", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "0cd620d5f80ad762323e69bd757bd602efdf128aed1fd71b8cede9a190ba0bbf"
    },
    {
      "id": "human-medicine-tonometer-purpose",
      "file": "src/content/topics/human-medicine.json",
      "relationshipJudgment": "Medical blood pressure, not atmospheric pressure; vocabulary proximity only.",
      "fullCurrentNeighborCard": {
        "id": "human-medicine-tonometer-purpose",
        "difficulty": "easy",
        "prompt": "Каким прибором измеряют артериальное давление?",
        "answers": [
          {"text": "Термометром", "note": "Термометр измеряет температуру."},
          {"text": "Стетоскопом", "note": "Стетоскоп позволяет выслушивать звуки сердца, лёгких и других органов."},
          {"text": "Тонометром", "note": "Артериальное давление измеряют тонометром, который также называют сфигмоманометром."},
          {"text": "Глюкометром", "note": "Глюкометр измеряет концентрацию глюкозы в образце крови."}
        ],
        "correctIndex": 2,
        "explanation": "Артериальное давление измеряют тонометром, который также называют сфигмоманометром. Результат обычно записывают двумя числами: систолическим и диастолическим давлением.",
        "source": {"title": "NHS: Blood pressure test", "url": "https://www.nhs.uk/conditions/blood-pressure-test/", "verifiedAt": "2026-09-02"}
      },
      "neighborCardSha256": "669699c96dfc5e37711fceb12f7b9a8a7e540832d39d98dec6e3da868607d614"
    }
  ],
  "preservation": {
    "newCaptures": 0,
    "fileWrites": 0,
    "testsRun": 0,
    "buildsRun": 0,
    "gameRuns": 0,
    "qualityCredit": 0,
    "nextStep": "Координатор передаёт единый пакет независимому читателю. До этого редактор не применяет предложения."
  }
}
```

Три примечания по доказательствам:

1. Во всех 17 сохранённых источниках тело и response headers совпали с manifest по байтам и SHA; все 30 процитированных raw/context диапазонов также совпали.
2. В source body Метеоинфо у строки про чередование стоит написание «Снег с дождем»; это сохранённый первоисточник. Я не исправлял его и не делал повторный захват.
3. Текущая карточка Rain формально оставляет морось вне вариантов ответа. Предложенная формулировка вопроса снимает эту неопределённость, а note у Rain добавляет независимое различие с моросью.

Никаких файлов, тестов, сборок или запусков не было. Изменения только предложены; независимая проверка впереди.

Следующий шаг: координатор передаёт этот пакет читателю, затем редактор применяет только квалифицированные изменения.