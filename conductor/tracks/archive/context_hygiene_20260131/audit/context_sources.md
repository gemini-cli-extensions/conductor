# Context Sources Inventory

This inventory lists the primary context inputs Conductor uses or generates, grouped by scope.

## Core Project Context (conductor/)
- `conductor/product.md`: product vision and goals.
- `conductor/product-guidelines.md`: optional brand/style guidance.
- `conductor/tech-stack.md`: technology choices and constraints.
- `conductor/workflow.md`: development workflow and verification protocol.
- `conductor/tracks.md`: track registry and status.
- `conductor/code_styleguides/*`: language-specific style guides.
- `conductor/setup_state.json`: setup progress state.

## Track Context (per track)
- `conductor/tracks/<track_id>/spec.md`: requirements and acceptance criteria.
- `conductor/tracks/<track_id>/plan.md`: phased tasks and checkpoints.
- `conductor/tracks/<track_id>/metadata.json`: track metadata (including optional VCS info).
- `conductor/tracks/<track_id>/index.md`: optional track index (when generated).
- `conductor/tracks/archive/<track_id>/`: archived track history.

## Tool Artifacts (adapter-generated)
- Gemini/Qwen: `commands/conductor/*.toml` (prompt templates packaged for CLI).
- Claude Code: `.claude/commands/*.md` and `.claude/skills/*`.
- Agent Skills (Codex/OpenCode/Claude CLI): `~/.<tool>/skills/<skill>/SKILL.md`.
- Antigravity: `.agent/workflows/*.md` (workspace), `~/.gemini/antigravity/global_workflows/*.md` (global).
- VS Code: `conductor-vscode/skills/*` (embedded prompts).
- Copilot: `~/.config/github-copilot/conductor.md`.

## Discovery and Filtering Patterns
- `.geminiignore` and `.gitignore` are used to limit context scanning (setup workflow).
- `git ls-files --exclude-standard -co` is preferred for listing relevant files when Git is present.
- Non-Git fallback relies on manual pruning rules from `setup` instructions.
