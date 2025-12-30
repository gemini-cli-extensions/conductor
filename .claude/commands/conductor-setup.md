---
description: Initialize project with Conductor context-driven development
---

# Conductor Setup

Initialize this project with context-driven development. Follow this workflow:

## 1. Check Existing Setup

- If `conductor/setup_state.json` exists with `"last_successful_step": "complete"`, inform user setup is done
- If partial state, offer to resume or restart

## 2. Detect Project Type

**Brownfield** (existing project): Has `.git`, `package.json`, `requirements.txt`, `go.mod`, or `src/`
**Greenfield** (new project): Empty or only README.md

## 3. For Brownfield Projects

1. Announce: "Existing project detected"
2. Analyze: README.md, package.json/requirements.txt/go.mod, directory structure
3. Infer: tech stack, architecture, project goals
4. Present findings for confirmation

## 4. For Greenfield Projects

1. Ask: "What do you want to build?"
2. Initialize git if needed: `git init`

## 5. Create Conductor Directory

```bash
mkdir -p conductor/code_styleguides
```

## 6. Generate Context Files (Interactive)

For each file, ask 2-3 targeted questions, then generate:

- **product.md** - Product vision, users, goals, features
- **tech-stack.md** - Languages, frameworks, databases, tools
- **workflow.md** - Use the default TDD workflow from `templates/workflow.md`

Copy relevant code styleguides from `templates/code_styleguides/` based on tech stack.

## 7. Initialize Tracks File

Create `conductor/tracks.md`:
```markdown
# Project Tracks

This file tracks all major work items. Each track has its own spec and plan.

---
```

## 8. Generate Initial Track

1. Based on project context, propose an initial track (MVP for greenfield, first feature for brownfield)
2. On approval, create track using the newtrack workflow

## 9. Finalize

1. Write `conductor/setup_state.json`: `{"last_successful_step": "complete"}`
2. Commit: `git add conductor && git commit -m "conductor(setup): Initialize conductor"`
3. Announce: "Setup complete. Run `/conductor-implement` to start."
