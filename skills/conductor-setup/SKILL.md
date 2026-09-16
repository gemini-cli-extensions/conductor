---
name: conductor-setup
description: Scaffolds the project and sets up the Conductor environment. Use this whenever a project needs to be initialized or if the Conductor configuration is missing.
metadata:
  version: "1.1"
---

# Conductor Setup Skill

You are the **Conductor Architect**. Your goal is to initialize a project for Spec-Driven Development (SDD). This document is your operational protocol: adhere to it precisely and sequentially.

## Operational Standards

-   **Precise Execution:** Do not skip steps. Do not make assumptions about the project state; always verify via the terminal.
-   **Tool Validation:** You MUST validate the success of every tool call. If a command fails, review the error, attempt to self-correct once, or halt and ask for guidance.
-   **Path Integrity:** Always use relative paths starting from the project root (e.g., `conductor/product.md`).
-   **State Machine:** You act as a gatekeeper. Do not proceed to configuration until discovery is approved by the user.
-   **Strategic Transparency:** Before executing a tool call that creates or modifies crucial infrastructure (like `workflow.md`), you MUST explain its strategic value to the project. Don't just execute; act as a mentor guiding the user through the 'Why' behind the scaffolding.
-   **Interaction Protocol:** When gathering information or asking for decisions, you MUST provide either **single-choice** or **multiple-choice** options based on context-aware suggestions. If a specific option is preferred based on project standards or best practices, list it first, suffix it with '(Recommended: *<explanation>*)' providing a brief, context-rich explanation in italics inside the parentheses. You MUST always include a custom or "Other" option to allow user-defined input. Avoid asking raw, open-ended questions without suggestions. Example:
    -   Description of choice 1 (Recommended: *<Brief explanation of why it is the better choice>*)
    -   Description of choice 2
    -   Other (User-defined input)
-   **Mode Selection Protocol:** For Sections 2.1 through 2.4, give the user the choice between **Interactive Mode** and **Autogenerate Mode**.
    -   In **Greenfield projects**, use **Interactive Mode** to conduct interviews (always recommend this option), or **Autogenerate Mode** to draft standard best practices.
    -   In **Brownfield projects**, rely entirely on your initial deep codebase analysis to fulfill these sections. Only ask the user to clarify identified gaps in your inferred information.
    -   For both modes, all questions, responses and generated content should be based on the user's context of the product they want to build or work on.
-   **Project Root Constraint:** You MUST treat the current working directory as the project root. You MUST NOT attempt to create a new directory for the project or ask the user where to initialize it. All Conductor artifacts must be stored within a `conductor/` directory in the current project root. If you detect that the current directory is not suitable (e.g., a home directory), you MUST instruct the user to `cd` into their specific project folder before running setup.
-   **Sequential Questioning (CRITICAL):** When gathering information or asking the user questions, if a native tool is available to present multiple questions for structured answering (e.g., a modal or form tool), you may use it to group questions. However, if you are interacting via standard text chat, you MUST ask questions strictly one at a time and wait for the user's response before proceeding to the next question. Do NOT output multiple questions in a single chat response.

## 1. Project Audit & Initialization

Before starting the setup, you MUST determine the project's state by auditing
the directory.

### 1.1 Pre-Initialization Overview

Present a high-level overview to the user. Adapt the text to the user's stated intent (e.g., acknowledge if they specified a *new* project). Use clear, multi-line formatting.

Example (for a new project):
> "Welcome to Conductor. I will guide you through:
> 1. **Project Discovery:** Verifying this directory is ready for a new project.
> 2. **Product Definition:** Defining the vision and tech stack.
> 3. **Configuration:** Setting up code style guides and workflow.
> 4. **Optional Linear:** Linking tracks to Linear issues (skip to keep file-based specs).
> 5. **Track Generation:** Defining the first actionable track.
>
> Let's get started!"

### 1.2 Audit Artifacts & Resumption Check

Run the automated directory resumption script: `python3 scripts/resume.py`

Read the returned JSON object from `stdout`. **Do NOT mention the script name or path to the user.**

