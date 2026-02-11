# Git Usage Audit

## Core Code
- `conductor-core/src/conductor_core/git_service.py`
  - Uses GitPython `Repo` to support: `is_dirty`, `add`, `commit`, `notes add`, `log`, `checkout`, `merge`.
  - No branch/worktree helpers beyond checkout/merge.
- `conductor-core/src/conductor_core/task_runner.py`
  - Instantiates `GitService` by default for the project root.
  - No direct git operations beyond creating the service.

## Prompt Templates
- `conductor-core/src/conductor_core/templates/setup.j2`
  - Detects `.git`/`.svn`/`.hg` and checks `git status --porcelain` for brownfield detection.
  - Uses `git ls-files --exclude-standard -co` when `.git` is present.
  - Initializes `git init` if `.git` missing.
- `conductor-core/src/conductor_core/templates/revert.j2`
  - References `git log`, `git show --name-only`, and `git revert --no-edit` in the workflow.

## Scripts
- `scripts/smoke_test.py`
  - Initializes a temporary git repo for smoke testing.

## Gaps vs Track Goals
- No explicit branch-per-track or worktree support.
- No VCS metadata stored in track metadata.
- Git operations are not gated by opt-in configuration.
