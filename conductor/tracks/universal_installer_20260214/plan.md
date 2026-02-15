# Implementation Plan: Universal Installer via Mise

## Phase 1: Mise Configuration & Core Setup

- [x] Task: Create `mise.toml` with tool definitions and dependencies
  - [x] Subtask: Define Python version and virtual environment setup
  - [x] Subtask: Define Node.js version for VS Code extension build
  - [x] Subtask: Add conductor-core as a custom tool
  - [x] Subtask: Add conductor-gemini as a custom tool
  - [x] Subtask: Define environment variables and paths
- [x] Task: Create project structure and directories
  - [x] Subtask: Create `scripts/` directory for installer logic
  - [x] Subtask: Create `tools/` directory for custom tool definitions
  - [x] Subtask: Create `templates/` directory for install scripts
- [x] Task: Implement `scripts/conductor_install.py` core installer
  - [x] Subtask: Component detection (detect installed tools)
  - [x] Subtask: Installation orchestration logic
  - [x] Subtask: Configuration file management
  - [x] Subtask: Error handling and rollback
- [x] Task: Conductor - Automated Verification 'Phase 1: Mise Configuration & Core Setup' (Protocol in workflow.md)

## Phase 2: Unix/macOS Installation Script

- [x] Task: Create `install.sh` one-liner script
  - [x] Subtask: Detect OS and architecture
  - [x] Subtask: Install mise if not present
  - [x] Subtask: Clone/download conductor-next repository
  - [x] Subtask: Run `mise install` and `mise run install-all`
  - [x] Subtask: Add to PATH and shell configuration
- [x] Task: Create `scripts/install_unix.py` helper
  - [x] Subtask: macOS-specific installation steps
  - [x] Subtask: Linux distribution detection and package manager integration
  - [x] Subtask: Homebrew integration for dependencies
- [x] Task: Implement component-specific installers
  - [x] Subtask: conductor-core pip installation
  - [x] Subtask: conductor-gemini symlink/setup
  - [x] Subtask: VS Code extension installation from VSIX
  - [x] Subtask: Claude Code commands installation
- [x] Task: Conductor - Automated Verification 'Phase 2: Unix/macOS Installation Script' (Protocol in workflow.md)

## Phase 3: Windows Installation Script

- [x] Task: Create `install.ps1` PowerShell script
  - [x] Subtask: Detect Windows version and PowerShell version
  - [x] Subtask: Install mise for Windows or WSL detection
  - [x] Subtask: Clone/download conductor-next repository
  - [x] Subtask: Run installation via WSL or native PowerShell
  - [x] Subtask: Add to Windows PATH and PowerShell profile
- [x] Task: Create `scripts/install_windows.py` helper
  - [x] Subtask: WSL integration for Linux-like experience
  - [x] Subtask: Native Windows fallback for PowerShell-only
  - [x] Subtask: Chocolatey/Scoop integration for dependencies
- [x] Task: Test Windows installation scenarios
  - [x] Subtask: Windows 11 with WSL2
  - [x] Subtask: Windows 10 with WSL2
  - [x] Subtask: Windows Server (PowerShell only)
- [x] Task: Conductor - Automated Verification 'Phase 3: Windows Installation Script' (Protocol in workflow.md)

## Phase 4: Mise Tasks & Workflows

- [x] Task: Implement `mise run sync-upstream` task
  - [x] Subtask: Script to fetch from gemini-cli-extensions/conductor
  - [x] Subtask: Script to fetch from jnorthrup/conductor2
  - [x] Subtask: Merge strategy for upstream changes
  - [x] Subtask: Conflict detection and manual intervention prompts
- [x] Task: Implement `mise run build-all` task
  - [x] Subtask: Build conductor-core Python package
  - [x] Subtask: Build conductor-gemini extension
  - [x] Subtask: Build VS Code extension (VSIX)
  - [x] Subtask: Package Claude Code commands
- [x] Task: Implement `mise run install-all` task
  - [x] Subtask: Install all built components
  - [x] Subtask: Verify installations
  - [x] Subtask: Configure environment
- [x] Task: Implement `mise run update-all` task
  - [x] Subtask: Check for updates in all components
  - [x] Subtask: Download and install updates
  - [x] Subtask: Handle breaking changes and migrations
- [x] Task: Conductor - Automated Verification 'Phase 4: Mise Tasks & Workflows' (Protocol in workflow.md)

## Phase 5: Install.cat Integration & Distribution

- [x] Task: Configure install.cat integration
  - [x] Subtask: Create install.cat manifest
  - [x] Subtask: Test `curl install.cat/edithatogo/conductor-next | sh`
  - [x] Subtask: Verify one-liner works on fresh systems
- [x] Task: Create release artifacts and workflow
  - [x] Subtask: `.github/workflows/release.yml` for automated releases
  - [x] Subtask: Version tagging and release notes generation
  - [x] Subtask: Artifact upload (VSIX, tarballs, checksums)
- [x] Task: Documentation and quick-start guide
  - [x] Subtask: Update README with installation instructions
  - [x] Subtask: Create INSTALL.md with detailed steps
  - [x] Subtask: Create TROUBLESHOOTING.md for common issues
  - [x] Subtask: Create QUICKSTART.md for new users
- [x] Task: Conductor - Automated Verification 'Phase 5: Install.cat Integration & Distribution' (Protocol in workflow.md)

## Phase 6: Testing & Finalization

- [x] Task: End-to-end installation testing
  - [x] Subtask: Test on fresh macOS installation
  - [x] Subtask: Test on fresh Ubuntu installation
  - [x] Subtask: Test on fresh Windows 11 installation
  - [x] Subtask: Test on existing installations (upgrade path)
- [x] Task: Verify all acceptance criteria
  - [x] Subtask: Check all components install correctly
  - [x] Subtask: Verify update mechanism works
  - [x] Subtask: Confirm install.cat integration
- [x] Task: Final documentation review
  - [x] Subtask: Review and update all docs
  - [x] Subtask: Add badges and installation shields
- [x] Task: Conductor - Automated Verification 'Phase 6: Testing & Finalization' (Protocol in workflow.md)
