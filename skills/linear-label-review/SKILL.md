---
name: linear-label-review
description: >
  Review a completed track or branch diff and recommend the Linear issue's
  labels (Class / Surface / Domain / Platform / Quality) from the project's
  conductor/linear.md taxonomy, then apply or list the add/remove delta. Use
  after implementing work, when finishing a track or PR, or whenever the user
  asks to check, fix, or suggest Linear labels. Activates only when
  conductor/linear.md exists. Pairs with linear-issues.
---

# Linear label review

Map the **actual diff** onto the **project** label taxonomy in
`conductor/linear.md` so the Linear issue's labels reflect what shipped.
This skill *applies* that taxonomy against changed files. It does not
define product-specific domains.

**Activate only when** `conductor/linear.md` exists.

## When this runs

- **Automatically:** a step inside **linear-review** — after the diff review.
- **On demand:** "do the labels reflect this change?", "review / fix the labels
  for PREFIX-XXX", "suggest Linear labels for this branch".

## Taxonomy recap (authoritative list: `conductor/linear.md`)

Every issue carries **2–4 labels** from orthogonal groups:

| Group | Pick | Source of the pick |
|-------|------|--------------------|
| **Class** | 1 (required) | Track type or the nature of the diff; names from `linear.md` |
| **Surface** | 1 (required) | Dominant changed code path vs `linear.md` Surface → path map |
| **Domain** | 0–1 | Product area, **only if** `linear.md` defines Domain labels |
| **Platform** | 0–1 | Infra/cross-cutting, **only if** defined |
| **Quality** | 0–1 | Primary quality goal, **only if** defined |

If Domain / Platform / Quality tables are empty, skip those groups.

## Protocol

### 1. Resolve scope + issue

- Reuse the review scope: a track's recorded commit range or the branch diff vs
  the base branch.
- Resolve PREFIX-XXX per **linear-issues** §1.
- Get the changed paths: `git diff --name-only <range>` (and `--stat` for
  dominant surface by churn).

### 2. Fetch current labels (MCP)

- Fetch the issue's current label set.
- If MCP is unavailable, continue read-only: produce the recommendation as a
  checklist for the user to apply by hand.

### 3. Derive recommended labels from the diff

**Class** — `feature→Feature`, `bug→Bug`, `chore→Chore`. No track? Infer: new
capability → **Feature**; fix → **Bug**; enhancement → **Improvement**;
refactor/tooling → **Chore**; planning-only → **Spec**. Use the Class names
listed in `linear.md`.

**Surface** — pick the path with the most substantive churn and look it up in
the Surface → path table in `linear.md`. A change that genuinely spans two
surfaces equally may carry both — flag it and prefer the dominant one.

**Domain / Platform / Quality** — only from `linear.md`. Do not invent labels
from another product's taxonomy.

### 4. Compute the delta

- **Add:** recommended labels not yet on the issue.
- **Remove:** labels that contradict the diff.
- **Keep:** correct labels already present.

If the current set already satisfies "1 Class + 1 Surface" and matches the
diff, report "labels already accurate" and skip the apply.

### 5. Detect taxonomy gaps

If the diff belongs to a Surface/Domain **no existing label covers**, do not
force-fit: propose a new label (name + one-line description) under the right
group. Confirm with the user before creating it. Mirror the name into
`conductor/linear.md` in the same change.

### 6. Confirm + apply

- Present the report and **confirm** before mutating Linear.
- Apply the full intended label set. Skip silently when there is no delta.

## Output format

```
Linear labels — PREFIX-XXX (<title>)
Scope: <track id | branch range>  ·  dominant surface: <path> (<n> files)

Current : <labels or none>
Proposed: Class=<…> · Surface=<…> · Domain=<…> · Platform=<…> · Quality=<…>

+ Add    : <labels>
- Remove : <labels>
= Keep   : <labels>

Taxonomy gap: <none | proposed new label + description>
```

## Guardrails

- Never exceed 4 labels without a reason; Class + Surface are mandatory.
- Don't add a label the diff doesn't justify.
- One Surface unless the change is genuinely split.
- Read-only fallback when MCP is down: emit the checklist, stop.
- Never hard-code domains that are not listed in `conductor/linear.md`.
