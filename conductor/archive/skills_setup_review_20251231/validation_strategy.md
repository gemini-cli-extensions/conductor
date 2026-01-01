# Validation and Sync Check Strategy

## Validation Scope
- Manifest validation against `skills/manifest.schema.json`.
- Template integrity checks:
  - Ensure `conductor-core/src/conductor_core/templates/*.j2` remain unchanged by generation.
- Generated artifact checks:
  - `skills/<skill>/SKILL.md`
  - `.antigravity/skills/<skill>/SKILL.md`
  - `conductor-vscode/skills/<skill>/SKILL.md`
  - `gemini-extension.json`, `qwen-extension.json`
  - `~/.config/github-copilot/conductor.md` (optional, local)

## Failure Messaging
- Fail with actionable guidance (e.g., "Run scripts/sync_skills.py" or "Regenerate with scripts/check_skills_sync.py --fix").
- Clearly identify missing or mismatched files and which tool they affect.

## Sync Check Integration
- Provide a local check command: `python3 scripts/check_skills_sync.py`.
- Optional CI hook: run the sync check and fail if generated outputs are stale.

## "No Protocol Changes" Guard
- Hash or diff template bodies (`*.j2`) vs generated protocol sections.
- If mismatch, fail with a message indicating which skill or template drifted.
