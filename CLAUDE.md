# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Conductor is a **Gemini CLI extension** that enables Context-Driven Development. It transforms Gemini CLI into a project manager that follows a strict protocol: **Context → Spec & Plan → Implement**.

The extension is defined in `gemini-extension.json` and provides slash commands through TOML files in `commands/conductor/`.

## Architecture

### Extension Structure
- `gemini-extension.json` - Extension manifest (name, version, context file)
- `GEMINI.md` - Context file loaded by Gemini CLI when extension is active
- `commands/conductor/*.toml` - Slash command definitions containing prompts

### Commands (in `commands/conductor/`)
| Command | File | Purpose |
|---------|------|---------|
| `/conductor:setup` | `setup.toml` | Initialize project with product.md, tech-stack.md, workflow.md, and first track |
| `/conductor:newTrack` | `newTrack.toml` | Create new feature/bug track with spec.md and plan.md |
| `/conductor:implement` | `implement.toml` | Execute tasks from current track's plan following TDD workflow |
| `/conductor:status` | `status.toml` | Display progress overview from tracks.md |
| `/conductor:revert` | `revert.toml` | Git-aware revert of tracks, phases, or tasks |

### Generated Artifacts (in user projects)
When users run Conductor, it creates:
```
conductor/
├── product.md           # Product vision and goals
├── product-guidelines.md # Brand/style guidelines
├── tech-stack.md        # Technology choices
├── workflow.md          # Development workflow (TDD, commits)
├── tracks.md            # Master track list with status
├── setup_state.json     # Resume state for setup
├── code_styleguides/    # Language-specific style guides
└── tracks/
    └── <track_id>/
        ├── metadata.json
        ├── spec.md      # Requirements
        └── plan.md      # Phased task list
```

### Templates (in `templates/`)
- `workflow.md` - Default workflow template (TDD, >80% coverage, git notes)
- `code_styleguides/*.md` - Style guides for Python, TypeScript, JavaScript, Go, HTML/CSS

## Key Concepts

### Tracks
A track is a logical unit of work (feature or bug fix). Each track has:
- Unique ID format: `shortname_YYYYMMDD`
- Status markers: `[ ]` new, `[~]` in progress, `[x]` completed
- Own directory with spec, plan, and metadata

### Task Workflow (TDD)
1. Select task from plan.md
2. Mark `[~]` in progress
3. Write failing tests (Red)
4. Implement to pass (Green)
5. Refactor
6. Verify >80% coverage
7. Commit with message format: `<type>(<scope>): <description>`
8. Attach summary via `git notes`
9. Update plan.md with commit SHA

### Phase Checkpoints
At phase completion:
- Run test suite
- Manual verification with user
- Create checkpoint commit
- Attach verification report via git notes

## Claude Code Implementation

A Claude Code implementation is available in `.claude/`:

### Slash Commands (User-Invoked)
```
/conductor-setup              # Initialize project
/conductor-newtrack [desc]    # Create feature/bug track
/conductor-implement [id]     # Execute track tasks
/conductor-status             # Show progress
/conductor-revert             # Git-aware revert
```

### Skill (Model-Invoked)
The skill in `.claude/skills/conductor/` automatically activates when Claude detects a `conductor/` directory or related context.

### Installation
Copy `.claude/` to any project to enable Conductor commands, or copy commands to `~/.claude/commands/` for global access.

### Interoperability
Both Gemini CLI and Claude Code implementations use the same `conductor/` directory structure. Projects set up with either tool work with both.

## Development Notes

- Commands are pure TOML files with embedded prompts - no build step required
- The extension relies on Gemini CLI's tool calling capabilities
- State is tracked in JSON files (setup_state.json, metadata.json)
- Git notes are used extensively for audit trails
- Commands always validate setup before executing
