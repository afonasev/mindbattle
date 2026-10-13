```json
{
  "status": "supplement_to_full_native_packet",
  "qualityCredit": 0,
  "sourceAndNeighborObjects": "Retained unchanged from the preceding full native packet. Neighbor-card identity SHA confirms object equality with the catalog; it is not itself a semantic-deduplication test.",
  "hashRecipes": {
    "wholeCard": "SHA-256 over UTF-8 json.dumps(fullCard, sort_keys=True, ensure_ascii=False, separators=(',', ':')); no trailing newline.",
    "compositePromptOrderedAnswerTextsAndKey": "For every card, hash the JSON object with exactly these members: {\"prompt\": card.prompt, \"answers\": card.answers.map(answer => answer.text) in array order, \"correctIndex\": card.correctIndex}. The answers array preserves choice order. Serialize the object using the whole-card recipe.",
    "stringScalars": "For each note and difficulty string, hash its JSON serialization, including surrounding quotes and JSON escaping, using ensure_ascii=False; do not hash bare UTF-8 string bytes.",
    "sourceMetadata": "Hash the full source metadata object using the whole-card recipe.",
    "orderedNotes": "Four independent JSON-string scalar hashes in answer-index order 0, 1, 2, 3."
  },
  "compositeValues": [
    {
      "id": "weather-climate-rain-liquid",
      "value": {
        "prompt": "В прогнозе сказано, что из облака осадки выпадают отдельными жидкими каплями, без снежинок или ледяных частиц. Как называется этот вид осадков?",
        "answers": ["Дождь", "Снег", "Град", "Мокрый снег"],
        "correctIndex": 0
      },
      "sha256": "dc9ef375c4d9eaf7a7e8c2178bc6b764f5b42ea5ea3be5a6a9f77b73917bd2e3"
    },
    {
      "id": "weather-climate-snow-crystals",
      "value": {
        "prompt": "Какие осадки выпадают в виде разветвлённых ледяных кристаллов, часто соединённых в снежинки?",
        "answers": ["Снег", "Дождь", "Град", "Мокрый снег"],
        "correctIndex": 0
      },
      "sha256": "2f33fa46f112bfa918b97cfe0374e1a8047cefb558c2d33a88177f79b71defbf"
    },
    {
      "id": "weather-climate-hail-ice-balls",
      "value": {
        "prompt": "После грозы на земле нашли твёрдые ледяные шарики и комочки. Как называются такие осадки?",
        "answers": ["Град", "Дождь", "Снег", "Мокрый снег"],
        "correctIndex": 0
      },
      "sha256": "4f4e447610a1a3afa4853e61d39ad2f4456b390014204f32e9bf0ae1181dc9d4"
    },
    {
      "id": "weather-climate-sleet-mix",
      "value": {
        "prompt": "В осадках одновременно присутствуют дождь и снег, причём снег преобладает. Как называется такой вид осадков?",
        "answers": ["Дождь", "Мокрый снег", "Снег", "Град"],
        "correctIndex": 1
      },
      "sha256": "fd9700273ea8efb44f93f938fdfe9728c1b65a9a90ed887928e1b0a043e35c3a"
    },
    {
      "id": "weather-climate-fog-ground-cloud",
      "value": {
        "prompt": "После ясной прохладной ночи воздух у земли помутнел, а предметы вдали стали плохо различимы. Как называется это явление?",
        "answers": ["Роса", "Туман", "Иней", "Облако"],
        "correctIndex": 1
      },
      "sha256": "84bf55e92f19ab1db7ae3f835c59f93f2a9ce01d7d18e2b2903805a827e71994"
    },
    {
      "id": "weather-climate-dew-condensation",
      "value": {
        "prompt": "После ясной ночи на листьях появились жидкие капли, хотя дождя не было. Как называется эта влага?",
        "answers": ["Туман", "Роса", "Иней", "Облако"],
        "correctIndex": 1
      },
      "sha256": "e2f0bdd98de3c2e1f0c0404424653d328157764c6c0e71d003b95f9460069ce9"
    },
    {
      "id": "weather-climate-frost-ice",
      "value": {
        "prompt": "На траве после холодной ночи видны тонкие белые кристаллы льда. Как называется такой налёт?",
        "answers": ["Туман", "Роса", "Иней", "Облако"],
        "correctIndex": 2
      },
      "sha256": "fcd6563ec6bdea2770128d7e689467d9dddb3f72bcab7017228e96f362ee683f"
    },
    {
      "id": "weather-climate-cloud-droplets",
      "value": {
        "prompt": "После подъёма влажного воздуха в небе на высоте появились видимые капли воды или кристаллы льда. Как называется это скопление?",
        "answers": ["Туман", "Роса", "Облако", "Иней"],
        "correctIndex": 2
      },
      "sha256": "bd8978afa2a001ce4cc6227cb3fcb1f52da26c118f8453ee0876cb3e1ca1672b"
    },
    {
      "id": "weather-climate-thermometer-temperature",
      "value": {
        "prompt": "Какой прибор на метеостанции защищают от прямого солнечного нагрева, чтобы его показания не искажались?",
        "answers": ["Барометр", "Анемометр", "Осадкомер", "Термометр"],
        "correctIndex": 3
      },
      "sha256": "ae44f1df3a57ee7d0830b88ffc42f904a372cbb43a8533e95507f4efd936389a"
    }
  ],
  "cardSpecificNeighborComparisons": [
    {
      "targetId": "weather-climate-rain-liquid",
      "neighborIds": [
        "weather-climate-convectional-rain",
        "weather-climate-frontal-rain",
        "weather-climate-orographic-rain",
        "weather-climate-rain-gauge",
        "weather-climate-rain-shadow",
        "weather-climate-rainbow-refraction",
        "weather-climate-warm-cloud-collision",
        "oceans-seas-precipitation-fall",
        "ecology-environment-acid-rain",
        "ecology-environment-stormwater-runoff"
      ],
      "comparison": "The target names liquid precipitation. The rain-process cards ask how rain forms; rain gauge asks how much fell; rain shadow names a dry region; rainbow asks about optics; acid rain concerns chemistry; stormwater runoff is a downstream flow; oceans-seas-precipitation-fall asks for the broad water-cycle category. None asks the same fact or its inverse. Within the selected nine, snow, hail, and wet snow are different phase/form choices."
    },
    {
      "targetId": "weather-climate-snow-crystals",
      "neighborIds": [
        "weather-climate-bergeron-ice",
        "weather-climate-cirrus-feathery",
        "weather-climate-cumulonimbus-storm",
        "weather-climate-cumulus-puffy",
        "weather-climate-riming-supercooled",
        "weather-climate-stratus-layer",
        "weather-climate-warm-cloud-collision",
        "oceans-seas-precipitation-fall"
      ],
      "comparison": "The target identifies crystal precipitation. Bergeron and riming ask about microphysical processes; cirrus, cumulus, cumulonimbus, and stratus identify cloud types; warm-cloud collision asks how rain forms; oceans-seas-precipitation-fall asks for the broad precipitation category. Within the selected nine, hail is compact ice, wet snow is a rain-snow mixture, and rain is liquid."
    },
    {
      "targetId": "weather-climate-hail-ice-balls",
      "neighborIds": [
        "weather-climate-bergeron-ice",
        "weather-climate-cumulonimbus-storm",
        "weather-climate-riming-supercooled",
        "weather-climate-warm-cloud-collision",
        "oceans-seas-precipitation-fall"
      ],
      "comparison": "The target names solid hail from observed ice balls. Cumulonimbus identifies a storm cloud; Bergeron, riming, and warm-cloud collision ask about cloud processes; the oceans card asks for the precipitation umbrella term. The selected snow and wet-snow cards describe different particle forms."
    },
    {
      "targetId": "weather-climate-sleet-mix",
      "neighborIds": [
        "weather-climate-convectional-rain",
        "weather-climate-frontal-rain",
        "weather-climate-orographic-rain",
        "weather-climate-rain-gauge",
        "weather-climate-warm-cloud-collision",
        "oceans-seas-precipitation-fall"
      ],
      "comparison": "The target names simultaneous rain and snow with snow predominating. Rain-process and warm-cloud cards ask about causes; rain gauge asks about quantity; the oceans card asks for the broader category. The NWS Sleet primary capture describes ice pellets in English, which is a different term from the Russian Meteoinfo definition used by this card. No reviewed neighbor states the same mixed-phase criterion or its inverse."
    },
    {
      "targetId": "weather-climate-fog-ground-cloud",
      "neighborIds": [
        "weather-climate-cirrus-feathery",
        "weather-climate-cumulus-puffy",
        "weather-climate-cumulonimbus-storm",
        "weather-climate-stratus-layer",
        "weather-climate-visibility-distance",
        "weather-climate-dew-point-saturation",
        "weather-climate-relative-humidity-ratio",
        "weather-climate-heat-index-feels",
        "weather-climate-wet-bulb-evaporation",
        "weather-climate-weather-current"
      ],
      "comparison": "The target identifies suspended moisture at ground level after nighttime cooling. Cloud-type cards ask about cloud shape or storm type; visibility-distance asks for a measurement; dew-point, humidity, heat-index, and wet-bulb cards ask about moisture or temperature indicators; weather-current asks for the broad atmospheric state. Within the selected nine, cloud is the airborne-at-height case, while dew and frost are surface deposits."
    },
    {
      "targetId": "weather-climate-dew-condensation",
      "neighborIds": [
        "weather-climate-dew-point-saturation",
        "weather-climate-relative-humidity-ratio",
        "weather-climate-wet-bulb-evaporation",
        "weather-climate-heat-index-feels",
        "weather-climate-visibility-distance",
        "laboratories-measurement-hygrometer-humidity"
      ],
      "comparison": "The target names liquid water deposited on leaves. Dew-point and humidity cards ask for air indicators; wet-bulb and heat-index ask about measurement or perceived temperature; visibility asks for distance; hygrometer asks which instrument measures humidity. These share moisture vocabulary but do not identify surface condensation. Within the selected nine, fog/cloud are airborne and frost is frozen."
    },
    {
      "targetId": "weather-climate-frost-ice",
      "neighborIds": [
        "weather-climate-bergeron-ice",
        "weather-climate-riming-supercooled",
        "weather-climate-cirrus-feathery",
        "weather-climate-visibility-distance",
        "weather-climate-dew-point-saturation"
      ],
      "comparison": "The target identifies crystals deposited on grass. Bergeron and riming ask about ice-growth processes; cirrus asks about a high-cloud type; visibility and dew-point ask about atmospheric measures. Shared references to ice or cold do not ask for surface frost. Within the selected nine, dew is liquid, while fog and cloud are suspended."
    },
    {
      "targetId": "weather-climate-cloud-droplets",
      "neighborIds": [
        "weather-climate-cirrus-feathery",
        "weather-climate-cumulus-puffy",
        "weather-climate-cumulonimbus-storm",
        "weather-climate-stratus-layer",
        "weather-climate-bergeron-ice",
        "weather-climate-warm-cloud-collision",
        "weather-climate-riming-supercooled",
        "weather-climate-visibility-distance",
        "weather-climate-weather-current",
        "oceans-seas-precipitation-fall"
      ],
      "comparison": "The target names an elevated aggregate of droplets or ice crystals after moist air rises. Cloud-shape and storm cards classify cloud forms; Bergeron, collision, and riming ask about microphysics; visibility asks for a distance; weather-current asks for an overall state; oceans-seas asks for the precipitation category. Within the selected nine, fog differs by near-surface altitude and dew/frost by surface deposition."
    },
    {
      "targetId": "weather-climate-thermometer-temperature",
      "neighborIds": [
        "weather-climate-anemometer-speed",
        "weather-climate-dew-point-saturation",
        "weather-climate-heat-index-feels",
        "weather-climate-relative-humidity-ratio",
        "weather-climate-wet-bulb-evaporation",
        "inventions-technology-thermometer-temperature",
        "inventions-technology-ext-barometer-torricelli",
        "laboratories-measurement-hygrometer-humidity",
        "laboratories-measurement-calibration-reference",
        "human-medicine-tonometer-purpose"
      ],
      "comparison": "The target asks which weather-station instrument needs shelter from direct sunlight. The anemometer and barometer cards ask what those instruments measure; the humidity and heat cards ask for atmospheric measures; the laboratory card asks about calibration; the tonometer measures medical pressure. The general thermometer neighbor asks for the quantity measured, not station exposure or shelter. The ext-barometer neighbor is a possible duplicate of the separate pressure-measurement card, but it is not an exact or inverse duplicate of this thermometer-shelter question."
    }
  ],
  "selectedSetComparison": {
    "precipitationCluster": "Rain, snow, hail, and wet snow share distractor labels but have distinct keys: liquid drops, ice crystals, solid ice balls, and simultaneous rain/snow with snow predominating.",
    "nearSurfaceCluster": "Fog and cloud both concern suspended moisture but differ by altitude; dew and frost are deposits on surfaces and differ by liquid versus ice.",
    "instrumentCluster": "The thermometer target asks about protecting a temperature instrument from solar heating; neighboring instrument cards ask what other instruments measure."
  },
  "preservation": {
    "rainProposalWithdrawn": true,
    "rainCurrentCardRetained": true,
    "sleetProposalUnchangedFromPreviousSupplement": true,
    "newSources": 0,
    "newCaptures": 0,
    "fileWrites": 0,
    "qualityCredit": 0,
    "independentReaderStarted": false,
    "nextStep": "Передать связанный полный native-пакет независимому читателю."
  }
}
```