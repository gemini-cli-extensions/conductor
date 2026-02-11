# Implementation Plan: `repository_excellence_20260210`

## Phase 1: Environment & Dependency Alignment
- [x] Task: Update `environment.yml` with missing stubs and runtime dependencies (click, pygls, lsprotocol).
- [x] Task: Purge all `pyrefly` references from the repository (pyproject.toml, ci.yml).
- [x] Task: Create `.devcontainer/` configuration files.
- [x] Task: Create `templates/projects/` directory with a basic scaffold.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Internal Tooling Consolidation
- [x] Task: Implement `scripts/conductor_dev.py` with `sync`, `verify`, and `build` commands.
- [x] Task: Implement `conductor:doctor` logic for self-diagnostics.
- [x] Task: Add unified `--version` support across CLI entry points.
- [x] Task: Implement telemetry logging to `conductor/logs/`.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: CI/CD Hardening
- [x] Task: Update GitHub Actions to use Mamba/Conda via `environment.yml`.
- [x] Task: Add VS Code extension tests to CI (`npm test`).
- [x] Task: Draft Marketplace publishing workflow (GitHub Action).
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Robustness & Parsing
- [x] Task: Implement "Markdown-to-Model" parser for `plan.md` and `tracks.md`.
- [ ] Task: Refactor `TaskRunner` to use structured parsing and persistence.
- [ ] Task: Implement file-based locking (`conductor/.lock`).
- [ ] Task: Enable Jinja2 `SandboxedEnvironment` in `prompts.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Multi-VCS Support
- [ ] Task: Abstract `GitService` into `VCSService` protocol.
- [ ] Task: Implement `JujutsuService` adapter.
- [ ] Task: Update `TaskRunner` to select VCS adapter based on project discovery.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

## Phase 6: Project Configuration
- [ ] Task: Implement `conductor/config.json` support in `conductor-core`.
- [ ] Task: Update `/conductor:setup` to support scaffolding from templates.
- [ ] Task: Conductor - User Manual Verification 'Phase 6' (Protocol in workflow.md)
