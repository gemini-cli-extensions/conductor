# Conductor Agents

This repository contains the core Conductor system that enables Context-Driven Development for AI coding assistants. The system is designed to work across multiple AI platforms and development environments.

## Core Architecture

- **`conductor-core`**: Platform-agnostic core library (Python). Contains the protocol logic, Pydantic models, and prompt templates.
- **`conductor-gemini`**: The Gemini CLI adapter.
- **`conductor-vscode`**: The VS Code extension (TypeScript).
- **`conductor-claude`**: Claude Code integration.

## Universal Installer

The system includes a universal installer that works across platforms:

### Quick Install

```bash
# Unix/macOS
curl -fsSL install.cat/edithatogo/conductor-next | sh

# Windows (PowerShell)
irm install.cat/edithatogo/conductor-next | iex
```

### Via mise

```bash
mise install edithatogo/conductor-next
```

## Supported Platforms

### Agent Skills Compatible CLIs

- Claude CLI
- OpenCode
- Codex
- Agent Skills specification compatible tools

### Direct Integrations

- Gemini CLI / Qwen Code
- Claude Code
- VS Code / Antigravity
- GitHub Copilot Chat

## Key Features

- **Platform Source of Truth**: All protocol prompts are centralized in the core library and synchronized to adapters.
- **Plan before you build**: Create specs and plans that guide the agent.
- **Smart revert**: Git-aware revert command that understands logical units of work.
- **High Quality Bar**: 95% test coverage requirement enforced for core modules.
- **Multi-VCS Support**: Git, Jujutsu, and other version control systems.
- **Cross-Platform**: Works consistently across different tools and operating systems.

## Usage

### 1. Set Up the Project

```bash
/conductor:setup
```

### 2. Start a New Track

```bash
/conductor:newTrack "Add a feature"
```

### 3. Implement the Track

```bash
/conductor:implement
```

## Installation Methods

Conductor supports multiple installation methods:

- **mise**: Cross-platform package manager
- **Smithery**: Modern package manager for CLI tools
- **PyPI**: Python package index
- **npm**: Node.js package manager
- **Homebrew**: macOS/Linux package manager
- **Chocolatey**: Windows package manager
- **Scoop**: Windows package manager

## Development

The system is built with:

- Python 3.9+ for core logic
- Node.js 16+ for VS Code extension
- TypeScript for VS Code extension
- Various CI/CD tools for automation

## License

Licensed under Apache License 2.0.

## Documentation

- [README.md](README.md): Main project documentation
- [INSTALL.md](INSTALL.md): Installation instructions
- [QUICKSTART.md](QUICKSTART.md): Quick start guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md): Troubleshooting guide
- [MARKETPLACE_INTEGRATION.md](MARKETPLACE_INTEGRATION.md): Marketplace integration details
