# Header Extension for Gemini CLI

**Measure twice, code once.**

Header is a Gemini CLI extension that enables **Context-Driven Development**. It turns the Gemini CLI into a proactive project manager that follows a strict protocol to specify, plan, and implement software features and bug fixes.

Instead of just writing code, Header ensures a consistent, high-quality lifecycle for every task: **Context -> Spec & Plan -> Implement**.

The philosophy behind Header is simple: control your code. By treating context as a managed artifact alongside your code, you transform your repository into a single source of truth that drives every agent interaction with deep, persistent project awareness.

## Features

- **Plan before you build**: Create specs and plans that guide the agent for new and existing codebases.
- **Maintain context**: Ensure AI follows style guides, tech stack choices, and product goals.
- **Iterate safely**: Review plans before code is written, keeping you firmly in the loop.
- **Work as a team**: Set project-level context for your product, tech stack, and workflow preferences that become a shared foundation for your team.
- **Build on existing projects**: Intelligent initialization for both new (Greenfield) and existing (Brownfield) projects.
- **Smart revert**: A git-aware revert command that understands logical units of work (tracks, phases, tasks) rather than just commit hashes.
- **Interactive exploration**: Guided codebase discovery with the explore command to understand architecture and design patterns.

## Installation

Install the Header extension by running the following command from your terminal:

```bash
gemini extensions install https://github.com/billlzzz18/header --auto-update
```

The `--auto-update` is optional: if specified, it will update to new versions as they are released.

## Usage

Header is designed to manage the entire lifecycle of your development tasks.

**Note on Token Consumption:** Header's context-driven approach involves reading and analyzing your project's context, specifications, and plans. This can lead to increased token consumption, especially in larger projects or during extensive planning and implementation phases. You can check the token consumption in the current session by running `/stats model`.

### 1. Set Up the Project (Run Once)

When you run `/header:setup`, Header helps you define the core components of your project context. This context is then used for building new components or features by you or anyone on your team.

- **Product**: Define project context (e.g. users, product goals, high-level features).
- **Product guidelines**: Define standards (e.g. prose style, brand messaging, visual identity).
- **Tech stack**: Configure technical preferences (e.g. language, database, frameworks).
- **Workflow**: Set team preferences (e.g. TDD, commit strategy). Uses [workflow.md](templates/workflow.md) as a customizable template.

**Generated Artifacts:**

- `header/product.md`
- `header/product-guidelines.md`
- `header/tech-stack.md`
- `header/workflow.md`
- `header/code_styleguides/`
- `header/tracks.md`

```bash
/header:setup
```

### 2. Start a New Track (Feature or Bug)

When you're ready to take on a new feature or bug fix, run `/header:newTrack`. This initializes a **track** — a high-level unit of work. Header helps you generate two critical artifacts:

- **Specs**: The detailed requirements for the specific job. What are we building and why?
- **Plan**: An actionable to-do list containing phases, tasks, and sub-tasks.

**Generated Artifacts:**

- `header/tracks/<track_id>/spec.md`
- `header/tracks/<track_id>/plan.md`
- `header/tracks/<track_id>/metadata.json`

```bash
/header:newTrack
# OR with a description
/header:newTrack "Add a dark mode toggle to the settings page"
```

### 3. Implement the Track

Once you approve the plan, run `/header:implement`. Your coding agent then works through the `plan.md` file, checking off tasks as it completes them.

**Updated Artifacts:**

- `header/tracks.md` (Status updates)
- `header/tracks/<track_id>/plan.md` (Status updates)
- Project context files (Synchronized on completion)

```bash
/header:implement
```

Header will:

1. Select the next pending task.
2. Follow the defined workflow (e.g., TDD: Write Test -> Fail -> Implement -> Pass).
3. Update the status in the plan as it progresses.
4. **Verify Progress**: Guide you through a manual verification step at the end of each phase to ensure everything works as expected.

During implementation, you can also:

- **Check status**: Get a high-level overview of your project's progress.

  ```bash
  /header:status
  ```

- **Explore codebase**: Interactively understand how components work.

  ```bash
  /header:explore "How does the track implementation work?"
  ```

- **Revert work**: Undo a feature or a specific task if needed.

  ```bash
  /header:revert
  ```

- **Review work**: Review completed work against guidelines and the plan.

  ```bash
  /header:review
  ```

## Commands Reference

| Command | Description | Artifacts |
| :--- | :--- | :--- |
| `/header:setup` | Scaffolds the project and sets up the Header environment. Run this once per project. | `header/product.md`, `header/product-guidelines.md`, `header/tech-stack.md`, `header/workflow.md`, `header/tracks.md` |
| `/header:newTrack` | Starts a new feature or bug track. Generates `spec.md` and `plan.md`. | `header/tracks/<id>/spec.md`, `header/tracks/<id>/plan.md`, `header/tracks.md` |
| `/header:implement` | Executes the tasks defined in the current track's plan. | `header/tracks.md`, `header/tracks/<id>/plan.md` |
| `/header:status` | Displays the current progress of the tracks file and active tracks. | Reads `header/tracks.md` |
| `/header:explore` | Interactive codebase exploration with guided discovery. | Read-only analysis |
| `/header:revert` | Reverts a track, phase, or task by analyzing git history. | Reverts git history |
| `/header:review` | Reviews completed work against guidelines and the plan. | Reads `plan.md`, `product-guidelines.md` |

## Resources

- [Gemini CLI extensions](https://geminicli.com/docs/extensions/): Documentation about using extensions in Gemini CLI
- [GitHub issues](https://github.com/billlzzz18/header/issues): Report bugs or request features

## Legal

- License: [Apache License 2.0](LICENSE)
