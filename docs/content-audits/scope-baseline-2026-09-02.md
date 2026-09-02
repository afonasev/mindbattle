# Scoped worktree baseline — 2026-09-02

## Source workspace preserved

- Branch/head: `feat/rebalance-difficulty-feedback` at `bfb9615`.
- Unrelated tracked changes present before apply: `docs/GAME_SPEC.md`, `src/domain/match.ts`, `src/domain/selectors.ts`, `src/ui/gameUi.tsx`, `tests/browser/game.spec.ts`, `tests/unit/domain-core.test.ts`.
- Unrelated untracked paths: `.codex/`, `openspec/changes/confirm-bonus-topic-before-question/`.
- User feedback data: `data/difficulty-feedback.ndjson`; excluded from Git and copied only to the non-committed snapshot `/private/tmp/mindbattle-feedback-snapshot-2026-09-02.ndjson`.

## Isolated implementation workspace

- Worktree: `/private/tmp/mindbattle-expand-catalog`.
- Branch: `feat/expand-recalibrate-catalog` from `main` at `3d4a2f4`.
- The active OpenSpec change was copied into this clean worktree before implementation and passed strict validation.
- Staging MUST use explicit paths from this change; raw feedback, `.codex`, the source workspace changes and `confirm-bonus-topic-before-question` MUST remain excluded.
