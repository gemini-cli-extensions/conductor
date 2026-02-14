# Implementation Plan: Universal Installer via Mise

## Phase 1: Mise Configuration & Core Setup
- [ ] Task: Create `mise.toml` with tool definitions and dependencies
    - [ ] Subtask: Define Python version and virtual environment setup
    - [ ] Subtask: Define Node.js version for VS Code extension build
    - [ ] Subtask: Add conductor-core as a custom tool
    - [ ] Subtask: Add conductor-gemini as a custom tool
    - [ ] Subtask: Define environment variables and paths
- [ ] Task: Create project structure and directories
    - [ ] Subtask: Create `scripts/` directory for installer logic
    - [ ] Subtask: Create `tools/` directory for custom tool definitions
    - [ ] Subtask: Create `templates/` directory for install scripts
- [ ] Task: Implement `scripts/conductor_install.py` core installer
    - [ ] Subtask: Component detection (detect installed tools)
    - [ ] Subtask: Installation orchestration logic
    - [ ] Subtask: Configuration file management
    - [ ] Subtask: Error handling and rollback
- [ ] Task: Conductor - Automated Verification 'Phase 1: Mise Configuration & Core Setup' (Protocol in workflow.md)

## Phase 2: Unix/macOS Installation Script
- [ ] Task: Create `install.sh` one-liner script
    - [ ] Subtask: Detect OS and architecture
    - [ ] Subtask: Install mise if not present
    - [ ] Subtask: Clone/download conductor-next repository
    - [ ] Subtask: Run `mise install` and `mise run install-all`
    - [ ] Subtask: Add to PATH and shell configuration
- [ ] Task: Create `scripts/install_unix.py` helper
    - [ ] Subtask: macOS-specific installation steps
    - [ ] Subtask: Linux distribution detection and package manager integration
    - [ ] Subtask: Homebrew integration for dependencies
- [ ] Task: Implement component-specific installers
    - [ ] Subtask: conductor-core pip installation
    - [ ] Subtask: conductor-gemini symlink/setup
    - [ ] Subtask: VS Code extension installation from VSIX
    - [ ] Subtask: Claude Code commands installation
- [ ] Task: Conductor - Automated Verification 'Phase 2: Unix/macOS Installation Script' (Protocol in workflow.md)

## Phase 3: Windows Installation Script
- [ ] Task: Create `install.ps1` PowerShell script
    - [ ] Subtask: Detect Windows version and PowerShell version
    - [ ] Subtask: Install mise for Windows or WSL detection
    - [ ] Subtask: Clone/download conductor-next repository
    - [ ] Subtask: Run installation via WSL or native PowerShell
    - [ ] Subtask: Add to Windows PATH and PowerShell profile
- [ ] Task: Create `scripts/install_windows.py` helper
    - [ ] Subtask: WSL integration for Linux-like experience
    - [ ] Subtask: Native Windows fallback for PowerShell-only
    - [ ] Subtask: Chocolatey/Scoop integration for dependencies
- [ ] Task: Test Windows installation scenarios
    - [ ] Subtask: Windows 11 with WSL2
    - [ ] Subtask: Windows 10 with WSL2
    - [ ] Subtask: Windows Server (PowerShell only)
- [ ] Task: Conductor - Automated Verification 'Phase 3: Windows Installation Script' (Protocol in workflow.md)

## Phase 4: Mise Tasks & Workflows
- [ ] Task: Implement `mise run sync-upstream` task
    - [ ] Subtask: Script to fetch from gemini-cli-extensions/conductor
    - [ ] Subtask: Script to fetch from jnorthrup/conductor2
    - [ ] Subtask: Merge strategy for upstream changes
    - [ ] Subtask: Conflict detection and manual intervention prompts
- [ ] Task: Implement `mise run build-all` task
    - [ ] Subtask: Build conductor-core Python package
    - [ ] Subtask: Build conductor-gemini extension
    - [ ] Subtask: Build VS Code extension (VSIX)
    - [ ] Subtask: Package Claude Code commands
- [ ] Task: Implement `mise run install-all` task
    - [ ] Subtask: Install all built components
    - [ ] Subtask: Verify installations
    - [ ] Subtask: Configure environment
- [ ] Task: Implement `mise run update-all` task
    - [ ] Subtask: Check for updates in all components
    - [ ] Subtask: Download and install updates
    - [ ] Subtask: Handle breaking changes and migrations
- [ ] Task: Conductor - Automated Verification 'Phase 4: Mise Tasks & Workflows' (Protocol in workflow.md)

## Phase 5: Install.cat Integration & Distribution
- [ ] Task: Configure install.cat integration
    - [ ] Subtask: Create install.cat manifest
    - [ ] Subtask: Test `curl install.cat/edithatogo/conductor-next | sh`
    - [ ] Subtask: Verify one-liner works on fresh systems
- [ ] Task: Create release artifacts and workflow
    - [ ] Subtask: `.github/workflows/release.yml` for automated releases
    - [ ] Subtask: Version tagging and release notes generation
    - [ ] Subtask: Artifact upload (VSIX, tarballs, checksums)
- [ ] Task: Documentation and quick-start guide
    - [ ] Subtask: Update README with installation instructions
    - [ ] Subtask: Create INSTALL.md with detailed steps
    - [ ] Subtask: Create TROUBLESHOOTING.md for common issues
    - [ ] Subtask: Create QUICKSTART.md for new users
- [ ] Task: Conductor - Automated Verification 'Phase 5: Install.cat Integration & Distribution' (Protocol in workflow.md)

## Phase 6: Testing & Finalization
- [ ] Task: End-to-end installation testing
    - [ ] Subtask: Test on fresh macOS installation
    - [ ] Subtask: Test on fresh Ubuntu installation
    - [ ] Subtask: Test on fresh Windows 11 installation
    - [ ] Subtask: Test on existing installations (upgrade path)
- [ ] Task: Verify all acceptance criteria
    - [ ] Subtask: Check all components install correctly
    - [ ] Subtask: Verify update mechanism works
    - [ ] Subtask: Confirm install.cat integration
- [ ] Task: Final documentation review
    - [ ] Subtask: Review and update all docs
    - [ ] Subtask: Add badges and installation shields
- [ ] Task: Conductor - Automated Verification 'Phase 6: Testing & Finalization' (Protocol in workflow.md)
