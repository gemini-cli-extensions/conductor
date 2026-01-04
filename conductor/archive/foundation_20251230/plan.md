# Track Plan: Project Foundation

## Phase 1: Preparation & PR Integration [checkpoint: 4c57b04]
- [x] Task: Create a new development branch `feature/foundation-core` <!-- id: 0 -->
- [x] Task: Merge [PR #9](https://github.com/gemini-cli-extensions/conductor/pull/9) and resolve any conflicts <!-- id: 1 -->
- [x] Task: Merge [PR #25](https://github.com/gemini-cli-extensions/conductor/pull/25) and resolve any conflicts <!-- id: 2 -->
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation & PR Integration' (Protocol in workflow.md) <!-- id: 3 -->

## Phase 2: Core Library Extraction [checkpoint: 2017ec5]
- [x] Task: Initialize `conductor-core` package structure (pyproject.toml, src/ layout) <!-- id: 4 -->
- [x] Task: Write Tests: Define schema for Tracks and Plans using Pydantic <!-- id: 5 -->
- [x] Task: Implement Feature: Core Data Models (Track, Plan, Task, Phase) <!-- id: 6 -->
- [x] Task: Write Tests: Prompt rendering logic with Jinja2 <!-- id: 7 -->
- [x] Task: Implement Feature: Abstract Prompt Provider <!-- id: 8 -->
- [x] Task: Write Tests: Git abstraction layer (GitPython) <!-- id: 9 -->
- [x] Task: Implement Feature: Git Service Provider <!-- id: 10 -->
- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Library Extraction' (Protocol in workflow.md) <!-- id: 11 -->

## Phase 3: Prompt Abstraction & Platform Source of Truth
- [x] Task: Initialize `conductor-core` template directory <!-- id: 15 -->
- [x] Task: Extract `setup` protocol into `setup.j2` <!-- id: 16 -->
- [x] Task: Extract `newTrack` protocol into `new_track.j2` <!-- id: 17 -->
- [x] Task: Extract `implement` protocol into `implement.j2` <!-- id: 18 -->
- [x] Task: Extract `status` protocol into `status.j2` <!-- id: 19 -->
- [x] Task: Extract `revert` protocol into `revert.j2` <!-- id: 20 -->
- [~] Task: Implement Feature: Prompt Export/Validation utility in Core <!-- id: 21 -->
- [x] Task: Conductor - Automated Verification 'Phase 3: Prompt Abstraction' <!-- id: 22 -->

## Phase 4: Platform Wrapper Validation [checkpoint: Automated]
- [x] Task: Verify Gemini CLI TOMLs match Core Templates <!-- id: 23 -->
- [x] Task: Verify Claude Code MDs match Core Templates <!-- id: 24 -->
- [x] Task: Ensure 95% test coverage for Core template rendering <!-- id: 25 -->
- [x] Task: Conductor - Automated Verification 'Phase 4: Platform Wrapper Validation' <!-- id: 26 -->

## Phase 5: Release Engineering & Deployment
- [x] Task: Update `.github/workflows/package-and-upload-assets.yml` to support VSIX and PyPI packaging <!-- id: 27 -->
- [x] Task: Implement Feature: Build script for VSIX artifact <!-- id: 28 -->
- [x] Task: Implement Feature: Build script for PyPI artifact (conductor-core) <!-- id: 29 -->
- [x] Task: Verify artifact generation locally <!-- id: 30 -->
- [~] Task: Push changes to upstream repository <!-- id: 31 -->
- [x] Task: Open Pull Request on upstream repository <!-- id: 32 -->
- [x] Task: Conductor - Automated Verification 'Phase 5: Release Engineering & Deployment' <!-- id: 33 -->
