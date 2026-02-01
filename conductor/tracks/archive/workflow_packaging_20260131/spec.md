# Track Specification: Workflow Packaging & Validation Schema (All Tools)

## Summary
Define a unified packaging and validation schema for Conductor artifacts across all supported tools (Gemini, Qwen, Claude Code, OpenCode, Codex, VS Code, Antigravity, Copilot). Establish a single source of truth so generated artifacts are consistent, discoverable, and verifiable.

## Goals
- Define a canonical schema that maps tool -> artifact type -> location -> command syntax.
- Make sync and validation tooling consume the same schema.
- Cover Antigravity global and workspace workflows, VSIX packaging, and Copilot rules.
- Provide a single validation command that fails on drift.

## Non-Goals
- Changing runtime behavior of adapters (handled in other tracks).
- Publishing to marketplaces or registries.

## Acceptance Criteria
- A schema file exists in-repo and is referenced by sync/validation tooling.
- Validation checks cover all tools and fail on missing or stale artifacts.
- Documentation references the schema as the canonical mapping and provides a quick reference.
