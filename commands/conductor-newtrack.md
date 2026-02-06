---
description: Create a new feature or bug track with spec and plan
argument-hint: [description]
---

# Conductor New Track

Create a new track for: $ARGUMENTS

## 1. Verify Setup

Check these files exist:
- `conductor/product.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`

If missing, tell user to run `/conductor-setup` first.

## 2. Get Track Description

- If `$ARGUMENTS` provided, use it
- Otherwise ask: "Describe the feature or bug fix you want to implement"

## 3. Generate Spec (Interactive)

Ask 3-5 clarifying questions based on track type:

**Feature**: What does it do? Who uses it? What's the UI? What data is involved?
**Bug**: Steps to reproduce? Expected vs actual behavior? When did it start?

Generate `spec.md` with:
- Overview
- Functional Requirements
- Acceptance Criteria
- Out of Scope

Present for approval, revise if needed.

## 4. Generate Plan

Read `conductor/workflow.md` for task structure (TDD, commit strategy).

Generate `plan.md` with phases, tasks, subtasks:
```markdown
# Implementation Plan

## Phase 1: [Name]
- [ ] Task: [Description]
  - [ ] Write tests
  - [ ] Implement
- [ ] Task: Conductor - Phase Verification

## Phase 2: [Name]
...
```

Present for approval, revise if needed.

## 5. Create Track Artifacts

1. Generate track ID: `shortname_YYYYMMDD` (use today's date)
2. Create directory: `conductor/tracks/<track_id>/`
3. Write files:
   - `metadata.json`: `{"track_id": "...", "type": "feature|bug", "status": "new", "created_at": "...", "description": "..."}`
   - `spec.md`
   - `plan.md`

## 6. Update Tracks File

Append to `conductor/tracks.md`:
```markdown

---

## [ ] Track: [Description]
*Link: [conductor/tracks/<track_id>/](conductor/tracks/<track_id>/)*
```

## 7. Announce

"Track `<track_id>` created. Run `/conductor-implement` to start working on it."
