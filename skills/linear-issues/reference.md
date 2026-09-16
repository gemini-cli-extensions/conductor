# Linear issues — reference

Team identity: `conductor/linear.md` in the **project**. Replace `ABC-` below
with that file's issue prefix.

## Epics and sub-issues

In Linear, an **epic is an issue with sub-issues**. Sub-issues are normal issues with
a `parent` pointing at the epic issue.

```text
ABC-10  Epic title (epic — parent issue)
├── ABC-12  First sub-issue
└── ABC-13  Second sub-issue
```

| Term | Meaning |
|------|---------|
| Epic | Parent issue that owns child sub-issues |
| Sub-issue | Issue with `parent` / `parentId` = epic id |
| Project | Separate release grouping — not the epic |
| Sibling | Another sub-issue under the same parent epic |

**Every epic has an epic track (track check):** before starting sub-issue work,
confirm the parent epic has an epic track (search
`conductor/tracks/*/metadata.json` for `"linear": "<epic id>"`) and open one
first if it is missing.

## Prompt prefixes

```text
Linear: ABC-12 — Short title
Track: conductor/tracks/<track_id>/
Implement per plan.md against the issue's acceptance criteria; update Linear at
phase boundaries.
```

## Branch names

```text
abc-12-short-slug
abc-13-another-slug
```

Lowercase prefix, issue number, kebab-case slug.

## Commit messages

```text
feat(area): add the thing (ABC-12)
```

## PR title and body

**Title:**

```text
ABC-12: Imperative summary
```

**Body (minimal):**

```markdown
## Linear
<issue URL>

Closes ABC-12

## Summary
- …

## Test plan
- [ ] <project test command from conductor/workflow.md>
```

## Linear comment templates

### Phase / milestone

```markdown
**Progress (ABC-12)**

- …

Next: …

Branch: `abc-12-short-slug`
```

### PR opened

```markdown
**PR ready for review (ABC-12)**

PR: https://github.com/…/pull/NNN

Verify:
1. <project test command>

Status → In Review
```

### Done

```markdown
**Shipped (ABC-12)**

Merged PR #NNN.

Closing ABC-12.
```

> Post this (and flip the status to Done) **only when the user has explicitly said
> to close the issue**. See SKILL §3 *Status transitions* hard rules.

### Blocked

```markdown
**Blocked (ABC-12)**

Waiting on: …

Branch pushed; will resume when unblocked.
```

## Conductor metadata.json (new tracks — pointer only)

```json
{
  "track_id": "shortname_YYYYMMDD",
  "linear": "ABC-12",
  "linear_url": "https://linear.app/<workspace>/issue/ABC-12/…"
}
```

Pointer only — no `type`, `description`, `status`, or `parent_linear`. `parent`
(the epic, if any) is read from the Linear issue via `get_issue`.

## plan.md header

```markdown
**Linear:** [ABC-12](https://linear.app/<workspace>/issue/ABC-12/…)
```

## plan.md close task

```markdown
- [ ] Mark **ABC-12** Done in Linear; link PR in issue comment
```

This plan task is a reminder, **not** authorization.
