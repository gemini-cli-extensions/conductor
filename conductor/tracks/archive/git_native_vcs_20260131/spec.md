# Track Specification: Git-Native Workflow & Multi-VCS Support

## Summary
Define optional, Git-native workflows (branch-per-track, worktrees) while preserving compatibility with non-Git or alternative VCS setups. Provide tooling that is opt-in, non-destructive, and cross-platform.

## Goals
- Optional Git integration with branch/worktree helpers per track.
- Metadata updates that capture branch/worktree association when enabled.
- Clear fallback when Git is unavailable or disabled.

## Non-Goals
- Enforcing Git usage for all users.
- Performing destructive Git operations without explicit opt-in.

## Acceptance Criteria
- Configurable Git integration (config file or env var) with safe defaults.
- New-track workflow can optionally create a branch or worktree and record it.
- Docs describe Git and non-Git usage patterns.
