# Workflow Packaging Inventory

This inventory captures current artifact outputs, locations, and command syntax for each supported tool.

## Artifact Outputs

| Tool | Artifact Type | Location | Notes |
| --- | --- | --- | --- |
| Gemini CLI | Extension commands | `commands/conductor/*.toml` | Extension metadata in `gemini-extension.json` |
| Qwen CLI | Extension commands | `commands/conductor/*.toml` | Extension metadata in `qwen-extension.json` |
| Claude Code | Commands + plugin | `.claude/commands/*.md`, `.claude-plugin/*` | Slash-dash syntax |
| OpenCode (Agent Skills) | Skills | `~/.opencode/skill/<skill>/SKILL.md` | Agent Skills format |
| Codex CLI | Skills | `~/.codex/skills/<skill>/SKILL.md` | Uses `$conductor-<cmd>` |
| Antigravity | Workflows (workspace + global) | `.agent/workflows/<skill>.md` and `~/.gemini/antigravity/global_workflows/<skill>.md` | Global workflows default for Antigravity; workspace overrides supported |
| Antigravity (legacy) | Skills | `.antigravity/skills/<skill>/SKILL.md` | Legacy path; keep compatible until skills.md adoption decision |
| VS Code Extension | Packaged skills | `conductor-vscode/skills/<skill>/SKILL.md` and `conductor.vsix` | @conductor /<cmd> syntax |
| GitHub Copilot Chat | Rules file | `~/.config/github-copilot/conductor.md` | Slash-dash syntax |

## Command Syntax Matrix

| Tool | Command Style | Example |
| --- | --- | --- |
| Gemini CLI | slash-colon | `/conductor:setup` |
| Qwen CLI | slash-colon | `/conductor:setup` |
| Claude Code | slash-dash | `/conductor-setup` |
| OpenCode (Agent Skills) | slash-dash | `/conductor-setup` |
| Codex CLI | dollar-dash | `$conductor-setup` |
| Antigravity | at-mention + slash | `@conductor /setup` |
| VS Code Extension | at-mention + slash | `@conductor /setup` |
| GitHub Copilot Chat | slash-dash | `/conductor-setup` |

## Source of Truth

- Primary: `skills/manifest.json`
- Reference docs: `docs/skill-command-syntax.md`
