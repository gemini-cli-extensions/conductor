# Generation Targets and Outputs

## Planned Targets (Manifest-Driven)

### Agent Skills (Directory + SKILL.md)
- `skills/<skill>/SKILL.md` (repo-local, per-command skills)
- `.antigravity/skills/<skill>/SKILL.md` (repo-local integration)
- `conductor-vscode/skills/<skill>/SKILL.md` (VS Code extension package)
- User-global paths (generated locally, not committed):
  - `~/.codex/skills/<skill>/SKILL.md`
  - `~/.claude/skills/<skill>/SKILL.md`
  - `~/.opencode/skill/<skill>/SKILL.md`

### Agent Skills (Flat / Workflow)
- `~/.gemini/antigravity/global_workflows/<skill>.md` (flat files for global workflows)

### Extension Manifests
- `gemini-extension.json` (points to `GEMINI.md` context)
- `qwen-extension.json` (points to `GEMINI.md` context)

### Claude Plugin Packaging
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

### Copilot Rules
- `~/.config/github-copilot/conductor.md` (consolidated commands)

## Output Notes
- Repository-committed outputs should remain deterministic and generated from templates + manifest.
- User-home outputs should be generated locally and validated via a sync check, but not committed.
