# Audit: Skill Abstraction and Tool Setup (Baseline)

## Source Templates (Authoritative Protocol Content)
- `conductor-core/src/conductor_core/templates/*.j2` (setup/new_track/implement/status/revert)
  - These appear to be the canonical protocol bodies used to generate SKILL.md artifacts.

## Generated Outputs (Automation)
- `scripts/sync_skills.py` generates command-specific skill artifacts from `*.j2`:
  - Local Agent Skills: `skills/<conductor-*>/SKILL.md`
  - Local Antigravity: `.antigravity/skills/<conductor-*>/SKILL.md`
  - Local VS Code extension package: `conductor-vscode/skills/<conductor-*>/SKILL.md`
  - Global targets (home directory, generated when run locally):
    - `~/.gemini/antigravity/global_workflows/<conductor-*>.md` (flat)
    - `~/.codex/skills/<conductor-*>/SKILL.md`
    - `~/.claude/skills/<conductor-*>/SKILL.md`
    - `~/.opencode/skill/<conductor-*>/SKILL.md`
    - `~/.config/github-copilot/conductor.md` (consolidated)

## Manually Maintained Artifacts (Non-Generated)
- Agent Skill (auto-activation):
  - `skills/conductor/SKILL.md` + `skills/conductor/references/workflows.md`
- Legacy single-skill package:
  - `skill/SKILL.md` (installed via `skill/scripts/install.sh`)
- Claude plugin packaging:
  - `.claude-plugin/plugin.json`
  - `.claude-plugin/marketplace.json`
- Gemini/Qwen extension entrypoints:
  - `gemini-extension.json`, `qwen-extension.json` (both reference `GEMINI.md`)
- CLI prompt files:
  - Gemini CLI TOML prompts: `commands/conductor/*.toml`
  - Markdown command prompts: `commands/conductor-*.md`
  - Claude local install prompts: `.claude/commands/conductor-*.md`

## Observed Drift/Overlap Risks
- Multiple Markdown command prompt locations exist (`commands/` vs `.claude/commands/`).
- `skill/SKILL.md` is a separate, single-skill package path, while `skills/` holds per-command skills.
- `gemini-extension.json` and `qwen-extension.json` do not appear to be generated from the same source as `scripts/sync_skills.py`.
- `scripts/sync_skills.py` writes to user home directories, which complicates repo-checked validation and CI checks.
