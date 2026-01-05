# Example prompts for the Conductor Copilot Agent

- "Run the project setup for Conductor with default options" -> triggers `conductor.setup` (adapter/setup.sh)
- "Create a new track called 'feature/xyz'" -> triggers `conductor.newTrack` (adapter/newTrack.sh)
- "Show current conductor status" -> triggers `conductor.status` (adapter/status.sh)

Examples for local shell users:

- Install the homedir helpers:

  ./copilot-agent/scripts/homedir-setup.sh

- Run the wrapper after installation:

  ~/.local/bin/conductor-agent status

Notes:
- If the `conductor` CLI is installed, the agent will prefer it. Otherwise the agent points developers at the TOML files in `commands/conductor/` or uses `skill/scripts/run-conductor.sh`.
