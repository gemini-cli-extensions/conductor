# Copilot Conductor Agent

This directory contains files and scripts to expose the repository's `conductor` commands as a per-project GitHub Copilot agent and to provide idempotent homedir setup for local users.

Structure:
- `agent-manifest.json` - agent metadata and mappings to commands
- `adapter/` - small scripts that translate agent actions into `commands/conductor` invocations
- `scripts/homedir-setup.sh` - idempotent script to install user dotfiles and helper wrappers
- `examples/` - example prompts and usage

See `../README.md` and `SKILL.md` for the project's usage and design notes.