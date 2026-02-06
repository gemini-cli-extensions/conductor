#!/bin/bash
# Install Conductor skill for Claude CLI / OpenCode / Codex
# Usage: ./install.sh [--target <claude|opencode|codex|all>] [--list] [--dry-run] [--force] [--link|--copy]
#
# This script creates a skill directory with symlinks or copies to the Conductor repository,
# so updates to the repo are automatically reflected when using --link.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONDUCTOR_ROOT="$(dirname "$SKILL_DIR")"

MODE="link"
TARGET=""
DRY_RUN="false"
FORCE="false"
LIST_ONLY="false"

print_targets() {
    echo "Available targets:"
    echo "  opencode (OpenCode)"
    echo "  claude (Claude)"
    echo "  codex (Codex)"
    echo "  all"
}

detect_environments() {
    DETECTED_TARGETS=()
    if [ -d "$HOME/.opencode" ]; then DETECTED_TARGETS+=("opencode"); fi
    if [ -d "$HOME/.claude" ]; then DETECTED_TARGETS+=("claude"); fi
    if [ -d "$HOME/.codex" ]; then DETECTED_TARGETS+=("codex"); fi

    if [ ${#DETECTED_TARGETS[@]} -gt 0 ]; then
        echo "Detected environments: ${DETECTED_TARGETS[*]}"
    fi
}

usage() {
    echo "Conductor Skill Installer"
    echo "========================="
    echo ""
    echo "Usage:"
    echo "  ./install.sh [--target <claude|opencode|codex|all>] [--list] [--dry-run] [--force] [--link|--copy]"
    echo ""
    print_targets
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --force)
            FORCE="true"
            shift
            ;;
        --list)
            LIST_ONLY="true"
            shift
            ;;
        --link)
            MODE="link"
            shift
            ;;
        --copy)
            MODE="copy"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

if [ "$LIST_ONLY" = "true" ]; then
    print_targets
    exit 0
fi

echo "Conductor Skill Installer"
echo "========================="
echo ""

# Check if we're running from within a conductor repo
if [ ! -f "$CONDUCTOR_ROOT/commands/conductor/setup.toml" ]; then
    echo "Error: This script must be run from within the Conductor repository."
    echo "Expected to find: $CONDUCTOR_ROOT/commands/conductor/setup.toml"
    echo ""
    echo "Please clone the repository first:"
    echo "  git clone https://github.com/gemini-cli-extensions/conductor.git"
    echo "  cd conductor"
    echo "  ./skill/scripts/install.sh"
    exit 1
fi

echo "Conductor repository found at: $CONDUCTOR_ROOT"

if [ -z "$TARGET" ]; then
    if [ "$FORCE" = "true" ]; then
        echo "Error: --force requires --target."
        usage
        exit 1
    fi
    echo ""
    echo "Where do you want to install the skill?"
    echo ""
    echo "  1) OpenCode global    (~/.opencode/skill/conductor/)"
    echo "  2) Claude CLI global  (~/.claude/skills/conductor/)"
    echo "  3) Codex global       (~/.codex/skills/conductor/)"
    echo "  4) All of the above"
    echo ""
    read -p "Choose [1/2/3/4]: " choice

    case "$choice" in
        1)
            TARGET="opencode"
            ;;
        2)
            TARGET="claude"
            ;;
        3)
            TARGET="codex"
            ;;
        4)
            TARGET="all"
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
fi

case "$TARGET" in
    opencode)
        TARGETS=("$HOME/.opencode/skill/conductor")
        ;;
    claude)
        TARGETS=("$HOME/.claude/skills/conductor")
        ;;
    codex)
        TARGETS=("$HOME/.codex/skills/conductor")
        ;;
    all)
        TARGETS=("$HOME/.opencode/skill/conductor" "$HOME/.claude/skills/conductor" "$HOME/.codex/skills/conductor")
        ;;
    *)
        echo "Invalid target: $TARGET"
        print_targets
        exit 1
        ;;
 esac

for TARGET_DIR in "${TARGETS[@]}"; do
    echo ""
    echo "Installing to: $TARGET_DIR"

    if [ "$DRY_RUN" = "true" ]; then
        echo "  [dry-run] rm -rf $TARGET_DIR"
        echo "  [dry-run] mkdir -p $TARGET_DIR"
        echo "  [dry-run] cp $SKILL_DIR/SKILL.md $TARGET_DIR/"
        echo "  [dry-run] $MODE $CONDUCTOR_ROOT/commands -> $TARGET_DIR/commands"
        echo "  [dry-run] $MODE $CONDUCTOR_ROOT/templates -> $TARGET_DIR/templates"
        continue
    fi

    # Remove existing installation
    rm -rf "$TARGET_DIR"

    # Create skill directory
    mkdir -p "$TARGET_DIR"

    # Copy SKILL.md (the only actual file)
    cp "$SKILL_DIR/SKILL.md" "$TARGET_DIR/"

    if [ "$MODE" = "copy" ]; then
        cp -R "$CONDUCTOR_ROOT/commands" "$TARGET_DIR/commands"
        cp -R "$CONDUCTOR_ROOT/templates" "$TARGET_DIR/templates"
    else
        ln -s "$CONDUCTOR_ROOT/commands" "$TARGET_DIR/commands"
        ln -s "$CONDUCTOR_ROOT/templates" "$TARGET_DIR/templates"
    fi

    echo "  Created: $TARGET_DIR/SKILL.md"
    echo "  $MODE: $TARGET_DIR/commands -> $CONDUCTOR_ROOT/commands"
    echo "  $MODE: $TARGET_DIR/templates -> $CONDUCTOR_ROOT/templates"
done

if [ "$DRY_RUN" = "true" ]; then
    echo ""
    echo "Dry-run complete. No files were changed."
    exit 0
fi

echo ""
echo "Conductor skill installed successfully!"
echo ""
echo "Structure:"
for TARGET_DIR in "${TARGETS[@]}"; do
    ls -la "$TARGET_DIR" 2>/dev/null || true
done
echo ""
echo "The skill references the Conductor repo at: $CONDUCTOR_ROOT"
if [ "$MODE" = "link" ]; then
    echo "Updates to the repo (git pull) will be reflected automatically."
fi
echo ""
echo "Restart your AI CLI to load the skill."
