#!/bin/bash
# Install Conductor skill for Claude CLI / OpenCode
# Usage: ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONDUCTOR_ROOT="$(dirname "$SKILL_DIR")"

echo "Conductor Skill Installer"
echo "========================="
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
    
    # Create parent directory if needed
    mkdir -p "$(dirname "$TARGET_DIR")"
    
    # Create skill directory structure
    mkdir -p "$TARGET_DIR"/{references,assets/code_styleguides}
    
    # Copy SKILL.md
    cp "$SKILL_DIR/SKILL.md" "$TARGET_DIR/"
    
    # Copy references
    cp "$SKILL_DIR/references/"*.md "$TARGET_DIR/references/"
    
    # Copy assets from templates (code styleguides)
    cp "$CONDUCTOR_ROOT/templates/code_styleguides/"*.md "$TARGET_DIR/assets/code_styleguides/"
    
    # Copy workflow template to references
    cp "$CONDUCTOR_ROOT/templates/workflow.md" "$TARGET_DIR/references/workflow-template.md"
    
    echo "Done: $TARGET_DIR"
done

echo ""
echo "Conductor skill installed successfully!"
echo ""
echo "Restart your AI CLI to load the skill."
