# New Track Protocol

Create a new feature or bug fix track with spec and plan.

## Pre-Check

Verify these files exist in `conductor/`:
- `tech-stack.md`
- `workflow.md`
- `product.md`

If missing, halt and instruct: "Run setup first."

## Phase 1: Track Initialization

### 1.1 Get Track Description

- If provided as argument, use it
- Otherwise ask: "Please provide a brief description of the track (feature, bug fix, chore, etc.)"

### 1.2 Infer Track Type

Analyze description to determine: Feature, Bug, Chore, Refactor
Do NOT ask user to classify.

## Phase 2: Interactive Spec Generation

### 2.1 Announce

> "I'll guide you through questions to build a comprehensive specification (`spec.md`) for this track."

### 2.2 Questioning Phase

**For Features** (3-5 questions):
- Clarify the feature request
- Implementation details
- User interactions
- Inputs/outputs
- Edge cases

**For Bugs/Chores** (2-3 questions):
- Reproduction steps (bugs)
- Specific scope
- Success criteria

**Question Guidelines**:
- Ask ONE question at a time
- Provide 2-3 suggested options (A, B, C)
- Last option always: "Type your own answer"
- Classify as "Additive" (select all) or "Exclusive Choice" (select one)
- Summarize understanding before next question

### 2.3 Draft spec.md

Include sections:
- Overview
- Functional Requirements
- Non-Functional Requirements (if any)
- Acceptance Criteria
- Out of Scope

### 2.4 User Confirmation

Present draft, ask for approval or changes. Loop until confirmed.

## Phase 3: Plan Generation

### 3.1 Generate plan.md

Based on approved spec and `conductor/workflow.md`:
- Hierarchical: Phases > Tasks > Sub-tasks
- Status markers: `[ ]` for each item
- Follow TDD structure if workflow specifies

**CRITICAL**: For each Phase, append meta-task:
```
- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)
```

### 3.2 User Confirmation

Present plan, ask for approval or changes. Loop until confirmed.

## Phase 4: Create Artifacts

### 4.1 Check for Duplicates

List existing tracks in `conductor/tracks/`
If proposed short name matches existing, halt and suggest different name.

### 4.2 Generate Track ID

Format: `shortname_YYYYMMDD`

### 4.3 Create Directory

`conductor/tracks/<track_id>/`

### 4.4 Create metadata.json

```json
{
  "track_id": "<track_id>",
  "type": "feature",
  "status": "new",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "<Initial description>"
}
```

### 4.5 Write Files

- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`

### 4.6 Update tracks.md

Append to `conductor/tracks.md`:

```markdown

---

## [ ] Track: <Track Description>
*Link: [./conductor/tracks/<track_id>/](./conductor/tracks/<track_id>/)*
```

### 4.7 Announce Completion

> "New track '<track_id>' has been created. Run implement to start working."
