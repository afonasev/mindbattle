## Atomic author packet: `history-japan-easy-01a-05`

I kept the card’s primary fact and prompt. The earlier anniversary rewrite would have disclosed the answer and mixed units among the choices; this candidate restores four comparable train systems and gives each option a useful, source-backed note.

### Candidate card

```json
{
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
      "note": "TGV вышел на линию 27 сентября 1981 года, после четырёх лет работ."
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
}
```

### Six authored-field reasons and two metadata reasons

1. **Prompt:** kept verbatim. It asks for the Japanese system; it does not name the answer.
2. **Answer 0:** kept “Синкансэн”; its note now adds the later top speed instead of repeating the prompt.
3. **Answer 1:** kept “TGV”; its note adds the service date, making it a credible rail-system alternative.
4. **Answer 2:** kept “ICE”; its note adds the German introduction date and ICE 1 speed.
5. **Answer 3:** kept “Acela”; its note adds the service date and corridor context.
6. **Explanation:** two sentences; gives the answer and route-opening year, then adds the speed milestone.
7. **Difficulty:** remains `easy`; the recognized system is distinguished from three well-known national high-speed services.
8. **Key and binding:** `correctIndex: 0`, ID, topic, and array position remain fixed. Canonical binding is `src/content/topics/history-japan.json` → `history-japan-easy-01a-05`.

### Source evidence and capture status

**Shinkansen:** full local primary capture is available at `coordinator-continuation-01a13294/capture-only/primary-04.body` with raw headers in `primary-04.headers`.

- Body: 137,885 bytes; SHA-256 `cd2913c6105527c0d721137ae0a4d6b8e0c3095c72874a56819f1c184a4a879c`.
- Headers: 583 bytes; SHA-256 `3f3ec0e4e493f4ea978dc8e108e0d7e6c770207c2da01dbe4237b7a9b7a12d5a`; HTTP 200, `text/html`.
- Main-fact paragraph: raw byte offset 101,884, length 422, SHA-256 `4c65c3fca18618e585a783bca7f6f836f42dfafec6603d6e0a01dc54e382907b`. It supports the route opening, 1964 date, anniversary, speed change, and ridership.
- Key-note paragraph: raw byte offset 102,356, length 996, SHA-256 `d89cfae2824095f47a5b90262a9d48b42422334c7609952f703769f84ffae757`; it supports the 50-year operating period and passenger-safety note if needed.
- Read recipe: strict UTF-8 decode; HTML character-reference decoding; collapse whitespace only in the readable text view. Hashes and offsets are over unchanged response bytes.

