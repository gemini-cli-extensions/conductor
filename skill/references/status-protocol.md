# Status Protocol

Display the current progress of all project tracks.

## Pre-Check

Verify these files exist in `conductor/`:
- `tech-stack.md`
- `workflow.md`
- `product.md`
- `tracks.md` (must exist and not be empty)

If missing, halt and instruct: "Run setup first."

## Phase 1: Read Project Plan

### 1.1 Read Main Tracks File

Read `conductor/tracks.md`

### 1.2 Read Individual Plans

```bash
ls conductor/tracks
```

For each track, read `conductor/tracks/<track_id>/plan.md`

## Phase 2: Parse and Summarize

### 2.1 Parse Content

Identify:
- Major phases (top-level headings)
- Individual tasks and their status:
  - `[ ]` = PENDING
  - `[~]` = IN PROGRESS
  - `[x]` = COMPLETED

### 2.2 Calculate Metrics

- Total phases
- Total tasks
- Tasks completed
- Tasks in progress
- Tasks pending
- Percentage complete

## Phase 3: Present Status

### Output Format

```
===========================================
PROJECT STATUS REPORT
===========================================

Date/Time: [Current timestamp]

PROJECT STATUS: [On Track | Behind | Blocked]

-------------------------------------------
CURRENT WORK
-------------------------------------------
Phase:    [Current phase name]
Task:     [Current in-progress task]

-------------------------------------------
NEXT ACTION
-------------------------------------------
[Next pending task description]

-------------------------------------------
BLOCKERS
-------------------------------------------
[Any items marked as blocked, or "None"]

-------------------------------------------
SUMMARY
-------------------------------------------
Phases:   [X] total
Tasks:    [Y] total
Progress: [completed]/[total] ([percentage]%)

[Visual progress bar if helpful]
===========================================
```

### Status Determination

- **On Track**: Has in-progress work, no blockers
- **Behind**: No in-progress work but pending tasks exist
- **Blocked**: Explicit blockers found
- **Complete**: All tasks marked `[x]`
