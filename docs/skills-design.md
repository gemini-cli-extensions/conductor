# Skills Integration Design

## Overview

This document describes the design for integrating *Agent Skills** into the Conductor framework. Skills - introduced by [Claude](https://code.claude.com/docs/en/skills) - are folders containing a `SKILL.md` file, installed to `conductor/skill-set/<skill-name>/` in the project root. They can be invoked as custom slash commands (e.g., `/gcp-deploy`) during development or used by the model to complete tasks.

Conductor maintains an opinionated **catalog** (`conductor/skill-set/catalog.md`) — a curated list of recommended Skills with their external download URLs. The actual Skill implementations are developed and hosted by 3rd parties (each in their own repository). During `/conductor:setup` and `/conductor:newTrack`, Conductor reads the catalog, recommends the relevant Skills based on the detected or required tech stack, and downloads the selected ones on demand.

---

## Motivation

Before this feature, teams using Conductor had to manually find and install Claude Code Skills for common tasks. With Skills integration:

- Teams get a curated set of AI-powered expert helpers on day one of setup.
- Skills are tailored to the detected or required stack (GCP skills are only offered for GCP projects).
- The catalog is extensible — new categories can be added without changing the setup command logic.

---

conductor/skill-set/
└── catalog.md    # Curated list of skills defined in YAML frontmatter

### catalog.md

The catalog is defined in `catalog.md` using YAML frontmatter. The `skills` list contains entries for each skill:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The name of the skill |
| `description` | string | One-line description shown to the user during selection |
| `url` | string | Raw GitHub URL to download `SKILL.md` |
| `alwaysRecommend` | boolean | (Optional) If `true`, recommended regardless of detected stack |
| `detectSignals` | object | (Optional) Signals that trigger recommendation for conditional skills |

`detectSignals` sub-keys (all optional):
- `files` — filenames whose presence in the project root triggers the skill
- `dependencies` — substring match against `package.json`, `requirements.txt`, or `go.mod`
- `keywords` — strings to search for in `conductor/tech-stack.md`

### Installation Path
Skills can be discovered from three tiers:

- **Global Tier**: `~/.agents/commands/` — Available across all projects for the current user.
- **Workspace Tier**: `.agents/commands/` at the repository root — Available to everyone working in the repository.
- **Project Tier**: `.agents/commands/` within a specific subdirectory — Scoped to a specific sub-project or package.

Conductor installs Skills at the **Workspace Tier** (`.agents/commands/<skill-name>/SKILL.md`) to ensure they are committed to version control and shared across the entire team.

---

## Installation

Skills installation is **Phase 2.6** of `/conductor:setup`, inserted between Phase 2.5 (Workflow selection) and Phase 2.7 (Finalization/Index generation). It is also integrated into `/conductor:newTrack` if Skills are deemed helpful for that specific track.

For each selected skill, the setup command executes:

mkdir -p .agents/commands/<skill-name>
curl -fsSL "https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/<skill-name>/SKILL.md" \
  -o ".agents/commands/<skill-name>/SKILL.md" 

### Detection Logic - GCP Example

The setup command detects GCP usage by checking for any of the following signals:

**File signals** (file presence in project root):
Example: `app.yaml`, `cloudbuild.yaml`, `.gcloudignore`, `Dockerfile` containing `gcr.io`

**Dependency signals** (substring match):
Example: `package.json` dependencies: `@google-cloud/`, `requirements.txt` entries: `google-cloud-`, `go.mod` entries: `cloud.google.com/go`

**Keyword signals** (in `conductor/tech-stack.md`):
Example: `Cloud Run`, `GKE`, `App Engine`, `Firestore`, `BigQuery`, `Pub/Sub`, `Google Cloud`, `GCP`

If any GCP signal is found, the GCP skills category is offered to the user.

### User Interaction

```
I will now help you select Agent Skills to install for this project.
Skills are Claude Code slash commands installed to .claude/commands/.

[Always Recommended]
 1. commit             - Generate a conventional commit message from staged changes
 2. pr-description     - Write a PR title and description from branch diff
 3. code-review        - Structured code review with severity levels
 4. changelog          - Generate a CHANGELOG entry from recent commits
 5. write-tests        - Generate unit/integration tests for a file or function
 6. fix-failing-tests  - Diagnose and fix failing tests
 7. document           - Add docstrings or JSDoc to selected code
 8. readme-update      - Update README to reflect recent changes
 9. security-review    - OWASP-focused security review
10. dependency-audit   - Identify outdated or vulnerable dependencies

[GCP (detected: cloudbuild.yaml, @google-cloud/* dependency)]
11. gcp-deploy         - Deploy to Cloud Run, GKE, or App Engine
12. gcp-cloudbuild     - Generate or update Cloud Build pipelines
13. gcp-terraform      - Generate GCP Terraform resource configs
14. gcp-iam            - Review and generate IAM policies (least-privilege)
15. gcp-monitoring     - Set up Cloud Monitoring alerts and dashboards
16. gcp-pubsub         - Design Pub/Sub schemas and generate client code
17. gcp-firestore      - Design Firestore schemas and optimize queries
18. gcp-bigquery       - Generate and optimize BigQuery schemas and SQL
19. gcp-secret-manager - Migrate secrets to Secret Manager

How would you like to proceed?
A) Install all recommended skills
B) Select specific skills (enter numbers separated by commas)
C) Skip skills installation
```

### Resume Support

The `setup_state.json` resume chain includes the Skills phase:

| `last_successful_step` | Resume at |
|------------------------|-----------|
| `2.5_workflow` | Section 2.6 (Skills) |
| `2.6_skills` | Phase 3.0 (Track generation) |

---

## Review Integration

The code review process should be aware of the capabilities available through installed skills.

### `commands/conductor/review.toml`

The review configuration will be updated to check for relevant installed skills (e.g., GCP-related skills) during the code review process.

- **Detection**: Check `.agents/commands/` for the presence of known skills.
- **Contextual Feedback**: If a relevant skill is found (e.g., `gcp-deploy`), the review agent can provide more specific feedback for deployment-related changes.

---

## Example of Available Skills Reference

### Workflow

| Skill | Command | Description |
|-------|---------|-------------|
| Generate Commit Message | `/commit` | Reads `git diff --staged`, generates a conventional commit message following the project's commit strategy from `conductor/workflow.md` |
| PR Description | `/pr-description` | Reads branch diff vs main, writes a PR title and body |
| Code Review | `/code-review` | Structured review with Critical/High/Medium/Low findings, checks against `conductor/code_styleguides/` |
| Changelog | `/changelog` | Generates a CHANGELOG entry from `git log` since last tag |

### Testing

| Skill | Command | Description |
|-------|---------|-------------|
| Write Tests | `/write-tests` | Generates unit and integration tests following the project's test framework from `conductor/tech-stack.md` |
| Fix Failing Tests | `/fix-failing-tests` | Takes failing test output, diagnoses root cause, proposes fix |

### Documentation

| Skill | Command | Description |
|-------|---------|-------------|
| Document | `/document` | Adds docstrings, JSDoc, or type hints to specified code |
| README Update | `/readme-update` | Updates README sections based on recent code changes |

### Security & Quality

| Skill | Command | Description |
|-------|---------|-------------|
| Security Review | `/security-review` | OWASP Top 10 focused review, checks for secrets in diff |
| Dependency Audit | `/dependency-audit` | Identifies outdated, deprecated, or CVE-flagged dependencies |

### GCP

| Skill | Command | Description |
|-------|---------|-------------|
| GCP Deploy | `/gcp-deploy` | Step-by-step deploy to Cloud Run, GKE, or App Engine |
| Cloud Build | `/gcp-cloudbuild` | Generate or update `cloudbuild.yaml` for CI/CD pipelines |
| GCP Terraform | `/gcp-terraform` | Generate Terraform configs for GCP resources (VPC, Cloud Run, GKE, IAM) |
| GCP IAM | `/gcp-iam` | Review bindings and generate least-privilege IAM policies |
| GCP Monitoring | `/gcp-monitoring` | Generate alert policies, dashboards, and SLO configs |
| Pub/Sub | `/gcp-pubsub` | Design Pub/Sub message schemas and generate publisher/subscriber code |
| Firestore | `/gcp-firestore` | Design Firestore collections, indexes, and optimize queries |
| BigQuery | `/gcp-bigquery` | Generate schemas, partition/clustering strategies, and optimized SQL |
| Secret Manager | `/gcp-secret-manager` | Migrate env vars to Secret Manager and generate typed access code |

---



## Extending the Catalog

To add a new skill to the catalog:

1. Publish the Skill in an external repository with a `SKILL.md` at the root (or a known path).
2. Add an entry to the `skills` list in `skills/catalog.md` (via YAML frontmatter) with the public raw `url`, `detectSignals` for conditional skills, or `"alwaysRecommend": true` for universal ones.
3. If introducing a new category with custom detection logic, update Phase 2.6 in `commands/conductor/setup.toml`.

The Skill implementation itself lives entirely outside this repository.

Categories planned for future releases: `aws`, `azure`, `mobile` (iOS/Android), `data-science`.

---

## File Changes Summary

| File | Change |
|------|--------|
| `docs/skills-design.md` | New — this document |
| `skills/catalog.md` | New — curated skill list defined in YAML frontmatter |
| `commands/conductor/setup.toml` | Modified — Phase 2.6 added, resume chain updated |
| `commands/conductor/review.toml` | Modified — Checks for relevant installed Skills (e.g., GCP) |


The actual `SKILL.md` implementations are **not** in this repository. They are hosted externally (see the `url` field in each catalog entry).


---

## Appendix: Authoring Skills

For complete details, see [Creating Agent Skills](https://geminicli.com/docs/cli/creating-skills/).

### Getting Started: `skill-creator`

The recommended way to create a new skill is to use the built-in skill `skill-creator`:

```bash
skill-creator
```

Provide a prompt like "create a new skill called 'code-reviewer'". This will generate:
1. A new directory (e.g., `code-reviewer/`)
2. `SKILL.md` with required metadata
3. Resource directories: `scripts/`, `references/`, `assets/`

### Manual Creation

To create a skill manually:
1. Create a directory for your skill.
2. Create a `SKILL.md` file inside it.

#### Folder Structure

While `SKILL.md` is the only requirement, the recommended structure is:

```
my-skill/
├── SKILL.md       # (Required) Instructions and metadata
├── scripts/       # (Optional) Executable scripts
├── references/    # (Optional) Static documentation
└── assets/        # (Optional) Templates and other resources
```

#### SKILL.md Format

The file uses YAML frontmatter for metadata and Markdown for instructions.

```markdown
---
name: my-skill-name
description: A description of what the skill does and when the agent should use it.
---
# My Skill Name

This skill guides the agent in completing specific tasks.

## Workflow
1. Step one...
2. Step two...
```


