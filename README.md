# Conductor - AI Agent Skill for Context-Driven Development

**Measure twice, code once.**

Conductor is a portable AI agent skill that enables **Context-Driven Development**. It works with Claude Code, OpenCode, Gemini CLI, and other AI coding agents, transforming them into proactive project managers that follow a strict protocol to specify, plan, and implement software features and bug fixes.

Instead of just writing code, Conductor ensures a consistent, high-quality lifecycle for every task: **Context -> Spec & Plan -> Implement**.

The philosophy behind Conductor is simple: control your code. By treating context as a managed artifact alongside your code, you transform your repository into a single source of truth that drives every agent interaction with deep, persistent project awareness.

## Features

- **Plan before you build**: Create specs and plans that guide the agent for new and existing codebases.
- **Maintain context**: Ensure AI follows style guides, tech stack choices, and product goals.
- **Iterate safely**: Review plans before code is written, keeping you firmly in the loop.
- **Work as a team**: Set project-level context for your product, tech stack, and workflow preferences that become a shared foundation for your team.
- **Build on existing projects**: Intelligent initialization for both new (Greenfield) and existing (Brownfield) projects.
- **Smart revert**: A git-aware revert command that understands logical units of work (tracks, phases, tasks) rather than just commit hashes.

## Installation

### Claude Code / OpenCode / AI Agent Skill

Conductor is available as a portable **skill** that works with Claude CLI, OpenCode, and other AI coding agents that support the skills standard.

```bash
# Clone the repository
git clone https://github.com/gemini-cli-extensions/conductor.git
cd conductor

# Run the install script
./skill/scripts/install.sh
```

The installer will ask where to install:
1. **OpenCode global** (`~/.opencode/skill/conductor/`)
2. **Claude CLI global** (`~/.claude/skills/conductor/`)
3. **Both**

The skill is installed with symlinks to this repository, so running `git pull` will automatically update the skill.

After installation, restart your AI CLI. The agent will automatically detect and use Conductor when you ask to create a new feature, write a spec, plan a feature, or set up a project.

### Gemini CLI Extension (Alternative)

Conductor can also be installed as a Gemini CLI extension:

```bash
gemini extensions install https://github.com/gemini-cli-extensions/conductor --auto-update
```

The `--auto-update` flag is optional and will update to new versions as they are released.

## Usage

Conductor is designed to manage the entire lifecycle of your development tasks.

**Note on Token Consumption:** Conductor's context-driven approach involves reading and analyzing your project's context, specifications, and plans. This can lead to increased token consumption, especially in larger projects or during extensive planning and implementation phases.

**Note for Claude Code/OpenCode users:** Simply ask your agent to perform tasks like "set up conductor" or "create a new feature". The agent will automatically invoke the appropriate Conductor protocols. You don't need to use slash commands.

**Note for Gemini CLI users:** Use the slash commands shown below (e.g., `/conductor:setup`).

### 1. Set Up the Project (Run Once)

Ask your agent to "set up conductor" or run `/conductor:setup` (Gemini CLI). This helps you define the core components of your project context, which is then used for building new components or features by you or anyone on your team.

- **Product**: Define project context (e.g. users, product goals, high-level features).
- **Product guidelines**: Define standards (e.g. prose style, brand messaging, visual identity).
- **Tech stack**: Configure technical preferences (e.g. language, database, frameworks).
- **Workflow**: Set team preferences (e.g. TDD, commit strategy). Uses [workflow.md](templates/workflow.md) as a customizable template.

**Generated Artifacts:**
- `conductor/product.md`
- `conductor/product-guidelines.md`
- `conductor/tech-stack.md`
- `conductor/workflow.md`
- `conductor/code_styleguides/`
- `conductor/tracks.md`

### 2. Start a New Track (Feature or Bug)

Ask your agent to "create a new feature" or "start a new track", or run `/conductor:newTrack` (Gemini CLI). This initializes a **track** — a high-level unit of work. Conductor helps you generate two critical artifacts:

- **Specs**: The detailed requirements for the specific job. What are we building and why?
- **Plan**: An actionable to-do list containing phases, tasks, and sub-tasks.

**Generated Artifacts:**
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/metadata.json`

### 3. Implement the Track

Once you approve the plan, ask your agent to "implement the track" or "start implementing", or run `/conductor:implement` (Gemini CLI). Your coding agent then works through the `plan.md` file, checking off tasks as it completes them.

**Updated Artifacts:**
- `conductor/tracks.md` (Status updates)
- `conductor/tracks/<track_id>/plan.md` (Status updates)
- Project context files (Synchronized on completion)

Conductor will:
1.  Select the next pending task.
2.  Follow the defined workflow (e.g., TDD: Write Test -> Fail -> Implement -> Pass).
3.  Update the status in the plan as it progresses.
4.  **Verify Progress**: Guide you through a manual verification step at the end of each phase to ensure everything works as expected.

During implementation, you can also:

- **Check status**: Ask "check project status" or run `/conductor:status` (Gemini CLI) to get a high-level overview of your project's progress.
- **Revert work**: Ask "revert the last track" or run `/conductor:revert` (Gemini CLI) to undo a feature or a specific task if needed.

## Commands Reference

**Note:** The slash commands below are for Gemini CLI users. Claude Code/OpenCode users should simply ask the agent to perform these tasks using natural language.

| Command | Description | Artifacts |
| :--- | :--- | :--- |
| `/conductor:setup` | Scaffolds the project and sets up the Conductor environment. Run this once per project. | `conductor/product.md`<br>`conductor/product-guidelines.md`<br>`conductor/tech-stack.md`<br>`conductor/workflow.md`<br>`conductor/tracks.md` |
| `/conductor:newTrack` | Starts a new feature or bug track. Generates `spec.md` and `plan.md`. | `conductor/tracks/<id>/spec.md`<br>`conductor/tracks/<id>/plan.md`<br>`conductor/tracks.md` |
| `/conductor:implement` | Executes the tasks defined in the current track's plan. | `conductor/tracks.md`<br>`conductor/tracks/<id>/plan.md` |
| `/conductor:status` | Displays the current progress of the tracks file and active tracks. | Reads `conductor/tracks.md` |
| `/conductor:revert` | Reverts a track, phase, or task by analyzing git history. | Reverts git history |

## Copilot Agent & Homedir Setup

This repository provides a per-project GitHub Copilot agent scaffold in `copilot-agent/` that exposes the repository's `conductor` commands as Copilot actions and a set of adapters to invoke them.

Quick start:

1. Run validation: `./copilot-agent/validate.sh`
2. Install homedir helpers for your user: `./copilot-agent/scripts/homedir-setup.sh`
3. After installing the skill (`./skill/scripts/install.sh`), ask Copilot or your AI CLI to run setup, create a new track, or check status. See `copilot-agent/examples/prompts.md` for sample prompts.

> Tip: The agent adapters prefer a `conductor` CLI if installed; otherwise they will point you to the TOML command definitions in `commands/conductor/` or use the repository invoker `skill/scripts/run-conductor.sh`.

## Resources

- [Gemini CLI extensions](https://geminicli.com/docs/extensions/): Documentation about using extensions in Gemini CLI
- [GitHub issues](https://github.com/gemini-cli-extensions/conductor/issues): Report bugs or request features

## Legal

- License: [Apache License 2.0](LICENSE)
