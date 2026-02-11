# Conductor

**Measure twice, code once.**

Conductor enables **Context-Driven Development** for AI coding assistants. It turns your AI assistant into a proactive project manager that follows a protocol to specify, plan, and implement software features and bug fixes.

**Works with:** [Gemini CLI](#gemini-cli) | [Claude Code](#claude-code) | [Agent Skills compatible CLIs](#agent-skills) | [VS Code](#vs-code)

## Architecture

Conductor is organized as a modular monorepo:

-   **`conductor-core`**: The platform-agnostic core library (Python). Contains the protocol logic, Pydantic models, and prompt templates.
-   **`conductor-gemini`**: The Gemini CLI adapter.
-   **`conductor-vscode`**: The VS Code extension (TypeScript).
-   **`conductor-claude`**: (Integration) Portable skills for Claude Code.

## Multi-Platform Support

Conductor is designed to provide a consistent experience across different tools:

-   **Gemini CLI**: Fully supported.
-   **Qwen Code**: Fully supported via `qwen-extension.json`.
-   **VS Code / Antigravity**: Supported via VSIX (supports Remote Development).
-   **Claude Code**: Supported via portable skills.

## Command Syntax by Tool

See `docs/skill-command-syntax.md` for tool-native command syntax and the artifacts each tool consumes.

Quick reference (paths are defaults):
- Gemini CLI: `commands/conductor/*.toml` → `/conductor:setup`
- Qwen CLI: `commands/conductor/*.toml` → `/conductor:setup`
- Claude Code: `.claude/commands/*.md` / `.claude-plugin/*` → `/conductor-setup`
- Claude CLI (Agent Skills): `~/.claude/skills/<skill>/SKILL.md` → `/conductor-setup`
- OpenCode (Agent Skills): `~/.opencode/skill/<skill>/SKILL.md` → `/conductor-setup`
- Codex (Agent Skills): `~/.codex/skills/<skill>/SKILL.md` → `$conductor-setup`
- Antigravity: `.agent/workflows/<skill>.md` (workspace) and `~/.gemini/antigravity/global_workflows/<skill>.md` (global) → `/conductor-setup`
- VS Code Extension: `conductor-vscode/skills/<skill>/SKILL.md` → `@conductor /setup`
- GitHub Copilot Chat: `~/.config/github-copilot/conductor.md` → `/conductor-setup`

## Features

-   **Platform Source of Truth**: All protocol prompts are centralized in the core library and synchronized to adapters.
-   **Plan before you build**: Create specs and plans that guide the agent.
-   **Smart revert**: Git-aware revert command that understands logical units of work.
-   **High Quality Bar**: 95% test coverage requirement enforced for core modules.

## Installation

### Gemini CLI / Qwen Code

```bash
gemini extensions install https://github.com/gemini-cli-extensions/conductor --auto-update
```

### Claude Code

**From marketplace (recommended):**
```bash
# Add the marketplace
/plugin marketplace add gemini-cli-extensions/conductor

# Install the plugin
/plugin install conductor
```

**Manual installation:**
```bash
# Clone and copy commands/skills to your global config
git clone https://github.com/gemini-cli-extensions/conductor.git
cp -r conductor/.claude/commands/* ~/.claude/commands/
cp -r conductor/.claude/skills/* ~/.claude/skills/
```

### VS Code

Download the `conductor.vsix` from the [Releases](https://github.com/gemini-cli-extensions/conductor/releases) page and install it in VS Code.

### Google Antigravity (Global Workflows)

For local development, the recommended path is to sync Antigravity **global workflows** and install the VSIX in one step:

```bash
python scripts/install_local.py
```

This script writes per-command workflows to `~/.gemini/antigravity/global_workflows/` and installs the VSIX into both VS Code and Antigravity.

Conductor also syncs **workspace workflows** to `.agent/workflows/` inside this repo, so `/conductor-setup` etc. work even when global workflows are disabled.

Optional skills output (experimental):
- Use `python scripts/install_local.py --sync-workflows --sync-skills --emit-skills` or set `CONDUCTOR_ANTIGRAVITY_SKILLS=1` and run `scripts/sync_skills.py`.
- Outputs to `.agent/skills/<skill>/SKILL.md` (workspace) and `~/.gemini/antigravity/skills/<skill>/SKILL.md` (global).
- Workflows remain the default until Antigravity skills.md support is fully validated.

Windows users can run the PowerShell wrapper:

```powershell
.\scripts\install_local.ps1
```

Common flags:
- `--verify` (run validations only)
- `--dry-run` (print planned actions)
- `--print-locations` (show resolved artifact paths)

### Agent Skills (Claude CLI / OpenCode / Codex)

For CLIs supporting the [Agent Skills specification](https://agentskills.io), you can install Conductor as a portable skill.

**Option 1: Point to local folder**
Point your CLI to the `skills/conductor/` directory in this repository.

**Option 2: Use install script**
```bash
# Clone the repository
git clone https://github.com/gemini-cli-extensions/conductor.git
cd conductor

# Run the install script
./skill/scripts/install.sh
```
The installer will ask where to install (OpenCode, Claude CLI, Codex, or all). You can also use flags:
```bash
./skill/scripts/install.sh --target codex
./skill/scripts/install.sh --list
```
The skill is installed with symlinks to this repository, so running `git pull` will automatically update the skill.

## Usage

Conductor is designed to manage the entire lifecycle of your development tasks.

**Note on Token Consumption:** Conductor's context-driven approach involves reading and analyzing your project's context, specifications, and plans. This can lead to increased token consumption.

### 1. Set Up the Project (Run Once)

When you run `/conductor:setup`, Conductor helps you define the core components of your project context.

**Generated Artifacts:**
- `conductor/product.md`, `tech-stack.md`, `workflow.md`, `tracks.md`

```bash
/conductor:setup
```

See `docs/setup-newtrack.md` for a cross-adapter setup/newTrack UX guide.

### 2. Start a New Track (Feature or Bug)

Run `/conductor:newTrack` to initialize a **track** — a high-level unit of work.

```bash
/conductor:newTrack "Add a dark mode toggle"
```

### 3. Implement the Track

Run `/conductor:implement`. Your coding agent then works through the `plan.md` file.

```bash
/conductor:implement
```

Conductor will:
1.  Select the next pending task.
2.  Follow the defined workflow (e.g., TDD: Write Test -> Fail -> Implement -> Pass).
3.  Update the status in the plan as it progresses.
4.  **Verify Progress**: Guide you through a manual verification step at the end of each phase to ensure everything works as expected.

### Optional Git Workflows (Adapter-Enabled)

Conductor works **with or without Git**. Adapters can opt-in to Git-native workflows by enabling VCS capability.

**Non-Git example (default):**
- No Git repository required.
- No branch/worktree creation.
- Track metadata stays free of VCS fields.

**Git-enabled example (adapter opt-in):**
- Branch-per-track: create `conductor/<track_id>` from the current base branch.
- Worktree-per-track: create `.conductor/worktrees/<track_id>` for isolated work.
- Record VCS metadata in `conductor/tracks/<track_id>/metadata.json` under a `vcs` key.

#### Ralph Mode (Autonomous Loop)
Ralph Mode is a functionality based on the Geoffrey Huntley's Ralph loop technique for the Gemini CLI that enables continuous autonomous development cycles. It allows the agent to iteratively improve your project until completion, following an automated Red-Green-Refactor loop with built-in safeguards to prevent infinite loops.

```bash
/conductor:implement --ralph
```
* `--max-iterations=N`: Change the retry limit (default: 10).
* `--completion-word=WORD`: Change the work completion magic word (default: TRACK_COMPLETE).

> [!NOTE]
> For a seamless autonomous experience, you may enable `accepts-edits` or YOLO mode in your configuration.

> [!WARNING]
> Using Gemini CLI in YOLO mode allows the agent to modify files and use tools without explicit confirmation and authorization from the user.


During implementation, you can also:

- **Check status**: Get a high-level overview of your project's progress.
  ```bash
  /conductor:status
  ```
- **Revert work**: Undo a feature or a specific task if needed.
  ```bash
  /conductor:revert
  ```
- **Review work**: Review completed work against guidelines and the plan.
  ```bash
  /conductor:review
  ```

## Context Hygiene

See `docs/context-hygiene.md` for the canonical context bundle and safety guidance. To report context size:

```bash
python scripts/context_report.py
```

## Commands Reference

| Gemini CLI | Claude Code | Description |
| :--- | :--- | :--- |
| `/conductor:setup` | `/conductor-setup` | Initialize project context |
| `/conductor:newTrack` | `/conductor-newtrack` | Create new feature/bug track |
| `/conductor:implement` | `/conductor-implement` | Execute tasks from the current track's plan. Use `--ralph` for autonomous loop. |
| `/conductor:status` | `/conductor-status` | Display progress overview |
| `/conductor:revert` | `/conductor-revert` | Git-aware revert of tracks, phases, or tasks |
| `/conductor:review` | `/conductor-review` | Review completed work against guidelines |

## Development

### Prerequisites
-   Python 3.9+
-   Node.js 16+ (for VS Code extension)

### Building Artifacts
```bash
# Build conductor-core
./scripts/build_core.sh

# Build VS Code extension
./scripts/build_vsix.sh
```

For release packaging and GitHub Releases flow, see `docs/release.md`.

### Running Tests
```bash
# Core tests
cd conductor-core && PYTHONPATH=src pytest

# Gemini adapter tests
cd conductor-gemini && PYTHONPATH=src:../conductor-core/src pytest
```

### Synchronization and Validation

To synchronize all platform artifacts (Gemini TOMLs, Claude MDs, global Agent Skills, etc.) from the core templates, run the unified sync script:

```bash
python scripts/sync_all.py
```

This script replaces the need to run `sync_skills.py` and `validate_platforms.py --sync` separately.

Verify generated skill artifacts match the manifest and templates:

```bash
python3 scripts/check_skills_sync.py
```

Validate all platform artifacts (including VSIX when built):

```bash
python3 scripts/validate_artifacts.py --require-vsix
```

If validation fails:
- Regenerate artifacts with `python3 scripts/sync_skills.py`.
- Resync platform files with `python3 scripts/validate_platforms.py --sync`.
- Rebuild the VSIX (`./scripts/build_vsix.sh`) before re-running validation.
See `docs/validation.md` for a deeper troubleshooting checklist.

The skills manifest schema lives at `skills/manifest.schema.json`. To regenerate the tool matrix in
`docs/skill-command-syntax.md`, run:

```bash
python3 scripts/render_command_matrix.py
```

## License
- License: [Apache License 2.0](LICENSE)
