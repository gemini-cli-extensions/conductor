# Conductor Conceptual Mapping: CLI to IDE

This document defines how Conductor's core concepts translate from a CLI-first environment (Gemini CLI) to an IDE-integrated environment (VS Code / Antigravity).

## 1. Core Abstractions

| CLI Concept (Gemini/Qwen) | IDE Concept (VS Code / Antigravity) | Description |
| :--- | :--- | :--- |
| **Extension API** | **Chat Participant** | The entry point for the tool. CLI uses a JSON manifest; IDE uses a `vscode.ChatParticipant`. |
| **Slash Command** | **Chat Command** | `/conductor:setup` maps directly to `@conductor /setup`. |
| **Interactive Prompt** | **Chat Request/Response** | Sequence of CLI questions maps to a multi-turn chat conversation. |
| **Output Log** | **Chat Response Stream** | Textual feedback maps to Markdown/Rich Text in the chat side-panel. |
| **Project Root** | **Workspace Folder** | The base directory for context resolution. |

## 2. Context Enrichment

IDEs provide significantly richer context than the CLI. Conductor adapters should leverage these where available:

- **Active File/Selection:** Instead of asking the user for a file path, the IDE adapter can default to the currently active editor or selection.
- **Project Structure:** Use native VS Code APIs for more efficient file listing and ignore-file parsing.
- **Terminal Integration:** Directly execute verification commands in the native terminal.

## 3. Skill Execution Model

### CLI Model
1. User enters command.
2. Extension parses arguments.
3. Extension executes protocol (TOML/Jinja2).
4. Extension interacts via stdin/stdout.

### IDE Model
1. User mentions `@conductor` with a command.
2. Participant receives the request and context.
3. Participant calls `conductor-core` to resolve the protocol.
4. Participant handles the interaction loop via the chat interface (using `ask_user` tool).

## 4. Key Conventions Adoption
- **Protocol-First:** Both models MUST share the same underlying protocol defined in `conductor-core`.
- **Markdown-Primary:** All structured output should be Markdown-first for consistency across CLI and IDE.
- **TDD Enforcement:** The TDD workflow must be identically enforced, regardless of the triggering interface.
