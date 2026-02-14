# Troubleshooting Guide

Common issues and solutions for conductor-next installation and usage.

## Installation Issues

### Issue: "command not found: mise"

**Cause**: mise is not installed or not in PATH

**Solution**:
```bash
# Install mise
curl https://mise.run | sh

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or restart your terminal
```

### Issue: "Permission denied" when running install.sh

**Cause**: Script doesn't have execute permissions

**Solution**:
```bash
# Make it executable
chmod +x install.sh

# Or run with bash explicitly
bash install.sh
```

### Issue: "git clone fails"

**Cause**: Git not installed or network issues

**Solution**:
```bash
# Check git is installed
git --version

# If not installed:
# macOS: brew install git
# Ubuntu/Debian: sudo apt-get install git
# Windows: Download from git-scm.com
```

### Issue: "Python not found"

**Cause**: Python not installed or not in PATH

**Solution**:
```bash
# Install Python 3.9+
# macOS: brew install python
# Ubuntu: sudo apt-get install python3
# Windows: Download from python.org

# Verify
python3 --version
# or
python --version
```

## Component Installation Issues

### Issue: VS Code extension won't install

**Cause**: VS Code CLI not in PATH

**Solution**:
```bash
# Check code command
code --version

# If not found, VS Code may need to be added to PATH
# macOS: ln -s "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" /usr/local/bin/code
# Windows: Usually automatic, but may need to reinstall VS Code with "Add to PATH" option
```

### Issue: "conductor-core import fails"

**Cause**: Python package not installed correctly

**Solution**:
```bash
# Reinstall core component
pip install ./conductor-core --force-reinstall

# Verify
python -c "import conductor_core; print(conductor_core.__version__)"
```

### Issue: Claude commands not appearing

**Cause**: Claude Code not installed or .claude directory not set up

**Solution**:
```bash
# Check if Claude Code is installed
which claude

# Install Claude Code if needed
# npm install -g @anthropic-ai/claude-code

# Copy conductor commands
cp -r .claude ~/.claude
```

## Mise Issues

### Issue: "mise: command not found"

**Solution**:
```bash
# Source mise activation
eval "$(mise activate)"

# Or add to shell profile
echo 'eval "$(mise activate bash)"' >> ~/.bashrc  # For bash
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc    # For zsh
```

### Issue: "mise run" commands fail

**Cause**: Tools not installed

**Solution**:
```bash
# Install all tools
mise install

# Check tool status
mise list
```

### Issue: Task "not found" errors

**Cause**: mise.toml not found or invalid

**Solution**:
```bash
# Check you're in the right directory
ls mise.toml

# If missing, clone the repository again
git clone https://github.com/edithatogo/conductor-next.git
cd conductor-next
```

## Verification Issues

### Issue: "verify_installation.py reports failures"

**Common Causes & Solutions**:

1. **Component not installed**
   ```bash
   # Install missing components
   python scripts/conductor_install.py --all
   ```

2. **PATH not updated**
   ```bash
   # Restart terminal or source profile
   source ~/.bashrc  # or ~/.zshrc
   ```

3. **Mise not activated**
   ```bash
   eval "$(mise activate)"
   ```

## Update Issues

### Issue: "update fails with merge conflicts"

**Cause**: Local changes conflict with upstream

**Solution**:
```bash
# Stash local changes
git stash

# Update
python scripts/conductor_update.py --all

# Restore local changes
git stash pop
```

### Issue: "No updates found but I know there are updates"

**Cause**: Git remote not configured correctly

**Solution**:
```bash
# Check remotes
git remote -v

# Add upstream if missing
git remote add upstream https://github.com/edithatogo/conductor-next.git

# Fetch
git fetch upstream
```

## Platform-Specific Issues

### Windows: PowerShell execution policy

**Error**: "cannot be loaded because running scripts is disabled"

**Solution**:
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single execution
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Windows: WSL not detected

**Cause**: WSL not installed or not in PATH

**Solution**:
```powershell
# Install WSL
wsl --install

# Or use native PowerShell installation (limited features)
.\install.ps1 -SkipWSLCheck
```

### macOS: "mise: command not found" after installation

**Cause**: Shell profile not reloaded

**Solution**:
```bash
# Add to PATH manually
export PATH="$HOME/.local/bin:$PATH"

# Or restart terminal
# Or reload profile
source ~/.zshrc  # or ~/.bashrc
```

### Linux: Permission denied errors

**Cause**: User doesn't have write permissions

**Solution**:
```bash
# Install to user directory instead of system
python scripts/conductor_install.py --all --user

# Or use pip with --user flag
pip install --user ./conductor-core
```

## Network Issues

### Issue: "Failed to fetch from GitHub"

**Cause**: Network connectivity or rate limiting

**Solution**:
```bash
# Check connectivity
ping github.com

# Configure git to use SSH instead of HTTPS
git remote set-url origin git@github.com:edithatogo/conductor-next.git

# Or set up GitHub token for API access
export GITHUB_TOKEN=your_token_here
```

## Performance Issues

### Issue: Installation is very slow

**Possible Causes**:
- Slow internet connection
- Large repository clone
- Many dependencies to install

**Solutions**:
```bash
# Use shallow clone
git clone --depth 1 https://github.com/edithatogo/conductor-next.git

# Skip optional components
python scripts/conductor_install.py --core --gemini  # Skip VS Code and Claude

# Use uv instead of pip for faster installs
pip install uv
uv pip install ./conductor-core
```

## Debug Mode

To get more information about issues:

```bash
# Run with verbose output
python scripts/conductor_install.py --all --verbose

# Check system info
python scripts/verify_installation.py --verbose

# Check mise debug output
mise run verify --verbose
```

## Getting More Help

If none of these solutions work:

1. **Run diagnostics**:
   ```bash
   python scripts/verify_installation.py > diagnostic.log 2>&1
   ```

2. **Check GitHub Issues**:
   - Visit: https://github.com/edithatogo/conductor-next/issues
   - Search for similar problems

3. **Create a new issue** with:
   - Operating system and version
   - Installation method used
   - Full error message
   - Output of `python scripts/verify_installation.py`

## Quick Fixes

### Nuclear Option: Clean Install

If nothing works, start fresh:

```bash
# Remove everything
rm -rf ~/.local/share/conductor-next
rm -rf ~/.claude/skills/conductor
pip uninstall conductor-core conductor-gemini -y

# Reinstall
curl -fsSL install.cat/edithatogo/conductor-next | sh
```

### Reset Mise

```bash
# Clear mise cache
mise cache clear

# Reinstall tools
mise install --force
```

### Check Git Status

```bash
# Check if repo is in good state
git status
git log --oneline -5

# Reset to clean state if needed
git reset --hard HEAD
git clean -fd
```
