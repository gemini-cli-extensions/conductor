# Track Specification: Upstream Sync & Cross-Platform Skill Abstraction

## Overview
This track focuses on synchronizing the current Conductor implementation with the latest upstream developments (gemini-cli-extensions/conductor and jnorthrup/conductor2) and refining the cross-platform skill abstraction layer. The goal is to ensure Conductor skills can be seamlessly adopted across Google Antigravity, VS Code, Codex, Gemini CLI, and Qwen, with a unified definition source and automated synchronization. Finally, the latest version will be built and installed locally for verification.

## Functional Requirements

### 1. Upstream Synchronization
-   **Audit:** Analyze upstream repositories (`gemini-cli-extensions/conductor` and `jnorthrup/conductor2`) to identify key architectural changes, new commands, and workflow improvements.
-   **Alignment:** Integrate identified features, including:
    -   Modularization updates to `conductor-core`.
    -   New or updated commands (e.g., `review`, `setup`).
    -   Documentation and guide refinements.
    -   Workflow protocol enhancements.

### 2. Skill Abstraction & Mapping
-   **Conceptual Mapping:** Define the role of the Gemini CLI extension as the primary definition source and map its concepts to other platforms (Antigravity, VS Code, Codex, Qwen).
-   **Skill Manifest Schema:** Define/Refine a strict schema (the "Skill Manifest") that acts as the single source of truth for a skill's definition.
    -   Must include triggers, description, parameters, core logic entry point.
    -   Must include **Engine Compatibility** fields (e.g., "Requires Core vX.Y").
    -   **Capability Awareness:** Include logic or metadata to handle platform differences (e.g., fallback behaviors if a platform lacks UI prompts).
-   **Interface Analysis:** Document how skills are surfaced in each tool (e.g., `/` commands, `$` triggers) and identify necessary adaptations.
-   **Implementation:**
    -   **Core-First Refactoring:** Move business logic from adapters into `conductor-core`, leaving adapters as thin translation layers.
    -   **Generative Synchronization:** Develop/Update scripts to generate platform-specific configuration (e.g. `package.json` contributions, `gemini-extension.json`) directly from the Skill Manifest.
    -   **Unified Error Reporting:** Implement a typed error handling protocol in `conductor-core` that allows adapters to render errors natively (Toast vs. stderr).

### 3. Standardization & Documentation
-   **Skill Style Guide:** Create a new standard (e.g., `conductor/code_styleguides/skill_definition.md`) defining naming conventions, metadata requirements, and directory structure for skills.
-   **SKILL.md Template:** Design and implement a standard `SKILL.md` template for documenting individual skills.
-   **Command Syntax Matrix:** Create a reference document mapping Conductor commands to their specific syntax in each target platform (Gemini, Antigravity, etc.).

### 4. Robustness & Validation
-   **Contract Tests:** Implement a suite of contract tests in `conductor-core` to verify skill logic independently of platform adapters.
-   **Artifact Validation (Smoke Test):** Develop a script to verify that generated artifacts (e.g., `package.json` entries) strictly match the Skill Manifest definitions.
-   **Cross-Platform Verification:** Verify the abstraction by demonstrating full functionality of a complex skill (e.g., `newTrack`) across Gemini CLI and VS Code using the shared core.

### 5. Build & Installation
-   **Build Process:** Create/update scripts to build the VSIX package from the updated source.
-   **Local Installation:** Automatically install the built VSIX into the local VS Code and Google Antigravity instances.
-   **Future-Proofing:** Draft a comprehensive roadmap for future automated deployment to VS Code Marketplace AND OpenVSX Registry.

## Non-Functional Requirements
-   **Code Quality:** Maintain >95% test coverage for new core logic.
-   **Consistency:** Ensure the "Spec -> Plan -> Implement" workflow remains consistent across all target platforms.
-   **Documentation:** Update architectural diagrams or documents to reflect the refined skill abstraction model.

## Acceptance Criteria
-   [ ] Local codebase reflects key features and architecture of upstream HEAD.
-   [ ] A "Skill Manifest" schema is defined with compatibility and capability fields.
-   [ ] A "Skill Mapping" document and "Command Syntax Matrix" exist.
-   [ ] A new `skill_definition.md` style guide is added to the project.
-   [ ] Unified Error Reporting protocol is implemented in Core and Adapters.
-   [ ] Contract tests are implemented for core skill logic.
-   [ ] Scripts exist to validate and sync skills across platform adapters from the manifest.
-   [ ] A "Smoke Test" script validates generated artifacts.
-   [ ] A valid VSIX is built from the updated code.
-   [ ] The updated extension is successfully installed and verified in the local VS Code/Antigravity environment.
-   [ ] A deployment roadmap document (covering VS Code Marketplace & OpenVSX) is created.

## Out of Scope
-   Immediate publishing to public VS Code marketplaces (only planning is required).
-   Full implementation of platform adapters for tools other than Gemini CLI, VS Code, and Antigravity (unless required for proof of concept).
