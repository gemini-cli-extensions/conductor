# Track Specification: Universal Installer via Mise

## Summary
Create a universal one-click installer for conductor-next using `mise` (mise-en-place) that installs ALL conductor components across platforms. This installer will serve as the primary entry point for new users and provide a consistent installation experience for conductor-core, conductor-gemini, VS Code extension, Claude Code commands, and future adapters.

## Goals
- One-command installation via `mise` that handles all conductor components
- Cross-platform support (macOS, Linux, Windows via WSL and native PowerShell)
- Integration with install.cat for one-liner installation (`curl install.cat/edithatogo/conductor-next | sh`)
- Automated dependency management and updates
- Support for installing from different sources (release artifacts, git, local development)

## Components to Install
1. **conductor-core** - Python package with core logic
2. **conductor-gemini** - Gemini CLI extension and commands
3. **VS Code extension** - conductor.vsix package
4. **Claude Code commands** - Slash commands for Claude Code integration
5. **Future adapters** - Extensible for Codex, Qwen, etc.

## Key Deliverables
- `mise.toml` - Main mise configuration defining all tools, tasks, and dependencies
- `install.sh` - One-liner install script for Unix/macOS
- `install.ps1` - One-liner install script for Windows
- `scripts/conductor_install.py` - Main installer logic with component detection and installation
- `scripts/conductor_update.py` - Update checker and updater
- `.github/workflows/release.yml` - Automated release workflow

## Mise Tasks
- `mise run sync-upstream` - Sync from upstream repositories
- `mise run build-all` - Build all components from source
- `mise run install-all` - Install all components
- `mise run update-all` - Check for and apply updates
- `mise run verify` - Verify installation integrity

## Acceptance Criteria
- [ ] `mise.toml` defines all conductor components as tools/tasks
- [ ] `install.sh` works on macOS and Linux with one command
- [ ] `install.ps1` works on Windows PowerShell with one command
- [ ] `scripts/conductor_install.py` handles component detection and installation
- [ ] All components can be installed individually or together
- [ ] Integration with install.cat for one-liner installs
- [ ] Update mechanism detects new versions and applies updates
- [ ] Verification command confirms all components are correctly installed
- [ ] Documentation includes quick-start guide and troubleshooting

## Non-Goals
- Windows native support without WSL (PowerShell script handles this)
- Automatic VS Code marketplace publishing (separate track)
- Support for package managers other than mise (npm/pip optional)

## References
- Previous track: [installer_ux_20260131](../archive/installer_ux_20260131/)
- Related: [upstream_sync_20260131](../archive/upstream_sync_20260131/)
