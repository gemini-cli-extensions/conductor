# Track Specification: Installer UX & Cross-Platform Release

## Summary
Improve the installation experience by providing consistent, cross-platform installers and verification steps for all supported tools. Evaluate whether a Node package release (npm/GitHub Packages) is worthwhile and define a release strategy.

## Goals
- One-command local install for Windows and macOS/Linux.
- Clear output showing installed artifacts and locations.
- Provide a verification mode that checks installations tool-by-tool.
- Evaluate and document a Node package release option.

## Non-Goals
- VS Code marketplace publication (separate track).
- Rewriting adapter internals.

## Acceptance Criteria
- Installers exist for Windows (PowerShell) and cross-platform (Node or Python wrapper) with consistent flags.
- Installers can install VSIX, Antigravity workflows, and CLI-based skill locations.
- Documentation explains the recommended install path and verification command.
