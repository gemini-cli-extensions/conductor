# ADR 0001: Monorepo Architecture for Multi-Platform Support

## Status
Accepted

## Context
Conductor was originally a single-package Gemini CLI extension. To support multiple platforms (VS Code, Qwen, Claude) while maintaining a consistent development protocol, we need a way to share logic and prompts.

## Decision
We adopt a monorepo structure with a central core library:
1. `conductor-core`: Platform-agnostic logic and Jinja2-based prompt templates.
2. Platform Adapters (`conductor-gemini`, `conductor-vscode`): Thin wrappers that delegate to the core.
3. Automated Synchronization: Core templates are the source of truth and are synced to platform artifacts (TOML, MD).

## Consequences
- Pros: Consistent behavior across all tools, centralized prompt management, shared data models.
- Cons: Slightly more complex build process, requires multiple packages.
