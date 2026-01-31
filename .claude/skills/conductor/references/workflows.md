# Workflow Reference

## Task Lifecycle
All tasks follow this lifecycle:
1. Red (Failing tests)
2. Green (Passing tests)
3. Refactor (Clean up)

## Commit Protocol
- One commit per task
- Summary attached via `git notes`
- Conventional commit messages

## Quality Gates
- >95% code coverage
- Pass all lint/type checks
- Validated on mobile if applicable