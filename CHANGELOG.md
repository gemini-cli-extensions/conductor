# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0](https://github.com/gemini-cli-extensions/conductor/compare/conductor-v0.1.1...conductor-v0.2.0) (2026-01-14)

### Features
- **Core Library (`conductor-core`)**: Extracted core logic into a standalone platform-agnostic Python package.
- **TaskRunner**: New centralized service for managing track and task lifecycles, including status updates and TDD loop support.
- **Git Notes Integration**: Automated recording of task summaries and phase verifications using `git notes`.
- **VS Code Extension**: Fully functional integration with `setup`, `status`, `new-track`, and `implement` commands.
- **Improved Project Status**: Detailed, structured status reports showing progress across all active and archived tracks.
- **Robust ID Generation**: Improved track ID generation using sanitized descriptions and hashes.
- **Multi-Platform Support**: Portable skill support for Claude CLI, OpenCode, and Codex.
- Add GitHub Actions workflow to package and upload release assets.
- **conductor:** implement tracks directory abstraction and Universal File Resolution Protocol.
- **styleguide:** Add comprehensive Google C# Style Guide summary.

### Bug Fixes
- **conductor:** ensure track completion and doc sync are committed automatically.
- **conductor:** remove hardcoded path hints in favor of Universal File Resolution Protocol.
- Correct typos, step numbering, and documentation errors.
- standardize Markdown checkbox format for tracks and plans.
- **setup:** Enhance project analysis protocol to avoid excessive token consumption.
- **styleguide:** Update C# guidelines and formatting rules for consistency.

## [0.1.0] - 2025-12-30

### Added
- Initial release of Conductor.
- Basic support for Gemini CLI and VS Code scaffolding.
- Track-based planning and specification system.
- Foundation for Context-Driven Development.