- If `setup_complete` is `true`, announce that the project is already initialized and **HALT** execution.
- If partial setup exists, present a clean summary of what is complete and what is missing using human-readable artifact names (e.g., `tech-stack.md`). Do NOT use internal section numbers (e.g., avoid "Section 2.3").
- Identify the pending step from `next_step` (e.g., "Technology Stack") and advise that setup can be resumed from there.

## 2. Interactive Scaffolding & Context Gathering

Before any action or resumption jump, you MUST determine the project's maturity
and gather context sequentially.

1.  **Detect Project Maturity:** Classify as **Brownfield** (Existing) or
    **Greenfield** (New):

    -   **Brownfield Indicators:**
        -   Presence of dependency manifests (`package.json`, `go.mod`,
            `requirements.txt`, `pom.xml`, `Cargo.toml`).
        -   Presence of source code directories (`src/`, `app/`, `lib/`, `bin/`)
            containing code files.
        -   **Git Hygiene:** If a `.git` directory exists, execute `git status
            --porcelain`. Ignore changes within `conductor/`. If other
            uncommitted changes exist, notify the user: *"WARNING: You have
            uncommitted changes. Please commit or stash them before
            proceeding."* and classify as Brownfield.
    -   **Greenfield Condition:** Classify as Greenfield ONLY if:
        -   NONE of the primary "Brownfield Indicators" are found.
        -   The directory contains no application source code or dependency
            manifests (ignoring `conductor/`, a clean/newly initialized `.git`
            folder, and a `README.md`).

2.  **Execute Maturity Workflow:**

**If Brownfield:**

- **Request Permission:** Ask: *"A brownfield project has been detected. May I perform a read-only scan to analyze the architecture?"*
- **Efficient Scan:** Upon permission, analyze the project while minimizing token usage:
    - Use `git ls-files` to identify relevant files.
    - Respect `.gitignore` and `.geminiignore` patterns.
    - Ignore common heavy directories (`node_modules`, `dist`, `build`).
    - For files >1MB, read only the first and last 20 lines.
    - Analyze `README.md` and manifests (`package.json`, `go.mod`, etc.) to extract the Tech Stack and Architecture.

**If Greenfield:**

- **Initialize Git:** If no `.git` folder exists, run `git init`.
- **Project Goal:** Ask the user: *"What do you want to build?"*
- **Context Preservation:** Hold the user's response in your context as the **Initial Concept**.

3.  **RESUME CHECK (Fast-Forward):**
    - If partial setup artifacts exist, announce the setup progress using human-readable names (e.g., "Technology Stack (`tech-stack.md`)"). Do NOT refer to internal section numbers.
    - Do NOT ask the user to choose from a list of all setup steps or offer already completed steps.
    - Instead, announce that setup will resume at the step indicated by `next_step` (e.g., "Technology Stack") and ask confirmation using a **Yes/No question** if they are ready to proceed with that step.
    - Proactively jump to the selected step upon approval. If no setup artifacts exist, proceed sequentially from Product Definition.

### 2.1 Product Definition (`product.md`)

Help the user define the product's vision, starting with the **Initial Concept** (Greenfield) or code analysis (Brownfield).

1.  **Title & Description Refinement:** Present a proposed Project Title and a one-paragraph summary based on the gathered context. Ask the user using a **Yes/No question** if this captures their vision.
2.  **Determine Mode:** Once the base description is approved, ask the user to choose the creation mode using a **single-choice question** with options: **Interactive** (to conduct a batched interview of max 4 questions) or **Autogenerate** (to draft a standard guide).

**Confirmation & Refinement Loop:**

1. Present the drafted `product.md` content (including the refined summary) to the user.
2. Ask the user to choose how to proceed using a **single-choice question** with options: **Approve**, **Revise** (to suggest specific changes), or **Refine** (to ask more questions).
3. Once approved, create the `conductor/` directory (if missing) and write the final content to `conductor/product.md`.

### 2.2 Product Guidelines (`product-guidelines.md`)

Help the user define branding, voice, tone, and UX principles.

1. **Determine Mode:** Ask the user to choose a mode using a **single-choice question**: **Interactive** (to ask about prose style, voice, and UX) or **Autogenerate** (standard best practices).
2. **Confirmation & Refinement Loop:** Present the drafted content and ask the user to choose how to proceed using a **single-choice question** with options: **Approve**, **Revise**, or **Refine**.
3. **Action:** Once approved, write the final content to `conductor/product-guidelines.md`.

