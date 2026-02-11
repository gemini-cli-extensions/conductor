const fs = require('fs');
const path = require('path');

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

  // Case: SUCCESS (Loop Complete)
  if (status === 'SUCCESS') {
    try {
      fs.unlinkSync(STATE_FILE);
    } catch (e) {
      console.error(`[Ralph] Warning: Could not delete state file: ${e.message}`);
    }
    
    console.log(JSON.stringify({
      decision: "allow",
      systemMessage: "✅ Ralph: Cycle complete. Plan Certified.",
    }));
    return;
  }

  // Case: STUCK (Loop Aborted by Agent)
  // The agent cannot solve the problem (e.g., Bad Spec).
  if (status === 'STUCK') {
    try {
      fs.unlinkSync(STATE_FILE);
    } catch (e) {
      console.error(`[Ralph] Warning: Could not delete state file: ${e.message}`);
    }

    console.log(JSON.stringify({
      decision: "allow",
      systemMessage: "🛑 Ralph: Stuck. Aborting loop to request user input.",
    }));
    return;
  }

  // Case: RETRY LOOP (Auto-Correction)
  
  // Check Iteration Limit
  if (state.iteration >= state.maxIterations) {
    try {
      fs.unlinkSync(STATE_FILE);
    } catch (e) {
      console.error(`[Ralph] Warning: Could not delete state file after max iterations: ${e.message}`);
    }
    console.log(JSON.stringify({
      continue: false,
      stopReason: "🛑 Ralph: Max iterations reached.",
    }));
    return;
  }

  // Increment Iteration for the next turn
  state.iteration += 1;
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));

  // Load Directive
  let directiveContent = "";
  try {
    const directivePath = path.join(__dirname, 'directive.md');
    directiveContent = fs.readFileSync(directivePath, 'utf8');
  } catch (e) {
    console.log(JSON.stringify({
      decision: "deny",
      reason: `CRITICAL: Ralph Mode controller failed. Could not read directive file (${e.message}). Aborting loop.`,
      systemMessage: "🛑 Ralph Controller Failed: Missing directive."
    }));
    return;
  }

  // Prepare Re-injection Context
  const directive = directiveContent;

  const failureContext = `
[RALPH ARCHITECT MESSAGE]:
The previous planning step was interrupted or incomplete.
LAST STATUS: ${status} (Iteration ${state.iteration} of ${state.maxIterations})
REASON: ${message || "No specific reason provided."}

ACTION REQUIRED:
1.  **RE-ORIENT:** Re-read the **Specification** and current **Implementation Plan**.
2.  **FIX:** Address the gaps, ambiguities, or dependency issues identified in the 'REASON'.
3.  **VERIFY:** Ensure 100% coverage and atomic tasks.
4.  **FINALIZE:** Call 'ralph_end' with status 'SUCCESS' only when the Plan is fully certified.
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
