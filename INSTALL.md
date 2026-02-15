# Installation Methods for Conductor

Conductor can be installed through multiple methods to suit different environments and preferences.

## Quick Install

### Via mise (Recommended)

```bash
# Install using mise (cross-platform)
mise install edithatogo/conductor-next

# Or run directly
curl -fsSL install.cat/edithatogo/conductor-next | sh
```

### Via Smithery (Coming Soon)

```bash
# Once published to Smithery
smithery install conductor
```

## Detailed Installation Methods

### 1. Traditional Package Managers

#### pip (Python)

```bash
pip install conductor-core conductor-gemini
```

#### npm (Node.js)

```bash
npm install -g @conductor/vscode-extension
```

### 2. Cross-Platform Package Managers

#### Homebrew (macOS/Linux)

```bash
# Coming soon
brew tap edithatogo/conductor
brew install conductor
```

#### Chocolatey (Windows)

```powershell
# Coming soon
choco install conductor
```

#### Scoop (Windows)

```powershell
# Coming soon
scoop bucket add conductor https://github.com/edithatogo/scoop-conductor
scoop install conductor
```

### 3. Direct Download

#### GitHub Releases

1. Visit [GitHub Releases](https://github.com/edithatogo/conductor-next/releases)
2. Download the appropriate binary for your platform
3. Extract and add to PATH

#### From Source

```bash
git clone https://github.com/edithatogo/conductor-next.git
cd conductor-next
./install.sh  # Unix/macOS
# or
./install.ps1  # Windows
```

## Prerequisites

All installation methods require:

- Git (>= 2.0)
- Python (>= 3.9) or Node.js (>= 18)
- Internet connection for initial setup

## Verification

After installation, verify Conductor is working:

```bash
# Check version
conductor --version

# Run setup
conductor:setup

# Verify installation
mise run verify  # if using mise
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Run with appropriate permissions (may require sudo on Unix)
   - Check PATH environment variable

2. **Missing Dependencies**
   - Ensure Git, Python/Node.js are installed
   - Check version requirements

3. **Network Issues**
   - Verify internet connection
   - Check firewall/proxy settings

## Contributing to Installation Methods

Want to add support for another package manager or marketplace?

1. Fork the repository
2. Add the necessary configuration files
3. Submit a pull request with your changes

Currently supported marketplace integrations:

- [x] mise
- [ ] Smithery
- [ ] Homebrew
- [ ] Chocolatey
- [ ] Scoop
- [ ] npm Registry
- [ ] PyPI
