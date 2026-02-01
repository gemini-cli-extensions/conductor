# Track Specification: Skills Abstraction & Tool Setup Review

## Overview
Review and improve how Conductor skills are abstracted, generated, and set up across target tools (Agent Skills directories/installers, Gemini/Qwen CLI extensions, VS Code/Antigravity). Ensure each tool uses the correct command syntax and receives the right artifact type (SKILL.md vs extension/workflow/manifest). Implement improvements in automation, install UX, documentation, and validation without changing skill protocol content.

## Functional Requirements
1. Audit the current skill sources, templates, and distribution paths across tools:
   - Agent Skills directories (`skills/`, `skill/`, installers)
   - Gemini/Qwen extension files (`commands/`, `gemini-extension.json`, `qwen-extension.json`)
   - VS Code / Antigravity integration (`conductor-vscode/`, `.antigravity/`)
2. Define a single source of truth for skill metadata and tool command syntax mapping.
3. Ensure automation generates all tool-specific artifacts from that single source of truth (including SKILL.md, extension manifests, and any workflow files).
4. Improve installation flows for each tool (non-interactive flags, clear errors, tool-specific guidance).
5. Add/extend validation/tests to detect mis-generated artifacts, missing tool requirements, or stale generated outputs.
6. Update documentation with tool-specific setup and command usage examples using native syntax (slash, `$`, `@`).

## Non-Functional Requirements
1. Skill content/protocols must remain unchanged.
2. No regressions in existing tool setups.
3. Changes must be maintainable and minimize manual steps.
4. Documentation must reflect tool-native syntax and actual setup steps.

## Acceptance Criteria
1. Each target tool has a documented, correct setup path using the appropriate artifact type and command syntax.
2. A single manifest/source of truth drives generation for all tool artifacts.
3. Validation/tests verify generated artifacts match templates and tool conventions.
4. No changes to skill protocol content.
5. Installation UX is improved (clear guidance, fewer manual steps, better error messages).
6. CI or a local check can detect when generated outputs are out of date (optional but preferred).

## Out of Scope
1. Modifying skill protocol content or logic.
2. Adding new skills.
3. Changing core Conductor workflows beyond setup/abstraction.
4. Changes that break compatibility with existing tool integrations.
