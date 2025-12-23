# Conductor Commands Quick Reference

## Overview

Conductor provides five main operations for managing software development tracks.

## Commands

### Setup

**Purpose**: Initialize Conductor in a new or existing project

**When to use**:
- Starting a new project
- Adding Conductor to existing codebase
- Resuming interrupted setup

**What it does**:
1. Detects project type (greenfield/brownfield)
2. Creates `conductor/` directory structure
3. Guides through product definition
4. Sets up tech stack documentation
5. Configures code styleguides
6. Establishes workflow rules
7. Creates initial track

**Files created**:
- `conductor/product.md`
- `conductor/product-guidelines.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`
- `conductor/tracks.md`
- `conductor/code_styleguides/*.md`
- `conductor/tracks/<initial_track>/`

---

### New Track

**Purpose**: Create a new feature or bug fix track

**When to use**:
- Starting new feature development
- Documenting a bug to fix
- Planning a refactoring effort

**What it does**:
1. Gathers requirements through Q&A
2. Generates detailed specification (spec.md)
3. Creates phased implementation plan (plan.md)
4. Adds track to master tracks list

**Files created**:
- `conductor/tracks/<track_id>/metadata.json`
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- Updates `conductor/tracks.md`

---

### Implement

**Purpose**: Execute tasks from a track's plan

**When to use**:
- Ready to start coding
- Continuing work on a track
- After creating a new track

**What it does**:
1. Selects track (auto or specified)
2. Follows TDD workflow per task
3. Commits with proper messages
4. Attaches git notes for traceability
5. Runs phase verification checkpoints
6. Updates documentation on completion

**Workflow per task**:
1. Mark in progress `[~]`
2. Write failing tests (Red)
3. Implement to pass (Green)
4. Refactor
5. Verify coverage
6. Commit code
7. Attach git note
8. Mark complete `[x]` with SHA

---

### Status

**Purpose**: View progress overview

**When to use**:
- Checking project state
- Planning next work session
- Reporting progress

**What it shows**:
- Current date/time
- Overall project status
- Current phase and task
- Next pending action
- Any blockers
- Progress statistics (tasks completed/total)

---

### Revert

**Purpose**: Git-aware rollback of work

**When to use**:
- Need to undo a task
- Rolling back a phase
- Reverting entire track

**What it does**:
1. Identifies target (interactive or specified)
2. Finds all related commits in git history
3. Handles rewritten history (rebases)
4. Presents execution plan for approval
5. Executes git revert commands
6. Synchronizes plan.md state

**Revert targets**:
- Single task
- Entire phase
- Complete track

---

## Status Markers

| Marker | Meaning |
|--------|---------|
| `[ ]` | Pending |
| `[~]` | In Progress |
| `[x]` | Completed |

## Track ID Format

```
shortname_YYYYMMDD
```

Example: `user_auth_20251223`

## Commit Message Prefixes

| Prefix | Use |
|--------|-----|
| `feat(scope):` | New feature code |
| `fix(scope):` | Bug fix code |
| `test(scope):` | Test additions |
| `conductor(plan):` | Plan updates |
| `conductor(setup):` | Setup files |
| `conductor(checkpoint):` | Phase checkpoints |
