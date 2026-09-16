# Conductor Plugin

**Measure twice, code once.**

Conductor is a plugin for AI coding agents (including Antigravity and Claude
Code) that enables **Spec-Driven Development**. It turns your agent into a
proactive project manager that follows a strict protocol to specify, plan, and
implement software features and bug fixes.

Instead of just writing code, Conductor ensures a consistent, high-quality
lifecycle for every task: **Context -> Spec & Plan -> Implement**.

The philosophy behind Conductor is simple: control your code. By treating
context as a managed artifact alongside your code, you transform your repository
into a single source of truth that drives every agent interaction with deep,
persistent project awareness.

--------------------------------------------------------------------------------

## 🛠 Installation Guide

Conductor is packaged as a standard agent plugin, compatible across modern AI
coding agents. Choose the installation method for your environment below.

### 1. Antigravity

#### A. End-User Installation (Recommended)

Install directly from GitHub in a single command:

```bash
agy plugins install https://github.com/gemini-cli-extensions/conductor
```

#### B. Developer Installation (Live-Sync Global Link)

If you are a developer or contributor who wants to fork the repository, write
custom skills, or modify rule configurations, clone the repository locally and
link it:

1.  Clone the repository:

    ```bash
    git clone https://github.com/gemini-cli-extensions/conductor.git
    cd conductor
    ```

2.  Link globally for Antigravity:

    ```bash
    mkdir -p ~/.gemini/config/plugins/ && ln -sfn "$(pwd)" ~/.gemini/config/plugins/conductor
    ```

*Why this method?* Creating a symlink acts as a live development link. Any edits
you make in your local Git branch are instantly loaded in real-time without
reinstalling!

#### C. Workspace-Level Isolation

If you want to isolate Conductor strictly inside a specific Git project:

1.  Create the local plugins directory in your target project's root:

    ```bash
    mkdir -p .agents/plugins/
    ```

2.  Link Conductor to your local project:

    ```bash
    ln -sfn /absolute/path/to/cloned/conductor .agents/plugins/conductor
    ```

--------------------------------------------------------------------------------

### 2. Claude Code

#### End-User Installation

Register the marketplace repository and install the Conductor plugin directly in
your Claude Code session:

```bash
/plugin marketplace add gemini-cli-extensions/conductor
/plugin install conductor
```

--------------------------------------------------------------------------------

## 🔄 Uninstallation

To safely remove Conductor from your environment:

*   **Antigravity:**
    *   **CLI Installation:** Run `agy plugins uninstall conductor`
    *   **Global Link:** Run `rm -f ~/.gemini/config/plugins/conductor`
    *   **Workspace Link:** Run `rm -f .agents/plugins/conductor`
*   **Claude Code:** Run `/plugin remove conductor` and `/plugin marketplace
    remove gemini-cli-extensions/conductor`

--------------------------------------------------------------------------------

## 🚀 Features

-   **Plan before you build**: Create specs and plans that guide the agent for
    new and existing codebases.
-   **Maintain context**: Ensure AI follows style guides, tech stack choices,
    and product goals.
-   **Iterate safely**: Review plans before code is written, keeping you firmly
    in the loop.
-   **Work as a team**: Set project-level context for your product, tech stack,
    and workflow preferences that become a shared foundation for your team.
-   **Build on existing projects**: Intelligent initialization for both new
    (Greenfield) and existing (Brownfield) projects.
-   **Smart revert**: A git-aware revert command that understands logical units
    of work (tracks, phases, tasks) rather than just commit hashes.
-   **Optional Linear-first**: When a project has `conductor/linear.md`, tracks
    use a Linear issue as the spec (pointer metadata + `plan.md`). File-based
    `spec.md` / `tracks.md` remains the default when that file is absent.

--------------------------------------------------------------------------------

## 🎨 Adaptive User Experience (UX Layer)

Conductor natively adapts its user interface to match the specific visual
capabilities of your active developer environment (IDE chat box, terminal
console, or web editor).

This is powered by the integrated **View Layer UX Adapter**:

*   **Interactive GUI Modals:** If your host editor supports visual interactive
    dialog elements, Conductor will automatically capture selections, decision
    interviews, and track options as native graphical modal dialog windows.
    *   `rules/`: Custom adapter rules tailored for visual IDE environments
        (like Antigravity).
*   **Graceful CLI Fallback:** If you are operating in a plain text terminal
    console (such as Claude Code), Conductor automatically detects the console
    environment and adapts all interactive steps into clean, structured
    text-based choice menus with bracketed numbers (e.g., `[1] Option A, [2]
    Option B`).

This dynamic, semantic adaptation occurs natively behind the scenes with **zero
configuration required**, ensuring the optimal developer experience regardless
of your chosen workflow environment.

