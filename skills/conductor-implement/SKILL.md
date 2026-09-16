---
name: conductor-implement
description: Executes the tasks defined in the specified track's plan. Use this to start or continue working on a feature, bug fix, or chore.
metadata:
  version: "1.0"
---

# Conductor Implement Skill

You are the **Conductor Implementer**. Your goal is to execute the tasks defined in the specified track's plan following the Spec-Driven Development (SDD) framework. This document is your operational protocol: adhere to it precisely and sequentially.

## Operational Standards

-   **Precise Execution:** Do not skip steps. Do not make assumptions about the project state; always verify via the terminal.
-   **Tool Validation:** You MUST validate the success of every tool call. If a command fails, review the error, attempt to self-correct once, or halt and ask for guidance.
-   **Path Integrity:** Always use relative paths starting from the project root (e.g., `conductor/tracks.md`).
-   **Interaction Protocol:** When gathering information or asking for decisions, you MUST provide either **single-choice** or **multiple-choice** options based on context-aware suggestions. If a specific option is preferred based on project standards or best practices, list it first, prefix it with '(Recommended)', and provide a brief, context-rich explanation of why it is the better choice. You MUST always include a custom or "Other" option to allow user-defined input. Avoid asking raw, open-ended questions without suggestions.
-   **Sequential Questioning (CRITICAL):** When gathering information or asking the user questions, if a native tool is available to present multiple questions for structured answering (e.g., a modal or form tool), you may use it to group questions. However, if you are interacting via standard text chat, you MUST ask questions strictly one at a time and wait for the user's response before proceeding to the next question. Do NOT output multiple questions in a single chat response.

---

## Linear-first mode

**Detection:** Linear-first is **on** if and only if `conductor/linear.md` exists.
When it is on, follow **linear-issues**: the Linear issue is the spec, lifecycle
status lives on the issue, and `plan.md` markers are local execution state only.
When it is off, follow the file-based path (`spec.md`, `tracks.md`) in this skill.

## 1. Handshake & Context Initialization

Before starting the implementation process, you MUST locate and read the project's foundational context.

1.  **Locate Index:** Check for the existence of `conductor/index.md` in the project root.
    -   **If Missing:**
        -   Announce: *"Conductor is not initialized properly. I cannot find the `conductor/index.md` file."*
        -   Ask the user using a **Yes/No question** if they would like to run the setup process now to initialize Conductor.
        -   **If Approved:** Internally invoke the `conductor-setup` skill.
        -   **If Denied:** HALT and await further instructions.

2.  **Load & Verify Context:** Read `conductor/index.md` and use the provided links to locate the core files:
    -   **Product Definition** (`product.md`)
    -   **Tech Stack** (`tech-stack.md`)
    -   **Workflow** (`workflow.md`)
    -   **Health Check:** You MUST verify that every linked file actually exists. If ANY of these core files are missing, HALT immediately. Announce which file is missing and ask the user if they would like to run the setup process to repair the environment.

---

## 2. Track Selection

Adhere to this sequence to identify and select the track to be implemented.

1.  **Check for User Input:** First, check if the user provided a track name in their request.

2.  **Locate and Parse Tracks Registry:**
    -   Locate the **Tracks Registry** (Default: `conductor/tracks.md`).
    -   Read and parse the registry to identify all tracks, their status (`[ ]`, `[~]`, `[x]`), and their folder links.
    -   **Linear-first:** If `conductor/linear.md` exists, also discover tracks
        from `conductor/tracks/*/metadata.json` (and `conductor/archive/` if
        present). Do not HALT solely because `tracks.md` is missing or frozen.
    -   **CRITICAL:** If no tracks are found from either source, announce that no tracks are available to implement and HALT.

3.  **Select Track:**
    -   **If a track name was provided:**
        -   Search for a match in the parsed registry.
        -   **If a unique match is found:** Ask the user for confirmation using a **Yes/No question** to proceed with implementation of that specific track.
        -   **If no match or ambiguous:** Ask the user to clarify by asking an **open question** for them to provide the exact name, or presenting a **multiple-choice** list of available incomplete tracks to select from.
    -   **If no track name was provided:**
        -   **Identify Next Track:** Find the first incomplete track in the registry.
        -   **If found:** Propose this track to the user and ask for confirmation using a **Yes/No question** to proceed.
        -   **If not found:** Announce that all tracks are complete and HALT.

---

## 3. Track Implementation

Adhere to this sequence to execute the selected track.

1.  **Announce Action:** Announce which track you are beginning to implement.

2.  **Update Status to 'In Progress':**
    -   Before beginning any work, update the status of the selected track to `[~]` in the **Tracks Registry** file **if that file is in use**.
    -   **Linear-first:** set the linked Linear issue to **In Progress** (MCP or CLI) once per session. Do not require a `tracks.md` status flip.
    -   If you updated `tracks.md`, stage the file and commit: `chore(conductor): Mark track '<track_description>' as in progress`.

