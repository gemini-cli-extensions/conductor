# Command Syntax by Tool

This document summarizes the command invocation style and artifact type used by each tool.
The canonical schema is `skills/manifest.schema.json`, and the data source is `skills/manifest.json`.

## Tool Matrix (Generated)

<!-- BEGIN: TOOL-MATRIX -->
| Tool | Artifact Type / Location | Command Style | Example |
| --- | --- | --- | --- |
| gemini | `commands/conductor/*.toml` | `slash-colon` | `/conductor:setup` |
| qwen | `commands/conductor/*.toml` | `slash-colon` | `/conductor:setup` |
| claude | `.claude/commands/*.md and .claude-plugin/*` | `slash-dash` | `/conductor-setup` |
| codex | `~/.codex/skills/<skill>/SKILL.md` | `dollar-dash` | `$conductor-setup` |
| opencode | `~/.opencode/skill/<skill>/SKILL.md` | `slash-dash` | `/conductor-setup` |
| antigravity | `.agent/workflows/<skill>.md and ~/.gemini/antigravity/global_workflows/<skill>.md` | `at-mention + slash` | `@conductor /setup` |
| vscode | `conductor-vscode/skills/<skill>/SKILL.md` | `at-mention + slash` | `@conductor /setup` |
| copilot | `~/.config/github-copilot/conductor.md` | `slash-dash` | `/conductor-setup` |
| aix | `~/.config/aix/conductor.md` | `slash-dash` | `/conductor-setup` |
| skillshare | `~/.config/skillshare/skills/<skill>/SKILL.md` | `slash-dash` | `/conductor-setup` |
<!-- END: TOOL-MATRIX -->
| Tool | Artifact Type / Location | Example Command |
| --- | --- | --- |
| Gemini CLI | `commands/conductor/*.toml` (extension) | `/conductor:setup` |
| Qwen CLI | `commands/conductor/*.toml` (extension) | `/conductor:setup` |
| Claude Code | `.claude/commands/*.md` and `.claude-plugin/*` | `/conductor-setup` |
| OpenCode (Agent Skills) | `~/.opencode/skill/<skill>/SKILL.md` | `/conductor-setup` |
| Claude CLI (Agent Skills) | `~/.claude/skills/<skill>/SKILL.md` | `/conductor-setup` |
| Codex CLI (Agent Skills) | `~/.codex/skills/<skill>/SKILL.md` | `$conductor-setup` |
| Antigravity | `.agent/workflows/<skill>.md` (workspace) and `~/.gemini/antigravity/global_workflows/<skill>.md` (global) | `/conductor-setup` |
| VS Code Extension | `conductor-vscode/skills/<skill>/SKILL.md` (packaged) | `@conductor /setup` |
| GitHub Copilot Chat | `~/.config/github-copilot/conductor.md` | `/conductor-setup` |

## Notes
- The single source of truth for command syntax is `skills/manifest.json`.
- If a tool behaves differently in your environment, update the manifest and regenerate outputs.
- The tool matrix above is generated via `scripts/render_command_matrix.py`.
- Antigravity workflows are the default output; optional skills output can be emitted to `.agent/skills/<skill>/SKILL.md` and `~/.gemini/antigravity/skills/<skill>/SKILL.md` via `--emit-skills`.
- VS Code Copilot integration remains separate from the VS Code extension packaging.
