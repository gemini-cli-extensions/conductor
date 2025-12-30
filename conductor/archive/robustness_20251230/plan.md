# Track Plan: Review and Robustness

## Phase 1: Codebase Audit & Gap Analysis [checkpoint: Automated]
- [x] Task: Use `codebase_investigator` to audit `conductor-core` architecture <!-- id: 34 -->
- [x] Task: Use `codebase_investigator` to audit `conductor-gemini` adapter <!-- id: 35 -->
- [x] Task: Use `codebase_investigator` to audit `conductor-vscode` scaffolding <!-- id: 36 -->
- [x] Task: Analyze audit reports for design flaws and weaknesses <!-- id: 37 -->
- [x] Task: Identify missing tests and abstraction gaps <!-- id: 38 -->
- [x] Task: Conductor - Automated Verification 'Phase 1: Codebase Audit & Gap Analysis' <!-- id: 39 -->

## Phase 2: Refactoring for Robustness [checkpoint: Automated]
- [x] Task: Implement Feature: `TaskStatus` and `TrackStatus` Enums in `conductor-core` models <!-- id: 40 -->
- [x] Task: Implement Feature: `ProjectManager` service in `conductor-core` to centralize Setup/Track logic <!-- id: 41 -->
- [x] Task: Write Tests: Improve test coverage for GitService (edge cases) <!-- id: 42 -->
- [x] Task: Implement Feature: Add robust error handling to PromptProvider <!-- id: 43 -->
- [x] Task: Refactor `conductor-gemini` to delegate all logic to `ProjectManager` <!-- id: 44 -->
- [x] Task: Conductor - Automated Verification 'Phase 2: Refactoring for Robustness' <!-- id: 45 -->

## Phase 3: Integration Robustness & Compatibility [checkpoint: Automated]
- [x] Task: Ensure prompt consistency across Gemini and Claude wrappers <!-- id: 48 -->
- [x] Task: Develop automated checks for prompt template synchronization <!-- id: 49 -->
- [x] Task: Implement Feature: Create `qwen-extension.json` (mirror of gemini-extension.json) <!-- id: 46 -->
- [x] Task: Configure `conductor-vscode` `extensionKind` for Remote/Antigravity support <!-- id: 47 -->
- [x] Task: Update documentation for extending the core library <!-- id: 50 -->
- [x] Task: Conductor - Automated Verification 'Phase 3: Integration Robustness & Compatibility' <!-- id: 51 -->

## Phase 4: Release Engineering & Deployment [checkpoint: Automated]
- [x] Task: Update `.github/workflows/package-and-upload-assets.yml` for core library <!-- id: 52 -->
- [x] Task: Implement Feature: PyPI release automation for `conductor-core` <!-- id: 53 -->
- [x] Task: Verify artifact generation locally <!-- id: 54 -->
- [~] Task: Push changes to upstream repository <!-- id: 55 -->
- [ ] Task: Open Pull Request on upstream repository
- [x] Task: Conductor - Automated Verification 'Phase 4: Release Engineering & Deployment' <!-- id: 56 -->

## Phase 5: Maturity Enhancements [checkpoint: Automated]
- [x] Task: Documentation Overhaul: Create ADRs and update root README for Monorepo <!-- id: 57 -->
- [x] Task: LSP Feasibility Study: Prototype simple LSP using `pygls` <!-- id: 58 -->
- [x] Task: Implement Feature: End-to-End Smoke Test script (`CLI -> Core -> Git`) <!-- id: 59 -->
- [x] Task: Conductor - Automated Verification 'Phase 5: Maturity Enhancements' <!-- id: 60 -->