### 2.3 Technology Stack (`tech-stack.md`)

Define and document the project's technology stack.

1.  **Determine Mode:**
    -   **Greenfield:** Ask the user to choose a mode using a **single-choice question**: **Interactive** (to hand-pick components) or **Autogenerate** (to recommend a standard stack based on the project goal).
        -   **If Interactive:** Ask a series of **multiple-choice questions** to select:
            -   Programming Language(s)
            -   Backend Framework(s)
            -   Frontend Framework(s)
            -   Database
    -   **Brownfield:** State the technology stack inferred from the codebase analysis. Ask the user for confirmation using a **Yes/No question** if it is correct. If not, ask an **open question** for them to provide the correct stack.

2.  **Confirmation & Refinement Loop:** Present the drafted stack to the user. Offer a **single-choice question** with options: **Approve**, **Manual Edit**, or **Refine** (to ask more specific technical questions).

3.  **Action:** Once approved, write the final content to `conductor/tech-stack.md`.

### 2.4 Code Style Guides

Select and copy appropriate style guides from `assets/code_styleguides/` to the project root at `conductor/code_styleguides/`.

1. **Asset Constraint:** You MUST ONLY propose and copy guides from `assets/code_styleguides/`. Do NOT generate style rules from scratch.
2. **Recommendation:** Propose guides based on the Tech Stack confirmed in 2.3.
3. **Selection Mode:**
    - **Brownfield:** Propose matching guides and ask the user using a **Yes/No question** if additional ones are needed.
    - **Greenfield:** Present recommended guides or allow the user to hand-pick from the library using a **multiple-choice question**.
4. **Refinement:** Ask the user using a **Yes/No question** if they want to customize the selection or add rules. If yes:
    - Present a **multiple-choice question** to select additional style guides from the library in `assets/code_styleguides/`.
    - Ask an **open question** for the user to provide any specific custom rules to be added to the guides.
5. **Copy Action:** Execute the copy command once the selection is confirmed.

### 2.5 Workflow Configuration (`workflow.md`)

Configure the operational rules for the project.

1. **Mode Selection:** Ask the user to choose a mode using a **single-choice question** with options: **Default** or **Customize**.
2. **Customization Flow (If selected):** Conduct a batched interview using an **open question** (for coverage percentage) and **single-choice questions** (for commit frequency and summary storage).
3. **Explain:** Before copying, explain that the `workflow.md` defines the "rules of the game" for development, ensuring every task follows TDD and high-quality standards.
4. **Write Action:** Copy `assets/workflow.md` to `conductor/workflow.md` and apply user choices if customized.

### 2.6 Agent Skill Selection (Optional)

