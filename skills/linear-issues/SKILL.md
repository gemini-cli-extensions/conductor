---
name: linear-issues
description: >
  Human-convention workflow for linking agent work to Linear issues (PREFIX-XXX):
  resolve the issue at session start, keep branch/commit/PR traceability during
  work, and post a milestone comment plus status update before finishing. Use
  when the user mentions Linear, PREFIX-XXX, an issue URL, starting or finishing
  issue work, opening a PR for a ticket, or prefixes a prompt with
  "Linear: PREFIX-XXX". Activates only when conductor/linear.md exists.
  For Conductor tracks, see §6 — the Linear issue is the spec.
---

# Linear issues (PREFIX-XXX)

This skill uses **human convention**, not hooks: the human (or prompt) names the
issue; the agent reads it, keeps git/PR traceability, and updates Linear at
milestones via MCP when authenticated.

**Activate only when** `conductor/linear.md` exists in the project. If it is
absent, do not follow this skill — Conductor is in file-based SDD
(`spec.md` / `tracks.md`).

**Workspace:** read `conductor/linear.md` in the **project** (not this plugin)
for team name, team id, and issue prefix. Never hard-code a prefix or workspace.

## Epics and sub-issues (Linear model)

In Linear, an **epic is an issue with sub-issues** — not a separate object type like a
project or initiative.

| Concept | What it is | MCP / fields |
|---------|------------|--------------|
| **Epic** | A parent **issue** that groups child work | Has sub-issues; list children by parent id |
| **Sub-issue** | A regular issue whose **parent** is another issue | `get_issue` → `parent`; create/update with `parentId` |
| **Project** | Release / product grouping — orthogonal to parent-child | Orthogonal to epics |

**Agent rules:**

- Say **parent epic** or **epic issue** when you mean the parent PREFIX-XXX that owns
  sub-issues. Do not treat "epic" as a synonym for **project**.
- When fetching context, if `get_issue` returns a `parent`, note it. If the
  current issue has children, list them.
- **Every epic has a Conductor track (track check).** An epic **must** have a
  corresponding **epic track** — a `conductor/tracks/*/metadata.json` whose
  `linear` is the epic id. Before starting sub-issue work, read the sub-issue's
  parent, search the tracks for that id, and open an epic track first if it is
  missing.
- A sub-issue's parent epic is the issue's Linear `parent` — read it from
  `get_issue`, not from a duplicated `metadata.json` field.

## Creating issues (default status)

When creating a new Linear issue (MCP `save_issue` with no `id`, or
`scripts/linear_create_issue.py`):

| Kind | Default `state` | Rule |
|------|-----------------|------|
| **Top-level** (no `parentId`) | **`Triage`** | Always, unless the user names another status in the same turn. |
| **Sub-issue** (`parentId` set) | **`Backlog`** | Always, unless the user names another status. Do **not** copy the parent's status and do **not** put sub-issues in Triage. |

**Hard rules:**

- Do not invent a non-Triage default for top-level issues just because the work
  feels ready.
- Sub-issues are queue work under a parent — park them in **Backlog**.
- Same defaults apply to every create path: Linear MCP, Conductor new-track,
  handoff sub-issues, and the GraphQL CLI.

## 1. Session start (always)

Copy this checklist and complete before coding:

```
Linear start:
- [ ] Issue ID resolved (PREFIX-XXX from conductor/linear.md)
- [ ] Issue fetched or user pasted acceptance criteria
- [ ] Status set to In Progress (MCP or user confirms)
- [ ] Branch name includes the lowercase prefix and number (mention mismatch once if not — do not create/rename unless user asks)
```

### Resolve the issue ID

Check, in order:

1. **User prompt** — `Linear: ABC-12 — …` or a Linear URL
2. **Active Conductor track** — `conductor/tracks/<id>/metadata.json` → `linear`
3. **Branch name** — `{prefix}-12-*` (prefix lowercased, e.g. `abc-12-slug`)
4. **Recent commits** — `(ABC-12)` in subject

If still unknown, **ask once**: "Which Linear issue (PREFIX-XXX) does this work belong to?"

Do not implement feature work without a linked issue unless the user explicitly
says it is a chore with no ticket.

### Fetch context

When **Linear MCP** is connected, fetch the issue and restate:

- Title and current status
- Acceptance criteria / description
- Blockers, **parent epic** (if this is a sub-issue), labels
- Sub-issues under the current issue (if it is an epic)
- Parent epic (if this is a sub-issue): run the **track check**

If MCP is unavailable, use `scripts/linear_cli.py get-issue` or ask the user to
paste the issue title + acceptance criteria.

### Set In Progress

Move the issue to **In Progress** at start (MCP or remind the user). One status
change per session is enough.

### Prompt prefix (human convention)

```text
Linear: ABC-12 — Short title
Track: conductor/tracks/<track_id>/   # optional
```

Replace `ABC-` with the prefix from `conductor/linear.md`.

## 2. During work (traceability)

Read the prefix from `conductor/linear.md`. Examples below use `ABC-`.

| Artifact | Convention | Example |
|----------|------------|---------|
| Branch | `{prefix}-{num}-{short-slug}` | `abc-12-get-protocol` |
| Commit subject | `(ABC-XXX)` suffix or prefix | `feat(server): add get_protocol (ABC-12)` |
| PR title | `ABC-XXX: <imperative summary>` | `ABC-12: Serve get_protocol from the server` |
| PR body | Link + closes line | issue URL · `Closes ABC-12` |

