# Conductor Code Maps

Below is an overview of the directory structure and the core responsibilities of the files in the Conductor repository.

## Repository Root
- **`gemini-extension.json`**: The core manifest defining the extension name ("conductor"), version, context file (`GEMINI.md`), and plan directory (`conductor`).
- **`README.md`**: Main instructions, workflow guide, and CLI command reference for the end-user.
- **`GEMINI.md`**: Defines the "Universal File Resolution Protocol" that teaches the Gemini CLI agent how to resolve standardized files (e.g., `spec.md`, `plan.md`) dynamically within a user's initialized workspace.

## `commands/conductor/`
Houses the prompt logic for the extension's commands:
- **`setup.toml`**: The massive bootstrapping prompt. Contains complex state-machine logic for scanning brownfield vs greenfield projects and interactively generating project context.
- **`newTrack.toml`**: Instructs the agent on structuring `tracks/<id>/spec.md` and `plan.md` into phased tasks.
- **`implement.toml`**: The worker prompt that commands the agent to read current plans and execute code modifications strictly according to the tasks and specs.
- **`review.toml`**: Validates completed implementation against `product-guidelines.md` and the current `plan.md`.
- **`status.toml`**: Summarizes the overarching `conductor/tracks.md`.
- **`revert.toml`**: Understands logical chunks of completion based on git commit history.

## `policies/`
- **`conductor.toml`**: Elevates tool privileges securely. Allows tools like `replace` and `write_file` in "plan" mode exclusively for the `conductor/` subdirectory.

## `skills/`
- **`catalog.md`**: Contains a structured catalog of available sub-skills with detection signals (e.g., keywords or dependencies). During `setup`, Conductor reads this to recommend targeted skills to the user.

## `templates/`
These files act as the foundational assets cloned into a user's repository during `/conductor:setup`.
- **`workflow.md`**: Contains standard definitions for workflows like Test-Driven Development (TDD), commit cadence, and phase-verification checkpoint protocols.
- **`code_styleguides/`**: A library of language-specific style guides presented interactively during setup.
