# Track Specification: Release Guidance & Packaging

## Summary
Document the release packaging flow and clarify that releases should be published on GitHub Releases. Keep Python/PowerShell tooling as the primary path and note that an optional Node wrapper is future work.

## Goals
- Provide a release guide that aligns with existing GitHub workflows.
- Clarify artifact packaging and validation steps.
- Avoid migrating core tooling to npx; optional wrapper remains future work.

## Non-Goals
- Changing release automation workflows.
- Introducing a new Node-based installer CLI.

## Acceptance Criteria
- A release guide exists with GitHub Releases flow and validation steps.
- README references the release guide.
