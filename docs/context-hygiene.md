# Context Hygiene & Memory Safety

This guide defines a minimal, repeatable context bundle for Conductor projects and safe practices to prevent context drift.

## Canonical Context Bundle

Include these files by default:
- `conductor/product.md`
- `conductor/product-guidelines.md` (if present)
- `conductor/tech-stack.md`
- `conductor/workflow.md`
- `conductor/tracks.md`
- `conductor/code_styleguides/*` (only active languages)
- Current track:
  - `conductor/tracks/<track_id>/spec.md`
  - `conductor/tracks/<track_id>/plan.md`
  - `conductor/tracks/<track_id>/metadata.json`

## Default Exclusions

Exclude these unless explicitly needed:
- `conductor/tracks/archive/**`
- `.git/**`, `.hg/**`, `.svn/**`
- `.agent/**` (generated workflows/skills)
- `node_modules/**`, `dist/**`, `build/**`, `.venv/**`, `.tox/**`, `.mypy_cache/**`
- Large lockfiles or dependency caches

## Size Thresholds (Guidance)

- **Warn:** file > 250 KB, total bundle > 2 MB
- **Block:** file > 1 MB, total bundle > 5 MB

## Safe Memory Practices

- Prefer linking to large files rather than inlining them in context.
- Keep the active track small; move completed work to `archive/`.
- Summarize long discussions into track notes or concise bullet lists.
- Avoid committing generated artifacts to the context bundle.

## Tooling

Run the context report to spot oversized files:

```bash
python scripts/context_report.py
```

You can override thresholds:

```bash
python scripts/context_report.py --warn-file-kb 200 --warn-total-kb 1500
```
