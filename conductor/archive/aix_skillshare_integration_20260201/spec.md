# Track Specification: AIX and SkillShare Integration

## Overview
This track adds support for two new AI platforms, **AIX** and **SkillShare**, to the Conductor ecosystem. This allows Conductor's context-driven development commands to be synchronized and utilized within these environments.

## Functional Requirements
1.  **Manifest Update:** Update `skills/manifest.json` to include `aix` and `skillshare` in the `tools` registry.
2.  **Platform Definitions:**
    *   **SkillShare:** Use a `slash-dash` command style (e.g., `/conductor-setup`) and a directory-based artifact structure (each skill in its own folder with a `SKILL.md`).
    *   **AIX:** Use a `slash-dash` command style and a consolidated markdown file for instructions, similar to the GitHub Copilot integration.
3.  **Sync Script Enhancement:** Update `scripts/sync_skills.py` to:
    *   Define default paths: `~/.config/skillshare/skills/` and `~/.config/aix/`.
    *   Implement the synchronization logic for both platforms.
    *   Ensure the "single source of truth" for SkillShare is correctly populated.
4.  **Skill Activation:** Enable `aix` and `skillshare` support for all core Conductor skills (`setup`, `new_track`, `implement`, `status`, `revert`) in the manifest.
5.  **Documentation:** Update `docs/skill-command-syntax.md` to include the new platforms in the tool matrix.

## Acceptance Criteria
- [ ] `scripts/sync_skills.py` successfully generates artifacts in the specified directories.
- [ ] `manifest.json` contains valid entries for `aix` and `skillshare`.
- [ ] The generated `SKILL.md` files for SkillShare follow the correct directory structure.
- [ ] The consolidated `conductor.md` for AIX contains all enabled commands.
- [ ] The tool matrix in `docs/skill-command-syntax.md` is updated and accurate.

## Out of Scope
- Implementing custom logic or bridges for AIX/SkillShare beyond command synchronization.
- Modifying the `aix` or `skillshare` tools themselves.
