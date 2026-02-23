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

**Status:** IN PROGRESS

- [ ] Update `conductor:setup` skill
  - [ ] Replace free-text prompts with AskUser calls
  - [ ] Batch related setup questions
- [ ] Update `conductor:newTrack` skill
  - [ ] Replace track creation prompts with AskUser
- [ ] Update `conductor:review` skill
  - [ ] Replace review confirmation with AskUser yesno
- [ ] Update `conductor:revert` skill
  - [ ] Replace revert confirmation with AskUser yesno
- [ ] Update `conductor:implement` skill
  - [ ] Replace task selection with AskUser choice

## Phase 4: Testing & Documentation

- [ ] Test all migrated commands
- [ ] Verify fewer interaction turns required
- [ ] Update documentation with AskUser patterns
- [ ] Run full test suite
- [ ] Code review and quality checks

## Phase 5: Verification & Completion

- [ ] Verify all acceptance criteria met
- [ ] Execute /conductor:review for final verification
- [ ] Mark track complete
- [ ] Archive track

## References

- Upstream Issue: https://github.com/gemini-cli-extensions/conductor/issues/105
