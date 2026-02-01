# Track Specification: Context Hygiene & Memory Safety

## Summary
Improve context hygiene by defining a minimal, repeatable context bundle and guardrails for memory or context growth across tools. Provide tooling to audit and report context size and contents.

## Goals
- Define a canonical context bundle for Conductor projects.
- Add tooling to report context size and highlight oversized files.
- Document safe memory handling guidelines for multi-tool environments.

## Non-Goals
- Automatic deletion of user data or files.
- Tool-specific memory behavior changes without opt-in.

## Acceptance Criteria
- A documented context bundle and inclusion/exclusion rules exist.
- A script can report context size and key files.
- Documentation includes guidance for safe memory updates.
