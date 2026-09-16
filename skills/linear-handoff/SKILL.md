---
name: linear-handoff
description: >
  Structured handoff of in-flight work via a Linear handoff sub-issue (PREFIX-XXX):
  when a session must stop mid-task, hand off between agents or between an agent
  and a human, park on a blocker, or change shift/runtime, the giver creates a
  handoff sub-issue under the in-flight issue (or its epic) and the receiver
  acknowledges → re-reads the parent → verifies state → resumes → closes only
  that handoff sub-issue (never the parent, epic, or other work issues). Use when
  the user says "hand off", "park this", "pick up where X left off". Activates
  only when conductor/linear.md exists. Pairs with linear-issues.
---

# Linear handoff (PREFIX-XXX)

The coordination primitive for parking in-flight work and passing the baton so
the next agent or person resumes cold — without archaeology.

**Activate only when** `conductor/linear.md` exists. Read prefix and team from
that file.

If the work has **no** Linear issue, do not use this skill — park in the track's
`plan.md` (and a `HANDOFF.md` in the track directory if the project has a
file-based handoff convention).

## Three principles (do not violate)

1. **Baton, not diary.** A **handoff sub-issue** is a discrete transfer. **Only that
   baton** closes — the moment the receiver acknowledges and verifies pickup —
   **not** when the feature ships, and **not** the parent work issue.
2. **Point, don't duplicate.** The **parent issue** (scope/acceptance criteria)
   and the **Conductor `plan.md`** stay the source of truth. The handoff captures
   only the **transfer delta**.
3. **Never close work issues as part of a handoff.** Allowed parent transitions
   during handoff are only **In Progress** or **Blocked**. Closing the real work
   is **linear-issues** / **linear-review** after the work actually finishes.
   **Not closing the parent yourself is not enough — Linear can close it for
   you** when the baton is the parent's last open sub-issue. Re-read the parent
   after closing the baton.

## When to create a handoff

- **Context exhaustion** — a session is about to end with a task half-done.
- **Agent → human** — blocked on a decision or credential only a human can resolve.
- **Human → agent** — parking work for an agent to continue from a known point.
- **Runtime switch** — e.g. Cursor ↔ Claude Code.
- **Blocked-and-parking** — an upstream dependency stalls the work.

If the work simply *finished*, this is not a handoff — close out with
**linear-issues** / **linear-review** instead.

## Where the handoff issue lives

| Field | Convention |
|-------|-----------|
| **Parent** | The in-flight `PREFIX-XXX` being handed off. |
| **Title** | `Handoff: PREFIX-XXX — <one-line resume point>` |
| **Labels** | **Handoff** + Class **Chore** + the parent's **Surface** label (from `linear.md`) |
| **Assignee** | The named receiver. Leave unassigned only for pool pickup. |
| **Handoff issue status** | **Backlog** (sub-issue default). |
| **Parent issue status** | Stays **In Progress**, or **Blocked** when parking on a dependency. **Never** Done / Cancelled. |

## Giver protocol (before you stop)

1. **Make the tree shareable.** Commit and **push** the branch.
2. **Update the source of truth first.** Flip `plan.md` markers and record task
   SHAs; set the parent to **In Progress** or **Blocked** only.
3. **Create the handoff sub-issue** (`parentId: "PREFIX-XXX"`, `state: "Backlog"`,
   labels `Handoff` + `Chore` + parent Surface). Fill the body template. Do **not**
   mark the baton Done as the giver.
4. **Assign** to the receiver — or leave unassigned for pool pickup.
5. **Set parent status** — In Progress or Blocked. Do **not** close the parent.
6. **Post a pointer comment on the parent** linking the handoff sub-issue.

## Receiver protocol (on pickup)

1. **Acknowledge** — comment "Picking up" on the handoff issue and assign it.
2. **Re-read the parent** — fetch the current parent issue; confirm acceptance
   criteria and status still match.
3. **Verify state** — check out the branch at the recorded SHA; named tests green.
4. **Resume** from the handoff's **Resume point**. The parent stays open.
5. **Close only the handoff baton** — mark **that** Handoff-labelled sub-issue
   **Done**. Never mark the parent Done/Cancelled here.
6. **Re-read the parent after closing the baton — always.** If Linear
   auto-completed it, `save_issue` it back to **In Progress** (or **Blocked**) and
   say so.

## Handoff body template

```markdown
## Handoff — PREFIX-XXX (<title>)

**Parent:** PREFIX-XXX  (epic: PREFIX-YYY)  ·  **From:** <giver>  →  **To:** <receiver / unassigned>
**Runtime:** <e.g. Claude Code → Cursor>   ·  **Conductor track:** conductor/tracks/<id>/

### Resume point (do this next)
- <the single, concrete next action>

### State
- **Branch:** prefix-xxx-slug @ <sha7>  (pushed: yes/no)
- **PR:** #NNN (draft) / none
- **Done:** <point at plan.md [x] markers>
- **In progress:** <the task left mid-flight>
- **Uncommitted / local-only:** <none | exactly what & where>

### Verification state
- **Green:** <project test command>
- **Not yet verified / known-red:** <what the receiver must (re)run>

### Open decisions / blockers
- <decision pending / blocker>

### Issue state at handoff
- **Acceptance criteria:** <link or key lines, verbatim>
- **Status / labels / assignee at handoff:** <…>

### Context notes
- <env/stack quirks>

---
*Receiver: acknowledge → re-read parent → verify branch@SHA → resume → close **this handoff sub-issue only**. Never Done/Cancelled the parent.*
```

## What this skill does not do

- It does **not** close the parent, epic, or siblings — only the baton.
- It does **not** review the code (that's **linear-review**).
- It does **not** replace `plan.md`.
- If Linear MCP is unavailable, post the filled template as a comment on the
  parent and create the sub-issue when MCP returns. Still do **not** close the
  parent.

Templates: [reference.md](reference.md).