--------------------------------------------------------------------------------

## 📖 Usage & Lifecycle

Conductor manages the entire lifecycle of your development tasks through
namespace-grouped commands.

> [!NOTE] **Note on Token Consumption:** Conductor's spec-driven approach
> involves reading and analyzing your project's context, specifications, and
> plans. This can lead to increased token consumption, especially in larger
> projects or during extensive planning and implementation phases. You can check
> the token consumption in the current session by running `/stats model` (in
> compatible clients).

### 1. Set Up the Project (Run Once)

When you run `/conductor:conductor-setup`, Conductor helps you define the core
components of your project context. This context is then used for building new
components or features by you or anyone on your team.

-   **Product**: Define project context (e.g. users, product goals, high-level
    features).
-   **Product guidelines**: Define standards (e.g. prose style, brand messaging,
    visual identity).
-   **Tech stack**: Configure technical preferences (e.g. language, database,
    frameworks).
-   **Workflow**: Set team preferences (e.g. TDD, commit strategy). Uses
    `workflow.md` as a customizable template.

**Generated Artifacts:**

-   `conductor/product.md`
-   `conductor/product-guidelines.md`
-   `conductor/tech-stack.md`
-   `conductor/workflow.md`
-   `conductor/code_styleguides/`
-   `conductor/tracks.md`
-   `conductor/linear.md` (only if you opt in to Linear-first)
-   `scripts/linear_cli.py` and `scripts/linear_create_issue.py` (copied when Linear is enabled)

```bash
/conductor:conductor-setup
```

### 2. Start a New Track (Feature or Bug)

When you’re ready to take on a new feature or bug fix, run
`/conductor:conductor-new-track`. This initializes a **track** — a high-level
unit of work. Conductor helps you generate two critical artifacts:

-   **Specs**: The detailed requirements for the specific job. What are we
    building and why?
-   **Plan**: An actionable to-do list containing phases, tasks, and sub-tasks.

**Generated Artifacts (file-based default):**

-   `conductor/tracks/<track_id>/spec.md`
-   `conductor/tracks/<track_id>/plan.md`
-   `conductor/tracks/<track_id>/metadata.json`
-   `conductor/tracks.md` entry

**Generated Artifacts (Linear-first, when `conductor/linear.md` exists):**

-   Linear issue (created or linked) — this is the spec
-   `conductor/tracks/<track_id>/metadata.json` (pointer: `track_id`, `linear`, `linear_url`)
-   `conductor/tracks/<track_id>/plan.md`
-   `conductor/tracks/<track_id>/index.md`
-   No `spec.md`, no `tracks.md` entry

```bash
/conductor:conductor-new-track
# OR with a description
/conductor:conductor-new-track "Add a dark mode toggle to the settings page"
```

### 3. Implement the Track

Once you approve the plan, run `/conductor:conductor-implement`. Your coding
agent then works through the `plan.md` file, checking off tasks as it completes
them.

**Updated Artifacts:**

-   `conductor/tracks.md` (Status updates)
-   `conductor/tracks/<track_id>/plan.md` (Status updates)
-   Project context files (Synchronized on completion)

```bash
/conductor:conductor-implement
```

During implementation, you can also monitor, revert, or review work using the
following commands:

*   **Check status**: Get a high-level overview of your project's progress.

    ```bash
    /conductor:conductor-status
    ```

*   **Revert work**: Safely undo a feature, phase, or a specific task.

    ```bash
    /conductor:conductor-revert
    ```

*   **Review work**: Review completed work against guidelines and the plan.

    ```bash
    /conductor:conductor-review
    ```

--------------------------------------------------------------------------------

## 📋 Commands Reference

Command                          | Description                                                                             | Generated Artifacts
:------------------------------- | :-------------------------------------------------------------------------------------- | :------------------
`/conductor:conductor-setup`     | Scaffolds the project and sets up the Conductor environment. Run this once per project. | `conductor/product.md`<br>`conductor/product-guidelines.md`<br>`conductor/tech-stack.md`<br>`conductor/workflow.md`<br>`conductor/tracks.md`<br>optional `conductor/linear.md` + CLI scripts
`/conductor:conductor-new-track` | Starts a new feature or bug track. File-based: `spec.md` + `plan.md`. Linear-first: issue as spec + pointer track. | File-based: `spec.md`, `plan.md`, `tracks.md`. Linear-first: Linear issue, pointer `metadata.json`, `plan.md`
`/conductor:conductor-implement` | Executes the tasks defined in the current track's plan.                                 | `plan.md` (and `tracks.md` when file-based; Linear status when Linear-first)
`/conductor:conductor-status`    | Displays the current progress of tracks.                                                | Reads `tracks.md` and/or `tracks/*/metadata.json` + Linear status
`/conductor:conductor-revert`    | Reverts a track, phase, or task by analyzing git history.                               | Reverts git history (optional Linear comment; no auto-cancel)
`/conductor:conductor-review`    | Reviews completed work against guidelines and the plan (or Linear AC).                  | Reads `plan.md`, styleguides; Linear-first also runs label review

