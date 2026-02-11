# Track Spec: Project Foundation

## Overview
This track aims to transform Conductor from a monolithic `gemini-cli` extension into a modular system with a platform-agnostic core. This involves merging community contributions (PR #9 and PR #25) and establishing the `conductor-core` package.

## Requirements
1. **PR Integration:** Merge [PR #9](https://github.com/gemini-cli-extensions/conductor/pull/9) and [PR #25](https://github.com/gemini-cli-extensions/conductor/pull/25) into the main branch.
2. **Core Abstraction:** Extract all non-platform-specific logic (Prompt rendering, Track management, Plan execution, Spec generation) into a `conductor-core/` directory.
3. **Platform Adapters:** Refactor the existing CLI code to become an adapter that imports from `conductor-core`.
4. **Technology Alignment:** Ensure all core logic uses `pydantic` for data models and `jinja2` for templates.
5. **Quality Standard:** Achieve 95% unit test coverage for the new `conductor-core` package.

## Architecture
- `conductor-core/`: The platform-independent logic.
- `conductor-gemini/`: The specific wrapper for Gemini CLI.
- `conductor-vscode/`: (Placeholder) Scaffolding for the VS Code extension.
