#!/bin/bash
# Install Conductor skill for Claude CLI / OpenCode
# Usage: ./install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONDUCTOR_ROOT="$(dirname "$SKILL_DIR")"

# Determine target directory
if [ -d "$HOME/.claude/skills" ]; then
    TARGET_DIR="$HOME/.claude/skills/conductor"
elif [ -d "$HOME/.opencode/skill" ]; then
    TARGET_DIR="$HOME/.opencode/skill/conductor"
else
    # Default to Claude location
    TARGET_DIR="$HOME/.claude/skills/conductor"
    mkdir -p "$HOME/.claude/skills"
fi

echo "Installing Conductor skill to: $TARGET_DIR"

# Create skill directory
mkdir -p "$TARGET_DIR"/{references,assets/code_styleguides}

# Copy SKILL.md
cp "$SKILL_DIR/SKILL.md" "$TARGET_DIR/"

# Copy references
cp "$SKILL_DIR/references/"*.md "$TARGET_DIR/references/"

# Copy assets from templates (code styleguides)
cp "$CONDUCTOR_ROOT/templates/code_styleguides/"*.md "$TARGET_DIR/assets/code_styleguides/"

# Copy workflow template to references
cp "$CONDUCTOR_ROOT/templates/workflow.md" "$TARGET_DIR/references/workflow-template.md"

echo ""
echo "Conductor skill installed successfully!"
echo ""
echo "Structure:"
tree "$TARGET_DIR" 2>/dev/null || find "$TARGET_DIR" -type f | head -20
echo ""
echo "Restart your AI CLI to load the skill."
