# Installer UX Contract

## Summary
Define a consistent installer interface and output format for Conductor across Windows (PowerShell) and cross-platform (Node or Python wrapper).

## CLI Flags

Required flags for all installers:

- `--verify`: run validation checks only, exit non-zero on failure
- `--dry-run`: show planned actions without writing or installing
- `--print-locations`: output resolved artifact paths for each tool
- `--repo-only`: only update repo-local artifacts (no global installs)

Optional flags:

- `--install-vsix`: install VSIX into VS Code and Antigravity
- `--sync-workflows`: sync Antigravity global/workspace workflows
- `--sync-skills`: sync skills to agent-skill directories (Codex/Claude/OpenCode)
- `--sync-copilot`: update Copilot rules file

## Output Format (Required)

Emit one line per tool with a fixed prefix, e.g.:

- `OK  vsix  C:\path\to\conductor.vsix`
- `OK  antigravity-global  C:\Users\...\.gemini\antigravity\global_workflows`
- `OK  codex  C:\Users\...\.codex\skills\conductor`
- `WARN  vscode  code.cmd not found`
- `FAIL  validate  schema mismatch in skills/manifest.json`

Each run should finish with a summary line:

- `SUMMARY  ok=<n> warn=<n> fail=<n>`

## Verification Contract

`--verify` should run the following in order (as applicable):

1. `python scripts/check_skills_sync.py`
2. `python scripts/validate_platforms.py`
3. `python scripts/validate_antigravity.py`
4. Verify VSIX file exists and is non-empty

## Release Strategy Decision

- **Node package release:** defer publishing to npm until installer parity is proven.
- **Preferred distribution:** GitHub Releases with bundled scripts + VSIX + PyPI artifacts.
- **Follow-up:** if adoption warrants, publish a minimal npm package that wraps the installer and pins release assets.