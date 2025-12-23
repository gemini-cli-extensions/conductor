# Setup Protocol

Initialize Conductor in a new or existing project.

## Pre-Setup Check

1. Check for `conductor/setup_state.json`:
   - If exists, read and resume from `last_successful_step`
   - If not, start fresh

## Resume States

| State | Action |
|-------|--------|
| `2.1_product_guide` | Skip to Product Guidelines (2.2) |
| `2.2_product_guidelines` | Skip to Tech Stack (2.3) |
| `2.3_tech_stack` | Skip to Code Styleguides (2.4) |
| `2.4_code_styleguides` | Skip to Workflow (2.5) |
| `2.5_workflow` | Skip to Initial Track (3.0) |
| `3.3_initial_track_generated` | Setup complete, suggest `/implement` |

## Phase 1: Project Setup

### 1.1 Detect Project Type

**Brownfield (Existing)** indicators:
- `.git`, `.svn`, or `.hg` directory exists
- `git status --porcelain` shows changes
- Dependency files: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`
- Source directories: `src/`, `app/`, `lib/`

**Greenfield (New)**: None of above, directory empty or only has README.md

### 1.2 For Brownfield Projects

1. Request permission for read-only scan
2. Respect `.gitignore` and `.geminiignore`
3. Analyze README, manifest files, directory structure
4. Extract: Language, Frameworks, Database, Architecture
5. Infer project goal from README/package.json

### 1.3 For Greenfield Projects

1. Initialize git if needed: `git init`
2. Ask: "What do you want to build?"
3. Create `conductor/` directory
4. Initialize `conductor/setup_state.json`: `{"last_successful_step": ""}`
5. Write response to `conductor/product.md` under `# Initial Concept`

### 2.1 Generate Product Guide

**Interactive Q&A** (max 5 questions):
- Target users, goals, features
- Provide 3 suggested answers per question
- Last options always: "Type your own" and "Autogenerate"

**Question Format**:
```
A) [Option A]
B) [Option B]  
C) [Option C]
D) Type your own answer
E) Autogenerate and review product.md
```

**After approval**: Write to `conductor/product.md`, update state to `2.1_product_guide`

### 2.2 Generate Product Guidelines

Similar interactive process for UX/brand guidelines.
Write to `conductor/product-guidelines.md`, update state to `2.2_product_guidelines`

### 2.3 Generate Tech Stack

For brownfield: State inferred stack, ask for confirmation only.
For greenfield: Interactive Q&A about languages, frameworks, databases.
Write to `conductor/tech-stack.md`, update state to `2.3_tech_stack`

### 2.4 Select Code Styleguides

1. List available guides from skill's `assets/code_styleguides/`
2. Recommend based on tech stack
3. Copy selected guides to `conductor/code_styleguides/`
4. Update state to `2.4_code_styleguides`

### 2.5 Select Workflow

1. Copy `references/workflow-template.md` to `conductor/workflow.md`
2. Ask to customize:
   - Test coverage threshold (default 80%)
   - Commit frequency (per task vs per phase)
   - Git notes vs commit message for summaries
3. Update state to `2.5_workflow`

## Phase 2: Initial Track Generation

### 3.1 Generate Requirements (Greenfield only)

Interactive Q&A about user stories, functional/non-functional requirements.

### 3.2 Propose Initial Track

- Greenfield: Usually an MVP track
- Brownfield: Maintenance or enhancement track

Ask user to confirm the track description.

### 3.3 Create Track Artifacts

1. Create `conductor/tracks.md` with header
2. Generate Track ID: `shortname_YYYYMMDD`
3. Create `conductor/tracks/<track_id>/`
4. Create files:
   - `metadata.json` (track_id, type, status, timestamps, description)
   - `spec.md` (detailed requirements)
   - `plan.md` (phased tasks with checkboxes)

**CRITICAL for plan.md**:
- Follow TDD structure from workflow.md
- Add phase completion meta-tasks: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>'`

5. Update state to `3.3_initial_track_generated`

### 3.4 Finalize

1. Commit all files: `conductor(setup): Add conductor setup files`
2. Announce completion
3. Suggest running implement command
