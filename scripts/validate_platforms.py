import os
import sys

from conductor_core.validation import ValidationService


def run_validation() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sync", action="store_true", help="Synchronize platform files from core templates")
    args = parser.parse_args()

    base_dir = os.getcwd()
    core_templates = os.path.join(base_dir, "conductor-core/src/conductor_core/templates")
    service = ValidationService(core_templates)

    # Gemini TOMLs
    gemini_mappings = {
        "commands/conductor/conductor.toml": "conductor.j2",
        "commands/conductor/setup.toml": "setup.j2",
        "commands/conductor/newTrack.toml": "new_track.j2",
        "commands/conductor/implement.toml": "implement.j2",
        "commands/conductor/status.toml": "status.j2",
        "commands/conductor/revert.toml": "revert.j2",
    }

    # Claude MDs
    claude_mappings = {
        "commands/conductor-info.md": "conductor.j2",
        ".claude/commands/conductor-setup.md": "setup.j2",
        ".claude/commands/conductor-newtrack.md": "new_track.j2",
        ".claude/commands/conductor-implement.md": "implement.j2",
        ".claude/commands/conductor-status.md": "status.j2",
        ".claude/commands/conductor-revert.md": "revert.j2",
    }

    all_valid = True

    for path, template in gemini_mappings.items():
        if args.sync:
            success, msg = service.synchronize_gemini_toml(path, template)
        else:
            valid, msg = service.validate_gemini_toml(path, template)
            if not valid:
                all_valid = False

    for path, template in claude_mappings.items():
        if args.sync:
            _success, msg = service.synchronize_claude_md(path, template)
        else:
            valid, _msg = service.validate_claude_md(path, template)
            if not valid:
                all_valid = False

    if not all_valid:
        sys.exit(1)
    else:
        pass


if __name__ == "__main__":
    run_validation()
