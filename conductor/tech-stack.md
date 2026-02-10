# Technology Stack

## Core
-   **Language:** Python 3.9+
    -   *Rationale:* Standard for Gemini CLI extensions and offers rich text processing capabilities for the core library.
-   **Project Structure:**
    -   `conductor-core/`: Pure Python library (PyPI package) containing the protocol, prompts, and state management.
    -   `conductor-gemini/`: The existing `gemini-cli` extension wrapper.
    -   `conductor-vscode/`: The new VS Code extension wrapper (likely TypeScript/Python bridge).

## Architecture Status
-   **Completed:** Extracted platform-agnostic core library into `conductor-core/`.
-   **Completed:** Aligned Gemini CLI and Claude Code prompt protocols via Jinja2 templates in Core.
-   **In Progress:** Development of VS Code adapter (`conductor-vscode`).

## Strategy: Refactoring and Integration (Completed)
-   **PR Consolidation:** Merged [PR #9](https://github.com/gemini-cli-extensions/conductor/pull/9) and [PR #25](https://github.com/gemini-cli-extensions/conductor/pull/25).
-   **Unified Core:** Successfully refactored shared logic into `conductor-core`.

## Dependencies
-   **Core Library:**
    -   `pydantic`: For robust data validation and schema definition (Specs, Plans, State).
    -   `jinja2`: For rendering prompt templates and markdown artifacts.
    -   `gitpython`: For abstracting git operations (reverts, diffs) across platforms.
-   **Gemini CLI Wrapper:**
    -   `gemini-cli-extension-api`: The standard interface.
-   **VS Code Wrapper:**
    -   `vscode-languageclient` (if using LSP approach) or a lightweight Python shell wrapper.

## Development Tools
-   **Linting/Formatting:** `ruff` (fast, unified Python linter/formatter, enforcing comprehensive rule sets).
-   **Testing:** `pytest` with `pytest-cov` (Enforcing 100% coverage for `conductor-core` and 99% for adapters).
-   **Type Checking:** `mypy` (Strict mode).
-   **Automation:** `pre-commit` hooks for local checks; GitHub Actions for CI/CD matrix (3.9-3.12) and automated monorepo releases (`release-please`).
