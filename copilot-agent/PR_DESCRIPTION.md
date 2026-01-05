# PR: Add Copilot Conductor Agent and homedir idempotent setup

Summary:
- Add `copilot-agent/` scaffold exposing conductor commands via `agent-manifest.json` and adapters in `adapter/`.
- Add `copilot-agent/scripts/homedir-setup.sh` to install a `conductor-agent` wrapper to `~/.local/bin` (idempotent).
- Add `skill/scripts/run-conductor.sh` invoker and mark it executable.
- Add `copilot-agent/validate.sh` and `copilot-agent/examples/prompts.md`.
- Update `README.md` and `skill/SKILL.md` with Copilot integration notes.

How to test locally:
1. Run validation: `./copilot-agent/validate.sh`
2. Install homedir wrapper: `./copilot-agent/scripts/homedir-setup.sh` and ensure `~/.local/bin` is in PATH.
3. Try `~/.local/bin/conductor-agent status` (or `conductor` if installed).
4. Try invoking `./skill/scripts/run-conductor.sh status` to see TOML output when `conductor` CLI is not installed.

Notes for PR reviewer:
- Confirm manifest keys and mappings in `agent-manifest.json`.
- Confirm adapter scripts follow expected signature and are idempotent.
- Suggest adding more adapters or richer integration with Copilot if desired.

Next steps:
- Create branch `feat/copilot-conductor-agent` and open a PR with this description.
- Consider adding automated tests or CI to run `copilot-agent/validate.sh` on PRs.