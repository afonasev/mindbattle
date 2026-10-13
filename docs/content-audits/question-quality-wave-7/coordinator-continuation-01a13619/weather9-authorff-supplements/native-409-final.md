```json
{
  "status": "supplement_to_full_native_packet",
  "scope": "Editorial reasons only: nine targets × six groups. The preceding packet retains the full cards, source reasons and references, class/metadata decisions, and all 29 full neighbor objects.",
  "weatherFileSha256": "29ba8f76ed2065eb33a85358b65369f01cc0791ecb48f059bf2a7525f1737a2d",
  "rainCurrentBinding": {
    "decision": "Retain current card; no prompt or answer-note proposal.",
    "wholeCardSha256": "665b125caaf703bd62c34234d65f7b44ee1f8f2408b6769f27cdb2413f6bd834",
    "hashRecipe": "SHA-256 UTF-8 json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')); no trailing newline.",
    "sixCanonicalGroups": {
      "compositePromptOrderedAnswerTextsAndKey": "dc9ef375c4d9eaf7a7e8c2178bc6b764f5b42ea5ea3be5a6a9f77b73917bd2e3",
      "explanation": "2608fc2313ae508caf28c8e101d1cda68c7c20e9329ea590f57f86cf95728b61",
      "orderedNotes": [
        "c8526be67ac7a8fdc56c991d55517d9181aeaa1af42d28546a9a768cc65f5148",
        "e69ac38c45c20000e0050ae47f9c6fe687d10400537aea091cb3dee635bc63ad",
        "4f675b4e2927939d5d57fc7b525384b16510dc82d14bb47d53a203fb5f8fe51c",
        "72f966328e74969d81ded8127ae939f8eb15573b547b23f3b7569bd3eb06a3a0"
      ],
      "difficulty": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
      "sourceMetadata": "b92400c79d3cd0c505d61ecd50ccd841fc893bb2b5366db463566fd0e581771b"
    },
    "note0SourceBinding": "The current Rain note is supported by the NWS Rain definition: drops greater than 0.5 mm. The separate drizzle threshold is not the basis for this note.",
    "uniqueness": "Rain is the only matching answer among the four current choices. Drizzle is absent, so the stem has no competing offered key."
  },
  "editorialReasons": {
    "weather-climate-rain-liquid": {
      "compositePromptOrderedAnswersAndKey": "The four choices partition the described liquid precipitation from crystals, solid ice balls, and a rain-snow mixture; the key follows from the presented choices.",
      "explanation": "The phase contrast gives a short reason for the selected term and reinforces why the solid alternatives do not fit.",
      "note0Rain": "The size threshold adds a measurable distinguishing property beyond the stem’s description of liquid drops.",
      "note1Snow": "The crystal-aggregation detail explains how snowflakes differ from liquid drops.",
      "note2Hail": "The repeated storm updraft cycle explains the growth of hailstones, adding a formation process rather than just naming their shape.",
      "note3WetSnow": "Snow predominance is the useful distinction from rain alone."
    },
    "weather-climate-snow-crystals": {
      "compositePromptOrderedAnswersAndKey": "Branching crystals joined into flakes point to snow; the other options refer to liquid drops, solid hail, or mixed-phase precipitation.",
      "explanation": "Cloud growth conditions help explain variation in snow-crystal shapes, giving context beyond identifying the form.",
      "note0Snow": "Direct formation from vapor and branching add formation details beyond the prompt’s crystal and flake description.",
      "note1Rain": "The two drop-size boundaries distinguish rain from drizzle and make this alternative informative.",
      "note2Hail": "Compact ice balls contrast with snowflakes assembled from crystals.",
      "note3WetSnow": "This describes a mixed precipitation type rather than snow by itself."
    },
    "weather-climate-hail-ice-balls": {
      "compositePromptOrderedAnswersAndKey": "Hard ice balls after a thunderstorm distinguish hail from liquid rain, crystal snow, and mixed wet snow.",
      "explanation": "The cloud association and size cutoff explain what classifies these particles as hail.",
      "note0Hail": "The 5 mm cutoff adds a useful classification boundary beyond the visual clue.",
      "note1Rain": "Liquid drops and their size criterion distinguish rain from solid hailstones.",
      "note2Snow": "Crystal flakes differ in structure from the solid ice balls in the stem.",
      "note3WetSnow": "Wet snow is mixed precipitation, so it does not describe separate hard ice balls."
    },
    "weather-climate-sleet-mix": {
      "compositePromptOrderedAnswersAndKey": "Simultaneous rain and snow with snow predominating identify wet snow; the other choices describe one phase alone or hail.",
      "explanation": "The difference between simultaneous precipitation and alternating snow and rain helps prevent confusion between neighboring forecast terms.",
      "note0Rain": "The drop-size detail gives a concrete property of the liquid component.",
      "note1WetSnow": "The proposed synonym adds a separate descriptive term instead of repeating the stem and keyed definition.",
      "note2Snow": "Crystal flakes distinguish snow alone from the mixed event in the question.",
      "note3Hail": "Ice balls distinguish hail from the stated rain-snow mixture."
    },
    "weather-climate-fog-ground-cloud": {
      "compositePromptOrderedAnswersAndKey": "Near-ground suspended moisture and reduced visibility identify fog; dew and frost are surface deposits, while cloud is higher in the atmosphere.",
      "explanation": "Night cooling followed by saturation gives a causal account of the described fog.",
      "note0Dew": "Dew is deposited on objects, which distinguishes it from suspended fog droplets.",
      "note1Fog": "The visibility threshold adds a practical severity consequence beyond the prompt’s general loss of clarity.",
      "note2Frost": "Frost crystals form on cold surfaces rather than remaining suspended as liquid droplets.",
      "note3Cloud": "The altitude distinction helps separate cloud from fog."
    },
    "weather-climate-dew-condensation": {
      "compositePromptOrderedAnswersAndKey": "Liquid drops on leaves after a dry night indicate a surface deposit; fog and cloud are airborne, while frost is frozen.",
      "explanation": "Cooling to the dew point explains the condensation that produced the drops.",
      "note0Fog": "Suspended droplets distinguish fog from water deposited on leaves.",
      "note1Dew": "Surface cooling below the dew point explains why condensation appears on objects.",
      "note2Frost": "Ice crystals distinguish frost from liquid dew.",
      "note3Cloud": "Cloud particles are aloft rather than deposited on leaves."
    },
    "weather-climate-frost-ice": {
      "compositePromptOrderedAnswersAndKey": "Thin white crystals on grass indicate a surface deposit; fog and cloud are airborne, while dew is liquid.",
      "explanation": "Cooling below freezing explains the formation of ice crystals on grass and other surfaces.",
      "note0Fog": "Ice fog shows that ice particles can be suspended in air, unlike the frost deposit in the stem.",
      "note1Dew": "Dew is liquid moisture on a surface, not ice crystals.",
      "note2Frost": "The listed shapes and sub-zero condition add recognizable frost detail beyond naming it.",
      "note3Cloud": "Cloud particles are airborne, unlike the coating on grass."
    },
    "weather-climate-cloud-droplets": {
      "compositePromptOrderedAnswersAndKey": "Visible droplets or ice crystals at altitude after moist air rises identify a cloud; fog is near the surface and dew or frost are surface deposits.",
      "explanation": "Small droplet size and rising air explain how cloud particles remain suspended.",
      "note0Fog": "Near-surface suspension distinguishes fog from the higher cloud in the prompt.",
      "note1Dew": "Dew is deposited on objects rather than forming a free-air aggregate.",
      "note2Cloud": "Small size and updrafts explain why the droplets remain aloft.",
      "note3Frost": "Frost crystals settle on cold surfaces; cloud particles remain airborne."
    },
    "weather-climate-thermometer-temperature": {
      "compositePromptOrderedAnswersAndKey": "The prompt asks which instrument needs shelter from solar heating; the alternatives measure pressure, wind speed, and precipitation quantity.",
      "explanation": "It links the thermometer’s purpose to the measurement error caused by direct solar heating.",
      "note0Barometer": "Pressure is a different measured quantity from temperature.",
      "note1Anemometer": "Wind speed is a different measured quantity from temperature.",
      "note2RainGauge": "Precipitation quantity distinguishes the rain gauge from the temperature instrument.",
      "note3Thermometer": "Protection from precipitation and condensation, with ventilation, extends the sunlight clue into the instrument’s practical shelter requirements."
    }
  },
  "sleetProposal": {
    "onlyChangedField": "weather-climate-sleet-mix.answers[1].note",
    "value": "В справочнике Росгидромета мокрый снег также назван тающим снегом.",
    "proposedWholeCardSha256": "d85914aded7b14dc90c7592b9710af06d8d29cb093f5a795d5b3e41576edab53"
  },
  "preservation": {
    "rainProposalWithdrawn": true,
    "otherSevenCardsUnchanged": true,
    "sourceReferencesAndFullNeighborObjects": "Retained from the preceding full native packet.",
    "newSourceWork": 0,
    "fileWrites": 0,
    "qualityCredit": 0,
    "independentReaderStarted": false
  }
}
```