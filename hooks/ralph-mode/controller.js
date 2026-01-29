const fs = require('fs');
const path = require('path');
const directiveContent = require('./directive.js');

/**
 * MANAGES THE AUTONOMOUS RALPH LOOP VIA AfterTool HOOK.
 */

const STATE_FILE = path.join(process.cwd(), 'conductor', '.ralph-state.json');

async function main() {
  // State File Missing (Quiet Exit)
  if (!fs.existsSync(STATE_FILE)) {
    console.log(JSON.stringify({}));
    return;
  }

  // Read & Parse Input
  let context;
  try {
    context = JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch (e) {
    console.log(JSON.stringify({}));
    return;
  }

  const { hook_event_name, tool_name, tool_input } = context;

  // Check if this is the end tool
  if (hook_event_name !== 'AfterTool' || !tool_name.endsWith('ralph_end')) {
    console.log(JSON.stringify({}));
    return;
  }

  // Load current Ralph loop state
  let state;
  try {
    state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    console.log(JSON.stringify({}));
    return;
  }

  const { status, message } = tool_input;

  // Case: SUCCESS
  if (status === 'SUCCESS') {
    try {
      fs.unlinkSync(STATE_FILE);
    } catch (e) {
      console.error(`[Ralph] Warning: Could not delete state file: ${e.message}`);
    }
    
    console.log(JSON.stringify({
      decision: "allow",
      systemMessage: "✅ Ralph: Cycle complete. State cleaned.",
    }));
    return;
  }

  // Case: FAILURE / RETRY LOOP
  
  // Check Iteration Limit
  if (state.iteration >= state.maxIterations) {
    try {
      fs.unlinkSync(STATE_FILE);
    } catch (e) {
      console.error(`[Ralph] Warning: Could not delete state file after max iterations: ${e.message}`);
    }
    console.log(JSON.stringify({
      decision: "deny",
      reason: "Stopping Ralph loop. Max iterations reached.",
      systemMessage: "🛑 Ralph: Max iterations reached. Stopping loop."
    }));
    return;
  }

  // Increment Iteration for the next turn
  state.iteration += 1;
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));

  // Prepare Re-injection Context
  const directive = directiveContent.replace('{{COMPLETION_WORD}}', state.completionWord);

  const failureContext = `
[RALPH SYSTEM MESSAGE]:
The previous session context was cleared to ensure focus.
LAST STATUS: ${status} (Iteration ${state.iteration - 1} of ${state.maxIterations})
REASON: ${message || "No specific reason provided."}

ACTION REQUIRED:
1.  **RE-ORIENT:** Analyze the current project state (git status, diff, logs).
2.  **FIX:** Modify the code, tests, or **Strategy** based on the failure reason.
3.  **VERIFY:** Run tests again.
4.  **FINALIZE:** Call 'ralph_end' with status 'SUCCESS' only when all tests pass and requirements are met.
`;

  const fullContextPrompt = `
${state.originalPrompt || ""}

---
${directive}
---

${failureContext}
`;

  // FORCE RETRY
  console.log(JSON.stringify({
    decision: "deny",
    reason: fullContextPrompt,  // Re-injects full context prompt.
    systemMessage: `🔄 Ralph: ${status} detected. Auto-retrying (Iter ${state.iteration}/${state.maxIterations})...`
  }));
}

main().catch(err => {
  console.error(`[Ralph Controller] Fatal: ${err.message}`);
  process.exit(1);
});
