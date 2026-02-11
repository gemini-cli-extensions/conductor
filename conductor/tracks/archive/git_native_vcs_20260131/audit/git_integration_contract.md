# Opt-in Git Integration Contract

## Goals
- Keep Git integration optional and safe by default.
- Support both branch-per-track and worktree-per-track workflows.
- Persist VCS context in track metadata for later actions (status/revert).

## Opt-in Mechanism
- Default: disabled.
- Enable via one of:
  - `conductor/workflow.md` setting (documented policy).
  - CLI flag on track creation (e.g., `--git` or `--worktree`).
- When disabled, no Git operations beyond existing prompts.

## Branch-per-Track Option
- Create a branch named `conductor/<track_id>` from the current HEAD (or configured base branch).
- Checkout the branch when starting the track (safe to noop if already on branch).
- Merge back is manual (no automatic merge in core).

## Worktree Option
- Create a worktree under `.conductor/worktrees/<track_id>`.
- Use base branch configured or current HEAD.
- Update metadata with worktree path and branch name.

## Metadata Fields (stored in track metadata.json)
```json
{
  "vcs": {
    "enabled": true,
    "provider": "git",
    "mode": "branch" | "worktree",
    "base_branch": "main",
    "branch": "conductor/<track_id>",
    "worktree_path": ".conductor/worktrees/<track_id>",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ"
  }
}
```

## Safety Constraints
- Never mutate branches/worktrees unless opt-in.
- Use `--dry-run` first in any helper that touches Git.
- Fail with clear messaging if Git is missing or repo is dirty.
