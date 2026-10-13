## Current atomic slice: two candidate cards

Only `history-japan-easy-01a-03` and `history-japan-easy-01a-05` are covered here. The other eight cards remain pending and frozen. These are proposed card literals for review; I did not write them to the repository.

### `history-japan-easy-01a-03` — Tokyo

```json
{
  "id": "history-japan-easy-01a-03",
  "difficulty": "easy",
  "prompt": "В каком году императорский эдикт переименовал Эдо в Токио?",
  "answers": [
    {
      "text": "1884 год",
      "note": "В 1884 году предложение губернатора Токийской префектуры Ёсикавы Масатадэ запустило проект городского переустройства."
    },
    {
      "text": "1923 год",
      "note": "Великое землетрясение Канто 1923 года разрушило и сожгло значительную часть Токио; затем начался план восстановления имперской столицы."
    },
    {
      "text": "1868 год",
      "note": "Эдикт от 17 июля 1868 года переименовал Эдо в Токио; тогда же была учреждена Токийская префектура."
    },
    {
      "text": "1964 год",
      "note": "В 1964 году открылось движение Синкансэн между Токио и Осакой."
    }
  ],
  "correctIndex": 2,
  "explanation": "Эдикт от 17 июля 1868 года переименовал Эдо в Токио и сопровождался учреждением Токийской префектуры. Позднее город пережил крупные проекты переустройства, Великое землетрясение Канто и восстановление.",
  "source": {
    "title": "Tokyo 150 Years — EDO-TOKYO MUSEUM",
    "url": "https://www.edo-tokyo-museum.or.jp/en/s-exhibition/tokyo150/",
    "verifiedAt": "2026-10-13"
  }
}
```

**Why each authored component is shaped this way**

1. **Prompt:** replaces the answer-revealing “what name did Edo receive?” with a direct date question about the same primary fact.
2. **Option 1884:** a competing date tied to the source’s city-planning chronology; its note identifies the proposal that initiated the project.
3. **Option 1923:** another date from Tokyo’s chronology; its note adds the earthquake and reconstruction context.
4. **Option 1868:** keeps the correct answer in slot 2; the note adds the edict date and prefecture founding.
5. **Option 1964:** a plausible Tokyo-related date; the note is supported by the captured JapanGov Shinkansen page.
6. **Explanation:** two sentences; distinguishes the correct date and adds sourced city-history context.

**Fixed metadata:** difficulty remains `easy`; `correctIndex` remains `2`; card ID and position remain unchanged. The date alternatives are all sourced milestones rather than unrelated city names. The existing prompt’s answer was directly exposed by its wording; the rewrite removes that cue.

### `history-japan-easy-01a-05` — Shinkansen

```json
{
  "id": "history-japan-easy-01a-05",
  "difficulty": "easy",
  "prompt": "Какую годовщину отмечал Синкансэн в 2014 году, спустя 50 лет после открытия движения между Токио и Осакой?",
  "answers": [
    {
      "text": "50 лет",
      "note": "В 2014 году Синкансэн отметил 50-летие; к тому времени поезда работали более 18 000 дней без гибели пассажиров."
    },
    {
      "text": "210 км/ч",
      "note": "210 км/ч — прежняя максимальная скорость; позднее максимальная скорость Синкансэна выросла до 320 км/ч."
    },
    {
      "text": "320 км/ч",
      "note": "320 км/ч — указанная в статье максимальная скорость после роста с первоначальных 210 км/ч."
    },
    {
      "text": "1 миллион пассажиров в день",
      "note": "Около миллиона пассажиров в день пользовались Синкансэном согласно статье 2014 года."
    }
  ],
  "correctIndex": 0,
  "explanation": "Движение Синкансэн между Токио и Осакой открылось в 1964 году, поэтому в 2014-м система отмечала 50-летие. Та же публикация сообщает о росте максимальной скорости до 320 км/ч и ежедневном пассажиропотоке около миллиона человек.",
  "source": {
    "title": "The Shinkansen, Japan’s High-Speed Rail, Is Full of Miracles — The Government of Japan",
    "url": "https://www.japan.go.jp/tomodachi/2014/autumn2014/the_shinkansen_japans_high-speed_rail.html",
    "verifiedAt": "2026-10-13"
  }
}
```

**Why each authored component is shaped this way**

1. **Prompt:** replaces “what is the system called?” with a distinct question about the source’s anniversary fact.
2. **Option 50 years:** preserves correct slot 0; its note adds the source’s safety record.
3. **Option 210 km/h:** uses the article’s earlier speed as a sourced distractor.
4. **Option 320 km/h:** uses the article’s later top speed as a sourced distractor.
5. **Option one million/day:** uses the article’s ridership figure as a sourced distractor.
6. **Explanation:** connects opening year to anniversary year and summarizes two additional figures from the same passage.

**Fixed metadata:** difficulty remains `easy`; `correctIndex` remains `0`; card ID and position remain unchanged. The numeric distractors are all real figures in the source. They are from different units, so this version is somewhat easier to eliminate by unit than four same-unit alternatives; the available captured source did not establish four distinct speed values.

## Source proof and locators

The captures are in the read-only worktree at:

