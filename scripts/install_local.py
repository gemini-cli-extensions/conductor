import argparse
import importlib
import os
import subprocess
import sys
from pathlib import Path, PurePath


def _log(status: str, name: str, detail: str) -> None:
    print(f"{status}  {name}  {detail}")  # noqa: T201


def install_vsix(vsix_path: Path, *, dry_run: bool) -> bool:
    local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
    program_files = Path(os.environ.get("PROGRAMFILES", ""))
    possible_code_cmds = [
        "code",
        local_app_data / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
        program_files / "Microsoft VS Code" / "bin" / "code.cmd",
    ]

    for cmd in possible_code_cmds:
        cmd_str = str(cmd)
        if dry_run:
            _log("OK", "vscode", f"{cmd_str} --install-extension {vsix_path}")
            return True
        try:
            subprocess.run([cmd_str, "--install-extension", str(vsix_path)], check=True)  # noqa: S603
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        else:
            _log("OK", "vscode", str(vsix_path))
            return True

    _log("WARN", "vscode", "code.cmd not found or failed to install extension")
    return False


def install_antigravity_vsix(vsix_path: Path, *, dry_run: bool) -> bool:
    possible_cmds = [
        "antigravity",
        "antigravity.cmd",
        "antigravity.exe",
    ]

    for cmd in possible_cmds:
        if dry_run:
            _log("OK", "antigravity", f"{cmd} --install-extension {vsix_path}")
            return True
        try:
            subprocess.run([cmd, "--install-extension", str(vsix_path)], check=True)  # noqa: S603
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        else:
            _log("OK", "antigravity", str(vsix_path))
            return True

    _log("WARN", "antigravity", "CLI not found or failed to install extension")
    return False


def sync_antigravity_global_workflows(repo_root: Path, *, dry_run: bool) -> bool:
    if dry_run:
        _log("OK", "antigravity-global", str(Path.home() / ".gemini" / "antigravity" / "global_workflows"))
        return True
    sys.path.insert(0, str(repo_root))
    skills_manifest = importlib.import_module("scripts.skills_manifest")
    sync_skills_module = importlib.import_module("scripts.sync_skills")

    manifest = skills_manifest.load_manifest(repo_root / "skills" / "manifest.json")
    skills = list(skills_manifest.iter_skills(manifest))
    sync_skills_module.sync_antigravity_global(skills)
    _log("OK", "antigravity-global", str(Path.home() / ".gemini" / "antigravity" / "global_workflows"))
    return True


def sync_antigravity_workspace_workflows(repo_root: Path, *, dry_run: bool) -> bool:
    if dry_run:
        _log("OK", "antigravity-workspace", str(repo_root / ".agent" / "workflows"))
        return True
    sys.path.insert(0, str(repo_root))
    skills_manifest = importlib.import_module("scripts.skills_manifest")
    sync_skills_module = importlib.import_module("scripts.sync_skills")

    manifest = skills_manifest.load_manifest(repo_root / "skills" / "manifest.json")
    skills = list(skills_manifest.iter_skills(manifest))
    sync_skills_module.sync_antigravity_workspace(skills)
    _log("OK", "antigravity-workspace", str(repo_root / ".agent" / "workflows"))
    return True


def sync_skills(repo_root: Path, *, dry_run: bool) -> None:
    if dry_run:
        _log("OK", "skills", str(repo_root / "skills"))
        return
    sys.path.insert(0, str(repo_root))
    sync_skills_module = importlib.import_module("scripts.sync_skills")
    sync_skills_module.sync_skills()
    _log("OK", "skills", str(repo_root / "skills"))


def sync_copilot(repo_root: Path, *, dry_run: bool) -> None:
    if dry_run:
        _log("OK", "copilot", str(Path.home() / ".config" / "github-copilot" / "conductor.md"))
        return
    sys.path.insert(0, str(repo_root))
    sync_skills_module = importlib.import_module("scripts.sync_skills")
    sync_skills_module.sync_skills()
    _log("OK", "copilot", str(Path.home() / ".config" / "github-copilot" / "conductor.md"))


