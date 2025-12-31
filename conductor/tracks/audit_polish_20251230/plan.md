# Track Plan: Deep Audit & Final Polish

## Phase 1: Gemini Adapter Completion [checkpoint: 31929a4]
- [x] Task: Refactor `status` command in `conductor-gemini` to use `ProjectManager` [31929a4]
- [x] Task: Port `implement` logic from TOML to `conductor-core` (create `TaskRunner`) [31929a4]
- [x] Task: Implement `implement` command in `conductor-gemini` using `TaskRunner` [31929a4]
- [x] Task: Conductor - Automated Verification 'Phase 1: Gemini Adapter Completion' (Protocol in workflow.md) [31929a4]

## Phase 2: VS Code Extension Completion
- [ ] Task: Add `setup`, `implement`, `status`, `revert` commands to `conductor-vscode/package.json`
- [ ] Task: Implement command handlers in `extension.ts` (calling Python CLI or Core)
- [ ] Task: Conductor - Automated Verification 'Phase 2: VS Code Extension Completion' (Protocol in workflow.md)

## Phase 3: Core Logic Refinement
- [ ] Task: Implement robust ID generator in `ProjectManager` (e.g., hash-based or human-readable)
- [ ] Task: Ensure `TaskRunner` handles the full TDD loop defined in `workflow.md`
- [ ] Task: Conductor - Automated Verification 'Phase 3: Core Logic Refinement' (Protocol in workflow.md)

## Phase 4: Final Release Prep
- [ ] Task: Bump versions in all `package.json` and `pyproject.toml` files to `0.2.0`
- [ ] Task: Update `CHANGELOG.md`
- [ ] Task: Push final changes and open PR
- [ ] Task: Conductor - Automated Verification 'Phase 4: Final Release Prep' (Protocol in workflow.md)
