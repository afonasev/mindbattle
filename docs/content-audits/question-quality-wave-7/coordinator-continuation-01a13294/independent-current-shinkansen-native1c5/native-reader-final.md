**Содержание текущей карточки проходит проверку:** все 6 групп, easy, метаданные и проверка дублей — PASS. Отдельно требуется исправить привязку хеша извлечённого фрагмента Acela: авторское значение содержит 63 hex-символа и не совпадает с вычисленным. Зачёт **+0**.

Текущие байты темы побайтово подтверждены в snapshot `e78ce7e`. Actual compactions **1**.

Следующий шаг: координатор сохраняет JSON и отдельное дополнение с фактическим хешем Acela, затем выполняет ручную оценку. Файлы и TMP не создавались.

```json
{
  "schema": "mindbattle.shinkansen.native-independent-current.v1",
  "nativeReaderId": "01a131c5-edfb-7b82-8ddf-bd88a8b95597",
  "sourceAuthorLabel": "Japan3f",
  "opaqueEditorLabel": "sourceeditor627",
  "identityQualification": "Reader actual full native ID verified. Author/editor labels are those supplied by coordinator; full native IDs are not fabricated.",
  "coordinatorId": "01a13294-7d84-7583-930d-02eb1c80eb45",
  "actualCompactions": 1,
  "scope": ["history-japan-easy-01a-05"],
  "workdir": "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle",
  "currentWholeCard": {
    "id": "history-japan-easy-01a-05",
    "difficulty": "easy",
    "prompt": "Как называется японская система скоростных поездов, открывшая движение между Токио и Осакой в 1964 году?",
    "answers": [
      {
        "text": "Синкансэн",
        "note": "К 2014 году максимальная скорость Синкансэна выросла с 210 до 320 км/ч."
      },
      {
        "text": "TGV",
        "note": "Коммерческие рейсы TGV Paris-Sud-Est между Парижем и Лионом начались 27 сентября 1981 года."
      },
      {
        "text": "ICE",
        "note": "2 июня 1991 года ICE начал эпоху высокоскоростных поездов в Германии; максимальная скорость ICE 1 — 280 км/ч."
      },
      {
        "text": "Acela",
        "note": "Acela начал работу 11 декабря 2000 года и обслуживает один из самых загруженных железнодорожных коридоров США."
      }
    ],
    "correctIndex": 0,
    "explanation": "Японская система скоростных поездов называется Синкансэн. Движение между Токио и Осакой открылось в 1964 году; к 2014 году максимальная скорость поездов выросла до 320 км/ч.",
    "source": {
      "title": "The Shinkansen, Japan’s High-Speed Rail, Is Full of Miracles",
      "url": "https://www.japan.go.jp/tomodachi/2014/autumn2014/the_shinkansen_japans_high-speed_rail.html",
      "verifiedAt": "2026-10-13"
    }
  },
  "wholeCanonicalSHA256": "4c04fc15908358caacb5f5acfaed8c06b3bd34527faaa5f0b24043cef057b569",
  "currentTopicRawSHA256": "d9210f084d0c55f3eaf6be67d61723f8ccb5929e2a41fb3d81c9e4214d5ea70f",
  "hashRecipes": {
    "wholeCompositeMetadata": "SHA256 UTF8 json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')); no trailing newline.",
    "scalarGroups": "SHA256 exact scalarUTF8 without JSON quotes or newline."
  },
  "sixGroups": [
    {
      "group": "prompt-all4-ordered-texts-index-explicitKey",
      "currentLiteral": {
        "prompt": "Как называется японская система скоростных поездов, открывшая движение между Токио и Осакой в 1964 году?",
        "orderedAnswerTextStrings": ["Синкансэн", "TGV", "ICE", "Acela"],
        "correctIndex": 0,
        "keyText": "Синкансэн"
      },
      "sha256": "e1f8be5014f4629a1971f328ec50b0fe3b93ea281bbcab7c8b022da21a10c1d1",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "JapanGov's full History of the Shinkansen paragraph explicitly names Japan's high-speed rail and states Tokyo–Osaka service opened in1964. All four choices name comparable high-speed rail systems/services; TGV, ICE and Acela are not the Japanese system. Key0 is unique and absent from the stem.",
      "proofRefs": ["Japan-opening-speed"]
    },
    {
      "group": "explanation",
      "currentLiteral": "Японская система скоростных поездов называется Синкансэн. Движение между Токио и Осакой открылось в 1964 году; к 2014 году максимальная скорость поездов выросла до 320 км/ч.",
      "sha256": "1bbd2427616882a71d5dd7dd80aee00252bc4729c43d1d9d17606aa7638097cc",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The two-sentence explanation answers with Shinkansen, restates the historically specified opening and adds the source-supported320km/h maximum by2014. The2014 limit prevents presenting an old snapshot as today's speed.",
      "proofRefs": ["Japan-opening-speed"]
    },
    {
      "group": "note0",
      "currentLiteral": "К 2014 году максимальная скорость Синкансэна выросла с 210 до 320 км/ч.",
      "sha256": "24b8f442521cccd81193a356a88b7dc7f4fd807a4cab4d539349858694cb5826",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The correct note adds a quantified historical speed change210→320km/h by2014, absent from the prompt/key. The original2014 article says top speed has risen from210 to320; it does not conflate a prototype speed record with this opening fact.",
      "proofRefs": ["Japan-opening-speed"],
      "variant": "Синкансэн",
      "index": 0,
      "isKey": true
    },
    {
      "group": "note1",
      "currentLiteral": "Коммерческие рейсы TGV Paris-Sud-Est между Парижем и Лионом начались 27 сентября 1981 года.",
      "sha256": "9d6205d1a86046d39ad39784173751bbbf68749bc196cb2fe43c85df4e2e9697",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The full SNCF paragraph states TGV Paris-Sud-Est commercial service Paris–Lyon began27September1981. Surrounding prototype/trials text distinguishes earlier1970s experiments from commercial service, so the note is precise and gives this option its own route/date fact.",
      "proofRefs": ["TGV-commercial-start", "TGV-adjacent-prototype"],
      "variant": "TGV",
      "index": 1,
      "isKey": false
    },
    {
      "group": "note2",
      "currentLiteral": "2 июня 1991 года ICE начал эпоху высокоскоростных поездов в Германии; максимальная скорость ICE 1 — 280 км/ч.",
      "sha256": "887d47e4c053eed20b50ded7de212b095fe63b0c8267be85b3a7a0bcd10eba50",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The full DB paragraph gives2June1991 introduction and the ICE1 comparison table labels Höchstgeschwindigkeit280km/h. The note specifies ICE1 rather than assigning one speed to all ICE generations. Its high-speed-era wording follows the cited introduction account.",
      "proofRefs": ["ICE-introduction", "ICE-speed-table"],
      "variant": "ICE",
      "index": 2,
      "isKey": false
    },
    {
      "group": "note3",
      "currentLiteral": "Acela начал работу 11 декабря 2000 года и обслуживает один из самых загруженных железнодорожных коридоров США.",
      "sha256": "3b2fc954855af45015000d4d1b22264fef62d3937ae357191d645bc60e281daf",
      "sourceVerdict": "PASS",
      "editorialVerdict": "PASS",
      "independentReason": "The complete Amtrak PDFpage2 passage says Acela entered service11December2000 and serves the nation's busiest rail corridor. The Russian one of the busiest wording is a conservative paraphrase. These are Acela-specific positive facts, not a bare rejection. Own exact181-byte extraction is bound to original PDF; the author's malformed expected digest is separately reported.",
      "proofRefs": ["Acela-service"],
      "variant": "Acela",
      "index": 3,
      "isKey": false
    }
  ],
  "difficulty": {
    "currentLiteral": "easy",
    "scalarSHA256": "97c10efe01d5c9c88704a12d361d8429b3a6aa2412290a0773109d5d2d603d5e",
    "sourceVerdict": "PASS",
    "editorialVerdict": "PASS",
    "independentReason": "Recognition of Japan's well-known national high-speed system, familiar to a broad geography/travel/cultural audience. Japan, route and year give direct context; no engineering details or speed statistic are needed to answer. Four national systems remain plausible choices. Easy is freshly justified, not inherited or accepted merely because frozen; no survey acceptance claim."
  },
  "sourceMetadata": {
    "currentLiteral": {
      "title": "The Shinkansen, Japan’s High-Speed Rail, Is Full of Miracles",
      "url": "https://www.japan.go.jp/tomodachi/2014/autumn2014/the_shinkansen_japans_high-speed_rail.html",
      "verifiedAt": "2026-10-13"
    },
    "canonicalSHA256": "e9c96f77e552ba95cc75a74c40d7189ec24f9678d332a7f426a12f1be847060e",
    "sourceVerdict": "PASS",
    "editorialVerdict": "PASS",
    "independentReason": "Visible JapanGov article title, Autumn2014 issue and URL match the primary opening/speed fact. Main source correctly belongs to the Japanese question; SNCF, DB and Amtrak separately support the wrong-option notes. verifiedAt2026-10-13 is review/capture provenance, not the publication year or a claim that the speed snapshot is current."
  },
  "sources": [
    {
      "id": "JapanGov",
      "bodyPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/primary-04.body",
      "bodyBytes": 137885,
      "bodySHA256": "cd2913c6105527c0d721137ae0a4d6b8e0c3095c72874a56819f1c184a4a879c",
      "headersPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/primary-04.headers",
      "headersBytes": 583,
      "headersSHA256": "3f3ec0e4e493f4ea978dc8e108e0d7e6c770207c2da01dbe4237b7a9b7a12d5a",
      "diskHEADGitExact": true,
      "httpStatus": 200,
      "url": "https://www.japan.go.jp/tomodachi/2014/autumn2014/the_shinkansen_japans_high-speed_rail.html"
    },
    {
      "id": "SNCF",
      "bodyPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-tgv-sncf-patrimoine/tgv.body",
      "bodyBytes": 46674,
      "bodySHA256": "6b34d0ee4ed1118818d19cebf0d1422012a2a939c8a892c77bd79045b30957e4",
      "headersPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-tgv-sncf-patrimoine/tgv.headers",
      "headersBytes": 1309,
      "headersSHA256": "abfddcc5a5544d5cf9fdc0dee21d9db6de1800c3e7a1c39a87403d8c374c9eba",
      "diskHEADGitExact": true,
      "httpStatus": 200,
      "url": "https://patrimoine.sncf.com/2024/10/31/le-premier-tgv-ne-date-pas-de-1981-mais-de-1971/"
    },
    {
      "id": "DB",
      "bodyPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/ice.body",
      "bodyBytes": 40341,
      "bodySHA256": "565f35e6274a9334821f5d50d645b6470de417a9e65ec04d824e5a5b0c67006b",
      "headersPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/ice.headers",
      "headersBytes": 5179,
      "headersSHA256": "269d14fa2cb84e6affa95e2423493bfe35739efec9e57b0f20a5418e63e0c570",
      "diskHEADGitExact": true,
      "httpStatus": 200,
      "url": "https://www.bahn.de/service/ueber-uns/zugtypen/ice-1"
    },
    {
      "id": "Amtrak",
      "bodyPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/acela.body",
      "bodyBytes": 259618,
      "bodySHA256": "e2fee2e1ce9afb474f7fb5ae1e6299a18dd6cbea28dd0cd3ff96b9bb019abd5f",
      "headersPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/acela.headers",
      "headersBytes": 310,
      "headersSHA256": "29c4439bfa8456afd31692af36aabe49e180f61a92ca3f786d1bb2a144c00034",
      "diskHEADGitExact": true,
      "httpStatus": 200,
      "url": "https://media.amtrak.com/wp-content/uploads/2025/08/Amtrak-NextGen-Acela-Fleet-Fact-Sheet.pdf"
    }
  ],
  "contexts": [
    {
      "id": "Japan-opening-speed",
      "source": "JapanGov",
      "rawByteRange": [101884, 102306],
      "sliceSHA256": "4c65c3fca18618e585a783bca7f6f836f42dfafec6603d6e0a01dc54e382907b",
      "fullNormalizedContext": "Shinkansen (lit. new trunk line), Japan’s high-speed rail, celebrates its 50th anniversary in 2014, having opened for service between Tokyo and Osaka in 1964. Over the past half century, the made-in-Japan technology behind these sleek trains has continued to evolve. Top speed has risen from 210 km/h (130 mph) to 320 km/h (200 mph), and ridership is now 1 million passengers per day."
    },
    {
      "id": "Japan-adjacent-safety",
      "source": "JapanGov",
      "rawByteRange": [102356, 103352],
      "sliceSHA256": "d89cfae2824095f47a5b90262a9d48b42422334c7609952f703769f84ffae757",
      "fullNormalizedContext": "Above all else, the Shinkansen has a remarkable safety record. These Shinkansens have now operated for 50 years, over 18,000 days, without a single passenger casualty. This is a testament to uncompromising attention to quality in the development of the technology and strong efforts for safety in operation by all staff involved—from the train operators to the engineers who maintain the trains, tracks, and other equipment. The strong safety record attests to their focus on disaster prevention. The Shinkansen’s earthquake warning systems have always functioned well to stop the trains safely. The Japanese insistence on quality is well established. Particularly in matters of public safety, Japan is known for its uncompromising stance and its perennial drive to improve. Japan takes pride in the Shinkansen’s record of zero fatal passenger accidents. Everyone concerned will strive to maintain this unblemished record."
    },
    {
      "id": "TGV-commercial-start",
      "source": "SNCF",
      "rawByteRange": [30301, 31007],
      "sliceSHA256": "3bcbde069bb05d0c9b82562918eebfa7c68fc4083b62f973577dcb793c27f0a8",
      "fullNormalizedContext": "Ce prototype a ouvert la voie à la série des rames de TGV Paris-Sud-Est qui sont mises en service commercial entre Paris et Lyon dès le 27 septembre 1981, adoptant un orange plus “franc” et un nez plus fin. Il a aussi marqué l’imaginaire des Français, par sa forme et sa couleur notamment, dont le designer industriel Jacques Cooper, récemment disparu, est l’auteur. Afin, selon ses propres paroles, de concevoir un “train qui ne ressemble pas à un train” long de 92,9 mètres dans une logique d’aérodynamisme qui lui donne son nez étiré et son centre de gravité bas, il s’est appuyé sur les innovations automobiles de l’époque auxquelles il avait beaucoup contribué."
    },
    {
      "id": "TGV-adjacent-prototype",
      "source": "SNCF",
      "rawByteRange": [29943, 30300],
      "sliceSHA256": "9d5197cc617b2aa5d2bba047bd1c45d79515ca3c1d2070ede73e8bcb5c76330e",
      "fullNormalizedContext": "Ce prototype a continué de rouler pour promouvoir le TGV à venir une fois que la décision a été prise de revenir à la traction électrique en 1974 : ses essais ont marqué les esprits dans la plaine d’Alsace, sur la ligne droite des Landes… Il a été exposé en France et à l’étranger. Finalement, il a parcouru 456 690 kilomètres."
    },
    {
      "id": "ICE-introduction",
      "source": "DB",
      "rawByteRange": [16374, 17035],
      "sliceSHA256": "089326bdb47863d18f4241c777748910b47113102a33fbdce77283dc549466ab",
      "fullNormalizedContext": "Am 2. Juni 1991 begann mit der Einführung des Intercity-Express – ICE – das Hochgeschwindigkeitszeitalter in Deutschland. Der ICE wurde zum Inbegriff für hohe Geschwindigkeiten, kurze Reisezeiten, größtmöglichen Komfort und moderne Fahrzeugausstattung. In den folgenden Jahren entwickelte sich der ICE mit insgesamt fast 60 Zügen auf vielen Verbindungen zum bevorzugten Verkehrsmittel. Der Grund: erhebliche Reisezeitverkürzungen gegenüber Auto und Flugzeug. Das Hightech-Symbol überzeugt mit einer reichhaltigen Ausstattung an Komfortdetails wie z. B. Klimaanlage und Fußbodenheizung."
    },
    {
      "id": "ICE-speed-table",
      "source": "DB",
      "rawByteRange": [20285, 20470],
      "sliceSHA256": "9c719132bbae5259cd2925a5432fe6dd860349233b7287197eb2767ea9e5c63f",
      "fullNormalizedContext": "Höchstgeschwindigkeit 280 km/h 280 km/h"
    },
    {
      "id": "Acela-service",
      "source": "Amtrak",
      "pdfPage": 2,
      "pageIndex": 1,
      "parserVersion": "6.19.0",
      "extractedLiteral": "Over 69 million guests have traveled on Acela since it entered \nservice on December 11, 2000. Acela provides a premium rail travel \nexperience on the nation's busiest rail corridor.",
      "extractedBytes": 181,
      "actualSHA256": "24aa9ff699963f6ed436df7e0f0766cd0f843a55d4dd84b6a61bccb6ca423975",
      "authorExpectedSHA256": "24aa9f699963f6ed436df7e0f0766cd0f843a55d4dd84b6a61bccb6ca423975",
      "authorExpectedHexLength": 63,
      "authorExpectedHashCheckPassed": false,
      "originalExpectedPreserved": true
    }
  ],
  "parserRecipes": {
    "HTML": "Exact originalUTF8 body; complete p element or complete ICE table row; Python HTMLParser(convert_charrefs=True); join text nodes with spaces, collapse whitespace. Original slice SHA/ranges refer to bytes before decoding, zero-based/end exclusive. Entire relevant paragraphs and nearby prototype/safety/table context personally read.",
    "PDF": "pypdf6.19.0 PdfReader(original PDF); pages[1].extract_text(); exact substring from Over69million guests literal through final period after experience on the nation's busiest rail corridor.; strip outer whitespace; UTF8 without joining line breaks or Unicode normalization. Full physical page2 personally read.",
    "PDFWarning": "Initial extraction warned that fontTools was unavailable for CFF Type1 font parsing. The selected ASCII passage extracted coherently and repeatedly as181bytes; own actual SHA preserved. No fonts installed, no file writes."
  },
  "proofDiscrepancy": {
    "item": "Author Acela extracted-text digest",
    "authorExpected": "24aa9f699963f6ed436df7e0f0766cd0f843a55d4dd84b6a61bccb6ca423975",
    "authorExpectedHexLength": 63,
    "ownActual": "24aa9ff699963f6ed436df7e0f0766cd0f843a55d4dd84b6a61bccb6ca423975",
    "ownActualHexLength": 64,
    "expectedCheck": "FAILED; retained unchanged",
    "rawPDFAndHeaders": "PASS exact expected SHA/bytes/diskHEADGit",
    "contentSupport": "PASS based on personally read original and independently bound actual extraction, not inherited author hash.",
    "requiredAction": "Coordinator preserves an append-only corrected extraction binding; do not silently rewrite historical expected digest."
  },
  "runtimePreservation": {
    "initialObservation": "e78ce7e:src/content/topics/history-japan.json is prior source version, RAW9dc1e6c6b812995be2ec03d537553f551e353686f4f91dd3e4781d01576b4ef6; differs from current disk.",
    "clarification": "Current runtimeRAW bytes were preserved separately as an editor snapshot in e78ce7e.",
    "snapshotPath": "docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/opaque-japan-editor-native627/current-japan-source-bytes.json",
    "snapshotCommit": "e78ce7e",
    "snapshotBytes": 195868,
    "snapshotRawSHA256": "d9210f084d0c55f3eaf6be67d61723f8ccb5929e2a41fb3d81c9e4214d5ea70f",
    "gitSnapshotEqualsRuntimeBytesPersonallyVerified": true,
    "priorObservationPreserved": true,
    "runtimeCommitAndQualityCountSeparate": true,
    "other99ExactAndFullOrderAgainstApplyBaselinePersonallyVerified": true,
    "applyBaseline": "a38a305796740ea4b22a12aac6136bb8dfbd1ef5"
  },
  "catalog": {
    "count": 11000,
    "queries": {
      "direct": "[сш]инкан|shinkansen|\\btgv\\b|\\bacela\\b|\\bICE\\b",
      "inverse": "япон.{0,40}скоростн|скоростн.{0,40}япон|токио.{0,40}осак|осак.{0,40}токио|bullet train",
      "semantic": "скоростн.{0,35}поезд|высокоскоростн.{0,35}желез|1964|1872"
    },
    "results": {
      "direct": ["history-japan-easy-01a-05"],
      "inverse": ["history-japan-easy-01a-05"],
      "semantic": [
        "history-china-medium-03a-02",
        "history-japan-easy-01a-05",
        "history-japan-easy-02a-04",
        "history-japan-easy-03a-01",
        "history-united-states-civil-rights-law",
        "history-united-states-tonkin-authority",
        "olympic-games-first-asia-summer",
        "olympic-games-satellite-broadcast",
        "railways-high-speed-train",
        "russian-music-melodiya-founded",
        "soviet-russian-cinema-hamlet-kozintsev"
      ]
    },
    "all11000ManualClaim": false,
    "fullRelevantManualCount": 3,
    "neighbors": [
      {
        "id": "history-japan-easy-03a-01",
        "fullCurrentCard": {
          "id": "history-japan-easy-03a-01",
          "difficulty": "easy",
          "prompt": "Какой вид транспорта впервые связал Токио и Иокогаму в 1872 году?",
          "answers": [
            {"text": "Железная дорога", "note": "Первая японская железная дорога соединила станцию Симбаси в Токио с портовым городом Иокогама."},
            {"text": "Линия метрополитена", "note": "Первый участок токийского метро открылся в 1927 году между станциями Уэно и Асакуса."},
            {"text": "Автомобильное шоссе", "note": "Современная сеть скоростных автомобильных дорог Японии начала быстро развиваться во второй половине XX века."},
            {"text": "Регулярная авиалиния", "note": "Регулярная гражданская авиация появилась в Японии значительно позднее железных дорог, уже в XX веке."}
          ],
          "correctIndex": 0,
          "explanation": "Токио и Иокогаму связала железная дорога. Она открылась в 1872 году, имела длину около 29 километров и стала заметным символом модернизации страны.",
          "source": {
            "title": "The Origin of Japan’s Modernization / The Government of Japan - JapanGov -",
            "url": "https://www.japan.go.jp/tomodachi/2018/spring2018/the_origin_of_japans_modernization.html",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "f7c2528ac6deaa82590c9bdfbc047f4995df4d63633293875019f158f548fcc0",
        "fullLiteralPersonallyRead": true,
        "semanticRelation": "DISTINCT",
        "foreignCardQualityCertification": false,
        "independentReason": "1872 Tokyo–Yokohama first railway transport mode differs from1964 Tokyo–Osaka named high-speed system. Different route, era and primary predicate."
      },
      {
        "id": "history-japan-easy-02a-04",
        "fullCurrentCard": {
          "id": "history-japan-easy-02a-04",
          "difficulty": "easy",
          "prompt": "Какой японский город принимал летние Олимпийские игры 1964 года — первые Олимпийские игры в Азии?",
          "answers": [
            {"text": "Саппоро", "note": "Саппоро принял зимние Олимпийские игры 1972 года, первые зимние Игры в Азии."},
            {"text": "Токио", "note": "Токио провёл летние Олимпийские игры 1964 года, первые в истории Азиатского континента."},
            {"text": "Нагано", "note": "Нагано принимал зимние Олимпийские игры 1998 года."},
            {"text": "Осака", "note": "Осака стала местом проведения Всемирной выставки Экспо-70."}
          ],
          "correctIndex": 1,
          "explanation": "Первые Олимпийские игры в Азии прошли в Токио с 10 по 24 октября 1964 года. В соревнованиях участвовали более пяти тысяч спортсменов из 93 стран и регионов.",
          "source": {
            "title": "TOKYO 1964 Olympic Games | JOC - Japanese Olympic Committee",
            "url": "https://www.joc.or.jp/english/historyjapan/tokyo1964.html",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "7b37b99a0b3ef63e122a15fbba0b04e1246f45573b008468e8349e89119175c8",
        "fullLiteralPersonallyRead": true,
        "semanticRelation": "DISTINCT",
        "foreignCardQualityCertification": false,
        "independentReason": "1964 Tokyo Olympic host-city identification is a sports event predicate, not high-speed rail-system identity. Shared city/year is contextual overlap."
      },
      {
        "id": "railways-high-speed-train",
        "fullCurrentCard": {
          "id": "railways-high-speed-train",
          "difficulty": "easy",
          "prompt": "Как называется пассажирский поезд для движения по специализированным линиям со скоростью около 250 км/ч и выше?",
          "answers": [
            {"text": "Высокоскоростной поезд", "note": "Высокоскоростной поезд рассчитан на быстрое междугородное сообщение."},
            {"text": "Ночной поезд", "note": "Ночной поезд позволяет пассажирам спать во время длительной поездки."},
            {"text": "Пассажирский поезд", "note": "Пассажирский поезд перевозит людей в вагонах с местами и сервисными помещениями."},
            {"text": "Грузовой поезд", "note": "Грузовой поезд состоит из вагонов для контейнеров, сырья, автомобилей или других грузов."}
          ],
          "correctIndex": 0,
          "explanation": "Высокоскоростной поезд рассчитан на быстрое междугородное сообщение. Для него нужны соответствующие путь, сигнализация и подвижной состав.",
          "source": {
            "title": "britannica.com: Высокоскоростной поезд",
            "url": "https://www.britannica.com/technology/high-speed-rail",
            "verifiedAt": "2026-09-02"
          }
        },
        "canonicalSHA256": "4744b8bb70b032cc2d0e3838272e04990d29290863c5621e5c83b62d8d0a99c1",
        "fullLiteralPersonallyRead": true,
        "semanticRelation": "DISTINCT",
        "foreignCardQualityCertification": false,
        "independentReason": "Generic high-speed train category/specialized-line description differs from identifying Japan's named Shinkansen system. No direct/inverse equivalent primary predicate."
      }
    ],
    "dedupVerdict": "PASS among independently retrieved and fully reviewed relevant current neighbors; no claim of full manual catalog review."
  },
  "verdict": "PASS_CURRENT_CONTENT_WITH_AUTHOR_EXTRACTION_DIGEST_FIX_PENDING",
  "counts": {
    "groups": 6,
    "sourcePASS": 6,
    "editorialPASS": 6,
    "orderedNotes": 4,
    "difficultyPASS": 1,
    "metadataPASS": 1,
    "qualityIncrement": 0
  },
  "provenance": {
    "nativeSessionId": "01a131c5-edfb-7b82-8ddf-bd88a8b95597",
    "compactedEventsCheckedBeforeAndClosure": 1,
    "rollout": "/Users/eaafonasev/.codex/sessions/2026/10/13/rollout-2026-10-13T01-20-17-01a131c5-edfb-7b82-8ddf-bd88a8b95597.jsonl",
    "observedClosureHEAD": "30f11ac92d7137f7bc1ac86762e01a06023af2de",
    "authorGradesInherited": false,
    "executed": [
      "Readonly current runtime/card/topic hashes and all99/order comparison to apply baseline.",
      "Readonly original4body/header SHA/bytes and HEADGit equality; HTTP200 verified.",
      "Own primary HTML full paragraphs/table and surrounding-context reading.",
      "Own pypdf6.19 physicalpage2 extraction and exact181byte proof; author expected digest failed, reported unchanged.",
      "Independent direct/inverse/semantic regex discovery across11000 current prompts+keys; full3 relevant neighbors personally read and canonical-bound.",
      "Readonly native rollout compaction count, Git status, task-cleanup.md read.",
      "Readonly e78ce7e editor rawsnapshot byte equality verification after root clarification."
    ],
    "verificationFailuresPreserved": [
      "Author PDF-extract digest malformed63hex and unequal to actual.",
      "Initial comparison to e78ce7e runtime source path failed; separate correct rawsnapshot path verified, both facts retained."
    ],
    "filesWritten": [],
    "testsBuildsRecaptures": [],
    "ownedResources": "Only completed synchronous read commands; no own temp/background process created.",
    "audio": "No game/browser/Unity launch or audible output; system volume untouched.",
    "foreignStatus": " M docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-fresh-rework19/sources/newadvent-rule-benedict.html\n M src/content/topics/history-japan.json\n",
    "foreignWorkPreserved": true,
    "failedCapturesExcluded": "Earlier timed-out SNCF Archives attempts/null bodies are not factual proof; valid SNCF Patrimoine full HTTP200 capture is used."
  },
  "handoff": {
    "qualityCredit": 0,
    "nextStep": "Coordinator opaque-preserves full native JSON and append-only Acela actual extraction binding; manually adjudicates current card before credit/runtime integration.",
    "archiveNow": false,
    "reason": "New reader receipt and digest clarification still await durable coordinator preservation/manual gate.",
    "cleanupDebt": "No own TMP or other filesystem resource created."
  }
}
```