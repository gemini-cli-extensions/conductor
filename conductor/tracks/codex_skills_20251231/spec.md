# Track Specification: Individual Conductor Skills Not Appearing in Codex

## Overview
The individual Conductor skills (e.g., "conductor:newtrack", "conductor:implement") are not appearing in the Codex command palette. Only the main "conductor" command appears, unlike in Qwen and Gemini-CLI where individual skills are properly exposed. This appears to be a platform-specific issue with Codex on macOS where the naming convention "conductor:newtrack" may not be properly recognized by Codex's skill registration system.

## Functional Requirements
1. Individual Conductor skills should be visible and accessible in the Codex command palette
2. Skills should follow Codex's expected naming convention and directory structure
3. Each skill should be properly registered and functional when invoked from Codex
4. Skills should be discoverable through Codex's command search functionality
5. Maintain compatibility with existing Qwen and Gemini-CLI implementations
6. Skills must work with Codex's skill registration mechanism (directory with SKILL.md files containing YAML frontmatter)
7. Skills should be properly categorized and searchable in Codex
8. Skill descriptions should be clear and informative for Codex users

## Non-Functional Requirements
1. The solution should maintain compatibility with existing Qwen and Gemini-CLI implementations
2. No regression should occur in other environments where the skills currently work
3. The fix should be specific to Codex without affecting other platforms
4. Performance of skill loading should not be significantly impacted
5. Skills should follow Codex's expected directory structure and file format requirements
6. Implementation should follow Test-Driven Development (TDD) methodology
7. All new code must have >95% test coverage
8. Solution should be maintainable and follow established project patterns
9. Changes should be minimal and focused to reduce risk of introducing bugs

## Acceptance Criteria
1. Individual skills appear in Codex command palette with proper naming convention
2. Each skill executes its intended functionality when invoked from Codex
3. Skills continue to work in Qwen and Gemini-CLI environments
4. Skills are properly categorized in Codex if applicable
5. Error handling is appropriate if skill registration fails
6. Skills follow Codex's expected structure: directory with SKILL.md file containing YAML frontmatter
7. All new code has >95% test coverage
8. Implementation follows TDD methodology (tests written before implementation)
9. Solution passes all existing tests without regression
10. Skills are properly documented with clear descriptions in Codex
11. Skill registration process is reliable and consistent across Codex sessions

## Out of Scope
1. Modifying the core functionality of individual skills
2. Changes to skill behavior in Qwen or Gemini-CLI environments
3. Adding new skills (this is purely about visibility/registration)
4. Modifying the underlying skill implementation logic
5. Changes that break existing functionality in other platforms
6. UI/UX changes unrelated to skill registration
7. Changes to the core Conductor engine functionality