# Gaps and Improvement Opportunities (Phase 1)

## Duplication and Drift Risks
- Multiple prompt sources for commands:
  - `conductor-core` templates (`*.j2`)
  - Gemini CLI TOML prompts (`commands/conductor/*.toml`)
  - Markdown command prompts (`commands/conductor-*.md` and `.claude/commands/conductor-*.md`)
- Separate skill packages:
  - Single-skill package (`skill/SKILL.md` + `skill/scripts/install.sh`)
  - Per-command skills (`skills/<conductor-*>/SKILL.md`)
- CLI extension entrypoints (`gemini-extension.json`, `qwen-extension.json`) are not generated from the same source as `scripts/sync_skills.py`.

## Manual Steps to Reduce
- `skill/scripts/install.sh` is fully interactive and copies a single SKILL.md; lacks a non-interactive path and does not cover per-command skills.
- `scripts/sync_skills.py` writes to user home directories directly, which is hard to validate in CI and easy to forget to run.
- No documented command-syntax matrix for tool-specific invocation styles.

## Missing Validations / CI Checks
- No manifest/schema validation for skill metadata or tool mapping.
- No automated check that generated artifacts match templates (risk of silent drift).
- No sync check to ensure local `skills/` and `conductor-vscode/skills/` are up to date.

## Tool-Specific Gaps
- Codex / OpenCode command styles are not documented in-repo; current assumptions need confirmation.
- Antigravity/VS Code command syntax is referenced in `product.md` but not reflected in any tool-specific docs.
