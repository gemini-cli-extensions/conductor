# Track Specification: Setup/NewTrack UX Consistency

## Summary
Unify setup and newTrack UX across adapters (Gemini, Qwen, Claude, Codex, VS Code) so output structure, metadata, and guidance are consistent and predictable.

## Goals
- Standardize setup/newTrack prompts and outputs.
- Ensure metadata and directory layouts are identical across tools.
- Provide clear error messages and next-step guidance.

## Non-Goals
- Changing core Conductor directory structure.
- Adding new commands outside setup/newTrack.

## Acceptance Criteria
- Setup/newTrack produce identical structures across tools.
- Errors are actionable and reference the correct file or command.
- Documentation includes consistent examples for each tool.
