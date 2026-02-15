# Troubleshooting Guide

This guide helps diagnose and resolve common issues with Conductor installation and usage.

## Installation Issues

### Prerequisites Missing

**Problem**: Installation fails with "command not found" errors.

**Solution**: Ensure all prerequisites are installed:

- Git (>= 2.0)
- Python (>= 3.9)
- Node.js (>= 18)
- npm (>= 8)

Check with:

```bash
git --version
python --version
node --version
npm --version
```

### mise Installation Issues

**Problem**: mise fails to install or is not recognized.

**Solution**:

1. Install mise manually:

   ```bash
   # Unix/macOS
   curl https://mise.run | sh

   # Windows (PowerShell)
   irm https://mise.run | iex
   ```

2. Add mise to PATH:

   ```bash
   # Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
   export PATH="$HOME/.local/bin:$PATH"
   eval "$(mise activate)"
   ```

### Permission Errors

**Problem**: Installation fails with permission denied errors.

**Solution**:

1. On Unix/macOS, run with appropriate permissions:

   ```bash
   # If needed, use sudo for system-wide installation
   sudo ./install.sh
   ```

2. On Windows, run PowerShell as Administrator.

### Network Issues

**Problem**: Installation fails with network errors or timeouts.

**Solution**:

1. Check internet connection
2. Verify firewall/proxy settings
3. Try cloning the repository manually:

   ```bash
   git clone https://github.com/edithatogo/conductor-next.git
   cd conductor-next
   ./install.sh
   ```

## Component-Specific Issues

### Python Components Not Found

**Problem**: Python modules like `conductor_core` are not found after installation.

**Solution**:

1. Check if installed with pip:

   ```bash
   pip list | grep conductor
   ```

2. Install manually if needed:

   ```bash
   pip install ./conductor-core
   pip install ./conductor-gemini
   ```

### VS Code Extension Not Working

**Problem**: VS Code extension doesn't appear after installation.

**Solution**:

1. Check if VS Code is installed and accessible from command line:

   ```bash
   code --version
   ```

2. Install manually:

   ```bash
   code --install-extension conductor.vsix
   ```

### Claude Code Commands Missing

**Problem**: Claude Code commands are not available.

**Solution**:

1. Verify `.claude` directory exists in your home directory:

   ```bash
   ls ~/.claude
   ```

2. Manually copy commands if needed:

   ```bash
   cp -r .claude/commands ~/.claude/commands/
   cp -r .claude/skills ~/.claude/skills/
   ```

## mise-Related Issues

### mise Tasks Not Working

**Problem**: `mise run` commands fail.

**Solution**:

1. Verify mise configuration:

   ```bash
   mise ls
   ```

2. Reinstall mise tools:

   ```bash
   mise install
   ```

3. Check mise.toml for correct configuration.

### Environment Variables Not Set

**Problem**: Environment variables defined in mise.toml are not available.

**Solution**:

1. Activate mise in your shell:

   ```bash
   eval "$(mise activate)"
   ```

2. Or restart your terminal to reload shell configuration.

## Platform-Specific Issues

### Windows Issues

**Problem**: Installation fails on Windows.

**Solutions**:

1. Ensure PowerShell execution policy allows scripts:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. Use WSL if native installation fails:

   ```powershell
   # Install WSL2 and run installer from within WSL
   wsl --install
   # Then run the Unix installer inside WSL
   ```

### macOS Issues

**Problem**: Installation fails on macOS.

**Solutions**:

1. Ensure Xcode command line tools are installed:

   ```bash
   xcode-select --install
   ```

2. Check for Homebrew and install dependencies:

   ```bash
   brew install python node git
   ```

## Verification Steps

### Check Installation Status

```bash
# Verify mise is working
mise --version

# Check installed tools
mise ls

# Verify Python packages
python -c "import conductor_core; print('Core version:', conductor_core.__version__)"
```

### Run Diagnostic Commands

```bash
# Run mise doctor
mise doctor

# Verify all components
python scripts/conductor_install.py --verify
```

## Getting Help

If issues persist:

1. Check the [GitHub Issues](https://github.com/edithatogo/conductor-next/issues) for known issues
2. Run the installer with verbose output:

   ```bash
   # Unix
   DEBUG=1 ./install.sh

   # Windows
   $DebugPreference = "Continue"; .\install.ps1
   ```

3. Share the full error message and system information when asking for help
4. Consider using the manual installation method as a workaround

## Common Solutions Summary

Most installation issues can be resolved by:

1. Ensuring all prerequisites are installed and up-to-date
2. Having proper network connectivity
3. Running with appropriate permissions
4. Activating mise in your shell environment
5. Verifying PATH includes necessary directories