**TGV:** SNCF Archives’ official page records TGV entering service on 27 September 1981 after four years of work. The relevant page context is its “Notice / Description” section, lines 60–65 in the opened page. [SNCF Archives](https://www.archives.sncf.com/tgv-an-un/)

**ICE:** Deutsche Bahn says ICE was introduced on 2 June 1991 and gives ICE 1’s maximum speed as 280 km/h. The relevant context is the ICE 1 general description and comparison table, lines 20–28 and 33–43. [Deutsche Bahn](https://www.bahn.de/service/ueber-uns/zugtypen/ice-1)

**Acela:** Amtrak’s fact sheet says it entered service on 11 December 2000 and describes its corridor service. The relevant context is page 2, lines 55–58. [Amtrak fact sheet](https://media.amtrak.com/wp-content/uploads/2025/08/Amtrak-NextGen-Acela-Fleet-Fact-Sheet.pdf)

The three foreign-system pages were personally checked as official primary pages through their parsed page contents. Their raw response bodies and headers are **not** in the local capture folder; capture those exact URLs before treating this packet as byte-proven. Their retrieved source contexts support the proposed notes, but I cannot supply raw-byte offsets or header hashes for them yet.

### Current-to-candidate literals

- **Prompt:** unchanged: `Как называется японская система скоростных поездов, открывшая движение между Токио и Осакой в 1964 году?`
- **Answer texts:** unchanged and remain four same-category rail systems.
- **Key note:** replaces the prompt-repeating text with the 2014 speed milestone.
- **TGV note:** replaces the broad “commercial work began in 1981” statement with the dated service event.
- **ICE note:** adds the precise German introduction date and ICE 1 top speed.
- **Acela note:** replaces the unspecific corridor description with its exact service date plus corridor context.
- **Explanation:** rewritten to two concise sentences; key remains at slot 0.

### Catalog scan and full relevant neighbors

I scanned 110 topic files / 11,000 cards. Prompt searches for Shinkansen, its Russian spellings, Japanese high-speed rail, TGV, ICE, and Acela found no other prompt about these systems; the only exact card-level occurrence of the four system names is this target card. The nearest thematic neighbors are Japanese rail history and Tokyo 1964, but they ask different facts.

Canonical bindings and full neighbor cards read:

```json
[
  {
    "canonical": "src/content/topics/history-japan.json#history-japan-easy-03a-01",
    "id": "history-japan-easy-03a-01",
    "difficulty": "easy",
    "prompt": "Какой вид транспорта впервые связал Токио и Иокогаму в 1872 году?",
    "answers": [
      {
        "text": "Железная дорога",
        "note": "Первая японская железная дорога соединила станцию Симбаси в Токио с портовым городом Иокогама."
      },
      {
        "text": "Линия метрополитена",
        "note": "Первый участок токийского метро открылся в 1927 году между станциями Уэно и Асакуса."
      },
      {
        "text": "Автомобильное шоссе",
        "note": "Современная сеть скоростных автомобильных дорог Японии начала быстро развиваться во второй половине XX века."
      },
      {
        "text": "Регулярная авиалиния",
        "note": "Регулярная гражданская авиация появилась в Японии значительно позднее железных дорог, уже в XX веке."
      }
    ],
    "correctIndex": 0,
    "explanation": "Токио и Иокогаму связала железная дорога. Она открылась в 1872 году, имела длину около 29 километров и стала заметным символом модернизации страны.",
    "source": {
      "title": "The Origin of Japan’s Modernization / The Government of Japan - JapanGov -",
      "url": "https://www.japan.go.jp/tomodachi/2018/spring2018/the_origin_of_japans_modernization.html",
      "verifiedAt": "2026-09-02"
    }
  },
  {
    "canonical": "src/content/topics/history-japan.json#history-japan-easy-02a-04",
    "id": "history-japan-easy-02a-04",
    "difficulty": "easy",
    "prompt": "Какой японский город принимал летние Олимпийские игры 1964 года — первые Олимпийские игры в Азии?",
    "answers": [
      {
        "text": "Саппоро",
        "note": "Саппоро принял зимние Олимпийские игры 1972 года, первые зимние Игры в Азии."
      },
      {
        "text": "Токио",
        "note": "Токио провёл летние Олимпийские игры 1964 года, первые в истории Азиатского континента."
      },
      {
        "text": "Нагано",
        "note": "Нагано принимал зимние Олимпийские игры 1998 года."
      },
      {
        "text": "Осака",
        "note": "Осака стала местом проведения Всемирной выставки Экспо-70."
      }
    ],
    "correctIndex": 1,
    "explanation": "Первые Олимпийские игры в Азии прошли в Токио с 10 по 24 октября 1964 года. В соревнованиях участвовали более пяти тысяч спортсменов из 93 стран и регионов.",
    "source": {
      "title": "TOKYO 1964 Olympic Games | JOC - Japanese Olympic Committee",
      "url": "https://www.joc.or.jp/english/historyjapan/tokyo1964.html",
      "verifiedAt": "2026-09-02"
    }
  }
]
```

The railway neighbor asks which transport first connected Tokyo and Yokohama in 1872; the target asks which high-speed system opened Tokyo–Osaka in 1964. The Olympics neighbor asks which city hosted the Games; it is a nearby Tokyo/1964 fact, not a duplicate.

I did not change Tokyo or the other eight pending cards. I did not write, commit, or run tests. **Next step:** capture the three official TGV, ICE, and Acela source pages with raw headers and bodies, then preserve this one-card candidate packet before resuming any other card. The session is not ready to archive because this packet has not been saved outside the chat and the three raw captures remain pending.