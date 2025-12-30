# Conductor

**Measure twice, code once.**

Conductor enables **Context-Driven Development** for AI coding assistants. It turns your AI assistant into a proactive project manager that follows a strict protocol to specify, plan, and implement software features and bug fixes.

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

## License

- License: [Apache License 2.0](LICENSE)