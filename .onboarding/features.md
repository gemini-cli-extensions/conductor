# Conductor Features

Conductor is a Gemini CLI extension that enables Context-Driven Development by functioning as a proactive project manager. It guides an agent to specify, plan, and implement software while maintaining strict protocol and context.

## Core Features
1. **Project Setup (`/conductor:setup`)**:
   - Analyzes whether a project is Greenfield (new) or Brownfield (existing).
   - Interactively generates core project context: Product Vision (`product.md`), Product Guidelines (`product-guidelines.md`), Tech Stack (`tech-stack.md`), and Workflow (`workflow.md`).
   - Recommends and installs relevant Agent Skills based on defined tech stacks (e.g., Firebase, GCP DevOps).
   
2. **Track Management (`/conductor:newTrack`)**:
   - Organizes work into **Tracks** (features or bug fixes).
   - Automatically generates a specification (`spec.md`) and an actionable step-by-step plan (`plan.md`) incorporating tasks and sub-tasks.
   
3. **Implementation (`/conductor:implement`)**:
   - Executes the track defined in the `plan.md` file.
   - Follows defined workflows (like TDD).
   - Pauses for manual phase verification (Checkpointing Protocol) as dictated by `workflow.md`.
   - Checks off tasks iteratively.

4. **Status Checking (`/conductor:status`)**:
   - Provides an aggregate view of project progress by reading the `conductor/tracks.md` registry and active tracks.

5. **Revert and Revise (`/conductor:revert` & `/conductor:review`)**:
   - Reverts specific work blocks (track, phase, or task) directly using git history analysis.
   - Reviews completed code against defined guidelines and specifications.
