# Track Specification: Artifact Drift Prevention & CI Sync

## Summary
Prevent drift between manifests, templates, and generated artifacts (skills, workflows, VSIX, Copilot rules) through automated validation and CI checks.

## Goals
- Single validation command that checks every supported tool.
- CI workflow that fails on drift.
- Clear troubleshooting guidance when validation fails.

## Non-Goals
- Changing adapter runtime behavior.
- Replacing existing sync scripts without parity.

## Acceptance Criteria
- Validation fails when artifacts are missing or out of date.
- CI runs validation on pull requests.
- Docs include canonical sync and validate commands.
