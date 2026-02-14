---
adapter_metadata:
  skill_name: conductor
  skill_version: 1.0.0
  last_synced: 2026-02-14
  source_path: skill/SKILL.md
  adapter_id: codex-cli
  adapter_format: AGENTS.md
---

# Conductor (agents manifest)

This repository defines the **Conductor** Context-Driven Development (CDD) framework. It transforms AI agents into proactive project managers by enforcing a strict **Context -> Spec & Plan -> Implement** protocol.

## Capability

Conductor provides a structured workflow for software development, ensuring that features and bug fixes are well-specified and planned before any code is written. It includes tools for project setup, track creation, task implementation with TDD, status reporting, and safe reverts.

### Core Protocols

- **Setup** (`commands/conductor/setup.toml`): Initialize CDD in a project.
- **New Track** (`commands/conductor/newTrack.toml`): Plan new features/fixes.
- **Implement** (`commands/conductor/implement.toml`): Execute tasks from a plan.
- **Status** (`commands/conductor/status.toml`): Track project progress.
- **Revert** (`commands/conductor/revert.toml`): Roll back changes safely.

Primary instructions: [skill/SKILL.md](skill/SKILL.md). Tool-specific versions are distributed via the sync script.

## Context

This file serves as the **Agents.md** standard manifest for this repository. It provides guidance for AI agents to understand how to interact with this codebase.

### Repository structure

- `conductor-core/`
  - Core logic and Jinja2 templates for skill generation.
- `skill/SKILL.md`
  - The canonical skill definition.
- `skills/`
  - Compiled individual skills (Setup, New Track, etc.).
- `scripts/`
  - Automation for syncing skills to multiple platforms.

### Core instructions

You are the Conductor agent. Follow the protocol in `skill/SKILL.md`. Always ensure the `conductor/` directory exists before performing operations, and never skip the "Spec & Plan" phase.

## Maintenance

To sync changes from templates to all tool adapters, run:

```bash
python scripts/sync_skills.py
```

## Interoperability

Conductor supports multiple platforms including Antigravity, Claude Code, Gemini CLI, OpenCode, Kilo Code, Amp, Cline, and GitHub Copilot. Check the tool-specific hidden directories (e.g., `.claude/skills/`, `.kilo/skills/`) for local installations.
