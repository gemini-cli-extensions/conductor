# Conductor Context Artifacts Analysis

This document analyzes the structure and format of the core Conductor context artifacts.

## 1. `product.md`

*   **Format:** Markdown
*   **Structure:**
    *   Uses Markdown headers (`#`, `##`, etc.) to define sections.
    *   Typically includes sections for Introduction, Target Audience, Core Problem & Solution, Key Features, and Future Roadmap.
*   **Purpose:** To provide a high-level overview of the product being built. It defines the "what" and "why" of the project.

## 2. `tech-stack.md`

*   **Format:** Markdown
*   **Structure:**
    *   Uses Markdown headers to categorize technologies (e.g., Core Framework, Configuration and Documentation, Managed Project Technologies).
    *   Uses lists to enumerate specific technologies within each category.
*   **Purpose:** To document the technology stack of the project. This ensures that the AI agent uses the correct languages, frameworks, and libraries.

## 3. `plan.md`

*   **Format:** Markdown
*   **Structure:**
    *   Organized into "Phases" using `##` headers.
    *   Each phase contains a list of "Tasks" using `- [ ]` syntax.
    *   Tasks can be broken down into "Sub-tasks" with indentation.
    *   Task status is tracked with `[ ]` (pending), `[~]` (in progress), and `[x]` (completed).
    *   Completed tasks include the git commit SHA.
*   **Purpose:** To provide a detailed, step-by-step plan for implementing a track. This is the primary document that the AI agent follows during implementation.

## 4. `workflow.md`

*   **Format:** Markdown
*   **Structure:**
    *   Defines the entire development process, including principles, task workflows, quality gates, and commit guidelines.
    *   Uses a combination of headers, lists, and code blocks to structure the information.
*   **Purpose:** To ensure a consistent and high-quality development process. It's the "how" of the project.

## 5. `spec.md`

*   **Format:** Markdown
*   **Structure:**
    *   Typically includes sections for Overview, Problem Statement, Scope (In/Out), and Acceptance Criteria.
*   **Purpose:** To provide a detailed specification for a particular track. It elaborates on the requirements and goals of the track.