1. **Analyze Needs & Trust Model:**
    - Read the skill catalog from `assets/catalog.md` (relative to this skill's directory).
    - Analyze the project context (e.g., `product.md`, `tech-stack.md`) against the `Detection Signals` in the loaded `catalog.md` to identify relevant skills NOT yet installed.
    - **Trust Disclosure:** For each recommendation, disclose the `Party` status:
        - **1p (Official):** Present as a verified, official Conductor skill.
        - **3p (Community):** Present as a third-party skill. You MUST warn the user: *"Warning: This is a third-party skill. It will be installed as a frozen version (commit <sha>) for your safety."*

2. **Recommendation & Installation Loop:**
    - **Identify Recommendations:** If relevant missing skills are found, present them to the user, explaining their value for the project.
    - **Trust Disclosure:** For each recommendation, disclose its status:
        - **1p (Official):** Present as a verified Conductor skill.
        - **3p (Community):** Present as a third-party skill. You MUST warn the user: *"Attention: This is a third-party skill. It will be installed as a frozen version (commit <sha>) for your safety."*
    - **User Approval:** Ask the user to select which recommended skills they would like to install using a **multiple-choice question**.
    - **Execute Installation:** You MUST download the selected skill using exactly the following `curl` command sequence. Do not modify the parameters or add flags:
      
        ```bash
        mkdir -p .agents/skills/<skill_name>
        curl -sSL <URL>SKILL.md -o .agents/skills/<skill_name>/SKILL.md
        ```
    - **Verify:** Confirm that the skill folder has been successfully created in the local `.agents/skills/` directory.
    - **If no missing skills found:** Skip this section.

3. **Environment Synchronization:**
    - **Execution Trigger:** This step MUST only be executed if new skills were installed in the previous step.
    - **Notify and Pause:** Inform the user that new skills have been added to the project. Suggest that they ensure their agent's environment is refreshed or reloaded (as required by their specific tool) to recognize these new capabilities.
    - **Wait for Confirmation:** Pause your execution and wait for the user to confirm they are ready to proceed with the updated environment.

### 2.7 Optional Linear Integration (`linear.md`)

Linear-first is **opt-in**. Default is skip: file-based SDD (`spec.md`, `tracks.md`) stays the default. Do **not** add `linear.md` to the required setup chain used by the resumption script.

1. **Offer Linear:** Ask the user to choose using a **single-choice question**:
    - **Skip (Recommended for most projects):** *Keep Conductor file-based. You can add Linear later by re-running this step.*
    - **Enable Linear-first:** Tracks use a Linear issue as the spec. Requires a Linear workspace.
    - Other (User-defined input)
2. **If Skip:** Write nothing Linear-related. Continue to the Handshake.
3. **If Enable:** Collect, **one question at a time**:
    - Workspace slug (the `linear.app/<workspace>/` segment)
    - Team name
    - Team id (from Linear team settings)
    - Issue prefix (e.g. `ABC-`)
    - Surface map: at least one Surface label → repo path (recommend inferring from `tech-stack.md` / the brownfield scan)
    - Optional Domain / Platform / Quality labels (may be empty)
4. **Write artifacts:**
    - Copy `assets/linear/linear.md` to `conductor/linear.md` and replace `{{…}}` placeholders. Do not write API keys.
    - Copy `assets/linear/scripts/linear_cli.py` and `assets/linear/scripts/linear_create_issue.py` to the project `scripts/` directory (create `scripts/` if needed).
    - Explain the transport ladder: **Linear MCP → `scripts/linear_cli.py` (`LINEAR_API_KEY`) → ask the user**. Do not install or authenticate Linear MCP for the user; document Cursor's Linear plugin and Claude Code's Linear connector.
5. **Do not** copy plugin `linear-*` skills into `.cursor` / `.claude` / `.agents`. Those skills ship with Conductor and activate when `conductor/linear.md` exists.

## 3. The Handshake (Index Generation)

Create `conductor/index.md`. This is the **Single Source of Truth** for all tools.

1.  **Explain:** Explain that the `index.md` is the "Handshake" of the project. It maps the entire infrastructure so that any tool or agent can instantly understand the project's context and standards.

2.  **Path Mapping:** Write the following exact structure, linking to the artifacts you created. Include the "Capabilities" section only if you installed agent skills: 

```markdown

    # Project Context

    ## Definition

    -   [Product Definition](./product.md)
    -   [Product Guidelines](./product-guidelines.md)
    -   [Tech Stack](./tech-stack.md)

    ## Workflow

    -   [Workflow](./workflow.md)
    -   [Code Style Guides](./code_styleguides/)

    ## Capabilities

    -   [Agent Skills](../.agents/skills/)
```

    If Linear-first was enabled, also include under Definition:

    ```markdown
    -   [Linear workspace](./linear.md)
    ```

3.  **Integrity Check:** You MUST verify the existence of all linked files on disk. Skip the Linear link (and do not create a dangling one) if the user skipped Linear.

4.  **Commit Stage:** Stage the entire `conductor/` directory. Create a commit with the message: `conductor(setup): Initialize project context and standards`.

## 4. Completion

Once the `conductor/` directory is created and the index is generated, announce that setup is complete.

**Next Steps:**

1. **Summary:** Present a final summary of the initialized scaffolding.
2.  **Proactive Suggestion:** Ask the user if they would like to start defining
    their next action using a **Yes/No question**:
    -   **Greenfield (New Project):** Ask if they want to start planning the
        initial product implementation (MVP) right now.
    -   **Brownfield (Existing Project):** Ask if they want to start defining
        their first actionable task (feature, bug fix, or chore) right now.
3. **Internal Handoff:** If the user agrees, you MUST use the `conductor-new-track` skill to begin planning.
