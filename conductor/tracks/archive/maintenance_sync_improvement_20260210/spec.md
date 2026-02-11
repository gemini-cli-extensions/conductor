# Draft Specification: `maintenance_sync_improvement_20260210`

## Overview
This track aims to improve the developer experience and repository health by consolidating maintenance scripts, improving context hygiene (ignoring large/temp files), fixing broken pre-commit hooks, and formally tracking dependencies.

## Goals
- Provide a single command for all synchronization tasks.
- Prevent large or temporary files from being committed.
- Restore a passing pre-commit state.
- Formalize the environment setup for future development.

## Functional Requirements

### 1. Consolidated Synchronization
- Create `scripts/sync_all.py`.
- This script must:
    - Run the logic currently in `scripts/sync_skills.py` (Global/Platform skills).
    - Run the logic currently in `scripts/validate_platforms.py --sync` (Repo-local TOML/MD files).
    - Provide clear status reporting for each phase of the sync.

### 2. Context Hygiene
- Update the root `.gitignore` to include:
    - `*.tar.gz` and `*.vsix`.
    - `.tmp_test.txt`.
    - Build artifacts and directories (e.g., `out/`, `dist/`).
    - Local state/config files (`.env`, `.gemini/tmp/`).

### 3. Pre-commit Hook Repair
- Remove the `pyrefly` hook from `.pre-commit-config.yaml`.
- Ensure remaining hooks (`ruff`, `mypy`, etc.) are functioning correctly.

### 4. Dependency Management
- Create `environment.yml` in the project root.
- Include necessary maintenance dependencies: `jinja2`, `pydantic`, `gitpython`, `ruff`, `mypy`, `pytest`.

## Acceptance Criteria
- [ ] Running `python scripts/sync_all.py` successfully updates all global skills and repository-local platform files.
- [ ] Large artifacts (`.tar.gz`, `.vsix`) are no longer tracked or suggestible by Git.
- [ ] `git commit` no longer fails due to a missing `pyrefly` executable.
- [ ] A new environment can be created/updated using `mamba env update -f environment.yml`.
