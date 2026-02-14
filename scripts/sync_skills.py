import json
import os
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.skills_manifest import (  # noqa: E402
    get_extension,
    iter_skills,
    load_manifest,
    render_antigravity_workflow_content,
    render_skill_content,
)
from scripts.skills_validator import validate_manifest  # noqa: E402

TEMPLATES_DIR = ROOT / "conductor-core" / "src" / "conductor_core" / "templates"
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
SCHEMA_PATH = ROOT / "skills" / "manifest.schema.json"
SKILLS_DIR = ROOT / "skills"
ANTIGRAVITY_DIR = ROOT / ".antigravity" / "skills"
ANTIGRAVITY_GLOBAL_DIR = Path.home() / ".gemini" / "antigravity" / "global_workflows"
ANTIGRAVITY_WORKSPACE_DIR = ROOT / ".agent" / "workflows"
ANTIGRAVITY_SKILLS_GLOBAL_DIR = Path.home() / ".gemini" / "antigravity" / "skills"
ANTIGRAVITY_SKILLS_WORKSPACE_DIR = ROOT / ".agent" / "skills"
CODEX_DIR = Path.home() / ".codex" / "skills"
CLAUDE_DIR = Path.home() / ".claude" / "skills"
CLINE_DIR = Path.home() / ".cline" / "skills"
KILO_DIR = Path.home() / ".kilo" / "skills"
AMP_DIR = Path.home() / ".amp" / "skills"
OPENCODE_DIR = Path.home() / ".opencode" / "skills"
COPILOT_DIR = Path.home() / ".config" / "github-copilot"
AIX_DIR = Path.home() / ".config" / "aix"
SKILLSHARE_DIR = Path.home() / ".config" / "skillshare" / "skills"
VSCODE_SKILLS_DIR = ROOT / "conductor-vscode" / "skills"
GEMINI_EXTENSION_PATH = ROOT / "gemini-extension.json"
QWEN_EXTENSION_PATH = ROOT / "qwen-extension.json"


def _clean_antigravity_global(target_base_dir: Path, skills: Iterable[dict]) -> None:
    allowed = {f"{skill['name']}.md" for skill in skills}
    if not target_base_dir.exists():
        return
    for workflow in target_base_dir.glob("conductor*.md"):
        if workflow.name not in allowed:
            workflow.unlink()


def update_vscode_package_json(skills: Iterable[dict]) -> None:
    vscode_package_json = ROOT / "conductor-vscode" / "package.json"
    if not vscode_package_json.exists():
        return

    data = json.loads(vscode_package_json.read_text(encoding="utf-8"))

    # Ensure contributes.commands exists
    if "contributes" not in data:
        data["contributes"] = {}
    if "commands" not in data["contributes"]:
        data["contributes"]["commands"] = []

    # Update commands
    existing_commands = {cmd["command"]: cmd for cmd in data["contributes"]["commands"]}
    for skill in skills:
        if not skill.get("enabled", {}).get("vscode", False):
            continue

        cmd_id = f"conductor.{skill['id']}"
        existing_commands[cmd_id] = {
            "command": cmd_id,
            "title": f"Conductor: {skill['id'].replace('_', ' ').title()}",
            "category": "Conductor",
        }

    data["contributes"]["commands"] = sorted(existing_commands.values(), key=lambda x: x["command"])

    vscode_package_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _perform_sync(target_base_dir: Path, skills: Iterable[dict], *, flat: bool = False) -> None:
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

        # Write bytes to avoid platform newline translation (Qwen requires LF-only frontmatter).
        target_file.write_bytes(content.encode("utf-8"))


def _perform_antigravity_global_sync(target_base_dir: Path, skills: Iterable[dict]) -> None:
    target_base_dir.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        content = render_antigravity_workflow_content(skill, TEMPLATES_DIR)
        target_file = target_base_dir / f"{skill['name']}.md"
        target_file.write_text(content, encoding="utf-8")


def _perform_antigravity_workspace_sync(target_base_dir: Path, skills: Iterable[dict]) -> None:
    target_base_dir.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        content = render_antigravity_workflow_content(skill, TEMPLATES_DIR)
        target_file = target_base_dir / f"{skill['name']}.md"
        target_file.write_text(content, encoding="utf-8")


