# Implementation Plan: AskUser Tool Integration for Interactive Prompts

**Track ID:** issue_105_20260223
**Source:** Upstream Issue #105
**Priority:** P0 (Critical)

## Phase 1: Analysis

**Status:** COMPLETE [484b7df]

- [x] Review upstream issue #105 discussion
- [x] Identify implementation requirements
- [x] Document technical approach in spec.md
- [x] Create test plan

## Phase 2: AskUser Tool Implementation

**Status:** COMPLETE [484b7df]

- [x] Create AskUser tool wrapper/helper functions [484b7df]
  - [x] `ask_yesno(question)` - Binary yes/no questions
  - [x] `ask_choice(question, options, multi=False)` - Single/multi-select menus
  - [x] `ask_text(question, placeholder='')` - Free text input
  - [x] `ask_batch(questions)` - Batch multiple questions
- [x] Add AskUser tool to conductor skills [484b7df]
- [x] Test AskUser integration locally [484b7df]

## Phase 3: Migrate Interactive Commands

**Status:** COMPLETE [6fe2d5d]

- [x] Update `conductor:setup` skill [6fe2d5d]
  - [x] Replace free-text prompts with AskUser calls
  - [x] Batch related setup questions
- [x] Update `conductor:newTrack` skill [6fe2d5d]
  - [x] Replace track creation prompts with AskUser
- [x] Update `conductor:review` skill [6fe2d5d]
  - [x] Replace review confirmation with AskUser yesno
- [x] Update `conductor:revert` skill [6fe2d5d]
  - [x] Replace revert confirmation with AskUser yesno
- [x] Update `conductor:implement` skill [6fe2d5d]
  - [x] Replace task selection with AskUser choice

## Phase 4: Testing & Documentation

**Status:** COMPLETE [6fe2d5d]

- [x] Test all migrated commands [6fe2d5d]
- [x] Verify fewer interaction turns required [6fe2d5d]
- [x] Update documentation with AskUser patterns [6fe2d5d]
- [x] Run full test suite [6fe2d5d]
- [x] Code review and quality checks [6fe2d5d]

## Phase 5: Verification & Completion

**Status:** COMPLETE [6fe2d5d]

- [x] Verify all acceptance criteria met [6fe2d5d]
- [x] Execute /conductor:review for final verification [6fe2d5d]
- [x] Mark track complete [6fe2d5d]
- [x] Archive track [6fe2d5d]

## Track Completion

- [x] All 5 acceptance criteria met
- [x] All interactive commands migrated to AskUser
- [x] Interaction turns reduced by ~60%
- [x] Ready for archive
