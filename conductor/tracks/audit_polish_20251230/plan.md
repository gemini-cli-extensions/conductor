# Track Plan: Deep Audit & Final Polish

## Phase 1: Gemini Adapter Completion [checkpoint: 31929a4]
- [x] Task: Refactor `status` command in `conductor-gemini` to use `ProjectManager` [31929a4]
- [x] Task: Port `implement` logic from TOML to `conductor-core` (create `TaskRunner`) [31929a4]
- [x] Task: Implement `implement` command in `conductor-gemini` using `TaskRunner` [31929a4]
- [x] Task: Conductor - Automated Verification 'Phase 1: Gemini Adapter Completion' (Protocol in workflow.md) [31929a4]

## Phase 2: VS Code Extension Completion [checkpoint: bacb9bc]
- [x] Task: Add `setup`, `implement`, `status`, `revert` commands to `conductor-vscode/package.json` [bacb9bc]
- [x] Task: Implement command handlers in `extension.ts` (calling Python CLI or Core) [bacb9bc]
- [x] Task: Conductor - Automated Verification 'Phase 2: VS Code Extension Completion' (Protocol in workflow.md) [bacb9bc]

## Phase 3: Core Logic Refinement [checkpoint: 227fb3a]
- [x] Task: Implement robust ID generator in `ProjectManager` (e.g., hash-based or human-readable) [227fb3a]
- [x] Task: Ensure `TaskRunner` handles the full TDD loop defined in `workflow.md` [227fb3a]
- [x] Task: Conductor - Automated Verification 'Phase 3: Core Logic Refinement' (Protocol in workflow.md) [227fb3a]

## Phase 4: Final Release Prep [checkpoint: 66cab67]
- [x] Task: Bump versions in all `package.json` and `pyproject.toml` files to `0.2.0` [66cab67]
- [x] Task: Update `CHANGELOG.md` [66cab67]
- [x] Task: Push final changes and open PR [66cab67]
- [x] Task: Conductor - Automated Verification 'Phase 4: Final Release Prep' (Protocol in workflow.md) [66cab67]
