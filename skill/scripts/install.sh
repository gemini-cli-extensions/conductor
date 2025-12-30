#!/bin/bash
# Install Conductor skill for Claude CLI / OpenCode
# Usage: ./install.sh
#
# This script creates a skill directory with symlinks to the Conductor repository,
# so updates to the repo are automatically reflected in the skill.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONDUCTOR_ROOT="$(dirname "$SKILL_DIR")"

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
echo ""
echo "Where do you want to install the skill?"
echo ""
echo "  1) OpenCode global    (~/.opencode/skill/conductor/)"
echo "  2) Claude CLI global  (~/.claude/skills/conductor/)"
echo "  3) Both"
echo ""
read -p "Choose [1/2/3]: " choice

case "$choice" in
    1)
        TARGETS=("$HOME/.opencode/skill/conductor")
        ;;
    2)
        TARGETS=("$HOME/.claude/skills/conductor")
        ;;
    3)
        TARGETS=("$HOME/.opencode/skill/conductor" "$HOME/.claude/skills/conductor")
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

for TARGET_DIR in "${TARGETS[@]}"; do
    echo ""
    echo "Installing to: $TARGET_DIR"
    
    # Remove existing installation
    rm -rf "$TARGET_DIR"
    
    # Create skill directory
    mkdir -p "$TARGET_DIR"
    
    # Copy SKILL.md (the only actual file)
    cp "$SKILL_DIR/SKILL.md" "$TARGET_DIR/"
    
    # Create symlinks to conductor repo directories
    ln -s "$CONDUCTOR_ROOT/commands" "$TARGET_DIR/commands"
    ln -s "$CONDUCTOR_ROOT/templates" "$TARGET_DIR/templates"
    
    echo "  Created: $TARGET_DIR/SKILL.md"
    echo "  Symlink: $TARGET_DIR/commands -> $CONDUCTOR_ROOT/commands"
    echo "  Symlink: $TARGET_DIR/templates -> $CONDUCTOR_ROOT/templates"
done

echo ""
echo "Conductor skill installed successfully!"
echo ""
echo "Structure:"
for TARGET_DIR in "${TARGETS[@]}"; do
    ls -la "$TARGET_DIR" 2>/dev/null || true
done
echo ""
echo "The skill references the Conductor repo at: $CONDUCTOR_ROOT"
echo "Updates to the repo (git pull) will be reflected automatically."
echo ""
echo "Restart your AI CLI to load the skill."
