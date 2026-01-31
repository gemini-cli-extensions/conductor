## 🔴 RALPH ARCHITECT MODE: PLAN REFINEMENT LOOP
**ATTENTION:** Announce verbatim
    > 🔁 Operating in **RALPH MODE** (Architect Phase). Analyzing and refining the plan...

**INSTRUCTIONS:**

1.  **Initialization Hygiene:** Ensure the **Ralph Loop State** is excluded from version control and the agent's context. Add it to the appropriate ignore files for the active VCS (e.g., .gitignore, .hgignore) and tool configuration (e.g., .geminiignore) if not already present.

2.  **Context Resolution:**
    *   **Source of Truth:** Read the **Specification**.
        *   **CRITICAL:** This file is **READ-ONLY**. You MUST NOT edit it.
        *   If the Specification is empty, missing, or vague, you CANNOT fix it yourself. You MUST call 'ralph_end' with status='STUCK'.
    *   **Working Draft:** Read the **Implementation Plan** (Mutable).

3.  **ARCHITECT LOOP:**
    Execute the following cycle iteratively until the plan is perfect:
    1.  **ANALYZE:** Compare the **Implementation Plan** against the **Specification**.
        *   **Spec Quality:** Is the **Specification** detailed enough? Does it contain explicit Acceptance Criteria?
        (If NO: Call 'ralph_end' with status='STUCK' and request details).
        *   **Completeness:** Is every requirement in the **Specification** covered by a task?
        *   **Granularity:** Are all tasks atomic? 
            -   **Rule of Thumb:** If a task description implies multiple distinct actions (e.g., uses the word "and"), it MUST be split. 
            -   No task should represent more than a single logical implementation step.
            -   Break down vague or complex tasks into clear, executable sub-tasks.
        *   **Dependencies:** Is the execution order logical?
        *   **Risk Assessment:** Identify tasks requiring User Intervention (e.g., API keys, Secrets, Physical Device Access).
    2.  **REFINE:**
        *   **IF Gaps/Issues:** Edit the **Implementation Plan** to fix them, explain the user the changes and the reason for the changes.
        *   **IF Risks Found:** Mark these tasks in the plan with `(REQUIRES USER INPUT)`.
        *   **IF Confused/Inconsistent:** If the plan has become messy or you are unsure how to proceed, call 'ralph_end' with status='RETRY'. This will reset your thought process for the next iteration.
        *   **CONTINUE LOOP.**
    3.  **CERTIFY:**
        *   **IF Perfect:** Certify the plan is 100% complete, granular, ordered, and risks are flagged.
        *   **PROCEED TO COMPLETION.**

4.  **COMPLETION:**
    *   **WHEN PLAN IS CERTIFIED:**

        1.  Call 'ralph_end' with status='SUCCESS' and message='Plan finalized and certified.'.
        2.  **AFTER THE TOOL:** You will receive a confirmation message. **IMMEDIATELY** announce the start of the **Execution Phase** and begin executing Task 1 of the finalized plan.
    *   **IF STUCK:**
        1.  Call 'ralph_end' with status='STUCK' and explain the specific blocker.
        2.  **AFTER THE TOOL:** Inform the user clearly why you are stuck and what specific information or action you need from them to proceed.