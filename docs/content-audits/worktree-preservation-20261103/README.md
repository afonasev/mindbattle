# Historical worktree preservation — 2026-11-03

This branch preserves the complete historical HEAD working tree, all unique tracked/untracked/ignored files and the exact original staged state. It is a preservation result, not approved production content and must not be merged wholesale into main.

`manifest.json` lists every changed working file with SHA-256. `original-index.bin` is the byte-exact index; its staged tree is also retained as a parent commit and on `codex/preserve-wave6-index-20261103`. The historical source branch remains intact.

Recover files using `git show <preservation-commit>:<path>` or `git archive <preservation-commit> <path>`. Materialize a temporary checkout only when needed. The original absolute worktree path was retired by explicit user authorization; planning records retain historical paths, so substitute this Git preservation reference when reading them.