`/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/`

Raw bodies and headers were preserved unchanged. Read recipe for both pages: strict UTF-8 decode; HTML parsing with character-reference decoding; collapse whitespace only for the human-readable text view. Offsets and hashes below refer to raw captured bytes, not normalized text.

| Card fact or note | Capture and raw locator |
|---|---|
| Edo renamed Tokyo by edict on 17 July 1868; Tokyo Prefecture established with it | `primary-02.body`, 30,187 bytes, SHA-256 `8b92f848dbcc94ff30dad812e79bd3c5eef77d7844a2f66851a758a0044e983d`; `<p>` at byte offset 10,950, length 1,170, SHA-256 `a6696969ca0f8d6798ba881661cc488caffc29948dc68e182a1cd9051fe7990b`. Short source excerpt: “an imperial edict was issued declaring that the city of Edo was being renamed Tokyo.” |
| 1884 Tokyo urban-planning distractor note | Same body; Japanese `<p>` at offset 13,674, length 582, SHA-256 `1383c4e267a43b0a9ca3b61c68050a923ed6a83d0296f65c7e6cc8c51f15fa22`. |
| 1923 earthquake and reconstruction distractor note | Same body; Japanese `<p>` at offset 15,784, length 510, SHA-256 `af319c6ec56a017d6e5491af3fefb6877223f1496852f5ebe7a9ac746aaa5358`. |
| 1964 Tokyo–Osaka service note; anniversary, speeds, ridership | `primary-04.body`, 137,885 bytes, SHA-256 `cd2913c6105527c0d721137ae0a4d6b8e0c3095c72874a56819f1c184a4a879c`; `<p class=" c-body">` at offset 101,884, length 422, SHA-256 `4c65c3fca18618e585a783bca7f6f836f42dfafec6603d6e0a01dc54e382907b`. Short source excerpt: “celebrates its 50th anniversary in 2014, having opened for service between Tokyo and Osaka in 1964.” |
| 50-year safety detail for the Shinkansen key note | Same body; following `<p class=" c-body">` at offset 102,356, length 996, SHA-256 `d89cfae2824095f47a5b90262a9d48b42422334c7609952f703769f84ffae757`. |

Raw-header evidence:

- `primary-02.headers`: 107 bytes, SHA-256 `471f99cd0962735ff798bc9951aabf5bc1c059dafba422ca26c62083c80c62fd`; HTTP 200, `text/html; charset=UTF-8`.
- `primary-04.headers`: 583 bytes, SHA-256 `3f3ec0e4e493f4ea978dc8e108e0d7e6c770207c2da01dbe4237b7a9b7a12d5a`; HTTP 200, `text/html`, with ETag and Last-Modified recorded in the raw header file. The body decoded strictly as UTF-8.

The Tokyo card’s primary prompt, key, and explanation are supported by the Edo-Tokyo Museum page. Its 1964 distractor note is separately supported by JapanGov. The Shinkansen prompt, all four metrics, notes, and explanation map to the JapanGov paragraphs listed above.

## Current-literal changes

| ID | Current prompt | Candidate change |
|---|---|---|
| `history-japan-easy-01a-03` | `Какое название получил город Эдо в 1868 году?` | Ask the year of the renaming edict; replace city-name options with four sourced Tokyo-history dates, retaining the key at index 2. |
| `history-japan-easy-01a-05` | `Как называется японская система скоростных поездов, открывшая движение между Токио и Осакой в 1964 году?` | Ask the anniversary recognized in 2014; replace the system-name options with the anniversary and three sourced metrics, retaining the key at index 0. |

All six content components—prompt, four answer-with-note entries, and explanation—have a specific rationale above. The difficulty, correct index, ID, order, and source-page body integrity are also accounted for.

## Catalog and neighbor review

I scanned **110 topic files / 11,000 cards** with targeted prompt families for Edo/Tokyo/1868/renaming and Shinkansen/high-speed-rail terms. Broad Tokyo/Edo prompt matching returned 27 results; the direct renaming question is the current target. The rail family returned only the current Shinkansen card. No inverse question asking for Edo as the former name of Tokyo appeared in the matching prompts.

Manually read full nearby cards include `history-japan-easy-02a-04` (Tokyo Olympics 1964), `history-japan-easy-04a-01` (imperial court in Kyoto until transfer to Tokyo), `history-japan-easy-03a-01` (Tokyo–Yokohama railway in 1872), `history-japan-medium-01a-04` (1923 Great Kantō earthquake), `history-japan-medium-01a-01` (Edo and sankin-kōtai), and `history-japan-medium-02a-05` (Boshin War, 1868–69). They concern related dates, cities, or rail history, but ask distinct primary facts. The Tokyo Olympics card is the closest 1964 neighbor; the proposed Tokyo question asks for the renaming year, while the Shinkansen question asks for the anniversary.

No repository files were written, no tests or builds were run, and no commit was made. **The remaining eight cards are still pending; this packet does not complete the original ten-card assignment.** The next step is for the coordinator or human to save this two-card payload, then resume the other eight within the same locked scope. The session cannot be archived yet because this candidate packet has not been preserved outside the chat.