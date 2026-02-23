# Specification: AskUser Tool Integration for Interactive Prompts

**Source Issue:** gemini-cli-extensions/conductor#105
**Priority:** P0 (Critical)
**Labels:** area:UX, area:implement, area:newTrack, area:revert, area:setup

## Overview

The Conductor extension's interactive commands (`setup`, `newTrack`, `review`, `revert`, `implement`) currently rely on unstructured, free-text prompts. This track migrates all human-in-the-loop interactions to use the **AskUser tool** for structured, reliable user input.

## Problem Statement

**Current Behavior:**
- Agent manually instructs users to type specific keywords (e.g., "Type A or B", "Reply with yes/no")
- Agent must parse natural language responses, leading to errors
- Long interaction flows require many individual turns, slowing down the process

**Expected Behavior:**
- All interactions use the AskUser tool
- Yes/No questions use `yesno` type
- Menu selections use `choice` type (single or multi-select)
- Data gathering uses `text` type with placeholders
- Related questions batched into single tool calls

## Requirements

### Functional Requirements

1. **AskUser Tool Integration**
   - Implement AskUser tool calls for all interactive commands
   - Support `yesno`, `choice`, and `text` input types
   - Batch related questions into single tool calls

2. **Command Updates**
   - `conductor:setup` - Migrate project setup interview to AskUser
   - `conductor:newTrack` - Migrate track creation prompts to AskUser
   - `conductor:review` - Migrate review confirmation prompts to AskUser
   - `conductor:revert` - Migrate revert confirmation to AskUser
   - `conductor:implement` - Migrate task selection prompts to AskUser

3. **Error Handling**
   - Handle user cancellations gracefully
   - Provide clear error messages for invalid inputs
   - Support timeout/retry logic

### Non-Functional Requirements

- Maintain backward compatibility where possible
- Follow existing code style and patterns
- Include documentation for new AskUser patterns
- All interactions should complete in fewer turns than before

## Acceptance Criteria

- [ ] All human-in-the-loop interactions utilize the AskUser tool
- [ ] Yes/No questions use the `yesno` type for binary decisions
- [ ] Menu selections use the `choice` type (single or multi-select)
- [ ] Data gathering steps use the `text` type with placeholders
- [ ] Related questions are batched into single tool calls
- [ ] Setup interview completes in fewer turns than before
- [ ] All existing tests pass
- [ ] Documentation updated with AskUser patterns

## References

- Upstream Issue: https://github.com/gemini-cli-extensions/conductor/issues/105
- Related: google-gemini/gemini-cli#17689
- AskUser Tool Documentation: https://github.com/google-gemini/gemini-cli
