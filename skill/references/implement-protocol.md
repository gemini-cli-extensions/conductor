# Implement Protocol

Execute tasks from a track's plan following the TDD workflow.

## Pre-Check

Verify these files exist in `conductor/`:
- `tech-stack.md`
- `workflow.md`
- `product.md`

If missing, halt and instruct: "Run setup first."

## Phase 1: Track Selection

### 1.1 Check User Input

If track name provided as argument, use it.

### 1.2 Parse tracks.md

Read `conductor/tracks.md`, split by `---` separator.
Extract: status (`[ ]`, `[~]`, `[x]`), description, link.

If empty or malformed, halt with error.

### 1.3 Select Track

**If track name provided**:
- Case-insensitive match against descriptions
- If found, confirm: "I found track '<description>'. Is this correct?"
- If not found, suggest next available

**If no track name**:
- Find first track NOT marked `[x]`
- Announce: "Automatically selecting: '<description>'"

If no incomplete tracks, announce all complete and halt.

## Phase 2: Track Implementation

### 2.1 Update Status

Change track in `conductor/tracks.md` from `[ ]` to `[~]`

### 2.2 Load Context

Read into context:
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/spec.md`
- `conductor/workflow.md`

### 2.3 Execute Tasks

For each task in plan.md, follow the **Task Workflow** from workflow.md:

#### Standard Task Lifecycle

1. **Select Task**: Next `[ ]` in sequential order
2. **Mark In Progress**: Change `[ ]` to `[~]` in plan.md
3. **Write Failing Tests (Red)**: Create tests, confirm they fail
4. **Implement (Green)**: Write minimum code to pass tests
5. **Refactor**: Improve code while keeping tests green
6. **Verify Coverage**: Run coverage reports, target >80%
7. **Document Deviations**: Update tech-stack.md if needed
8. **Commit Code**: `feat(scope): description`
9. **Attach Git Note**: 
   ```bash
   git notes add -m "<task summary>" <commit_hash>
   ```
10. **Update Plan**: Change `[~]` to `[x]`, append commit SHA (7 chars)
11. **Commit Plan Update**: `conductor(plan): Mark task 'X' as complete`

#### Phase Completion Protocol

When a task completes a phase:

1. **Announce**: Phase complete, starting verification
2. **Ensure Test Coverage**:
   - Find previous checkpoint SHA from plan.md
   - `git diff --name-only <previous_sha> HEAD`
   - Verify/create tests for each code file
3. **Run Tests**: Announce command, execute, debug if needed (max 2 attempts)
4. **Manual Verification Plan**: Present step-by-step instructions for user
5. **Await User Confirmation**: Must receive explicit "yes"
6. **Create Checkpoint Commit**: `conductor(checkpoint): End of Phase X`
7. **Attach Verification Report**: Via git notes
8. **Update Plan**: Add `[checkpoint: <sha>]` to phase heading
9. **Commit Plan Update**: `conductor(plan): Mark phase 'X' as complete`

### 2.4 Finalize Track

After all tasks complete:
- Update `conductor/tracks.md`: Change `[~]` to `[x]`
- Announce track completion

## Phase 3: Documentation Sync

**Only when track reaches `[x]` status.**

### 3.1 Load Files

- `conductor/tracks/<track_id>/spec.md`
- `conductor/product.md`
- `conductor/product-guidelines.md`
- `conductor/tech-stack.md`

### 3.2 Analyze and Update

For each file, if changes needed:
1. Generate proposed changes (diff format)
2. Present to user for confirmation
3. Only apply after explicit approval

**product-guidelines.md**: Extra caution, only for branding/strategic changes.

### 3.3 Report

Summarize which files were updated (or not).

## Phase 4: Track Cleanup

Offer user options:

```
A) Archive: Move to conductor/archive/, remove from tracks.md
B) Delete: Permanently delete (requires confirmation)
C) Skip: Leave in tracks.md
```

### Archive Steps
1. Create `conductor/archive/` if needed
2. Move `conductor/tracks/<track_id>` to `conductor/archive/<track_id>`
3. Remove section from tracks.md

### Delete Steps
1. Confirm: "This cannot be undone. Are you sure?"
2. If yes: Delete folder, remove from tracks.md
