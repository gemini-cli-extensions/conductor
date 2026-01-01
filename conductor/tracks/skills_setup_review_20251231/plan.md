# Track Implementation Plan: Skills Abstraction & Tool Setup Review

## Phase 1: Audit and Baseline [checkpoint: 5de5e94]
- [x] Task: Inventory current skill templates and generated outputs [2e1d688]
  - [x] Sub-task: Map source templates to generated artifacts (`skills/`, `.antigravity/`, CLI manifests)
  - [x] Sub-task: Identify manual vs generated artifacts and drift risks
- [x] Task: Document tool command syntax and artifact types [1def185]
  - [x] Sub-task: Capture native command syntax per tool (slash /, $, @)
  - [x] Sub-task: Document required artifact types per tool
  - [x] Sub-task: Draft a command syntax matrix artifact (tool -> syntax + example)
- [x] Task: Summarize gaps and improvement opportunities [eab13cc]
  - [x] Sub-task: List duplication or manual steps to remove
  - [x] Sub-task: Identify missing validations or CI checks
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Audit and Baseline' (Protocol in workflow.md)

## Phase 2: Manifest and Design [checkpoint: 95d8dbb]
- [x] Task: Define a skills manifest schema as the single source of truth [a8186ef]
  - [x] Sub-task: Include skill metadata fields and tool visibility flags
  - [x] Sub-task: Include command syntax mapping per tool
  - [x] Sub-task: Define a JSON Schema (or equivalent) for validation
- [x] Task: Design generation targets and outputs [081f1f1]
  - [x] Sub-task: Define outputs for Agent Skills directories and `.antigravity/skills`
  - [x] Sub-task: Define outputs for Gemini/Qwen extension manifests
- [x] Task: Design validation and sync check strategy [5ba0b4a]
  - [x] Sub-task: Define validation scope and failure messaging
  - [x] Sub-task: Plan CI/local check integration
  - [x] Sub-task: Define a "no protocol changes" guard (hash/compare template bodies)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Manifest and Design' (Protocol in workflow.md)

## Phase 3: Automation and Generation [checkpoint: ca3043d]
- [x] Task: Write failing tests for manifest loading and generated outputs (TDD Phase) [5a8c4f9]
  - [x] Sub-task: Add fixture manifest and expected outputs
  - [x] Sub-task: Add golden-file snapshot tests for generated artifacts
 - [x] Task: Implement manifest-driven generation in `scripts/sync_skills.py` [47c4349]
  - [x] Sub-task: Load manifest and replace hardcoded metadata
  - [x] Sub-task: Generate Agent Skills directories and `.antigravity/skills`
 - [x] Task: Extend generator to emit CLI extension manifests [9173dcf]
  - [x] Sub-task: Update `gemini-extension.json` and `qwen-extension.json` from manifest
  - [x] Sub-task: Ensure correct command syntax entries where applicable
- [x] Task: Implement the "no protocol changes" guard in generation or validation [4e8eda3]
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Automation and Generation' (Protocol in workflow.md)

## Phase 4: Install UX and Validation
- [x] Task: Write failing tests for installer flags and validation script (TDD Phase) [8ec6e38]
  - [x] Sub-task: Add tests for non-interactive targets and dry-run output
  - [x] Sub-task: Add tests for `--link/--copy` behavior
  - [x] Sub-task: Add tests for validation failures on missing outputs
- [~] Task: Improve `skill/scripts/install.sh` UX
  - [ ] Sub-task: Add flags (`--target`, `--force`, `--dry-run`, `--list`, `--link`, `--copy`)
  - [ ] Sub-task: Improve error messages and tool-specific guidance
- [ ] Task: Add validation script for tool-specific requirements
  - [ ] Sub-task: Validate generated `SKILL.md` frontmatter vs manifest
  - [ ] Sub-task: Validate tool-specific command syntax mapping
  - [ ] Sub-task: Validate manifest against schema
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Install UX and Validation' (Protocol in workflow.md)

## Phase 5: Documentation and Sync Checks
- [ ] Task: Update docs with tool-native command syntax and setup steps
  - [ ] Sub-task: Add table of tools -> command syntax (/, $, @)
  - [ ] Sub-task: Clarify which artifacts each tool consumes
  - [ ] Sub-task: Publish the command syntax matrix artifact
- [ ] Task: Add a sync check command or CI hook
  - [ ] Sub-task: Provide a `scripts/check_skills_sync.py` (or equivalent)
  - [ ] Sub-task: Document how to run the sync check locally
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Documentation and Sync Checks' (Protocol in workflow.md)