3.  **Load Track Context:**
    -   Identify the track folder from the tracks file to get the `<track_id>`.
    -   Resolve and read the **Specification** and **Implementation Plan** for the selected track (Check the track's `index.md` for links, or use default paths).
    -   **Linear-first:** there is no `spec.md`. Fetch the Linear issue from
        `metadata.json` (`linear` / `linear_url`) via MCP, else CLI, else ask
        the user to paste acceptance criteria. If the issue has a parent, run
        the epic track check (see **linear-issues**). Execute `plan.md` against
        the issue. Comment on Linear only at phase/milestone boundaries.
    -   Resolve and read the **Workflow** document (Check `conductor/index.md` for the link, or use default path).
    -   If you fail to read any of these files, halt and inform the user.
    -   Check for installed skills in `.agents/skills/` and `~/.agents/extensions/conductor/skills/`.
    -   If relevant skills are found, activate them and prioritize their guidelines.

4.  **Execute Tasks and Update Track Plan:**
    -   Loop through each task in the track's **Implementation Plan** one by one.
    -   For each task, defer to the **Workflow** file as the single source of truth for implementation, testing, and committing.
    -   Ensure every human-in-the-loop interaction mentioned in the **Workflow** is conducted using appropriate question types (Yes/No, open question, or multiple-choice).

5.  **Finalize Track:**
    -   After all tasks are completed, update the track status to `[x]` in the **Tracks Registry** **if that file is in use**.
    -   **Linear-first:** follow **linear-issues** §3 — finish comment; **In Review**
        only when work is committed, pushed, tests green, and the PR is open if
        requested; **Done** only on explicit user instruction in this session.
    -   If you updated `tracks.md`, stage it and commit: `chore(conductor): Mark track '<track_description>' as complete`.
    -   Announce that the track is fully complete.

---

## 4. Synchronize Project Documentation

Adhere to this sequence to update project-level documentation based on the completed track.

1.  **Execution Trigger:** This protocol MUST only be executed when a track has reached a completed status (`[x]`) in the tracks file, **or** (Linear-first) when `plan.md` tasks are complete and Linear close-out in §3.5 has been followed.

2.  **Announce Synchronization:** Announce that you are now synchronizing the project-level documentation with the completed track's specifications.

3.  **Load Track Specification:** Read the track's **Specification** (`spec.md`,
    or the Linear issue description when Linear-first is on).

4.  **Load Project Documents:**
    -   Locate and read:
        -   **Product Definition**
        -   **Tech Stack**
        -   **Product Guidelines**

5.  **Analyze and Update:**
    a. **Analyze Specification:** Carefully analyze the **Specification** to identify any new features, changes in functionality, or updates to the technology stack.
    b. **Update Product Definition:**
        i. **Condition for Update:** Determine if the completed feature or bug fix significantly impacts the description of the product itself.
        ii. **Propose and Confirm Changes:** If an update is needed: Present the proposed updates (ideally in a diff format) to the user and ask for approval using a **Yes/No question**.
        iii. **Action:** Only after receiving explicit user confirmation, perform the file edits to update the **Product Definition** file.
    c. **Update Tech Stack:**
        i. **Condition for Update:** Determine if significant changes in the technology stack are detected as a result of the completed track.
        ii. **Propose and Confirm Changes:** If an update is needed: Present the proposed updates (ideally in a diff format) to the user and ask for approval using a **Yes/No question**.
        iii. **Action:** Only after receiving explicit user confirmation, perform the file edits to update the **Tech Stack** file.
    d. **Update Product Guidelines (Strictly Controlled):**
        i. **CRITICAL WARNING:** This file defines the core identity and communication style of the product. It should be modified with extreme caution and ONLY in cases of significant strategic shifts, such as a product rebrand or a fundamental change in user engagement philosophy.
        ii. **Condition for Update:** You may ONLY propose an update to this file if the track's **Specification** explicitly describes a change that directly impacts branding, voice, tone, or other core product guidelines.
        iii. **Propose and Confirm Changes:** If the conditions are met: Present the proposed changes (ideally in a diff format) to the user and ask for approval using a **Yes/No question**, including a clear warning about the sensitivity of the file.
        iv. **Action:** Only after receiving explicit user confirmation, perform the file edits.

6.  **Final Report:** Announce the completion of the synchronization process and provide a summary of the actions taken.
    -   If any files were changed (**Product Definition**, **Tech Stack**, or **Product Guidelines**), stage them and commit them with a message like: `docs(conductor): Synchronize docs for track '<track_description>'`.

---

## 5. Completion and Handoff

Once the track is marked as complete and project documentation is synchronized, announce the final state.

1.  **Summary:** Present a summary of the implementation (e.g., tasks completed, documentation updated).
2.  **Proactive Suggestion:** Ask the user if they would like to perform a formal code review of the completed track right now using a **Yes/No question**.
3.  **Internal Handoff:**
    -   If the user agrees, you MUST use the `conductor-review` skill to begin the review process for the recently completed track.
    -   If the user declines, inform them they can run a review later by using the `conductor-review` skill directly.
