# Track Plan: Review and Robustness

## Phase 1: Codebase Audit & Gap Analysis [checkpoint: Automated]
- [x] Task: Use `codebase_investigator` to audit `conductor-core` architecture <!-- id: 34 -->
- [x] Task: Use `codebase_investigator` to audit `conductor-gemini` adapter <!-- id: 35 -->
- [x] Task: Use `codebase_investigator` to audit `conductor-vscode` scaffolding <!-- id: 36 -->
- [x] Task: Analyze audit reports for design flaws and weaknesses <!-- id: 37 -->
- [x] Task: Identify missing tests and abstraction gaps <!-- id: 38 -->
- [x] Task: Conductor - Automated Verification 'Phase 1: Codebase Audit & Gap Analysis' <!-- id: 39 -->

## Phase 2: Refactoring for Robustness
- [x] Task: Implement Feature: `TaskStatus` and `TrackStatus` Enums in `conductor-core` models <!-- id: 40 -->
- [~] Task: Implement Feature: `ProjectManager` service in `conductor-core` to centralize Setup/Track logic <!-- id: 41 -->
- [ ] Task: Write Tests: Improve test coverage for GitService (edge cases)
- [ ] Task: Implement Feature: Add robust error handling to PromptProvider
- [ ] Task: Refactor `conductor-gemini` to delegate all logic to `ProjectManager`
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Refactoring for Robustness' (Protocol in workflow.md)

## Phase 3: Integration Robustness & Compatibility
- [ ] Task: Ensure prompt consistency across Gemini and Claude wrappers
- [ ] Task: Develop automated checks for prompt template synchronization
- [ ] Task: Implement Feature: Create `qwen-extension.json` (mirror of gemini-extension.json)
- [ ] Task: Configure `conductor-vscode` `extensionKind` for Remote/Antigravity support
- [ ] Task: Update documentation for extending the core library
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration Robustness & Compatibility' (Protocol in workflow.md)

## Phase 4: Release Engineering & Deployment
- [ ] Task: Update `.github/workflows/package-and-upload-assets.yml` for core library
- [ ] Task: Implement Feature: PyPI release automation for `conductor-core`
- [ ] Task: Verify artifact generation locally
- [ ] Task: Push changes to upstream repository
- [ ] Task: Open Pull Request on upstream repository
- [ ] Task: Conductor - Automated Verification 'Phase 4: Release Engineering & Deployment' (Protocol in workflow.md)

## Phase 5: Maturity Enhancements
- [ ] Task: Documentation Overhaul: Create ADRs and update root README for Monorepo
- [ ] Task: LSP Feasibility Study: Prototype simple LSP using `pygls`
- [ ] Task: Implement Feature: End-to-End Smoke Test script (`CLI -> Core -> Git`)
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Maturity Enhancements' (Protocol in workflow.md)
