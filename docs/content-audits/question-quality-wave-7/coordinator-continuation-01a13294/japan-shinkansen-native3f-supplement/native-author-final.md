## Shinkansen — revised one-card candidate

I chose a different official SNCF primary page for the TGV note: [SNCF Patrimoine’s TGV history](https://patrimoine.sncf.com/2024/10/31/le-premier-tgv-ne-date-pas-de-1981-mais-de-1971/). It identifies the commercial TGV Paris–Lyon service and gives its 27 September 1981 start date. The relevant context is the article’s TGV Paris-Sud-Est paragraph. Short excerpt: “mises en service commercial entre Paris et Lyon dès le 27 septembre 1981” [SNCF Patrimoine](https://patrimoine.sncf.com/2024/10/31/le-premier-tgv-ne-date-pas-de-1981-mais-de-1971/).

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

### Six content reasons and separate class/metadata reasons

1. **Prompt:** retained verbatim; it asks for the Japanese system and does not reveal its name.
2. **Синкансэн:** retained as key at slot 0; its note adds the later speed increase.
3. **TGV:** remains a credible French high-speed rail alternative; its note adds a specific Paris–Lyon commercial-service date.
4. **ICE:** remains a credible German alternative; its note adds the 1991 introduction date and ICE 1’s top speed.
5. **Acela:** remains a credible U.S. alternative; its note adds its service date and corridor.
6. **Explanation:** two sentences, supported by the JapanGov source; adds the 2014 speed milestone.

**Difficulty** stays `easy`. **Metadata** stays bound to `src/content/topics/history-japan.json#history-japan-easy-01a-05`, with `correctIndex: 0` and the existing fifth-item position.

### Source and capture evidence

- **Shinkansen:** the full JapanGov capture supports the prompt, key, note, and explanation. The main paragraph is raw byte offset `101884`, length `422`, SHA-256 `4c65c3fca18618e585a783bca7f6f836f42dfafec6603d6e0a01dc54e382907b`. Body SHA-256 `cd2913c6105527c0d721137ae0a4d6b8e0c3095c72874a56819f1c184a4a879c`; headers SHA-256 `3f3ec0e4e493f4ea978dc8e108e0d7e6c770207c2da01dbe4237b7a9b7a12d5a`, HTTP 200. [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/primary-04.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/primary-04.headers" purpose="source"}]
- **ICE:** full HTTP 200 body SHA-256 `565f35e6274a9334821f5d50d645b6470de417a9e65ec04d824e5a5b0c67006b`; headers SHA-256 `269d14fa2cb84e6affa95e2423493bfe35739efec9e57b0f20a5418e63e0c570`. The launch paragraph is at byte offset `16374`, length `661`, SHA-256 `089326bdb47863d18f4241c777748910b47113102a33fbdce77283dc549466ab`; its table row for 280 km/h is at offset `20285`, length `185`, SHA-256 `9c719132bbae5259cd2925a5432fe6dd860349233b7287197eb2767ea9e5c63f`. [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/ice.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/ice.headers" purpose="source"}]
- **Acela:** full PDF body SHA-256 `e2fee2e1ce9afb474f7fb5ae1e6299a18dd6cbea28dd0cd3ff96b9bb019abd5f`; headers SHA-256 `29c4439bfa8456afd31692af36aabe49e180f61a92ca3f786d1bb2a144c00034`. On page 2, under “Acela: A Success Story,” the service-date passage was read with pypdf 6.19.0; extracted text SHA-256 `24aa9ff699963f6ed436df7e0f0766cd0f843a55d4dd84b6a61bccb6ca423975`. [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/acela.body" purpose="source"}] [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/acela.headers" purpose="source"}]
- **TGV:** SNCF Patrimoine is the new exact URL selected for raw capture. It has not yet been captured locally, so the TGV note still needs a complete body and headers before byte-level qualification. The earlier `archives.sncf.com` route timed out and its alternate host failed DNS; those failures are recorded in [:codex-file-citation{path="/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/japan-rail-primary/tgv-retry-manifest.json" purpose="source"}].

### Current/candidate group hashes

Canonicalization: sorted-key compact JSON, UTF-8, SHA-256, no trailing newline.

- Current whole-card hash: `02df18114754a2781f9e3c4347f28b00015b51272b06f87826b8a33f2dc6dc41`
- Candidate whole-card hash: `4c04fc15908358caacb5f5acfaed8c06b3bd34527faaa5f0b24043cef057b569`
- Group 1 (prompt + four ordered answer texts + key index): unchanged; current and candidate hash `efddd626a931e2f8caa816f53e8cf482cd509d93469c4be238d34ea449fa8b9f`.
- Group 2 (explanation + four ordered notes): current hash `82772d3d9f274210e7ac8ddddd620d5b907b2d90bc2bce19716c0a05d02e5d86`; revised candidate hash `909527c75289bfd5eb68990ed014252247d0ba25a7ff3f202ac32eb806694e1c`.

**Status:** the TGV source choice is now concrete and its official context supports the note, but this candidate remains unqualified until that exact URL has a successful raw capture. No files were written, no commit or tests were run. The other nine cards remain pending. **Next step:** capture the selected SNCF Patrimoine URL with complete response headers and body, then verify its exact context and hashes.