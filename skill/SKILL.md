---
name: conductor
description: Use when the user wants to setup a new project, create a new feature, write a spec, plan a feature, fix a bug with a plan, start a new track, check project status, implement next task, or revert changes. Also use when user mentions "conductor", "track", or "spec-driven development". If conductor is not yet configured in the project, start with setup.
---

# Conductor

Conductor is a Context-Driven Development (CDD) framework that transforms AI agents into proactive project managers. The philosophy is "Measure twice, code once" - every feature follows a strict protocol: **Context -> Spec & Plan -> Implement**.

## Core Concepts

- **Track**: A unit of work (feature or bug fix) with its own spec and plan
- **Spec**: Detailed requirements document (`spec.md`)
- **Plan**: Phased task list with checkboxes (`plan.md`)
- **Workflow**: Rules for task lifecycle, TDD, commits, and quality gates

## Directory Structure

When initialized, Conductor creates this structure in the project:

```
conductor/
├── product.md              # Product vision and goals
├── product-guidelines.md   # UX/brand guidelines
├── tech-stack.md           # Technology choices
├── workflow.md             # Development workflow rules
├── tracks.md               # Master list of all tracks
├── code_styleguides/       # Language-specific style guides
├── tracks/                 # Active tracks
│   └── <track_id>/
│       ├── metadata.json
│       ├── spec.md
│       └── plan.md
└── archive/                # Completed tracks
```

## Available Commands

| Command | Purpose |
|---------|---------|
| **Setup** | Initialize Conductor in a project (new or existing) |
| **New Track** | Create a new feature/bug track with spec and plan |
| **Implement** | Execute tasks from a track's plan following TDD workflow |
| **Status** | Show progress overview of all tracks |
| **Revert** | Git-aware rollback of tracks, phases, or tasks |

## Protocol References

The detailed protocols are in TOML format. Read the `prompt` field from each file:

| Action | Protocol File |
|--------|---------------|
| Setup project | `commands/conductor/setup.toml` |
| Create new track | `commands/conductor/newTrack.toml` |
| Implement tasks | `commands/conductor/implement.toml` |
| Check status | `commands/conductor/status.toml` |
| Revert changes | `commands/conductor/revert.toml` |

**How to read**: Each `.toml` file has a `prompt` field containing the full protocol instructions.

## Task Status Markers

- `[ ]` - Pending
- `[~]` - In Progress
- `[x]` - Completed

## Key Workflow Principles

1. **The Plan is Source of Truth**: All work tracked in `plan.md`
2. **Test-Driven Development**: Write tests before implementing
3. **High Code Coverage**: Target >80% coverage
4. **Commit After Each Task**: With git notes for traceability
5. **Phase Checkpoints**: Manual verification at phase completion

## When to Use Each Protocol

- **"set up conductor" or "initialize project"** -> Read `commands/conductor/setup.toml`
- **"new feature", "new track", "plan a feature"** -> Read `commands/conductor/newTrack.toml`
- **"implement", "start working", "next task"** -> Read `commands/conductor/implement.toml`
- **"status", "progress", "where are we"** -> Read `commands/conductor/status.toml`
- **"revert", "undo", "rollback"** -> Read `commands/conductor/revert.toml`

## Assets

- **Code Styleguides**: `templates/code_styleguides/` (general, go, python, javascript, typescript, html-css)
- **Workflow Template**: `templates/workflow.md`

## Critical Rules

1. **Validate every tool call** - If any fails, halt and report to user
2. **Sequential questions** - Ask one question at a time, wait for response
3. **User confirmation required** - Before writing files or making changes
4. **Check setup first** - Verify `conductor/` exists before any operation
