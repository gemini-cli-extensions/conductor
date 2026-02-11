# Skill Definition Standards

This guide defines the standards for creating and maintaining Conductor skills.

## 1. Directory Structure

Skills should be defined in `conductor-core` and synchronized to platform adapters.

```
skills/
└── <skill_id>/
    ├── SKILL.md          # User-facing documentation and triggers
    └── metadata.json     # Optional platform-specific metadata
```

## 2. Naming Conventions

- **Skill ID:** `kebab-case` (e.g., `new-track`, `setup-project`).
- **Command Name:** `camelCase` (e.g., `newTrack`, `setupProject`).
- **File Names:** Use standard extensions (`.md`, `.py`, `.json`).

## 3. Skill Manifest (metadata.json)

Every skill MUST be defined in the central `skills/manifest.json`.

Required fields:
- `id`: Unique identifier for the skill.
- `name`: Human-readable name.
- `description`: Short summary of purpose.
- `version`: Semver format (X.Y.Z).
- `engine_compatibility`: Minimum required core version.
- `triggers`: List of phrases that activate the skill.

## 4. Documentation (SKILL.md)

Each skill must have a `SKILL.md` file following the standard template.
- **Frontmatter:** Must contain `name`, `description`, and `triggers`.
- **Content:** Should explain the skill's purpose, how to use it, and its outputs.

## 5. Implementation Rules

- **Core-First:** All business logic must reside in `conductor-core`.
- **Agnostic Logic:** Logic should not assume a specific interface (CLI vs. IDE) unless explicitly using Capability Flags.
- **Contract Tests:** Every skill must have corresponding contract tests in `conductor-core/tests/contract/`.
