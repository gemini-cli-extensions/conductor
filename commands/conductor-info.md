---
name: conductor
description: Context-driven development methodology. Understands projects set up with Conductor (via Gemini CLI or Claude Code). Use when working with conductor/ directories, tracks, specs, plans, or when user mentions context-driven development.
license: Apache-2.0
compatibility: Works with Claude Code, Gemini CLI, and any Agent Skills compatible CLI
metadata:
  version: "0.1.0"
  author: "Gemini CLI Extensions"
  repository: "https://github.com/gemini-cli-extensions/conductor"
  keywords:
    - context-driven-development
    - specs
    - plans
    - tracks
    - tdd
    - workflow
---

# Conductor: Context-Driven Development

Measure twice, code once.

## Overview

Conductor enables context-driven development by:
1. Establishing project context (product vision, tech stack, workflow)
2. Organizing work into "tracks" (features, bugs, improvements)
3. Creating specs and phased implementation plans
4. Executing with TDD practices and progress tracking

**Interoperability:** This skill understands conductor projects created by either:
- Gemini CLI extension (`/conductor:setup`, `/conductor:newTrack`, etc.)
- Claude Code commands (`/conductor-setup`, `/conductor-newtrack`, etc.)

Both tools use the same `conductor/` directory structure.

## When to Use This Skill

Automatically engage when:
- Project has a `conductor/` directory
- User mentions specs, plans, tracks, or context-driven development
- User asks about project status or implementation progress
- Files like `conductor/tracks.md`, `conductor/product.md` exist
- User wants to organize development work

## Slash Commands

Users can invoke these commands directly:

| Command | Description |
|---------|-------------|
| `/conductor-setup` | Initialize project with product.md, tech-stack.md, workflow.md |
| `/conductor-newtrack [desc]` | Create new feature/bug track with spec and plan |
| `/conductor-implement [id]` | Execute tasks from track's plan |
| `/conductor-status` | Display progress overview |
| `/conductor-revert` | Git-aware revert of work |

## Conductor Directory Structure

When you see this structure, the project uses Conductor:

```
conductor/
â”œâ”€â”€ product.md              # Product vision, users, goals
â”œâ”€â”€ product-guidelines.md   # Brand/style guidelines (optional)
â”œâ”€â”€ tech-stack.md           # Technology choices
â”œâ”€â”€ workflow.md             # Development standards (TDD, commits, coverage)
â”œâ”€â”€ tracks.md               # Master track list with status markers
â”œâ”€â”€ setup_state.json        # Setup progress tracking
â”œâ”€â”€ code_styleguides/       # Language-specific style guides
â””â”€â”€ tracks/
    â””â”€â”€ <track_id>/         # Format: shortname_YYYYMMDD
        â”œâ”€â”€ metadata.json   # Track type, status, dates
        â”œâ”€â”€ spec.md         # Requirements and acceptance criteria
        â””â”€â”€ plan.md         # Phased task list with status
```

## Status Markers

Throughout conductor files:
- `[ ]` - Pending/New
- `[~]` - In Progress
- `[x]` - Completed (often followed by 7-char commit SHA)

## Reading Conductor Context

When working in a Conductor project:

1. **Read `conductor/product.md`** - Understand what we're building and for whom
2. **Read `conductor/tech-stack.md`** - Know the technologies and constraints
3. **Read `conductor/workflow.md`** - Follow the development methodology (usually TDD)
4. **Read `conductor/tracks.md`** - See all work items and their status
5. **For active work:** Read the current track's `spec.md` and `plan.md`

## Workflow Integration

When implementing tasks, follow `conductor/workflow.md` which typically specifies:

1. **TDD Cycle:** Write failing test â†’ Implement â†’ Pass â†’ Refactor
2. **Coverage Target:** Usually >80%
3. **Commit Strategy:** Conventional commits (`feat:`, `fix:`, `test:`, etc.)
4. **Task Updates:** Mark `[~]` when starting, `[x]` when done + commit SHA
5. **Phase Verification:** Manual user confirmation at phase end

## Gemini CLI Compatibility

Projects set up with Gemini CLI's Conductor extension use identical structure.
The only differences are command syntax:

| Gemini CLI | Claude Code |
|------------|-------------|
| `/conductor:setup` | `/conductor-setup` |
| `/conductor:newTrack` | `/conductor-newtrack` |
| `/conductor:implement` | `/conductor-implement` |
| `/conductor:status` | `/conductor-status` |
| `/conductor:revert` | `/conductor-revert` |

Files, workflows, and state management are fully compatible.

## Example: Recognizing Conductor Projects

When you see `conductor/tracks.md` with content like:

```markdown
## [~] Track: Add user authentication
*Link: [conductor/tracks/auth_20241215/](conductor/tracks/auth_20241215/)*
```

You know:
- This is a Conductor project
- There's an in-progress track for authentication
- Spec and plan are in `conductor/tracks/auth_20241215/`
- Follow the workflow in `conductor/workflow.md`

## References

For detailed workflow documentation, see [references/workflows.md](references/workflows.md).