## Shinkansen — завершённый авторский срез

Официальный SNCF Patrimoine capture получен целиком. Кандидат ниже сохраняет исходный вопрос и четыре сопоставимых варианта поездных систем; меняются пояснение и заметки.

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
}
```

### Шесть content-групп и отдельные class/meta причины

1. **Prompt:** оставлен без изменений; он не содержит ответа.
2. **Синкансэн:** key остаётся в слоте 0; новая заметка добавляет скоростную динамику, а не повторяет вопрос.
3. **TGV:** сопоставимая высокоскоростная система; заметка добавляет дату начала коммерческих рейсов и маршрут.
4. **ICE:** сопоставимая система; заметка даёт дату запуска в Германии и максимальную скорость ICE 1.
5. **Acela:** сопоставимый американский rail service; заметка даёт дату начала работы и контекст коридора.
6. **Explanation:** два предложения; отвечает на вопрос и добавляет скорость, подтверждённую JapanGov.

**Difficulty:** остаётся `easy`. **Metadata:** ID `history-japan-easy-01a-05`, `correctIndex: 0`, пятая позиция в topic-массиве — прежние. Canonical binding: `src/content/topics/history-japan.json#history-japan-easy-01a-05`.

### Raw source proofs

**JapanGov / Shinkansen.** Полный HTML-body: 137,885 bytes, SHA-256 `cd2913c6105527c0d721137ae0a4d6b8e0c3095c72874a56819f1c184a4a879c`; raw headers: 583 bytes, SHA-256 `3f3ec0e4e493f4ea978dc8e108e0d7e6c770207c2da01dbe4237b7a9b7a12d5a`, HTTP 200. Article paragraph at byte offset `101884`, length `422`, SHA-256 `4c65c3fca18618e585a783bca7f6f836f42dfafec6603d6e0a01dc54e382907b`: Tokyo–Osaka opened in 1964; the article marks the 50th anniversary in 2014, speed rising from 210 to 320 km/h, and daily ridership at one million. The next safety paragraph is at offset `102356`, length `996`, SHA-256 `d89cfae2824095f47a5b90262a9d48b42422334c7609952f703769f84ffae757`. [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/primary-04.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/primary-04.headers" purpose="source"}]

**SNCF Patrimoine / TGV.** Full HTTP 200 body: 46,674 bytes, SHA-256 `6b34d0ee4ed1118818d19cebf0d1422012a2a939c8a892c77bd79045b30957e4`; headers: 1,309 bytes, SHA-256 `abfddcc5a5544d5cf9fdc0dee21d9db6de1800c3e7a1c39a87403d8c374c9eba`. The TGV Paris-Sud-Est commercial-service paragraph is at raw offset `30301`, length `706`, SHA-256 `3bcbde069bb05d0c9b82562918eebfa7c68fc4083b62f973577dcb793c27f0a8`. It states that commercial service between Paris and Lyon began 27 September 1981. The full page is [SNCF Patrimoine](https://patrimoine.sncf.com/2024/10/31/le-premier-tgv-ne-date-pas-de-1981-mais-de-1971/). Read recipe: strict UTF-8; HTML character-reference decoding; preserve raw bytes for offsets and hashes. [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-tgv-sncf-patrimoine/tgv.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-tgv-sncf-patrimoine/tgv.headers" purpose="source"}]

**Deutsche Bahn / ICE.** Full HTTP 200 body: 40,341 bytes, SHA-256 `565f35e6274a9334821f5d50d645b6470de417a9e65ec04d824e5a5b0c67006b`; headers: 5,179 bytes, SHA-256 `269d14fa2cb84e6affa95e2423493bfe35739efec9e57b0f20a5418e63e0c570`. The 1991 introduction paragraph is at offset `16374`, length `661`, SHA-256 `089326bdb47863d18f4241c777748910b47113102a33fbdce77283dc549466ab`. The ICE 1 maximum-speed table row is at offset `20285`, length `185`, SHA-256 `9c719132bbae5259cd2925a5432fe6dd860349233b7287197eb2767ea9e5c63f`. Short excerpt: “Am 2. Juni 1991 begann … das Hochgeschwindigkeitszeitalter in Deutschland.” [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/ice.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/ice.headers" purpose="source"}]

**Amtrak / Acela.** Full PDF: 259,618 bytes, SHA-256 `e2fee2e1ce9afb474f7fb5ae1e6299a18dd6cbea28dd0cd3ff96b9bb019abd5f`; headers: 310 bytes, SHA-256 `29c4439bfa8456afd31692af36aabe49e180f61a92ca3f786d1bb2a144c00034`. I read page 2 with pypdf 6.19.0. Under “Acela: A Success Story,” the passage states the service date and corridor; extracted-text SHA-256 `24aa9f699963f6ed436df7e0f0766cd0f843a55d4dd84b6a61bccb6ca423975`. Short excerpt: “service on December 11, 2000.” [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/acela.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/acela.headers" purpose="source"}]

### Group receipts and binding

Canonicalization is UTF-8 JSON with sorted keys and compact separators, SHA-256, no trailing newline.

- Current whole-card SHA-256: `02df18114754a2781f9e3c4347f28b00015b51272b06f87826b8a33f2dc6dc41`
- Candidate whole-card SHA-256: `4c04fc15908358caacb5f5acfaed8c06b3bd34527faaa5f0b24043cef057b569`
- **Group 1** (prompt + four ordered answer texts + key): unchanged; current/candidate SHA-256 `efddd626a931e2f8caa816f53e8cf482cd509d93469c4be238d34ea449fa8b9f`.
- **Group 2** (explanation + four ordered notes): current SHA-256 `82772d3d9f274210e7ac8ddddd620d5b907b2d90bc2bce19716c0a05d02e5d86`; candidate SHA-256 `909527c75289bfd5eb68990ed014252247d0ba25a7ff3f202ac32eb806694e1c`.

Topic binding read-only baseline: `src/content/topics/history-japan.json`, 195,739 bytes, SHA-256 `9dc1e6c6b812995be2ec03d537553f551e353686f4f91dd3e4781d01576b4ef6`.

### Other nine-card source map

This batch map records the preserved source state; it does **not** claim those nine cards are authored or qualified.

| ID | Primary source state / remaining issue |
|---|---|
| `history-japan-easy-01a-01` | Met Shōguns and Art capture timed out; parsed page was read, but raw proof is unavailable. |
| `history-japan-easy-01a-02` | British Museum source returned 403; needs an admissible alternative capture and proof for class notes. |
| `history-japan-easy-01a-03` | Edo-Tokyo Museum full capture exists in `primary-02`; other city-note evidence needs review. |
| `history-japan-easy-01a-04` | Met Shinto capture timed out; parsed page was read, but raw proof is unavailable. |
| `history-japan-easy-01b-01` | NPS complete entity body is preserved as assembled full ranges; two matching passes, not one HTTP 200 capture. Similarity with the U.S. entry-to-war question needs resolution. |
| `history-japan-easy-01b-02` | Nagasaki city full capture exists in `primary-06`; direct Hiroshima/Nagasaki sequence pair needs a replacement fact. |
| `history-japan-easy-01b-03` | Imperial Household Agency full capture exists in `primary-07`; each emperor distractor note still needs source mapping. |
| `history-japan-easy-01b-04` | National Diet Library full capture exists in `primary-08`; prompt and notes need the previously identified editorial revision. |
| `history-japan-easy-01b-05` | JACAR full capture exists in `primary-09`; distinct from the Port Arthur/Portsmouth neighbors, but distractor-note proof remains. |

**Current slice status:** the Shinkansen candidate now has complete raw proof for all four system notes. No repository files were written or committed; no tests, builds, or deployment were run. The other nine cards remain pending. **Next step:** author and source-review those nine within the same locked ten-card scope. The session is not ready to archive because that work remains unfinished and this packet is only in chat.