# Specification: `repository_excellence_20260210`

## Overview
This track implements a major upgrade to the Conductor repository's infrastructure, CI/CD pipelines, developer experience, and system robustness. It unifies fragmented tools, hardens the delivery pipeline, introduces self-diagnostic capabilities, and improves core parsing logic.

## Goals
- Achieve 100% environment parity between local development and CI.
- Consolidate all maintenance and synchronization logic into a single internal CLI.
- Introduce project-level configuration and diagnostic tools ("Doctor").
- Modernize static analysis and dependency management.
- Replace brittle regex-based plan parsing with robust structured models.
- Enable multi-VCS support and basic concurrency protection.

## Functional Requirements

### 1. Hardened CI/CD Pipeline
- **Environment Parity:** Update `.github/workflows/ci.yml` to use `conda-incubator/setup-miniconda` with the project's `environment.yml`.
- **VS Code Testing:** Integrate `npm test` for the VS Code extension into the CI test suite.
- **Publishing Automation:** Add a (disabled by default) workflow step for automated VS Code Marketplace publishing.

### 2. Unified Dev CLI (`conductor-dev`)
- Create `scripts/conductor_dev.py` as the single entry point for all developer tasks.
- **Commands:**
    - `sync`: Consolidates logic from `sync_all.py`, `sync_skills.py`, etc.
    - `verify`: Runs all validation scripts (`validate_platforms.py`, `validate_antigravity.py`).
    - `doctor`: Checks the local environment for common issues (missing dependencies, invalid context).
    - `build`: Triggers builds for core and VS Code extension.

### 3. Project Configuration & Metadata
- **Project Config:** Support `conductor/config.json` for per-project settings (default model, iteration limits).
- **Versioning:** Implement a unified `--version` flag for the core and all adapters.
- **Observability:** Add `conductor/logs/` for persisting implementation telemetry (JSON format).

### 4. Robustness & Parsing
- **Structured Parsing:** Refactor `TaskRunner` to use Pydantic models for reading/writing `plan.md` and `tracks.md`.
- **Concurrency:** Implement a file-based lock (`conductor/.lock`) to prevent simultaneous modifications.
- **Template Security:** Enable Jinja2 `SandboxedEnvironment` for rendering prompts.

### 5. Advanced DX
- **Dev Container:** Create `.devcontainer/` for one-click setup.
- **Project Templates:** Add `templates/projects/` for scaffolding common tech stacks.
- **Multi-VCS:** Abstract `GitService` into `VCSService` and add an experimental adapter for `jj` (Jujutsu).

### 6. Technical Debt Purge
- Remove all remaining `pyrefly` references.
- Standardize all template encodings to UTF-8.

## Acceptance Criteria
- [ ] CI uses the project `environment.yml` and passes all tests (including VS Code).
- [ ] `python scripts/conductor_dev.py doctor` reports a healthy environment.
- [ ] `plan.md` can be updated successfully even with non-standard whitespace using structured parsing.
- [ ] `.devcontainer` builds successfully.
- [ ] `pyrefly` is completely removed from all config files.
