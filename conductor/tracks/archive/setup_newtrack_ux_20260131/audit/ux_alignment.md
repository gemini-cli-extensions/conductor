# Adapter Alignment Check

## Summary

- Ran `python scripts/validate_platforms.py --sync` to ensure adapter prompts match core templates.
- No file diffs were produced; adapters appear in sync with canonical setup/newTrack guidance.

## Notes
- Adapter prompts are sourced from core templates and regenerated via sync tooling.
- Future UX changes should update templates first, then re-run sync to propagate.
