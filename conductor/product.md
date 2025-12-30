# Product Context

## Initial Concept
Conductor is a Context-Driven Development tool originally built for `gemini-cli`. The goal is to evolve it into a platform-agnostic standard that manages project context, specifications, and plans across multiple development environments.

## Vision
To create a universal "Conductor" that orchestrates AI-assisted development workflows identically, regardless of the underlying tool or IDE. Whether a user is in a terminal with `gemini-cli` or `qwen-cli`, or inside VS Code (Antigravity), the experience should be consistent, context-aware, and command-driven.

## Core Objectives
-   **Multi-Platform Support:** Expand beyond `gemini-cli` to support `qwen-cli` (and other CLI ports) and a native VS Code extension (targeting Google Antigravity/Copilot environments).
-   **Unified Core:** Extract the business logic (prompts, state management, file handling) into a platform-agnostic core library. This ensures that the "brain" of Conductor is written once and shared.
-   **Consistent Workflow:** Guarantee that the `Spec -> Plan -> Implement` loop behaves identically across all platforms.
-   **Familiar Interface:** Maintain the slash-command UX (e.g., `/conductor:newTrack`) as the primary interaction model, adapting it to platform-specific equivalents (like `@conductor /newTrack` in IDE chat) where necessary.
-   **Enhanced IDE Integration:** In IDE environments, leverage native capabilities (active selection, open tabs) to enrich the context passed to the Conductor core, streamlining the "Context" phase of the workflow.

## Key Resources
-   **Reference Implementation:** [PR #25](https://github.com/gemini-cli-extensions/conductor/pull/25) - Port for claude-cli, opencode, and codex. This will serve as a primary reference for the abstraction layer design.