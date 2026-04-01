# Conductor Architecture

Conductor is built as a **Gemini CLI extension**. Rather than containing traditional application source code, it mostly acts as a prompt-engineering and configuration wrapper that defines new commands, tool policies, and standard templates to direct the Gemini CLI agent.

## Components

1. **Commands Configuration (`commands/**/*.toml`)**: 
   - Each CLI command mapping to a `/conductor:*` prompt is defined by a TOML file.
   - These files contain massive `SYSTEM DIRECTIVE` prompts. For example, `setup.toml` acts as a complex workflow engine, guiding the agent to detect project state, present an interactive wizard using the `ask_user` tool, and ultimately scaffold the directory structure.

2. **Templates (`templates/`)**: 
   - Predefined Markdown templates (like `workflow.md`) and code style guides. These are selectively copied into a consumer's project during `setup`.

3. **Policies (`policies/conductor.toml`)**: 
   - Custom permission overrides for the Gemini CLI agent when executing Conductor commands.
   - For instance, it allows the agent to create/write files within the `conductor/` directory in "plan" mode, and executes `git` setup commands without excessive prompting.

4. **Agent Skills Catalog (`skills/catalog.md`)**:
   - A registry of predefined skills (e.g., `firebase-auth-basics`, `gcp-cicd-terraform`) that the setup agent can dynamically fetch and install into a project's `.agents/skills` directory, giving the agent domain-specific knowledge.

5. **Universal File Resolution (`GEMINI.md`)**:
   - Instructions on how the agent should navigate a user's repository consistently mapping references like "Product Definition" to `conductor/product.md`.
