# Linear workspace

Skills in `linear-issues`, `linear-review`, `linear-handoff`, and
`linear-label-review` read this file for team identity and label taxonomy.
Change it here, not in each skill.

Linear-first is **on** when this file exists. Do not commit API keys.

| Field | Value |
|-------|-------|
| **Workspace** | `{{WORKSPACE}}` |
| **Team name** | `{{TEAM_NAME}}` |
| **Team id** | `{{TEAM_ID}}` |
| **Issue prefix** | `{{PREFIX}}` |
| **Issue URL** | `https://linear.app/{{WORKSPACE}}/issue/{{PREFIX}}XXX/…` |

**Fallback:** `LINEAR_API_KEY` (Linear → Settings → API → Personal API keys)
powers `scripts/linear_cli.py` when the Linear MCP is unavailable.
`LINEAR_TEAM_NAME` (or `--team`) is required by `scripts/linear_create_issue.py`.

## Label taxonomy

Every issue should carry **2–4 labels** from orthogonal groups.
`linear-label-review` reads this section.

### Class (required — pick 1)

| Label | Use when |
|-------|----------|
| Feature | New capability |
| Bug | Defect / regression |
| Improvement | Enhancement of existing behavior |
| Chore | Tooling, refactor, maintenance |
| Spec | Planning / specification-only |

### Surface (required — pick 1)

Map the **dominant changed path** to a Surface label. Replace the examples
with this project's paths during setup.

| Surface label | Repo path |
|---------------|-----------|
| `{{SURFACE_EXAMPLE_NAME}}` | `{{SURFACE_EXAMPLE_PATH}}` |

### Domain (optional — pick 0–1)

| Domain label | Use when |
|--------------|----------|
| *(none yet)* | Add product-area labels here if the team uses them |

### Platform (optional — pick 0–1)

| Platform label | Use when |
|----------------|----------|
| CI & Dev Environment | CI, scripts, dependency files, Conductor/Linear automation |
| MCP / Claude Code | MCP registration, Claude/Cursor connectors |
| Security | Auth, secrets, path handling |

### Quality (optional — pick 0–1)

| Quality label | Use when it is the **primary** goal |
|---------------|--------------------------------------|
| Performance | Speed / resource use |
| Usability | Human interaction quality |
| AI Output Quality | Agent/LLM output quality |
| Code Quality | Structure, tests, maintainability |
