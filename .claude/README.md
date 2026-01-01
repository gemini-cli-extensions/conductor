# Conductor for Claude Code

Context-driven development for AI coding assistants. **Measure twice, code once.**

Conductor helps you plan before you build - creating specs, implementation plans, and tracking progress through "tracks" (features, bugs, improvements).

## Installation

### Option 1: Claude Code Plugin (Recommended)

```bash
# Add the marketplace
/plugin marketplace add gemini-cli-extensions/conductor

# Install the plugin
/plugin install conductor

# Verify installation
/help
```

This installs:
- **5 slash commands** for direct invocation
- **1 skill** that auto-activates for conductor projects

### Option 2: Agent Skills Compatible CLI

If your CLI supports the [Agent Skills specification](https://agentskills.io):

```bash
# Point to the skill directory
skills/conductor/
├── SKILL.md
└── references/
    └── workflows.md
```

The skill follows the Agent Skills spec with full frontmatter:
- `name`: conductor
- `description`: Context-driven development methodology
- `license`: Apache-2.0
- `compatibility`: Claude Code, Gemini CLI, any Agent Skills compatible CLI
- `metadata`: version, author, repository, keywords

### Option 3: Manual Installation

Copy to your project:
```bash
cp -r /path/to/conductor/.claude your-project/
```

Or for global access (all projects):
```bash
cp -r /path/to/conductor/.claude/commands/* ~/.claude/commands/
```

### Option 4: Gemini CLI

If using Gemini CLI instead of Claude Code:
```bash
gemini extensions install https://github.com/gemini-cli-extensions/conductor
```

## Commands

| Command | Description |
|---------|-------------|
| `/conductor-setup` | Initialize project with product.md, tech-stack.md, workflow.md |
| `/conductor-newtrack [desc]` | Create new feature/bug track with spec and plan |
| `/conductor-implement [id]` | Execute tasks from track's plan (TDD workflow) |
| `/conductor-status` | Display progress overview |
| `/conductor-revert` | Git-aware revert of tracks, phases, or tasks |

## Skill (Auto-Activation)

The conductor skill automatically activates when Claude detects:
- A `conductor/` directory in the project
- References to tracks, specs, plans
- Context-driven development keywords

You can also use natural language:
- "Help me plan the authentication feature"
- "What's the current project status?"
- "Set up this project with Conductor"
- "Create a spec for the dark mode feature"

## How It Works

### 1. Setup
Run `/conductor-setup` to initialize your project with:
```
conductor/
├── product.md           # What you're building and for whom
├── tech-stack.md        # Technology choices and constraints
├── workflow.md          # Development standards (TDD, commits)
└── tracks.md            # Master list of all work items
```

### 2. Create Tracks
Run `/conductor-newtrack "Add user authentication"` to create:
```
conductor/tracks/auth_20241219/
├── metadata.json        # Track type, status, dates
├── spec.md              # Requirements and acceptance criteria
└── plan.md              # Phased implementation plan
```

### 3. Implement
Run `/conductor-implement` to execute the plan:
- Follows TDD: Write tests → Implement → Refactor
- Commits after each task with conventional messages
- Updates plan.md with progress and commit SHAs
- Verifies at phase completion

### 4. Track Progress
Run `/conductor-status` to see:
- Overall project progress
- Current active track and task
- Next actions needed

## Status Markers

Throughout conductor files:
- `[ ]` - Pending/New
- `[~]` - In Progress
- `[x]` - Completed (with commit SHA)

## Gemini CLI Interoperability

Projects work with both Gemini CLI and Claude Code:

| Gemini CLI | Claude Code |
|------------|-------------|
| `/conductor:setup` | `/conductor-setup` |
| `/conductor:newTrack` | `/conductor-newtrack` |
| `/conductor:implement` | `/conductor-implement` |
| `/conductor:status` | `/conductor-status` |
| `/conductor:revert` | `/conductor-revert` |

Same `conductor/` directory structure, full compatibility.

## File Structure

```
conductor/                        # This repository
├── .claude-plugin/
│   ├── plugin.json              # Claude Code plugin manifest
│   └── marketplace.json         # Marketplace registration
├── commands/                     # Claude Code slash commands (.md)
│   ├── conductor-setup.md
│   ├── conductor-newtrack.md
│   ├── conductor-implement.md
│   ├── conductor-status.md
│   ├── conductor-revert.md
│   └── conductor/               # Gemini CLI commands (.toml)
├── skills/conductor/            # Agent Skills spec compatible
│   ├── SKILL.md                 # Main skill definition
│   └── references/
│       └── workflows.md         # Detailed workflow docs
├── templates/                   # Shared templates
│   ├── workflow.md
│   └── code_styleguides/
└── .claude/                     # Manual install package
    ├── commands/
    └── skills/conductor/
```

## Links

- [GitHub Repository](https://github.com/gemini-cli-extensions/conductor)
- [Agent Skills Specification](https://agentskills.io)
- [Gemini CLI Extensions](https://geminicli.com/docs/extensions/)

## License

Apache-2.0