def verify(repo_root: Path) -> bool:
    python = sys.executable
    commands = [
        [python, "scripts/check_skills_sync.py"],
        [python, "scripts/validate_platforms.py"],
        [python, "scripts/validate_antigravity.py"],
    ]
    all_ok = True
    for cmd in commands:
        result = subprocess.run(cmd, cwd=repo_root, check=False)  # noqa: S603
        if result.returncode == 0:
            _log("OK", "verify", " ".join(cmd[1:]))
        else:
            _log("FAIL", "verify", " ".join(cmd[1:]))
            all_ok = False
    vsix_path = repo_root / "conductor.vsix"
    if vsix_path.exists() and vsix_path.stat().st_size > 0:
        _log("OK", "vsix", str(vsix_path))
    else:
        _log("FAIL", "vsix", str(vsix_path))
        all_ok = False
    return all_ok


def _resolve_locations(repo_root: PurePath, home: PurePath) -> dict[str, PurePath]:
    return {
        "repo-skills": repo_root / "skills",
        "antigravity-workspace": repo_root / ".agent" / "workflows",
        "antigravity-global": home / ".gemini" / "antigravity" / "global_workflows",
        "antigravity-skills-workspace": repo_root / ".agent" / "skills",
        "antigravity-skills-global": home / ".gemini" / "antigravity" / "skills",
        "codex": home / ".codex" / "skills",
        "claude": home / ".claude" / "skills",
        "opencode": home / ".opencode" / "skill",
        "copilot": home / ".config" / "github-copilot" / "conductor.md",
        "vsix": repo_root / "conductor.vsix",
    }


def _print_locations(repo_root: Path) -> None:
    locations = _resolve_locations(repo_root, Path.home())
    for name, path in locations.items():
        _log("OK", "location", f"{name}={path}")


def _summarize(ok: int, warn: int, fail: int) -> None:
    print(f"SUMMARY  ok={ok} warn={warn} fail={fail}")  # noqa: T201


def main() -> int:  # noqa: C901, PLR0912
    parser = argparse.ArgumentParser(description="Install Conductor artifacts locally.")
    parser.add_argument("--verify", action="store_true", help="Run validation checks only")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions without changes")
    parser.add_argument("--print-locations", action="store_true", help="Print resolved artifact locations")
    parser.add_argument("--repo-only", action="store_true", help="Only update repo-local artifacts")
    parser.add_argument("--install-vsix", action="store_true", help="Install VSIX into VS Code and Antigravity")
    parser.add_argument("--sync-workflows", action="store_true", help="Sync Antigravity global/workspace workflows")
    parser.add_argument("--sync-skills", action="store_true", help="Sync skills to agent-skill directories")
    parser.add_argument("--sync-copilot", action="store_true", help="Sync Copilot rules file")
    parser.add_argument("--emit-skills", action="store_true", help="Emit Antigravity skills output")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    vsix_path = repo_root / "conductor.vsix"

    action_flags = [
        args.verify,
        args.install_vsix,
        args.sync_workflows,
        args.sync_skills,
        args.sync_copilot,
        args.print_locations,
    ]
    default_mode = not any(action_flags)

    ok = warn = fail = 0

    if args.print_locations:
        _print_locations(repo_root)

    if args.repo_only:
        os.environ["CONDUCTOR_SYNC_REPO_ONLY"] = "1"
    if args.emit_skills:
        os.environ["CONDUCTOR_ANTIGRAVITY_SKILLS"] = "1"

    if args.verify:
        return 0 if verify(repo_root) else 1

    if default_mode or args.sync_workflows:
        if sync_antigravity_workspace_workflows(repo_root, dry_run=args.dry_run):
            ok += 1
        else:
            warn += 1
        if not args.repo_only:
            if sync_antigravity_global_workflows(repo_root, dry_run=args.dry_run):
                ok += 1
            else:
                warn += 1

    if default_mode or args.sync_skills:
        sync_skills(repo_root, dry_run=args.dry_run)
        ok += 1

    if args.sync_copilot:
        sync_copilot(repo_root, dry_run=args.dry_run)
        ok += 1

    if default_mode or args.install_vsix:
        if not vsix_path.exists() and not args.dry_run:
            _log("FAIL", "vsix", str(vsix_path))
            fail += 1
            _summarize(ok, warn, fail)
            return 1
        ok += 1 if install_vsix(vsix_path, dry_run=args.dry_run) else 0
        ok += 1 if install_antigravity_vsix(vsix_path, dry_run=args.dry_run) else 0

    _summarize(ok, warn, fail)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
