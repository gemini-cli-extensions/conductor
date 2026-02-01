# Context Bundle Rules and Thresholds

## Canonical Context Bundle (Default Include)
- `conductor/product.md`
- `conductor/product-guidelines.md` (if present)
- `conductor/tech-stack.md`
- `conductor/workflow.md`
- `conductor/tracks.md`
- `conductor/code_styleguides/*` (only the language(s) in active use)
- Current track files:
  - `conductor/tracks/<track_id>/spec.md`
  - `conductor/tracks/<track_id>/plan.md`
  - `conductor/tracks/<track_id>/metadata.json`

## Explicit Exclusions (Default)
- `conductor/tracks/archive/**`
- `.git/**`, `.hg/**`, `.svn/**`
- `.agent/**` (workflows/skills are generated artifacts)
- `node_modules/**`, `dist/**`, `build/**`, `.venv/**`, `.tox/**`, `.mypy_cache/**`
- `**/*.lock` and package caches when not needed for the current change

## Size Thresholds (Guidance)
- **Warn** when a single file exceeds **250 KB**.
- **Block** when a single file exceeds **1 MB** unless explicitly needed.
- **Warn** when the total context bundle exceeds **2 MB**.
- **Block** when the total context bundle exceeds **5 MB** unless the user opts in.

## Notes
- The current track’s spec/plan always take priority for inclusion.
- When a file is excluded but still required (e.g., vendor docs), explicitly list the exception in the task or plan.
