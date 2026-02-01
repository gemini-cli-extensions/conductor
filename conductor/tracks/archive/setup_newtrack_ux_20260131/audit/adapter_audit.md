# Setup/NewTrack Adapter Audit

This audit summarizes where each adapter sources setup/newTrack prompts and the expected outputs.

## Shared Core Behavior
- **Source of truth:** `conductor-core/src/conductor_core/templates/setup.j2` and `new_track.j2`.
- **Artifacts created:** `conductor/product.md`, `product-guidelines.md`, `tech-stack.md`, `workflow.md`, `tracks.md`,
  `conductor/tracks/<track_id>/{spec.md,plan.md,metadata.json,index.md}`, and `conductor/setup_state.json`.

## Adapter Inventory

### Gemini CLI / Qwen
- **Command files:** `commands/conductor/setup.toml`, `commands/conductor/newTrack.toml`.
- **Commands:** `/conductor:setup`, `/conductor:newTrack`.
- **Notes:** Prompts are synced from core templates via validation scripts; TOML wraps the prompt payload.

### Claude Code
- **Command files:** `.claude/commands/conductor-setup.md`, `.claude/commands/conductor-newtrack.md`.
- **Commands:** `/conductor-setup`, `/conductor-newtrack`.
- **Notes:** Markdown prompts mirror core templates.

### VS Code Extension
- **Skills:** `conductor-vscode/skills/*` (synced from templates).
- **Commands:** `@conductor /setup`, `@conductor /newtrack` (via VS Code chat).
- **Notes:** Uses the packaged extension; skills are embedded in the VSIX.

### Antigravity
- **Workflows:** `.agent/workflows/*.md` (workspace) and `~/.gemini/antigravity/global_workflows/*.md` (global).
- **Commands:** `/conductor-setup`, `/conductor-newtrack`.
- **Notes:** Workflows are rendered from the same templates; global install preferred for UX.

### Agent Skills (Codex/OpenCode/Claude CLI)
- **Skill files:** `skills/conductor/SKILL.md` (synced into tool-specific directories).
- **Commands:** `$conductor-setup`, `/conductor-setup`, or tool-specific variants.
- **Notes:** Skill metadata defines per-tool command syntax; content is template-derived.

### GitHub Copilot Chat
- **Rules file:** `~/.config/github-copilot/conductor.md`.
- **Commands:** `/conductor-setup`, `/conductor-newtrack`.
- **Notes:** Single rules file combines all commands for the assistant.
