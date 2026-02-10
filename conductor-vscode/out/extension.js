"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
const skills_1 = require("./skills");
function activate(context) {
    const outputChannel = vscode.window.createOutputChannel("Conductor");
    const cliName = 'conductor-gemini';
    let cliCheckPromise = null;
    const getWorkspaceCwd = () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        return workspaceFolders?.[0]?.uri.fsPath ?? null;
    };
    const buildCliArgsFromPrompt = (command, prompt) => {
        switch (command) {
            case 'setup':
                return prompt ? ['setup', '--goal', prompt] : ['setup'];
            case 'newtrack':
                return prompt ? ['new-track', prompt] : ['new-track'];
            case 'status':
                return ['status'];
            case 'implement':
                return ['implement'];
            case 'revert':
                return prompt ? ['revert', prompt] : ['revert'];
            default:
                return ['status'];
        }
    };
    const hasConductorCli = () => {
        if (process.env.CONDUCTOR_VSCODE_FORCE_SKILLS === '1') {
            return Promise.resolve(false);
        }
        if (!cliCheckPromise) {
            const checkCommand = process.platform === 'win32'
                ? `where ${cliName}`
                : `command -v ${cliName}`;
            cliCheckPromise = new Promise((resolve) => {
                (0, child_process_1.exec)(checkCommand, (error, stdout) => {
                    resolve(!error && stdout.trim().length > 0);
                });
            });
        }
        return cliCheckPromise;
    };
    const runCli = (args, cwd) => {
        return new Promise((resolve, reject) => {
            (0, child_process_1.execFile)(cliName, args, { cwd }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(stderr || stdout || error.message));
                    return;
                }
                resolve(stdout || '');
            });
        });
    };
    const formatSkillFallback = (command, prompt, skillContent, hasWorkspace) => {
        const sections = [
            `**Conductor skill loaded for /${command}**`,
            `Running in skills mode because ${cliName} was not found on PATH.`,
        ];
        if (!hasWorkspace) {
            sections.push("**Note:** No workspace folder is open; some steps may require an active workspace.");
        }
        if (prompt) {
            sections.push(`**User prompt:** ${prompt}`);
        }
        sections.push('---', skillContent);
        return sections.join('\n\n');
    };
    const runConductor = async (command, prompt, cliArgs) => {
        const cwd = getWorkspaceCwd();
        const args = cliArgs ?? buildCliArgsFromPrompt(command, prompt);
        if (await hasConductorCli()) {
            if (!cwd) {
                throw new Error("No workspace folder open.");
            }
            return runCli(args, cwd);
        }
        const skillContent = await (0, skills_1.readSkillContent)(context.extensionPath, command);
        if (!skillContent) {
            throw new Error(`Conductor CLI not found and skill content is missing for /${command}.`);
        }
        return formatSkillFallback(command, prompt, skillContent, Boolean(cwd));
    };
    // Copilot Chat Participant
    const handler = async (request, chatContext, stream, token) => {
        const commandKey = (0, skills_1.normalizeCommand)(request.command);
        const prompt = request.prompt || '';
        stream.progress(`Conductor is processing /${commandKey}...`);
        try {
            const result = await runConductor(commandKey, prompt);
            stream.markdown(result);
        }
        catch (err) {
            stream.markdown(`**Error:** ${err.message}`);
        }
        return { metadata: { command: commandKey } };
    };
    const agent = vscode.chat.createChatParticipant('conductor.agent', handler);
    agent.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'icon.png');
    async function runConductorCommand(command, prompt, cliArgs) {
        try {
            const result = await runConductor(command, prompt, cliArgs);
            outputChannel.appendLine(result);
            outputChannel.show();
        }
        catch (error) {
            let message = error?.message ?? String(error);
            // Try to parse structured error from core if it's JSON
            try {
                const parsed = JSON.parse(message);
                if (parsed.error) {
                    message = `[${parsed.error.category.toUpperCase()}] ${parsed.error.message}`;
                }
            }
            catch (e) {
                // Not JSON, use original message
            }
            outputChannel.appendLine(message);
            outputChannel.show();
            vscode.window.showErrorMessage(`Conductor: ${message}`);
        }
    }
    context.subscriptions.push(vscode.commands.registerCommand('conductor.setup', async () => {
        const goal = await vscode.window.showInputBox({ prompt: "Enter project goal" });
        if (goal) {
            runConductorCommand('setup', goal, ['setup', '--goal', goal]);
        }
    }), vscode.commands.registerCommand('conductor.newTrack', async () => {
        const desc = await vscode.window.showInputBox({ prompt: "Enter track description" });
        if (desc) {
            runConductorCommand('newtrack', desc, ['new-track', desc]);
        }
    }), vscode.commands.registerCommand('conductor.status', () => {
        runConductorCommand('status', '', ['status']);
    }), vscode.commands.registerCommand('conductor.implement', async () => {
        const desc = await vscode.window.showInputBox({ prompt: "Enter track description (optional)" });
        const args = ['implement'];
        if (desc)
            args.push(desc);
        runConductorCommand('implement', desc ?? '', args);
    }), vscode.commands.registerCommand('conductor.revert', async () => {
        const trackId = await vscode.window.showInputBox({ prompt: "Enter track ID" });
        const taskDesc = await vscode.window.showInputBox({ prompt: "Enter task description to revert" });
        if (trackId && taskDesc) {
            runConductorCommand('revert', `${trackId} ${taskDesc}`, ['revert', trackId, taskDesc]);
        }
    }));
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map
