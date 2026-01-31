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

### VS Code

Download the `conductor.vsix` from the [Releases](https://github.com/gemini-cli-extensions/conductor/releases) page and install it in VS Code.

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

## Commands Reference

| Gemini CLI | Claude Code | Description |
| :--- | :--- | :--- |
| `/conductor:setup` | `/conductor-setup` | Initialize project context |
| `/conductor:newTrack` | `/conductor-newtrack` | Create new feature/bug track |
| `/conductor:implement` | `/conductor-implement` | Execute tasks from the current track's plan |
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

### Running Tests
```bash
# Core tests
cd conductor-core && PYTHONPATH=src pytest

# Gemini adapter tests
cd conductor-gemini && PYTHONPATH=src:../conductor-core/src pytest
```

### Skill Sync Checks

Verify generated skill artifacts match the manifest and templates:

```bash
python3 scripts/check_skills_sync.py
```

## License
- License: [Apache License 2.0](LICENSE)
