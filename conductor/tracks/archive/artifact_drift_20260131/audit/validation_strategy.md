# Validation Strategy & Expected Signatures

## Strategy
- Treat `skills/manifest.json` as the source of truth for all generated artifacts.
- Use deterministic renderers (`scripts/sync_skills.py`) to generate skills/workflows and manifests.
- Validate drift with a single entrypoint (`scripts/check_skills_sync.py`) that compares rendered output to on-disk artifacts.
- Ensure CI runs validation on every PR and fails on mismatches.

## Expected Signatures
- Skills content matches template rendering of `conductor-core/src/conductor_core/templates/SKILL.md.j2`.
- Antigravity workflows match template rendering of `<template>.j2` with YAML front-matter.
- VS Code `package.json` commands are derived from manifest-enabled skills.
- `gemini-extension.json` / `qwen-extension.json` must match the manifest `extensions` section.
- `conductor.vsix` must exist and be non-empty when `--require-vsix` is enabled.

## Validation Inputs
- Repo-local artifacts: `skills/`, `.antigravity/skills/`, `conductor-vscode/skills/`, `.agent/workflows/`.
- Optional outputs: Antigravity global workflows and skills (gated by flags).

## Failure Signals
- Missing artifact directory or file.
- Content mismatch (rendered output differs from on-disk output).
- Missing VSIX or zero-length VSIX when required.
