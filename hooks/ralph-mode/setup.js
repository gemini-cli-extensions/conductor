const fs = require('fs');
const path = require('path');
const directiveContent = require('./directive.js');

/**
 *
 * INITIALIZES RALPH MODE BEFORE THE AGENT STARTS.
 * 
 * Strategy:
 * 1. Check user prompt for '--ralph' flag.
 * 2. If found, create .ralph-state.json.
 * 3. Inject the Ralph Protocol Directive
 **/

const STATE_FILE = path.join(process.cwd(), 'conductor', '.ralph-state.json');

/**
 * Extracts the value of a specific flag from a text string.
 * Supports formats like --flag=value, --flag value, --flag="value".
 * 
 * @param {string} text - The input text to search.
 * @param {string} flag - The flag name (including dashes).
 * @returns {string|null} The extracted value or null if not found.
 */
function getFlag(text, flag) {
  const regex = new RegExp(`${flag}[=\\s]+(?:["']([^"']+)["']|([^\\s]+))`);
  const match = text.match(regex);
  if (!match) return null;
  // match[1] is the quoted value, match[2] is the unquoted value
  return match[1] || match[2];
}

async function main() {
  // Read Input
  let context;
  try {
    context = JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch (e) {
    console.log(JSON.stringify({}));
    return;
  }

  const { prompt, timestamp } = context;

  // Check for Flag and Command Scope
  if (!prompt || !prompt.includes('/conductor:implement') || !prompt.includes('--ralph')) {
    console.log(JSON.stringify({}));
    return;
  }

  // --- RALPH MODE DETECTED ---

  // Robust Argument Parsing
  const completionWord = getFlag(prompt, '--completion-word') || 'TRACK_COMPLETE';
  const maxIterationsStr = getFlag(prompt, '--max-iterations');
  const maxIterations = maxIterationsStr ? parseInt(maxIterationsStr, 10) : 10;

  // Create State File
  const state = {
    completionWord: completionWord,
    maxIterations: maxIterations,
    iteration: 1,
    startedAt: timestamp || new Date().toISOString(),
    originalPrompt: prompt,
  };

  try {
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (e) {
    console.log(JSON.stringify({
      systemMessage: `⚠️ Ralph Init Failed: Could not create state file (${e.message}). Loop will not be active.`
    }));
    return;
  }

  // Inject Directive
  const directive = directiveContent.replace('{{COMPLETION_WORD}}', completionWord);

  // Output the JSON response
  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "BeforeAgent",
      additionalContext: directive
    },
    systemMessage: "🔴 Ralph Mode Activated: TDD Loop Engaged.",
  }));
}

main().catch(err => {
  console.error(`[Ralph Init] Fatal: ${err.message}`);
  process.exit(1);
});
