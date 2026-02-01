# Canonical Setup/NewTrack UX

This document defines canonical user-facing messages and metadata fields to align adapter behavior.

## Canonical Setup Messages

### Start
- "Welcome to Conductor. I will guide you through the following steps to set up your project: ..."

### Resume (setup_state.json)
- "Resuming setup: The Product Guide (`product.md`) is already complete. Next, we will create the Product Guidelines."
- "Resuming setup: The Product Guide and Product Guidelines are complete. Next, we will define the Technology Stack."
- "Resuming setup: The Product Guide, Guidelines, and Tech Stack are defined. Next, we will select Code Styleguides."
- "Resuming setup: All guides and the tech stack are configured. Next, we will define the project workflow."
- "Resuming setup: The initial project scaffolding is complete. Next, we will generate the first track."
- When complete: "The project has already been initialized. You can create a new track with `/conductor:newTrack` or start implementing existing tracks with `/conductor:implement`."

### Brownfield Warning
- "WARNING: You have uncommitted changes in your Git repository. Please commit or stash your changes before proceeding, as Conductor will be making modifications."

## Canonical NewTrack Messages

- "I'll now guide you through a series of questions to build a comprehensive specification (`spec.md`) for this track."
- "Now I will create an implementation plan (plan.md) based on the specification."
- "The track for \"<Track Description>\" has been created."

## Metadata Fields (metadata.json)

Required:
- `track_id` (string)
- `description` (string)
- `type` ("feature" | "bug")
- `status` ("new" | "in_progress" | "completed" | "cancelled")
- `created_at` (ISO 8601)
- `updated_at` (ISO 8601)

Optional:
- `vcs` (object) when Git integration is enabled:
  - `enabled`, `provider`, `mode`, `base_branch`, `branch`, `worktree_path`, `created_at`

## Notes
- All adapters should emit the same high-level messages even if their command syntax differs.
- Track ID formatting should be consistent with the canonical template guidance to avoid UX drift.
