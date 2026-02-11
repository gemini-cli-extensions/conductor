---
description: Git-aware revert of tracks, phases, or tasks
argument-hint: [track|phase|task]
---

# Conductor Revert

Revert Conductor work: $ARGUMENTS

## 1. Check Setup

If `conductor/tracks.md` doesn't exist, tell user to run `/conductor-setup` first.

## 2. Identify Target

**If `$ARGUMENTS` provided:**
- Parse to identify track, phase, or task name
- Find it in `conductor/tracks.md` or relevant `plan.md`

**If no arguments:**
Show menu of recent revertible items:

```
## What would you like to revert?

### In Progress Items
1. [~] Task: "Add user authentication" (track: auth_20241215)
2. [~] Phase: "Backend API" (track: auth_20241215)

### Recently Completed
3. [x] Task: "Create login form" (abc1234)
4. [x] Task: "Add validation" (def5678)

Enter number or describe what to revert:
```

Prioritize showing in-progress items first, then recently completed.

## 3. Find Associated Commits

For the selected item:

1. Read the relevant `plan.md` file
2. Extract commit SHAs from completed tasks (the 7-char hash after `[x]`)
3. Find implementation commits
4. Find corresponding plan-update commits

**For track revert:** Also find the commit that added the track to `tracks.md`

## 4. Present Revert Plan

```
## Revert Plan

**Target:** [Task/Phase/Track] - "[Description]"

**Commits to revert (newest first):**
1. def5678 - conductor(plan): Mark task complete
2. abc1234 - feat(auth): Add login form

**Action:** Will run `git revert --no-edit` on each commit

Proceed? (yes/no)
```

Wait for explicit user confirmation.

## 5. Execute Revert

For each commit, newest to oldest:
```bash
git revert --no-edit <sha>
```

**If conflicts occur:**
1. Stop and inform user
2. Show conflicting files
3. Guide through manual resolution or abort

## 6. Update Plan State

After successful revert:
- Change `[x]` back to `[ ]` for reverted tasks
- Change `[~]` back to `[ ]` if reverting in-progress items
- Remove commit SHAs from reverted task lines

## 7. Announce Completion

"Reverted [target]. Plan updated. Status markers reset to pending."
