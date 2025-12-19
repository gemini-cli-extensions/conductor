---
description: Execute tasks from a track's implementation plan
argument-hint: [track_id]
---

# Conductor Implement

Implement track: $ARGUMENTS

## 1. Verify Setup

Check these files exist:
- `conductor/product.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`

If missing, tell user to run `/conductor-setup` first.

## 2. Select Track

- If `$ARGUMENTS` provided (track_id), find that track in `conductor/tracks.md`
- Otherwise, find first incomplete track (`[ ]` or `[~]`) in `conductor/tracks.md`
- If no tracks found, suggest `/conductor-newtrack`

## 3. Load Context

Read into context:
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- `conductor/workflow.md`

## 4. Update Track Status

In `conductor/tracks.md`, change `## [ ] Track:` to `## [~] Track:` for selected track.

## 5. Execute Tasks

For each incomplete task in plan.md:

### 5.1 Mark In Progress
Change `[ ]` to `[~]` in plan.md

### 5.2 TDD Workflow (if workflow.md specifies)
1. Write failing tests for the task
2. Run tests, confirm they fail
3. Implement minimum code to make tests pass
4. Run tests, confirm they pass
5. Refactor if needed (keep tests passing)

### 5.3 Commit Changes
```bash
git add .
git commit -m "feat(<scope>): <description>"
```

### 5.4 Update Plan
- Change `[~]` to `[x]` for completed task
- Append first 7 chars of commit SHA

### 5.5 Commit Plan Update
```bash
git add conductor/
git commit -m "conductor(plan): Mark task '<task name>' complete"
```

## 6. Phase Verification

At end of each phase:
1. Run full test suite
2. Present manual verification steps to user
3. Ask for explicit confirmation: "Does this work as expected?"
4. Create checkpoint commit: `conductor(checkpoint): Phase <name> complete`

## 7. Track Completion

When all tasks done:
1. Update `conductor/tracks.md`: change `## [~]` to `## [x]`
2. Ask user: "Track complete. Archive, Delete, or Keep the track folder?"
3. Announce completion

## Status Markers Reference

- `[ ]` - Pending
- `[~]` - In Progress
- `[x]` - Completed
