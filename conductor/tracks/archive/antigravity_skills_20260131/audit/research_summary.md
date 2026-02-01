# Antigravity Skills.md Research Summary

## Official docs (workflows/rules)
- The Antigravity codelab describes Rules and Workflows as two customization types.
- Rules and Workflows can be applied globally or per workspace.
- Documented locations:
  - Global rule: `~/.gemini/GEMINI.md`
  - Global workflow: `~/.gemini/antigravity/global_workflows/global-workflow.md`
  - Workspace rules: `your-workspace/.agent/rules/`
  - Workspace workflows: `your-workspace/.agent/workflows/`

## Official skills.md docs
- The official `https://antigravity.google/docs/skills` endpoint did not return readable content in this environment (likely JS-rendered). Treat skills.md format requirements as unverified until we can access the canonical doc.

## Community references (lower confidence)
- Community posts describe a skills directory at `~/.gemini/antigravity/skills/` for global skills and `your-workspace/.agent/skills/` for workspace skills, with a `SKILL.md` definition file and optional `scripts/`, `references/`, `assets/` folders.
- Community comments report that Antigravity does not load workspace rules/workflows when `.agent` is gitignored; `.git/info/exclude` can be used instead.

## Workflow vs Skills (current understanding)
- **Workflows:** Single markdown file per command, stored under global or workspace workflow paths.
- **Skills (community):** Directory per skill with `SKILL.md` and supporting assets/scripts; may allow richer capability packaging than workflows.
- **Implication:** Keep workflows as the default for now; treat skills output as an optional alternative until the official spec is confirmed.

## Recommendations
- Keep workflows as the default install target (global + workspace) per official guidance.
- Add an optional `--emit-skills` or config flag to generate Antigravity `skills/` output once the official skills.md spec is confirmed.
- Add a warning in docs/installer output if `.agent` is gitignored, as workflows may not show in the UI.

## Sources
- https://codelabs.developers.google.com/getting-started-google-antigravity#9
- https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2
- https://vertu.com/lifestyle/mastering-google-antigravity-skills-a-comprehensive-guide-to-agentic-extensions-in-2026/
- https://www.reddit.com/r/google_antigravity/comments/1q6vt5k/antigravity_does_not_load_workspacelevel_rules/
