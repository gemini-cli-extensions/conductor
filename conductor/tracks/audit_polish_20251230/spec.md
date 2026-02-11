# Track Spec: Deep Audit & Final Polish

## Overview
This track addresses the gaps identified by the `codebase_investigator` audit. The goal is to fill the implementation holes in the Gemini adapter (specifically the `implement` command) and the VS Code extension, and to finalize the `ProjectManager` logic.

## Requirements
1.  **Gemini Adapter Completion:**
    *   Refactor `status` command to use `ProjectManager`.
    *   Implement the `implement` command logic (calling the core `TaskLoop` or equivalent - likely need to port this from the original `implement.toml` logic into Python).
2.  **VS Code Extension Completion:**
    *   Add commands for `setup`, `implement`, `status`, `revert`.
3.  **Core Refinement:**
    *   Implement a robust ID generator in `ProjectManager`.
4.  **Verification:**
    *   All commands must be functional, not mocks.

## Dependencies
-   `conductor-core`
-   `conductor-gemini`
-   `conductor-vscode`
