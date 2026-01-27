/**
 *
 * Exports the Ralph Protocol directive
 */

const directive = `
## 🔴 RALPH MODE ACTIVE: TASK EXECUTION OVERRIDE
**ATTENTION:** 🔁 Announce you are operating in **RALPH MODE** loop.

**INSTRUCTIONS:**
1.  **Execute Standard Protocol:** You MUST follow Steps **3.1**, **3.2**, **3.3**, and **3.5** of the "TRACK IMPLEMENTATION" protocol exactly as defined in the prompt. This includes updating the plan status to [~] and eventually [x].
2.  **Shell Command Execution:** When executing shell commands, you MUST use flags that reject or prevent interactive user input (e.g., \`-n\`, \`--no-input\`).
3.  **OVERRIDE Step 3.4.c ONLY:**
    -   Do **NOT** defer to the "Task Workflow" in the **Workflow** file.
    -   Instead, for each task, execute this **RALPH AUTONOMOUS CYCLE**:
        1.  **RED:** Write failing tests based on the **Specification**.
        2.  **GREEN:** Implement code to pass tests.
        3.  **VERIFY:** Run tests.
            -   **IF FAIL:** You may attempt to fix the code and re-run tests **ONCE** within this turn.
            -   **IF STILL FAILING:** You must attempt to devise and execute a single alternative fix within this turn. If the alternative also fails, you MUST respond with the following message and HALT immediately, awaiting user feedback:
            > [Ralph]: <Concise reason for final failure>
            -   **PASS:** Proceed to the next step. Do NOT output the 	\`[Ralph]:\` prefix.
        4.  **RECORD:**
            - Update the task status in the **Implementation Plan** to [x].
            - Stage and commit all changes (implementation + plan update) with a clear commit message.
        5.  **NEXT:** Proceed to the next task in the plan immediately. Do NOT ask for permission or wait for feedback.
4.  **SKIP MANUAL TASKS & INTERACTIONS:**
    -   **CRITICAL:** You must **NOT** ask the user for verification, confirmation, or feedback.
    -   If a task in the **Implementation Plan** involves "Manual Verification", "User Manual Verification", or "User Feedback":
        1.  Do **NOT** perform the manual steps.
        2.  Do **NOT** print the verification steps to the user.
        3.  **IMMEDIATELY** mark the task as [x] in the plan.
        4.  Proceed to the next task.
    -   **Ralph's automated tests are the ONLY source of truth.** If tests pass, the work is verified.
5.  **COMPLETION & CLEANUP:**
    -   After you have finished **Step 3.5** (Finalizing the track, updating registry, committing), **YOU MUST VERIFY ONE LAST TIME.**
    -   **CRITICAL:** For all of the following conditions, you MUST output the specified \`[Ralph]:\` message directly to the user as a standard text response, NOT as a shell command.
    -   If **ALL** tasks in the **Implementation Plan** are marked as [x] AND **one** single test fail You MUST respond the following message directly to the user as a standard text response, NOT as a shell command:
            > [Ralph]: <Concise reason for failure>
            -   **HALT immediately, finish your turn completely, and await for user feedback.
    -   **IF STUCK OR BLOCKED:** If you are unable to proceed for ANY reason (e.g., ambiguous specs, tool failures), first attempt to formulate and execute a single alternative strategy to overcome the obstacle within the same turn. If the alternative strategy also fails, you MUST respond with the following message and HALT immediately, awaiting user feedback:
        	> [Ralph]: <reason for being stuck>
    -   Only if **ALL** tasks in the **Implementation Plan** are marked as [x] AND **ALL** project tests are currently passing, you MUST perform the following steps sequentially in your response:
        1.  Execute **Section 4.0** (Doc Sync) from the original "TRACK IMPLEMENTATION" protocol, with one critical override: you MUST apply all generated documentation changes automatically without asking for user approval.
        2.  Output the following consolidated completion message directly to the user as a standard text response:
            > "Ralph has completed the track. Please manually verify the changes. If you are unsatisfied, you can revert the changes using commands \`/conductor:revert\` and retry with \`/conductor:implement --ralph\`. 
            >
            > If you are satisfied, please ask me to **Archive**, **Delete**, or **Skip** the track for cleanup."
        3. As the absolute final step, after all other output, include the promise token on its own line:
            > [Ralph]: <promise>{{COMPLETION_WORD}}</promise>

**CONSTRAINT:** The **Workflow** file is valid ONLY for "Development Commands", "Testing Requirements", and "Code Style".
`;

module.exports = directive;
