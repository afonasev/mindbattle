# Author review — current three-card freeze

Actual author identity: `01a12fe9-74d9-7272-a1d2-f26317e06001`. Coordinator identity `01a12fcd-2bbd-72a3-b127-23455e847ca7` is recorded separately.

Scope is exactly `middle-ages-indulgence`, `middle-ages-reconquista`, `middle-ages-jihad`; baseline freeze `523588fcbed61c4d6aa705230ac9c2ac0918a928`. The three native records are frozen with full SHA256 and individually reviewed source/editorial bindings in `author-sourcebound-freeze-01a12fe9.json`.

- **Indulgence** — Easy / key index 2 retained. The prompt now asks for the Catechism’s essential definition of an indulgence, independently of the duplicate reverse Luther association in `history-germany-easy-02a-01`. The Vatican §1471 source directly defines the term and its partial/plenary distinction. This remains Easy because it tests the core meaning of the concept, not a date, quotation, or specialist detail.
- **Reconquista** — Medium / key index 1 retained. Only note 3’s source genre is corrected: Fordham labels the item journal extracts, and Columbus’s entry records the Granada/Alhambra observation. The reported historical fact is preserved.
- **Jihad** — Medium / key index 1 retained. The conditional legal duty remains the tested fact. Alternatives are parallel Islamic military/legal terms (`qitāl`, `ghazw`, `siyar`) rather than Christian events or pilgrimage. Syed’s complete chapter supports the key rule; Bonner’s captured chapter supplies the neighboring-term distinctions. `Ribāṭ` was excluded because Bonner describes it as a defensive counterpart to jihad, risking overlap.

The 97 protected full-card SHA256 values in the frozen scope were recomputed with the scope’s sorted-key canonical recipe: all 97 match. No test, counter, full-QA, build, deploy, or acceptance gate was run. This is author freeze only; independent reader review remains required.
