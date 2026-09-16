# Linear handoff — reference

Team identity: `conductor/linear.md` in the **project**. Replace `ABC-` with
that file's issue prefix.

## Handoff issue body (copy-paste)

```markdown
## Handoff — ABC-12 (<title>)

**Parent:** ABC-12  (epic: ABC-10)  ·  **From:** <giver>  →  **To:** <receiver>
**Runtime:** <from> → <to>  ·  **Conductor track:** conductor/tracks/<id>/

### Resume point (do this next)
- <the single, concrete next action>

### State
- **Branch:** abc-12-slug @ a1b2c3d  (pushed: yes)
- **PR:** none
- **Done:** <plan.md [x]>
- **In progress:** <task left mid-flight>
- **Uncommitted / local-only:** none

### Verification state
- **Green:** <project test command>
- **Not yet verified / known-red:** <what to re-run>

### Open decisions / blockers
- None

### Issue state at handoff
- **Acceptance criteria:** <issue URL>
- **Status / labels / assignee at handoff:** In Progress · Feature, <Surface>

### Context notes
- …

---
*Receiver: acknowledge → re-read parent → verify branch@SHA → resume → close **this handoff sub-issue only**.*
```

## Comment templates

### Pointer on the PARENT issue (giver)

```markdown
**Handoff out (ABC-12)** → ABC-20

Parked at: <resume point> (pushed on `abc-12-slug` @ a1b2c3d).
Baton: ABC-20. Parent stays In Progress — **not** Done.
```

### Acknowledge on the HANDOFF issue (receiver)

```markdown
**Picking up (ABC-20)**

Assigned to me. Re-reading ABC-12, then verifying `a1b2c3d` before I continue.
```

### Close the HANDOFF baton only

```markdown
**Pickup verified — closing baton (ABC-20)**

Re-read ABC-12 — criteria/status unchanged. Checked out `a1b2c3d`; named tests green; resuming on ABC-12.
Handoff baton spent → Done. Verified after closing: ABC-12 still In Progress — parent **not** closed.
```

If the parent *was* auto-closed:

```markdown
Note: closing the baton auto-completed ABC-12 (Linear closes a parent when its last
sub-issue closes). Reverted to In Progress — the work is not finished.
```

## MCP shapes

- **Create the handoff sub-issue** — `save_issue` with `parentId`, `state: "Backlog"`,
  labels `["Handoff", "Chore", "<parent Surface>"]`.
- **Pointer comment on parent** — `save_comment` on the parent.
- **Parent status (giver only)** — `In Progress` or `Blocked` — **never** Done.
- **Acknowledge / close baton only** — `save_issue` Done on the **handoff id**, not the parent.
- **Receiver re-read** — `get_issue` on the parent immediately after closing the baton.
