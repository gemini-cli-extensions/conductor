# Track Specification: Platform Adapter Expansion

## Overview
This track focuses on the full implementation of platform adapters for tools beyond the initial set (Gemini CLI and VS Code). Specifically, it targets Claude CLI, Codex, and OpenCode, ensuring that the Conductor protocol is natively supported and easily installable in these environments using the unified `conductor-core`.

## Functional Requirements
- **Claude CLI Adapter:** Implement a robust bridge for Claude Code that leverages its skill system.
- **Codex/Agent Skills:** Finalize the integration for Codex, ensuring all core commands are mapped.
- **Unified Installer:** Enhance `skill/scripts/install.sh` to handle all new platform targets.
- **Protocol Parity:** Verify that `Spec -> Plan -> Implement` works identically in Claude and Codex as it does in Gemini.

## Acceptance Criteria
- [ ] Claude CLI can execute `/conductor-setup`, `/conductor-newtrack`, etc.
- [ ] Codex correctly registers and displays Conductor skills.
- [ ] `install.sh` supports `--target claude` and `--target codex`.
- [ ] Documentation updated for all new platforms.
