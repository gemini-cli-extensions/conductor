# Command Syntax by Tool

This document summarizes the command invocation style and artifact type used by each tool.

| Tool | Artifact Type | Example Command |
| --- | --- | --- |
| Gemini CLI | `commands/conductor/*.toml` (extension) | `/conductor:setup` |
| Qwen CLI | `commands/conductor/*.toml` (extension) | `/conductor:setup` |
| Claude Code | `.claude/commands/*.md` (plugin) | `/conductor-setup` |
| Agent Skills (Claude/OpenCode) | `~/.claude/skills/<skill>/SKILL.md` / `~/.opencode/skill/<skill>/SKILL.md` | `/conductor-setup` |
| Codex CLI (Agent Skills) | `~/.codex/skills/<skill>/SKILL.md` | `$conductor-setup` |
| Antigravity / VS Code chat | `.antigravity/skills/<skill>/SKILL.md` / `conductor-vscode/skills/<skill>/SKILL.md` | `@conductor /setup` |
| GitHub Copilot Chat | `~/.config/github-copilot/conductor.md` | `/conductor-setup` |

## Notes
- The single source of truth for command syntax is `skills/manifest.json`.
- If a tool behaves differently in your environment, update the manifest and regenerate outputs.
