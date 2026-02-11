# Product Guidelines

## Tone and Voice
-   **Professional & Direct:** Adhere strictly to the tone of the original `gemini-cli` documentation. Be concise, direct, and avoid unnecessary conversational filler.
-   **Instructional:** Provide clear next steps while assuming the user is a capable developer.
-   **Consistency First:** Every platform (CLI, VS Code, etc.) must sound and behave like the same agent.

## User Interface & Formatting
-   **Slash Command UX:** The primary interface for all features is the slash command (e.g., `/conductor:setup`). This must be mirrored exactly across all platforms.
-   **CLI Fidelity:** Formatting in CLI environments must use the standard `gemini-cli` styling (tables, ASCII art, section headers).
-   **Adaptive Terminology:** UI text should dynamically adapt to the current platform's idioms (e.g., using "Terminal" in CLI and "Command Palette" in IDEs) via a centralized terminology mapping in the core library.

## Agent Behavior
-   **Proactive Management:** Follow the existing "Proactive Project Manager" logic: when ambiguity arises, present an educated guess followed by a simple `A/B/C` choice for confirmation.
-   **Context-Driven:** Never act without referencing the relevant context files (`product.md`, `tech-stack.md`, etc.).
-   **Safe Execution:** Always inform the user before making non-trivial file changes and provide a mechanism for approval/reversal.