def _perform_consolidated_sync(target_file: Path, skills: Iterable[dict], templates_dir: Path) -> None:
    target_file.parent.mkdir(parents=True, exist_ok=True)
    all_instructions = ["# Conductor Protocol", ""]
    for skill in skills:
        template_file = templates_dir / f"{skill['template']}.j2"
        if template_file.exists():
            template_content = template_file.read_text(encoding="utf-8")
            all_instructions.append(f"## Command: /{skill['name']}")
            all_instructions.append(template_content)
            all_instructions.append("\n---\n")

    target_file.write_text("\n".join(all_instructions), encoding="utf-8")


def _write_global_workflow_index(target_base_dir: Path, skills: Iterable[dict]) -> None:
    target_base_dir.mkdir(parents=True, exist_ok=True)
    index_path = target_base_dir / "global-workflow.md"
    lines = [
        "---",
        "description: Conductor workflow index",
        "---",
        "",
        "Available Conductor workflows:",
        "",
    ]
    lines.extend([f"- `/{skill['name']}`" for skill in skills])
    lines.extend(
        [
            "",
            "Use any of the commands above (e.g., `/conductor-setup`).",
        ]
    )
    index_path.write_text("\n".join(lines), encoding="utf-8")


def sync_antigravity_global(skills: Iterable[dict]) -> None:
    _clean_antigravity_global(ANTIGRAVITY_GLOBAL_DIR, skills)
    _perform_antigravity_global_sync(ANTIGRAVITY_GLOBAL_DIR, skills)
    _write_global_workflow_index(ANTIGRAVITY_GLOBAL_DIR, skills)


def sync_antigravity_workspace(skills: Iterable[dict]) -> None:
    _perform_antigravity_workspace_sync(ANTIGRAVITY_WORKSPACE_DIR, skills)


def sync_antigravity_skills(skills: Iterable[dict], *, repo_only: bool) -> None:
    _perform_sync(ANTIGRAVITY_SKILLS_WORKSPACE_DIR, skills)
    if not repo_only:
        _perform_sync(ANTIGRAVITY_SKILLS_GLOBAL_DIR, skills)


def sync_skills() -> None:
    validate_manifest(MANIFEST_PATH, SCHEMA_PATH)
    manifest = load_manifest(MANIFEST_PATH)
    skills = list(iter_skills(manifest))
    to_repo_only = os.environ.get("CONDUCTOR_SYNC_REPO_ONLY") == "1"
    emit_antigravity_skills = os.environ.get("CONDUCTOR_ANTIGRAVITY_SKILLS") == "1"

    # Sync to standard skills directory
    _perform_sync(SKILLS_DIR, skills)

    # Sync to Antigravity directory for local development/integration
    _perform_sync(ANTIGRAVITY_DIR, skills)

    # Sync to Antigravity workspace workflows (repo-local)
    sync_antigravity_workspace(skills)
    if emit_antigravity_skills:
        sync_antigravity_skills(skills, repo_only=to_repo_only)

    if not to_repo_only:
        # Sync to Global Antigravity directory (FLAT structure)
        sync_antigravity_global(skills)

    if not to_repo_only:
        # Sync to Codex
        _perform_sync(CODEX_DIR, skills)

        # Sync to Claude
        _perform_sync(CLAUDE_DIR, skills)

        # Sync to Cline
        _perform_sync(CLINE_DIR, skills)

        # Sync to Kilo
        _perform_sync(KILO_DIR, skills)

        # Sync to Amp
        _perform_sync(AMP_DIR, skills)

        # Sync to OpenCode
        _perform_sync(OPENCODE_DIR, skills)

        # Sync to SkillShare
        _perform_sync(SKILLSHARE_DIR, skills)

        # Sync to AIX
        _perform_consolidated_sync(AIX_DIR / "conductor.md", skills, TEMPLATES_DIR)

    # Sync to VS Code Extension (Packaged)
    _perform_sync(VSCODE_SKILLS_DIR, skills)
    update_vscode_package_json(skills)

    if not to_repo_only:
        # Sync to Copilot (Consolidated instructions)
        _perform_consolidated_sync(COPILOT_DIR / "conductor.md", skills, TEMPLATES_DIR)

    # Sync Gemini/Qwen extension manifests (repo-local)
    for tool_name, target_path in (
        ("gemini", GEMINI_EXTENSION_PATH),
        ("qwen", QWEN_EXTENSION_PATH),
    ):
        extension = get_extension(manifest, tool_name)
        if not extension:
            continue
        target_path.write_text(json.dumps(extension, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sync_skills()
