# Track Plan: Project Foundation

## Phase 1: Preparation & PR Integration [checkpoint: 4c57b04]
- [x] Task: Create a new development branch `feature/foundation-core` <!-- id: 0 -->
- [x] Task: Merge [PR #9](https://github.com/gemini-cli-extensions/conductor/pull/9) and resolve any conflicts <!-- id: 1 -->
- [x] Task: Merge [PR #25](https://github.com/gemini-cli-extensions/conductor/pull/25) and resolve any conflicts <!-- id: 2 -->
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation & PR Integration' (Protocol in workflow.md) <!-- id: 3 -->

## Phase 2: Core Library Extraction
- [x] Task: Initialize `conductor-core` package structure (pyproject.toml, src/ layout) <!-- id: 4 -->
- [x] Task: Write Tests: Define schema for Tracks and Plans using Pydantic <!-- id: 5 -->
- [x] Task: Implement Feature: Core Data Models (Track, Plan, Task, Phase) <!-- id: 6 -->
- [ ] Task: Write Tests: Prompt rendering logic with Jinja2
- [ ] Task: Implement Feature: Abstract Prompt Provider
- [ ] Task: Write Tests: Git abstraction layer (GitPython)
- [ ] Task: Implement Feature: Git Service Provider
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Library Extraction' (Protocol in workflow.md)

## Phase 3: Platform Adapter Refactoring
- [ ] Task: Refactor `conductor-gemini` to use `conductor-core` for all logic
- [ ] Task: Write Tests: Verify CLI slash command routing to core library
- [ ] Task: Implement Feature: Gemini CLI Adapter implementation
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Platform Adapter Refactoring' (Protocol in workflow.md)

## Phase 4: Final Validation & Coverage
- [ ] Task: Ensure 95% test coverage for `conductor-core`
- [ ] Task: Verify multi-platform support (mocking a qwen-cli environment)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Validation & Coverage' (Protocol in workflow.md)

## Phase 5: Release Engineering & Deployment
- [ ] Task: Update `.github/workflows/package-and-upload-assets.yml` to support VSIX and PyPI packaging
- [ ] Task: Implement Feature: Build script for VSIX artifact
- [ ] Task: Implement Feature: Build script for PyPI artifact (conductor-core)
- [ ] Task: Verify artifact generation locally
- [ ] Task: Push changes to upstream repository
- [ ] Task: Open Pull Request on upstream repository
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Release Engineering & Deployment' (Protocol in workflow.md)
