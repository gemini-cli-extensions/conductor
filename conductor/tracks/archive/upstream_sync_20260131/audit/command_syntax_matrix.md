# Conductor Command Syntax Matrix

This document maps the Conductor protocol commands to their native syntax across supported platforms.

| Command (Logical) | Gemini CLI / Qwen | VS Code / Antigravity | Claude CLI / OpenCode | Codex / Agent Skills |
| :--- | :--- | :--- | :--- | :--- |
| **Trigger** | `/conductor:...` | `@conductor /...` | "I want to use conductor" | "I want to use conductor" |
| **Setup** | `/conductor:setup` | `@conductor /setup` | "Set up conductor" | "Initialize conductor" |
| **New Track** | `/conductor:newTrack` | `@conductor /newTrack` | "Create new track" | "New feature track" |
| **Implement** | `/conductor:implement` | `@conductor /implement` | "Implement next task" | "Start implementation" |
| **Status** | `/conductor:status` | `@conductor /status` | "Show track status" | "Project status" |
| **Revert** | `/conductor:revert` | `@conductor /revert` | "Revert changes" | "Rollback work" |

## Notes on Platform-Specific Behavior

### Gemini CLI / Qwen
- Uses standard slash-command syntax.
- Commands are explicitly mapped in `gemini-extension.json` or `qwen-extension.json`.

### VS Code / Antigravity
- Integrated as a Chat Participant.
- Uses the `@conductor` handle followed by a slash command.
- Can leverage active editor context and selections.

### Claude CLI / OpenCode
- Relies on natural language triggers defined in `SKILL.md`.
- No fixed slash commands; uses intent detection.

### Codex / Agent Skills
- Similar to Claude CLI; intent-based activation.
- Uses `SKILL.md` for discovery and protocol definition.
