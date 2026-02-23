# Markdownlint Setup Guide

This guide explains how to set up and use markdownlint for documentation validation in the conductor-next project.

## Quick Start

### Install markdownlint CLI

```bash
# Using npm (Node.js required)
npm install -g markdownlint-cli

# Using pip (Python)
pip install markdownlint-cli

# Using Homebrew (macOS)
brew install markdownlint-cli
```

### Verify Installation

```bash
markdownlint --version
```

## Usage

### Lint All Markdown Files

```bash
# From project root
markdownlint "**/*.md"

# With custom config (uses .markdownlint.json automatically)
markdownlint -c .markdownlint.json "**/*.md"
```

### Lint Specific Files

```bash
markdownlint README.md
markdownlint docs/**/*.md
```

### Auto-Fix Issues

```bash
# Fix automatically (safe fixes only)
markdownlint --fix "**/*.md"
```

## Configuration

The project uses `.markdownlint.json` in the root directory with these key settings:

- **Line length**: 120 characters (excludes code blocks and tables)
- **Heading style**: ATX (`#` symbols)
- **List style**: Dash (`-`) for unordered lists
- **Code blocks**: Fenced with backticks
- **Ignored paths**: `node_modules/`, `.git/`, `vendor/`, `*.min.*`

## Editor Integration

### VS Code

1. Install the [markdownlint extension](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
2. The extension automatically picks up `.markdownlint.json`
3. Violations appear as warnings/errors in the editor

### Other Editors

- **IntelliJ IDEA**: Built-in markdown linting support
- **Vim/Neovim**: Use [ALE](https://github.com/dense-analysis/ale) or [coc.nvim](https://github.com/neoclide/coc.nvim)
- **Sublime Text**: Install [SublimeLinter-contrib-markdownlint](https://packagecontrol.io/packages/SublimeLinter-contrib-markdownlint)

## Pre-commit Hooks

The project includes pre-commit hooks that automatically run markdownlint:

```bash
# Install pre-commit hooks (one-time setup)
pip install pre-commit
pre-commit install

# Hooks run automatically on git commit
```

## Common Violations and Fixes

### MD013 - Line Too Long

**Violation**: Line exceeds 120 characters

**Fix**: Break long lines or add to config exceptions:

```json
{
  "MD013": {
    "line_length": 120,
    "code_blocks": false,
    "tables": false
  }
}
```

### MD024 - Multiple Headings with Same Content

**Violation**: Duplicate headings in the same document

**Fix**: Make headings unique or use HTML anchors:

```markdown
## Installation {#installation}
## Installation for Windows {#installation-windows}
```

### MD033 - Inline HTML

**Violation**: HTML tags in markdown (disabled by default in our config)

**Fix**: Use markdown syntax instead, or allow specific tags in config

### MD041 - First Line Should Be H1

**Violation**: Document doesn't start with `# Title`

**Fix**: Add H1 heading as the first line

## CI/CD Integration

Documentation linting runs automatically in GitHub Actions on:

- All pull requests
- Pushes to main branch

See `.github/workflows/docs-lint.yml` for configuration.

## Validation Script

Run the comprehensive documentation validation script:

```bash
python scripts/validate_docs.py
```

This checks:
- Markdown syntax and style
- Mermaid diagram syntax
- CSL-JSON reference format
- Internal link validity

## Troubleshooting

### "markdownlint: command not found"

Ensure markdownlint-cli is installed and in your PATH:

```bash
# Check installation
which markdownlint  # Linux/macOS
where markdownlint  # Windows

# Reinstall if needed
npm uninstall -g markdownlint-cli
npm install -g markdownlint-cli
```

### Configuration Not Applied

Verify `.markdownlint.json` is in the project root:

```bash
ls -la .markdownlint.json
```

### Too Many False Positives

Review and adjust rules in `.markdownlint.json`. Some rules can be disabled or configured:

```json
{
  "MD013": false,  // Disable line length check
  "MD024": { "siblings_only": true }  // Only flag adjacent duplicate headings
}
```

## Resources

- [markdownlint Rules Reference](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [markdownlint-cli Documentation](https://github.com/igorshubovych/markdownlint-cli)
- [Project Style Guide](../templates/code_styleguides/markdown.md)
