# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-12-31

### Added
- **Core Library (`conductor-core`)**: Extracted core logic into a standalone Python package.
- **TaskRunner**: New centralized service for managing track and task lifecycles, including status updates and TDD loop support.
- **Git Notes Integration**: Automated recording of task summaries and phase verifications using `git notes`.
- **VS Code Extension**: Fully functional integration with `setup`, `status`, `new-track`, and `implement` commands.
- **Improved Project Status**: Detailed, structured status reports showing progress across all active and archived tracks.
- **Robust ID Generation**: Improved track ID generation using sanitized descriptions and hashes.

### Changed
- **Gemini Adapter**: Refactored to delegate all business logic to `conductor-core`.
- **Project Structure**: Modernized monorepo architecture with clear separation between core and platform adapters.
- **CLI Commands**: Enhanced `status` and `implement` commands for better user experience.

### Fixed
- Various regex and parsing issues in `tracks.md` and `plan.md`.
- Improved project initialization and setup robustness.

## [0.1.0] - 2025-12-30

### Added
- Initial release of Conductor.
- Basic support for Gemini CLI and VS Code scaffolding.
- Track-based planning and specification system.
