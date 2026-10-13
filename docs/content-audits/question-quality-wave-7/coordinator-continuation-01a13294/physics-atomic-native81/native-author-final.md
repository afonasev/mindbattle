```json
{
  "schema": "mindbattle-physics-same-exact7-atomic-author-packet-v1",
  "identity": {
    "nativeThreadId": "01a13281-553f-7a12-a494-469f909fd04b",
    "coordinatorRootId": "01a13294-7d84-7583-930d-02eb1c80eb45",
    "actualCompactions": 1,
    "worktree": "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle",
    "branch": "codex/question-quality-wave-6",
    "sourceBaseline": "663ea03",
    "scopeFile": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a131f2/physics-exact-pending7-successor-current-scope.json"
  },
  "status": "PARTIAL_AUTHOR_PACKET_NOT_APPLIED",
  "qualification": {
    "atomicSubset": ["physics-current-si-unit"],
    "pending": [
      "physics-force-si-unit",
      "physics-heat-spontaneous-direction",
      "physics-rainbow-color-separation",
      "physics-sound-vacuum",
      "physics-mass-weight-distinction",
      "physics-density-definition"
    ],
    "reason": "Only the current-direction card has a complete candidate and review packet in this response. No content was written. The OpenStax source body matches its pinned Git blob, but its captured headers hash differs from the historical manifest value; that provenance discrepancy is disclosed below."
  },
  "topicSnapshot": {
    "path": "src/content/topics/physics.json",
    "bytes": 178520,
    "sha256": "324ff43f47531a73e338da21e2affa8b937553f407daec2cc6ef049baf080db3",
    "canonicalCardRecipe": "SHA256(UTF-8 JSON with sort_keys=true, ensure_ascii=false, separators=(\",\", \":\")); no trailing LF.",
    "fixedScopeSlots": {
      "physics-force-si-unit": ["easy", 3],
      "physics-heat-spontaneous-direction": ["easy", 0],
      "physics-rainbow-color-separation": ["easy", 3],
      "physics-current-si-unit": ["easy", 1],
      "physics-sound-vacuum": ["easy", 2],
      "physics-mass-weight-distinction": ["medium", 3],
      "physics-density-definition": ["medium", 3]
    },
    "currentTargetCanonicalSha256": {
      "physics-force-si-unit": "fc251dc8cba537d9451c3d093a2ac35dee0bfd0d634cf25c139e757fa086ad38",
      "physics-heat-spontaneous-direction": "f0ca000d5c6384c406fb62a7c8bd33b9fbf8afc72d59d918ed0fe6226295f56d",
      "physics-rainbow-color-separation": "c8ce1dba9ef24253eddce21be7216878e6fcf39873d2edac2463a81a3daba50c",
      "physics-current-si-unit": "0f92fc0b25c282ac1b0a68c2209c042eee7bba6c0f4d85f7823f1ae7edb4e5dc",
      "physics-sound-vacuum": "07ef8b2d8c166c2599b07a19c45c50b698ff230d0961f0c1c529dce16d024404",
      "physics-mass-weight-distinction": "ba394755c38ffc998324419a50780301d74be13e01b5f319896ba0220d171417",
      "physics-density-definition": "370dcb24bb104b6a1fc2d279ea5bd157abf5d018d4957ca4036bea322b34034a"
    },
    "preservation": "The six pending cards, the other 93 physics cards, the three certified cards, full order, difficulty slots and key slots remain outside this proposed edit. No fresh post-edit 93-card baseline comparison is claimed in this packet."
  },
  "currentLiteral": {
    "card": {
      "id": "physics-current-si-unit",
      "difficulty": "easy",
      "prompt": "Каким символом в СИ обозначают ампер?",
      "answers": [
        {
          "text": "V",
          "note": "V — символ вольта, единицы электрического напряжения."
        },
        {
          "text": "A",
          "note": "Символы единиц СИ печатают прямым шрифтом; если символ происходит от имени собственного, его первая буква — заглавная."
        },
        {
          "text": "C",
          "note": "C — символ кулона, единицы электрического заряда."
        },
        {
          "text": "Ω",
          "note": "Ω — символ ома, единицы электрического сопротивления."
        }
      ],
      "correctIndex": 1,
      "explanation": "Ампер обозначают символом A. В обозначениях единиц СИ символы не переводят в форму множественного числа и пишут без точки.",
      "source": {
        "title": "BIPM, The International System of Units, 9th edition",
        "url": "https://www.bipm.org/documents/d/guest/si-brochure-9-2_01",
        "verifiedAt": "2026-10-13"
      }
    },
    "canonicalCardSha256": "0f92fc0b25c282ac1b0a68c2209c042eee7bba6c0f4d85f7823f1ae7edb4e5dc",
    "groupSha256": {
      "prompt_answers_key": "d033c01ad21f346ce539321e2dd5cd2de9d78e0927aac60850642ef9def4c084",
      "explanation": "fd9c6496b143858db523db9615487d08cff09c2c3fbc722c3bef669360af94de",
      "note0": "0a36e2e76c4f78ebb52c755e6724e33c9fe30712a733ce6e367bbc667e5663c7",
      "note1": "137411ad650de952b89b6e6091c67b5643a2cd3a6a2b6178be8777d884d751e2",
      "note2": "a8fdda4e2773cd13bbbb1bff9a7b015acfb1a33be511b744c47c378e8bd8308b",
      "note3": "e7a165f1b167c4ae4ac0f65ad8c01d1c5437d0ce7ae8775449b241bda4922266"
    }
  },
  "candidate": {
    "id": "physics-current-si-unit",
    "difficulty": "easy",
    "prompt": "Электроны в металлическом проводе дрейфуют вдоль провода. Как соотносится с этим направлением условное направление тока?",
    "answers": [
      {
        "text": "Совпадает с дрейфом электронов",
        "note": "Электроны имеют отрицательный заряд, поэтому их дрейф противоположен условному направлению тока."
      },
      {
        "text": "Противоположно дрейфу электронов",
        "note": "Условный ток направлен так, как двигался бы положительный заряд; отрицательные электроны дрейфуют в противоположную сторону."
      },
      {
        "text": "Перпендикулярно дрейфу электронов",
        "note": "И дрейф электронов, и ток в данном проводе направлены вдоль него; различается направление движения, а не ось."
      },
      {
        "text": "У металлического тока нет условного направления",
        "note": "Направление условного тока определено и для металлического провода: оно совпадает с направлением движения положительного заряда."
      }
    ],
    "correctIndex": 1,
    "explanation": "Условное направление тока задают как направление движения положительного заряда. В металле ток переносят отрицательно заряженные электроны, поэтому их дрейф направлен противоположно условному току.",
    "source": {
      "title": "OpenStax, College Physics 2e 20.1 Current",
      "url": "https://openstax.org/books/college-physics-2e/pages/20-1-current",
      "verifiedAt": "2026-10-13"
    }
  },
  "candidateCanonicalSha256": "df4252fb04a54fa034f3d3a1222a6984e7c52e0bfcbfcde9a4eb9ad862ddc344",
  "candidateSixGroupReceipt": [
    {
      "group": "prompt+ordered-answer-texts+correctIndex",
      "verdict": "AUTHOR_PASS",
      "sha256": "caf3aca92aacfdf88b5d9a4b8ab915e606dfc2894fde0873b6780045faadf6d2",
      "rationale": "Tests the direction convention relative to electron drift, a separate primary fact from the old ampere-symbol prompt and from current-as-charge-per-time."
    },
    {
      "group": "explanation",
      "verdict": "AUTHOR_PASS",
      "sha256": "614ee4aad8f3b54f444e7d8594900ec605a5c2c3744e1c57d73b9011c73e9ad7",
      "rationale": "States the positive-charge convention and applies the negative sign of electrons to obtain the opposite drift direction."
    },
    {
      "group": "note0",
      "verdict": "AUTHOR_PASS",
      "sha256": "ecb2ac72dc6e2e1f98b46bfbf9d7de3c648ce9bebb4f3dde07be91c70533317b",
      "rationale": "Explains why the same-direction distractor reverses the sign convention."
    },
    {
      "group": "note1",
      "verdict": "AUTHOR_PASS",
      "sha256": "5cfa3ebe486a326af81659a4f1a19ea6bbacc51fd93459af225d67b44f226f0b",
      "rationale": "Gives the positive-charge definition and its application to negative electron carriers."
    },
    {
      "group": "note2",
      "verdict": "AUTHOR_PASS",
      "sha256": "a18f249692532d24eeefffe20ed715fc7b13dce5d9be9654b36b9fd059112536",
      "rationale": "Explains that the direction is along the conductor; the convention reverses orientation, not the wire axis."
    },
    {
      "group": "note3",
      "verdict": "AUTHOR_PASS",
      "sha256": "4f3eeadc1e94916a39b344755c71afb3fbbe45c5c11e38a7df74b3981e8b58ed",
      "rationale": "The primary paragraph defines conventional current for positive-charge motion and explicitly applies it to metal wires carrying electron current."
    }
  ],
  "difficultyAndSourceMetadata": {
    "difficulty": {
      "literal": "easy",
      "sha256": "3ed870088e7410ee05d36e4fc20bf73104130ef98000b268b11378d0800d1703",
      "verdict": "AUTHOR_PASS",
      "rationale": "The prompt supplies the electron drift and asks for the elementary school-circuit sign convention; it requires one familiar charge-sign relation, with no rare date or advanced calculation. This is the current-direction candidate, not the specialized candela proposal."
    },
    "sourceMetadata": {
      "literal": {
        "title": "OpenStax, College Physics 2e 20.1 Current",
        "url": "https://openstax.org/books/college-physics-2e/pages/20-1-current",
        "verifiedAt": "2026-10-13"
      },
      "sha256": "2baeff153a04db7c3206c684318c72e5276571d640e91d628988663e76eefb2d",
      "verdict": "AUTHOR_PASS_WITH_CAPTURE_HEADER_MISMATCH_DISCLOSED",
      "rationale": "The captured body matches the pinned OpenStax Git blob. The actual headers file is hashed below; its hash differs from the value recorded by the old capture manifest."
    },
    "difficultyPolicy": "GAME_SPEC.md § Контент вопросов: Easy tests a widely known adult-audience fact, including facts common within a large demographic or cultural group, and avoids rare terminology/trivia. This item applies the basic school-circuit convention rather than asking for a specialized unit name."
  },
  "sourceProof": {
    "capture": {
      "title": "OpenStax, College Physics 2e 20.1 Current",
      "url": "https://raw.githubusercontent.com/openstax/osbooks-college-physics-bundle/fd1b25dfd5d8c6580c6e2b2b34a19e29cc69ada9/modules/m42341/index.cnxml",
      "path": "docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/openstax-m42341-index.cnxml",
      "bytes": 79843,
      "sha256": "aea3ce841c221934d07f022163311c178cab50b6480de398744838c890539e76",
      "gitBlobSha1": "10ef2f3e78e7ef0b5d915a3f18929bcc843be887",
      "matchesPinnedGitBlob": true,
      "headersPath": "docs/content-audits/question-quality-wave-7/physics/first10-native-01a13201-b4e9-7b12-b72d-3538bd95ad14/originals/openstax-m42341.headers.txt",
      "headersBytes": 897,
      "actualHeadersSha256": "1a6d11daf19637c338ee0e20dc2716769a4fffc0951d1ce00dd6570a9c945d4b4",
      "historicalManifestHeadersSha256": "357ed1f2b5de3850509b51890cfc9369cc58a1afbedc0f434b335a47c84301e8",
      "handling": "Preserve both values; do not claim the historical headers receipt matches. Source body bytes match the pinned OpenStax module blob."
    },
    "fullRelevantSourceContext": {
      "locator": "OpenStax College Physics 2e 20.1 Current, module m42341, section Electric Current, paragraph id import-auto-id1207319, raw byte offsets 13063–14267 in the captured body.",
      "literal": "<para id=\"import-auto-id1207319\">Note that the direction of current flow in <link target-id=\"import-auto-id2931325\"/> is from positive to negative. <emphasis effect=\"italics\">The direction of conventional current is the direction that positive charge would flow</emphasis>. Depending on the situation, positive charges, negative charges, or both may move. In metal wires, for example, current is carried by electrons—that is, negative charges move. In ionic solutions, such as salt water, both positive and negative charges move. This is also true in nerve cells. A Van de Graaff generator used for nuclear research can produce a current of pure positive charges, such as protons. <link target-id=\"import-auto-id1575921\"/> illustrates the movement of charged particles that compose a current. The fact that conventional current is taken to be in the direction that positive charge would flow can be traced back to American politician and scientist Benjamin Franklin in the 1700s. He named the type of charge associated with electrons negative, long before they were known to carry current in so many situations. Franklin, in fact, was totally unaware of the small-scale structure of electricity.</para>",
      "supportMap": {
        "prompt+key+explanation": "The source defines conventional current as positive-charge motion and says metal-wire current is carried by negative electrons.",
        "note0": "The source identifies electrons in metal wires as negative charges and defines conventional direction by positive-charge motion.",
        "note1": "The source explicitly states the positive-charge convention and that electrons carry current in metal wires.",
        "note2": "The current-flow sentence and the metal-wire carrier sentence support the same-conductor axis; the opposite orientation follows from the defined sign convention.",
        "note3": "The paragraph explicitly defines conventional-current direction, including for wires carrying electron current."
      }
    }
  },
  "deduplication": {
    "wholeCatalogScan": {
      "cardsScanned": 11000,
      "retrieval": "Russian lexical patterns for conditional-current direction and electron drift produced one unrelated result, spaceflight-hall-thruster. Earlier broad semantic retrieval surfaced the current-definition and ammeter cards listed below.",
      "conclusion": "No exact or direct/inverse duplicate was found among the manually inspected current-direction candidates. Retrieval is a shortlist method, not a claim that every one of 11,000 cards was read manually."
    },
    "fullCurrentNeighborReceipts": [
      {
        "id": "physics-ext-electric-current-charge-flow",
        "difficulty": "easy",
        "prompt": "Какая электрическая величина измеряется в амперах и равна заряду, проходящему за единицу времени?",
        "answers": [
          {
            "text": "Напряжение",
            "note": "Напряжение равно изменению электрической потенциальной энергии на единицу заряда."
          },
          {
            "text": "Сила тока",
            "note": "Сила тока равна заряду, проходящему через сечение проводника за единицу времени."
          },
          {
            "text": "Частота",
            "note": "Частота равна числу циклов, происходящих за секунду."
          },
          {
            "text": "Длина волны",
            "note": "Длина волны — расстояние между соседними гребнями или другими однофазными точками."
          }
        ],
        "correctIndex": 1,
        "explanation": "Сила тока равна заряду, проходящему через сечение проводника за единицу времени. Её измеряют в амперах.",
        "source": {
          "title": "OpenStax Physics: Ohm’s Law",
          "url": "https://openstax.org/books/physics/pages/19-1-ohms-law",
          "verifiedAt": "2026-09-02"
        },
        "review": "This asks for current as charge per time; the candidate asks the sign convention relating electron drift to conventional current. Related topic, distinct tested fact."
      },
      {
        "id": "laboratories-measurement-ammeter-current",
        "difficulty": "easy",
        "prompt": "Какой прибор включают последовательно для измерения силы тока?",
        "answers": [
          {
            "text": "Амперметр",
            "note": "Амперметр измеряет электрический ток и включается последовательно в цепь."
          },
          {
            "text": "Вольтметр",
            "note": "Вольтметр измеряет разность потенциалов и подключается параллельно участку."
          },
          {
            "text": "Омметр",
            "note": "Омметр измеряет электрическое сопротивление, используя собственный источник питания."
          },
          {
            "text": "Осциллограф",
            "note": "Осциллограф отображает изменение электрического сигнала во времени."
          }
        ],
        "correctIndex": 0,
        "explanation": "Амперметр измеряет электрический ток и включается последовательно в цепь. Малое внутреннее сопротивление уменьшает влияние на цепь.",
        "source": {
          "title": "Encyclopaedia Britannica",
          "url": "https://www.britannica.com/technology/ammeter",
          "verifiedAt": "2026-09-02"
        },
        "review": "This asks which instrument and connection measure current; the candidate asks the electron/current direction convention."
      },
      {
        "id": "physics-lenz-law-direction",
        "difficulty": "medium",
        "prompt": "Что определяет правило Ленца в явлении электромагнитной индукции?",
        "answers": [
          {
            "text": "Число электронов в атоме",
            "note": "Число электронов связано с зарядовым состоянием атома и не описывает направление электрического эффекта в контуре."
          },
          {
            "text": "Скорость света в веществе",
            "note": "Скорость света в веществе зависит от показателя преломления среды."
          },
          {
            "text": "Направление индукционного тока",
            "note": "Правило Ленца задаёт такое направление индукционного тока, при котором его магнитное поле противодействует изменению магнитного потока."
          },
          {
            "text": "Температуру плавления проводника",
            "note": "Температура плавления — свойство материала проводника, а не правило выбора направления индукционного тока."
          }
        ],
        "correctIndex": 2,
        "explanation": "Правило Ленца задаёт такое направление индукционного тока, при котором его магнитное поле противодействует изменению магнитного потока. Этот знак согласуется с законом сохранения энергии.",
        "source": {
          "title": "Encyclopaedia Britannica: Lenz's law",
          "url": "https://www.britannica.com/science/Lenzs-law",
          "verifiedAt": "2026-09-02"
        },
        "review": "Lenz's law determines induced-current direction from changing magnetic flux; this candidate tests the conventional sign of conduction current relative to electron drift."
      }
    ]
  },
  "worktreeAndChecks": {
    "writesThisTurn": false,
    "testsRun": false,
    "buildsRun": false,
    "commitsMade": false,
    "preexistingUncommittedChangesPreserved": [
      "src/content/topics/physics.json: two earlier note edits remain from prior task turns",
      "docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-fresh-rework19/sources/newadvent-rule-benedict.html",
      "src/content/topics/weather-climate.json"
    ]
  },
  "handoff": {
    "nextStep": "Coordinator may preserve this response body verbatim as the current atomic partial author packet; six remaining exact7 cards are still pending author review.",
    "stop": true
  }
}
```

Канделу снял с рассмотрения по критерию Easy: корректность определения СИ не делает сам термин широко известным. Незакоммиченные изменения не трогал; кандидат выше в рабочий файл не записывал. Сессия ещё не закрыта: координатору нужно сохранить этот partial packet и продолжить с оставшимися шестью карточками.