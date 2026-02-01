# Antigravity skills.md Adoption Recommendation

Date: 2026-01-31

Recommendation:
- Keep Antigravity workflows as the default distribution format.
- Offer skills.md output as an opt-in path via `--emit-skills` / `CONDUCTOR_ANTIGRAVITY_SKILLS=1`.

Rationale:
- Antigravity workflows are stable and verified end-to-end in the current toolchain.
- skills.md support is emerging; optional output enables early adopters without breaking defaults.

Fallback Plan:
- If skills.md output proves incompatible or unstable, continue shipping workflows only.
- Preserve installer flags so workflow-only remains a single command path.

Watchpoints:
- Keep VS Code Copilot instructions separate from VS Code extension packaging.
- Revisit once Antigravity skills.md schema/behavior stabilizes.