--------------------------------------------------------------------------------

## 🔗 Optional Linear-first

Conductor stays file-based unless the project has `conductor/linear.md`.

During setup, you can **skip** Linear (default) or **enable** it. Enabling writes
team identity and a label taxonomy into `conductor/linear.md` and copies:

- `scripts/linear_cli.py` — `get-issue`, `list-sub-issues`, `set-state`, `comment`
- `scripts/linear_create_issue.py` — create issues when MCP is unavailable

**Transport ladder:** Linear MCP (Cursor plugin / Claude Linear connector) →
CLI (`LINEAR_API_KEY`) → ask the user. Conductor does not bundle or authenticate
MCP.

When Linear-first is on:

- New tracks **create or link** a Linear issue. The issue description is the spec.
- Track folders hold pointer `metadata.json` + `plan.md` only.
- Implement/review/status use Linear acceptance criteria and Linear issue status.
- **In Review** only when work is complete; **Done** only on explicit instruction.
- Label review reads Class / Surface (and optional Domain / Platform / Quality)
  from `linear.md`, not from a built-in product taxonomy.

Plugin skills `linear-issues`, `linear-review`, `linear-handoff`, and
`linear-label-review` activate only when `linear.md` exists.

CLI tests (no network):

```bash
uv run --with pytest pytest skills/conductor-setup/assets/linear/tests/
```

--------------------------------------------------------------------------------

## 💡 Best Practices for Task Corrections

When a task or phase in your Conductor project wasn't completed correctly, you
have three native recovery flows:

1.  **Agile In-Flight Corrections**: If you notice an implementation gap while
    the agent is actively coding, specify the fix directly in the chat. The
    agent will natively adapt its coding loop and verify the fix before
    finalizing the task.
2.  **Review Corrections (`/conductor:conductor-review`)**: If issues are caught
    after a task/phase is marked completed, run the review command. The review
    agent will audit changes, verify style guides, execute tests, and append a
    `Review Fixes` tracking phase to `plan.md` to resolve them.
3.  **Safe State Reversions (`/conductor:conductor-revert`)**: If a task
    implementation is fundamentally flawed and needs a complete reset, run the
    revert command. This rolls back specific Git commits safely and resets the
    task state back to pending `[ ]` so you can prompt a fresh approach.

--------------------------------------------------------------------------------

## 🚂 Getting Started (Natural Language Triggering)

Once Conductor is installed in your environment, you don't need to memorize
slash commands. You can interact with Conductor natively using natural language.
Your active agent will dynamically recognize your intent and execute the
corresponding Conductor protocol in the background:

-   **To Scaffold a Project**: > *"Let's create a new Conductor project"* or
    *"Run setup for Conductor"*
-   **To Plan a Feature**: > *"Let's start a new track to add a login screen"*
    or *"Create a plan for the dark mode track"*
-   **To Execute the Plan**: > *"Start implementing the active plan"* or
    *"Proceed with the implementation"*
-   **To Check Progress**: > *"How is our track progress going?"* or *"Show the
    current project status"*
-   **To Revert or Fix a Task**: > *"Revert the last completed task"* or *"Let's
    review the completed phase"*

--------------------------------------------------------------------------------

## 📂 Repository Structure

-   `/skills`: The protocol logic (`SKILL.md`) for each command, including optional `linear-*` skills.
-   `/skills/conductor-setup/assets/linear`: `linear.md` template and CLI scripts copied into projects that opt in.
-   `/rules`: Platform-specific operational rules files.

--------------------------------------------------------------------------------

## 🎓 Resources

-   [Antigravity Plugins Documentation](https://antigravity.google/docs/plugins):
    Official guidelines for using plugins in Antigravity.
-   [Claude Code Plugins Documentation](https://code.claude.com/docs/en/discover-plugins):
    Guidelines for managing plugins in Claude Code.
-   [GitHub Issues](https://github.com/gemini-cli-extensions/conductor/issues):
    Report bugs or request features.
-   The team gratefully acknowledges Keith Ballinger's original
    [.conductor](https://github.com/keithballinger/.conductor) project as the
    groundwork for this repository.

--------------------------------------------------------------------------------

## ⚖ License

-   License: [Apache License 2.0](LICENSE)
