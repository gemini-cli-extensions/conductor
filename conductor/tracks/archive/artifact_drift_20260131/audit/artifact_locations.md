# Generated Artifact Locations

## Repo-local outputs
- skills: `skills/<skill>/SKILL.md`
- Antigravity local skills (dev): `.antigravity/skills/<skill>/SKILL.md`
- Antigravity workspace workflows: `.agent/workflows/<skill>.md`
- Antigravity workspace skills (optional): `.agent/skills/<skill>/SKILL.md`
- VS Code packaged skills: `conductor-vscode/skills/<skill>/SKILL.md`
- Gemini/Qwen manifests: `gemini-extension.json`, `qwen-extension.json`
- VSIX build: `conductor.vsix`

## Global user outputs
- Antigravity global workflows: `~/.gemini/antigravity/global_workflows/<skill>.md`
- Antigravity workflow index: `~/.gemini/antigravity/global_workflows/global-workflow.md`
- Antigravity global skills (optional): `~/.gemini/antigravity/skills/<skill>/SKILL.md`
- Claude CLI skills: `~/.claude/skills/<skill>/SKILL.md`
- Codex skills: `~/.codex/skills/<skill>/SKILL.md`
- OpenCode skills: `~/.opencode/skill/<skill>/SKILL.md`
- Copilot rules: `~/.config/github-copilot/conductor.md`

## Adapter/command scaffolding
- Gemini/Qwen commands: `commands/conductor/*.toml`
- Claude commands/plugins: `.claude/commands/*.md` and `.claude-plugin/*`
