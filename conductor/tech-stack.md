# Technology Stack

## Core
-   **Language:** Python 3.9+
    -   *Rationale:* Standard for Gemini CLI extensions and offers rich text processing capabilities for the core library.
-   **Project Structure:**
    -   `conductor-core/`: Pure Python library (PyPI package) containing the protocol, prompts, and state management.
    -   `conductor-gemini/`: The existing `gemini-cli` extension wrapper.
    -   `conductor-vscode/`: The new VS Code extension wrapper (likely TypeScript/Python bridge).

## Strategy: Refactoring and Integration
-   **PR Consolidation:** Merge [PR #9](https://github.com/gemini-cli-extensions/conductor/pull/9) and [PR #25](https://github.com/gemini-cli-extensions/conductor/pull/25) into the repository.
-   **Evolutionary Path:** Use the merged code as a baseline to identify common patterns, then refactor them into a platform-agnostic `conductor-core` library.
-   **Issue-Driven Development:** Prioritize resolving open [GitHub Issues](https://github.com/gemini-cli-extensions/conductor/issues) during the refactoring process to ensure the new architecture solves existing pain points.

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
-   **Linting/Formatting:** `ruff` (fast, unified Python linter/formatter).
-   **Testing:** `pytest` for the core library; platform-specific runners for wrappers.
-   **Type Checking:** `mypy` (Strict mode).