**Do not** comment on Linear for every file save. Comment only at **milestones**
(phase done, PR opened, blocked, ready for review).

## 3. Session finish (before "done" or PR)

```
Linear finish:
- [ ] Milestone comment posted (summary, PR URL, how to verify)
- [ ] Status updated (In Review only once agent code work is done — committed, pushed, tests green; Done only on explicit user instruction)
- [ ] PR title/body include PREFIX-XXX
```

### Comment template

Use [reference.md](reference.md) → *Linear comment templates*. Minimum:

- What changed (1–3 bullets)
- PR link (if any)
- How to verify / test plan pointer (use the project's test command from `conductor/workflow.md`)

### Status transitions

| Situation | Linear status |
|-----------|---------------|
| Work started | In Progress |
| Agent code work done (committed + pushed, checks green, PR open if requested) | In Review |
| User explicitly says to close / mark Done | Done |
| Blocked | Blocked + comment explaining blocker |

**Hard rules (status changes):**

- **In Review** only when the agent's code work is actually **complete**: changes
  committed and pushed, tests for the touched surfaces green, finish comment
  posted, and the PR open when one was requested. Never set In Review with
  unpushed work, failing checks, or tasks still in flight.
- **Done** requires an **explicit user instruction in the current session**. A
  merged PR, a `Closes PREFIX-XXX` line, or a "Mark Done" plan task is **not**
  authorization — post the finish comment, leave the status at In Review, and ask.

If the user has not asked for a PR yet, post the finish comment and leave status at
**In Progress** — move to **In Review** only once the code work above is complete.

## 4. Linear MCP

- **Cursor:** Linear plugin. Authenticate in **Cursor Settings → MCP** before
  relying on fetch/update tools.
- **Claude Code:** account-level **claude.ai Linear connector**.
  Authorize once in claude.ai → Settings → Connectors.
- If MCP is unavailable, fall back **deterministically**: **Linear MCP →
  `scripts/linear_cli.py` (GraphQL + `LINEAR_API_KEY`) → human convention**.
  Use `linear_cli.py` for `get-issue`, `list-sub-issues`, `set-state`, `comment`.
  Exit `2` = no key (degraded); exit `1` = hard failure. See
  `conductor/linear.md`.
- **GraphQL fallback for issue creation:**
  `LINEAR_API_KEY=lin_api_... LINEAR_TEAM_NAME="Team" python scripts/linear_create_issue.py --title "…" --description-file body.md --label Bug`
  Prefer MCP when available so you can set `state: "Triage"` or `"Backlog"`.

## 5. Issue labels

Every issue should carry **2–4 labels** from orthogonal groups defined in
`conductor/linear.md` (not in this skill).

### Required

| Group | Pick | Source |
|-------|------|--------|
| **Class** | 1 | `linear.md` Class table (defaults: Bug, Feature, Improvement, Chore, Spec) |
| **Surface** | 1 | `linear.md` Surface → path map |

### Recommended

| Group | Pick | When |
|-------|------|------|
| **Domain** | 0–1 | Product-facing work, if the project defined Domain labels |
| **Platform** | 0–1 | Infra/cross-cutting, if defined |
| **Quality** | 0–1 | Primary quality goal, if defined |

### Agent behavior

- At **session start**, if the issue has no labels, **propose** Class + Surface
  (+ Domain) before coding, using the maps in `linear.md`.
- Map Conductor track type → Class: `feature` → Feature, `bug` → Bug,
  `chore` → Chore.
- Do not duplicate project/release names in labels.
- Do not invent another project's domains. If `linear.md` has empty
  Domain/Platform/Quality tables, skip those groups.

## 6. Conductor tracks (Linear-first)

A Conductor track is a **thin local execution artifact**, not a second copy of
the issue.

- **The Linear issue is the spec.** Do **not** write a `spec.md` copy.
- **The track directory holds only** a pointer `metadata.json` (`track_id`,
  `linear`, `linear_url`), the executable `plan.md`, and an `index.md` pointer.
  New tracks are **not** registered in `conductor/tracks.md`.
- **Commands:** `conductor-new-track` still knows the file-based four-file
  shape — **when `linear.md` exists, override it** using this section.
  Create/link the issue, write pointer metadata + `plan.md` only, post a
  track-opened comment.
- **Element sub-issues (optional):** one Linear sub-issue per phase as a child of
  the primary; annotate `plan.md` headings with `(PREFIX-YYY)`. The track still
  closes on the **primary** issue.

**Epics (track check):** an epic **must** have an epic track (`linear` = epic
id), one phase per sub-issue. Before starting sub-issue work, confirm the parent
epic has an epic track.

**If a command asks for `spec.md` or a `tracks.md` entry while Linear-first is
on, refuse that part** and follow this contract instead.

## 7. Pair with other skills

| When | Also use |
|------|----------|
| Reviewing a PREFIX-XXX change | **linear-review** |
| Park in-flight work | **linear-handoff** |
| Conductor implement / new track | this §6 |
| Commit message only | user rule |

Templates and examples: [reference.md](reference.md).
