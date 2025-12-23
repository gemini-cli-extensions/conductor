# Revert Protocol

Git-aware rollback of tracks, phases, or tasks.

## Pre-Check

Verify `conductor/tracks.md` exists and is not empty.
If missing, halt and instruct: "Run setup first."

## Phase 1: Target Selection

### 1.1 Check for User Input

If target provided (e.g., "revert track <track_id>"), use **Path A**.
Otherwise, use **Path B**.

### Path A: Direct Confirmation

1. Find the referenced track/phase/task in tracks.md or plan.md
2. Ask: "You asked to revert [Track/Phase/Task]: '[Description]'. Is this correct?"
   - A) Yes
   - B) No
3. If yes, proceed to Phase 2
4. If no, ask clarifying questions

### Path B: Guided Selection Menu

1. **Scan All Plans**:
   - Read `conductor/tracks.md`
   - Read all `conductor/tracks/*/plan.md`

2. **Find Candidates**:
   - First: All in-progress items `[~]`
   - Fallback: 5 most recently completed items `[x]`

3. **Present Hierarchical Menu**:

For in-progress items:
```
I found multiple in-progress items. Please choose which one to revert:

Track: track_20251208_user_profile
  1) [Phase] Implement Backend API
  2) [Task] Update user model

3) A different Track, Task, or Phase.
```

For completed items:
```
No items are in progress. Please choose a recently completed item to revert:

Track: track_20251208_user_profile
  1) [Phase] Foundational Setup
  2) [Task] Initialize React application

Track: track_20251208_auth_ui
  3) [Task] Create login form

4) A different Track, Task, or Phase.
```

4. **Process Choice**:
   - If numbered selection matches, set as target and proceed
   - If "different", ask clarifying questions, then use Path A

5. If no completed items found, announce and halt.

## Phase 2: Git Reconciliation

### 2.1 Find Implementation Commits

- Get SHA(s) for all tasks/phases in target's plan.md
- **Handle Rewritten History**: If SHA not found in git log, search for similar commit message, ask user to confirm

### 2.2 Find Plan-Update Commits

For each implementation commit, find the corresponding plan-update commit that modified plan.md.

### 2.3 Find Track Creation Commit (Track Revert Only)

If reverting entire track:
```bash
git log -- conductor/tracks.md
```
Find commit that added the `## [ ] Track: <Description>` line.

### 2.4 Compile Final List

All SHAs to revert, checking for:
- Merge commits (warn user)
- Cherry-pick duplicates (warn user)

## Phase 3: Execution Plan Confirmation

### 3.1 Summarize

```
I have analyzed your request. Here is the plan:

- Target: Revert Task '[Task Description]'
- Commits to Revert: 2
  - <sha_code> ('feat: Add user profile')
  - <sha_plan> ('conductor(plan): Mark task complete')
- Action: I will run `git revert` on these commits in reverse order.
```

### 3.2 Final Confirmation

> "Do you want to proceed? (yes/no)"
- A) Yes
- B) No

If no, ask for correct plan.

## Phase 4: Execution

### 4.1 Execute Reverts

```bash
git revert --no-edit <sha>
```

Start from most recent, work backward.

### 4.2 Handle Conflicts

If merge conflict:
1. Halt immediately
2. Provide clear instructions for manual resolution
3. List conflicting files
4. Suggest resolution steps

### 4.3 Verify Plan State

Read plan.md again to ensure reverted items show correct status.
If not correct, edit and commit the fix.

### 4.4 Announce Completion

> "Revert complete. The plan has been synchronized with the git history."
