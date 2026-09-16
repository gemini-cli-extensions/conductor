---
name: linear-review
description: >
  Canonical review protocol for any PREFIX-XXX change — the review intent is the
  Linear issue's acceptance criteria. Derive the diff scope from branch vs base
  (or a track's plan.md SHAs), load repo standards (code_styleguides + workflow.md
  Quality Gates), review the diff, run linear-label-review, map findings back to
  the issue, and drive the Linear status + finish comment. Use when finishing
  or reviewing Linear-linked work. Activates only when conductor/linear.md exists.
  Pairs with linear-issues and linear-label-review.
---

# Linear review

The **canonical review protocol** for any PREFIX-XXX change when Linear-first is
on (`conductor/linear.md` exists). Review intent comes from the **Linear issue's
acceptance criteria** — the single source of the spec — and close-out updates
the Linear issue. It applies whether or not the work has a `conductor/tracks/`
directory.

This skill **frames** the diff against the Linear issue, reviews it, runs
`linear-label-review`, then maps the results back onto the issue.

If `conductor/linear.md` is absent, do not use this skill; use **conductor-review**
against `spec.md` / `plan.md`.

## When this runs

- **On demand:** "review ABC-12", "review this branch / PR", "is this ready to
  merge?", "review my changes" (when Linear-first is on).
- **At session finish** (per **linear-issues** §3) for any non-trivial change
  against a PREFIX-XXX issue.
- **Via conductor-review** — that wrapper derives the revision range from the
  track's `plan.md` SHAs and adds track archival, then delegates here.

## Protocol

1. **Resolve the issue & scope.**
   - Resolve PREFIX-XXX via **linear-issues** §1 (prompt → branch name → recent
     commit subject). If still unknown, ASK once.
   - Derive the diff range from **branch vs base** (default `origin/main`):
     `git fetch origin main` then review `git diff origin/main...HEAD`. For
     uncommitted work, review the working tree. Confirm the range if ambiguous.

2. **Load the review intent (the issue is the spec).**
   - Fetch the **current** issue via Linear MCP — title, description,
     **acceptance criteria**, current status, labels, parent. If the
     status/criteria no longer match what was built, pause and confirm.
   - If MCP is unavailable, use `scripts/linear_cli.py get-issue` or ask the user to
     paste the acceptance criteria.

3. **Load standards (repo-wide).**
   - `conductor/code_styleguides/*.md` — violations here are **High** severity.
   - The **Quality Gates** in `conductor/workflow.md` — they apply to every
     change (project test command, coverage target, no secrets).

4. **Review the diff.** Against the issue's acceptance criteria and the
   styleguides: correctness, tests for new logic, no unrelated edits, no
   secrets.

5. **Map findings back to the issue.** Check, against PREFIX-XXX:
   - **Acceptance-criteria compliance** — did it build what the issue asked?
   - **Test presence** — new logic has tests; the project test command on the
     relevant files is green.
   - **Quality-Gate conformance** — styleguides, coverage, no secrets.

6. **Review Linear labels.** Invoke **`linear-label-review`** on the same
   diff/range. Confirm before applying via Linear MCP.

7. **Decide & act.** If there are Critical/High issues, recommend fixing them
   first; offer to apply the fixes, stop for a manual fix, or proceed. Then
   drive the issue **close-out** (below).

## Close out

- **Post the finish/PR-ready comment** to PREFIX-XXX: what changed (1–3 bullets),
  the PR link if any, how to verify (project test command).
- **Update status** — **In Review** only when the agent's code work is complete
  (committed + pushed, review findings resolved or accepted, checks green, PR
  open when one was requested). **Never set Done from this skill** unless the
  user explicitly instructs it in the current session. See **linear-issues** §3.
- **Apply the label delta** from step 6.
- Confirm the PR title is `PREFIX-XXX: …` and the body links the issue
  (`Closes PREFIX-XXX`).

## What this skill does not do

- It does not redefine `linear-label-review` — it sequences it and binds the
  results to the Linear issue.
- It does not create or archive Conductor tracks.
- It does not replace **conductor-review** for file-based (no `linear.md`) projects.

## Pairs with

| Need | Skill |
|------|-------|
| Resolve PREFIX-XXX, finish comment, status, labels taxonomy | **linear-issues** |
| Label add/remove delta | **linear-label-review** |
| Track lifecycle (file-based) | **conductor-review** |
