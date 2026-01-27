const fs = require('fs');
const path = require('path');
const directiveContent = require('./directive.js');

/**
 *
 * MANAGES THE AUTONOMOUS RALPH LOOP. 
 * 
 */

const STATE_FILE = path.join(process.cwd(), 'conductor', '.ralph-state.json');

async function main() {

  // State File Missing (Quiet Exit for normal usage)
  if (!fs.existsSync(STATE_FILE)) {
    console.log(JSON.stringify({}));
    return;
  }

  // Read & Parse Input
  let context;
  try {
    context = JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch (e) {
    console.error(`[Ralph] Error reading input: ${e.message}`);
    console.log(JSON.stringify({}));
    return;
  }

  const { prompt_response, stop_hook_active } = context;

  // Safety Checks
  if (stop_hook_active || !prompt_response) {
    console.log(JSON.stringify({}));
    return;
  }

  // Load current Ralph loop state
  let state;
  try {
    state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    console.log(JSON.stringify({
      systemMessage: `⚠️ Ralph Error: State file is corrupt (${e.message}). Please delete .ralph-state.json.`
    }));
    return;
  }

  // --- CORE LOGIC START ---
  
  // Check for Ralph Token (Agent reporting task completion status)
  if (!prompt_response.includes('[Ralph]:')) {
    console.log(JSON.stringify({}));
    return;
  }

  // Analyze for Success
  const escapedWord = state.completionWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const successRegex = new RegExp('<promise>\\s*' + escapedWord + '\\s*</promise>', 'i');
  
  // Case: SUCCESS
  if (successRegex.test(prompt_response)) {
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
  // The agent reported [Ralph]: but NOT the success token.
  
  // Check Iteration Limit
  if (state.iteration >= state.maxIterations) {
    try {
      fs.unlinkSync(STATE_FILE);
    } catch (e) {
      console.error(`[Ralph] Warning: Could not delete state file after max iterations: ${e.message}`);
    }
    console.log(JSON.stringify({
      decision: "deny",
      reason: "Stopping Ralph loop.",
      systemMessage: "🛑 Ralph: Max iterations reached. Stopping loop."
    }));
    return;
  }

  // Increment Iteration for the next turn
  const currentIteration = state.iteration || 0;
  state.iteration = currentIteration + 1;
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));

  // Prepare Re-injection Context
  const directive = directiveContent.replace('{{COMPLETION_WORD}}', state.completionWord);

  const failureContext = `
[RALPH SYSTEM MESSAGE]:
The previous session context was cleared to ensure focus.
LAST STATUS: FAILED (Iteration ${state.iteration - 1} of ${state.maxIterations})
ACTION REQUIRED:
1.  **RE-ORIENT:** Run \`git status\` and \`git diff\` (or read the modified files) to understand what changes were made in the previous failed attempt.
2.  **ANALYZE:** Use the failure reason provided above to determine why those changes failed or why you were stuck.
3.  **FIX:** Modify the code, tests, or **Strategy** (if stuck).
4.  **VERIFY:** Run tests again.
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
    clearContext: true,
    reason: fullContextPrompt,  // Re-injects full context prompt.
    systemMessage: `🔄 Ralph: Test failure detected. Auto-retrying (Iter ${state.iteration}/${state.maxIterations})...`
  }));
}

main().catch(err => {
  console.error(`[Ralph] Fatal Error: ${err.message}`);
  process.exit(1);
});
