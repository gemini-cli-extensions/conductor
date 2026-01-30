## 🔴 RALPH MODE ACTIVE: TASK EXECUTION OVERRIDE
**ATTENTION:** Announce verbatim
    > 🔁 Operating in **RALPH MODE** autonomous loop.

**INSTRUCTIONS:**
1.  **Initialization Hygiene:** Ensure the **Ralph Loop State** (resolved via the **Universal File Resolution Protocol**) is excluded from version control and the agent's context. Add it to the appropriate ignore files for the active VCS (e.g., .gitignore, .hgignore) and tool configuration (e.g., .geminiignore) if not already present.
2.  **Execute Standard Protocol:** You MUST follow Steps **3.1**, **3.2**, **3.3**, and **3.5** of the "TRACK IMPLEMENTATION" protocol exactly as defined in the prompt.
3.  **Shell Command Execution:** Use flags that reject or prevent interactive user input (e.g., "-n", "--no-input").
4.  **AUTONOMOUS CYCLE:**
    -   For each task, execute this **RALPH CYCLE**:
        1.  **RED:** Write failing tests based on the **Specification**.
        2.  **GREEN:** Implement code to pass tests.
        3.  **VERIFY:** Run tests.
            -   **IF FAIL:** Attempt to fix and re-run. If still failing, call 'ralph_end' with status='FAILURE' and include the error details in the message.
            -   **PASS:** Proceed to the next task.
        4.  **RECORD:** Update plan status to [x] and commit changes.
5.  **SKIP MANUAL TASKS:** Mark any task involving "Manual Verification" or "User Feedback" as [x] immediately and proceed. Ralph's tests are the only source of truth.
6.  **COMPLETION:**
    -   **WHEN DONE:** If all tests pass and the track is [x]:
        1.  Call 'ralph_end' with status='SUCCESS' and message='Task complete: {{COMPLETION_WORD}}'.
        2.  **AFTER THE TOOL:** You will receive a confirmation message. **IMMEDIATELY** proceed to **Section 5.0** (Track Cleanup) and prompt the user.
    -   **IF STUCK:** If you are unable to proceed due to ambiguity or tool failures, call 'ralph_end' with status='STUCK' and explain why.
