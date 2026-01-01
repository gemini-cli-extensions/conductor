import json
from pathlib import Path

from scripts.skills_manifest import (
    get_extension,
    iter_skills,
    load_manifest,
    render_skill_content,
)

ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "conductor-core" / "src" / "conductor_core" / "templates"
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
SKILLS_DIR = ROOT / "skills"
ANTIGRAVITY_DIR = ROOT / ".antigravity" / "skills"
ANTIGRAVITY_GLOBAL_DIR = Path.home() / ".gemini" / "antigravity" / "global_workflows"
CODEX_DIR = Path.home() / ".codex" / "skills"
CLAUDE_DIR = Path.home() / ".claude" / "skills"
OPENCODE_DIR = Path.home() / ".opencode" / "skill"
COPILOT_DIR = Path.home() / ".config" / "github-copilot"
VSCODE_SKILLS_DIR = ROOT / "conductor-vscode" / "skills"
GEMINI_EXTENSION_PATH = ROOT / "gemini-extension.json"
QWEN_EXTENSION_PATH = ROOT / "qwen-extension.json"

def _perform_sync(target_base_dir, skills, flat=False):
    for skill in skills:
        content = render_skill_content(skill, TEMPLATES_DIR)

        if flat:
            # For Antigravity global workflows, use flat .md files
            target_file = target_base_dir / f"{skill['name']}.md"
            target_base_dir.mkdir(parents=True, exist_ok=True)
        else:
            # For standard skills, use directory/SKILL.md
            skill_dir = target_base_dir / skill["name"]
            skill_dir.mkdir(parents=True, exist_ok=True)
            target_file = skill_dir / "SKILL.md"

        with open(target_file, "w", encoding="utf-8") as handle:
            handle.write(content)

        print(f"Synced skill: {skill['name']} -> {target_file}")

def sync_skills():
    manifest = load_manifest(MANIFEST_PATH)
    skills = list(iter_skills(manifest))

    # Sync to standard skills directory
    print("Syncing to local skills directory...")
    _perform_sync(SKILLS_DIR, skills)
    
    # Sync to Antigravity directory for local development/integration
    print("\nSyncing to local Antigravity...")
    _perform_sync(ANTIGRAVITY_DIR, skills)

    # Sync to Global Antigravity directory (FLAT structure)
    print("\nSyncing to Global Antigravity (Flat)...")
    _perform_sync(ANTIGRAVITY_GLOBAL_DIR, skills, flat=True)

    # Sync to Codex
    print("\nSyncing to Codex...")
    _perform_sync(CODEX_DIR, skills)

    # Sync to Claude
    print("\nSyncing to Claude...")
    _perform_sync(CLAUDE_DIR, skills)

    # Sync to OpenCode
    print("\nSyncing to OpenCode...")
    _perform_sync(OPENCODE_DIR, skills)

    # Sync to VS Code Extension (Packaged)
    print("\nSyncing to VS Code Extension...")
    _perform_sync(VSCODE_SKILLS_DIR, skills)

    # Sync to Copilot (Consolidated instructions)
    print("\nSyncing to Copilot (Consolidated)...")
    COPILOT_DIR.mkdir(parents=True, exist_ok=True)
    consolidated_file = COPILOT_DIR / "conductor.md"
    all_instructions = ["# Conductor Protocol", ""]
    for skill in skills:
        template_file = TEMPLATES_DIR / f"{skill['template']}.j2"
        if template_file.exists():
            template_content = template_file.read_text(encoding="utf-8")
            all_instructions.append(f"## Command: /{skill['name']}")
            all_instructions.append(template_content)
            all_instructions.append("\n---\n")
    
    with open(consolidated_file, "w", encoding="utf-8") as handle:
        handle.write("\n".join(all_instructions))
    print(f"Synced consolidated Copilot rules: {consolidated_file}")

    # Sync Gemini/Qwen extension manifests (repo-local)
    for tool_name, target_path in (
        ("gemini", GEMINI_EXTENSION_PATH),
        ("qwen", QWEN_EXTENSION_PATH),
    ):
        extension = get_extension(manifest, tool_name)
        if not extension:
            print(f"Warning: No extension metadata for {tool_name}. Skipping.")
            continue
        with open(target_path, "w", encoding="utf-8") as handle:
            json.dump(extension, handle, indent=2)
            handle.write("\n")
        print(f"Synced extension manifest: {tool_name} -> {target_path}")

if __name__ == "__main__":
    sync_skills()
