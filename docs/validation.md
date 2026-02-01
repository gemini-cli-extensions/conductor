# Artifact Validation Troubleshooting

## Common Drift Cases

### Missing SKILL.md outputs
- Run `python3 scripts/sync_skills.py` to regenerate `skills/`, `.antigravity/skills/`, and `conductor-vscode/skills/`.

### Antigravity workflows mismatched
- Regenerate workflows with `python3 scripts/sync_skills.py`.
- For global workflows, re-run `python3 scripts/install_local.py --sync-workflows`.

### VSIX missing or out of date
- Rebuild the VSIX with `./scripts/build_vsix.sh` and re-run validation with `--require-vsix`.

### Platform mapping drift (Claude/Gemini/Qwen)
- Re-sync from core templates: `python3 scripts/validate_platforms.py --sync`.

### Global Antigravity checks fail in CI
- Global workflow checks are optional. Use `--check-global` only on machines with `~/.gemini/antigravity/global_workflows/` configured.
