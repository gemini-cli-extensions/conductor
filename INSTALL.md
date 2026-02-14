# Installation Guide

This guide covers installing conductor-next on your system.

## Quick Install (Recommended)

### macOS / Linux

```bash
curl -fsSL install.cat/edithatogo/conductor-next | sh
```

### Windows

```powershell
irm install.cat/edithatogo/conductor-next | iex
```

## Manual Installation

### Prerequisites

- **Git**: Required for cloning the repository
- **Python 3.9+**: For running Python components
- **Node.js 18+**: For VS Code extension (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/edithatogo/conductor-next.git
cd conductor-next
```

### Step 2: Install Mise

Conductor uses [mise](https://mise.jdx.dev/) for tool management.

**macOS/Linux:**
```bash
curl https://mise.run | sh
```

**Windows:**
```powershell
# Via winget
winget install jdx.mise

# Or via scoop
scoop install mise
```

### Step 3: Install Components

Using the installer script:
```bash
python scripts/conductor_install.py --all
```

Or using mise tasks:
```bash
mise install
mise run install-all
```

### Step 4: Verify Installation

```bash
mise run verify
```

## Component-Specific Installation

### Install Individual Components

```bash
# Install only core
python scripts/conductor_install.py --core

# Install only gemini CLI
python scripts/conductor_install.py --gemini

# Install only VS Code extension
python scripts/conductor_install.py --vscode

# Install only Claude commands
python scripts/conductor_install.py --claude
```

## Installation Methods Comparison

| Method | Best For | Notes |
|--------|----------|-------|
| One-liner (`install.cat`) | New users | Quickest way to get started |
| Manual clone | Developers | Full control over installation |
| Mise tasks | Daily use | Integrated with development workflow |
| Python script | Automation | Can be scripted in other tools |

## Post-Installation Setup

### Shell Integration

**Bash:**
```bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
```

**Zsh:**
```bash
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
```

**PowerShell:**
```powershell
Add-Content $PROFILE 'if (Get-Command mise -ErrorAction SilentlyContinue) { mise activate pwsh | Out-String | Invoke-Expression }'
```

### Verify Everything Works

```bash
# Check conductor-core
python -c "import conductor_core; print('✓ conductor-core installed')"

# Check conductor-gemini
conductor-gemini --help

# Check VS Code extension
code --list-extensions | grep conductor

# Check Claude commands
ls ~/.claude/skills/conductor/
```

## Development Installation

If you want to contribute or modify conductor:

```bash
# Clone the repo
git clone https://github.com/edithatogo/conductor-next.git
cd conductor-next

# Setup development environment
mise install
mise run dev-setup

# Run tests
mise run test

# Verify everything
mise run verify
```

## Updating

To update to the latest version:

```bash
# Check for updates
mise run check-updates

# Apply updates
mise run update-all

# Or use the update script directly
python scripts/conductor_update.py --all
```

## Uninstalling

To remove conductor-next:

```bash
# Remove installation directory
rm -rf ~/.local/share/conductor-next

# Remove Claude commands
rm -rf ~/.claude/skills/conductor
rm -rf ~/.claude/commands/conductor*

# Remove mise configuration (optional)
rm -rf ~/.config/mise
```

## Platform-Specific Notes

### macOS

- **Homebrew**: If you have Homebrew, the installer will use it for dependencies
- **Apple Silicon**: Fully supported on M1/M2/M3 Macs

### Linux

- **Package Managers**: The installer will detect apt, yum, dnf, or pacman
- **WSL**: Works on WSL2 (Windows Subsystem for Linux)

### Windows

- **WSL Recommended**: For best compatibility, use WSL2
- **Native PowerShell**: Also supported with some limitations
- **Git Bash**: May work but not officially supported

## Next Steps

After installation:

1. Read the [Quick Start Guide](QUICKSTART.md)
2. Review [Troubleshooting](TROUBLESHOOTING.md) if you encounter issues
3. Explore the [Workflow Documentation](conductor/workflow.md)

## Getting Help

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Run `mise run verify` to diagnose issues
3. Open an issue on GitHub
