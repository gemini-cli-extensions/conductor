const fs = require('fs');
const path = require('path');

/**
 * INITIALIZES RALPH MODE AFTER THE START TOOL IS CALLED.
 **/

const STATE_FILE = path.join(process.cwd(), 'conductor', '.ralph-state.json');

async function main() {
  // Read Input
  let context;
  try {
    context = JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch (e) {
    console.log(JSON.stringify({}));
    return;
  }

  const { hook_event_name, tool_name, tool_input } = context;

  // Check if this is the start tool
  if (hook_event_name !== 'AfterTool' || !tool_name.endsWith('ralph_start')) {
    console.log(JSON.stringify({}));
    return;
  }

  // --- RALPH MODE DETECTED ---

  const prompt = tool_input.prompt || "";
  const maxIterations = tool_input.maxIterations || 10;

  // Create State File
  const state = {
    maxIterations: maxIterations,
    iteration: 1,
    startedAt: new Date().toISOString(),
    originalPrompt: prompt,
  };

  try {
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (e) {
    console.log(JSON.stringify({
      decision: "deny",
      reason: `CRITICAL: Ralph Mode failed to initialize. Could not create state file (${e.message}). Aborting autonomous mode.`,
      systemMessage: "🛑 Ralph Init Failed: File system error."
    }));
    return;
  }

  // Inject Directive
  let directiveContent = "";
  try {
    const directivePath = path.join(__dirname, 'directive.md');
    directiveContent = fs.readFileSync(directivePath, 'utf8');
  } catch (e) {
    console.log(JSON.stringify({
      decision: "deny",
      reason: `CRITICAL: Ralph Mode failed to initialize. (${e.message}). Aborting.`,
      systemMessage: "🛑 Ralph Init Failed: Missing directive."
    }));
    return;
  }

  const directive = directiveContent;

  // Output the JSON response
  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "AfterTool",
      additionalContext: directive
    },
    systemMessage: "🔴 Ralph Mode Activated: Architect Phase Engaged.",
  }));
}

main().catch(err => {
  console.error(`[Ralph Init] Fatal: ${err.message}`);
  process.exit(1);
});