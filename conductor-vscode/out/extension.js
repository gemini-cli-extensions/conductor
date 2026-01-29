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
function activate(context) {
    const outputChannel = vscode.window.createOutputChannel("Conductor");
    // Copilot Chat Participant
    const handler = async (request, context, stream, token) => {
        const command = request.command || 'status';
        const prompt = request.prompt || '';
        stream.progress(`Conductor is processing /${command}...`);
        // Map Copilot commands to Conductor CLI args
        const cmdMap = {
            'setup': ['setup', '--goal', prompt],
            'newtrack': ['new-track', `"${prompt}"`],
            'status': ['status'],
            'implement': ['implement'],
            'revert': ['revert']
        };
        const args = cmdMap[command] || ['status'];
        try {
            const result = await runConductorCommandAsync(args);
            stream.markdown(result);
        }
        catch (err) {
            stream.markdown(`**Error:** ${err.message}`);
        }
        return { metadata: { command } };
    };
    const agent = vscode.chat.createChatParticipant('conductor.agent', handler);
    agent.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'icon.png');
    function runConductorCommandAsync(args) {
        return new Promise((resolve, reject) => {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (!workspaceFolders) {
                reject(new Error("No workspace folder open."));
                return;
            }
            const cwd = workspaceFolders[0].uri.fsPath;
            const command = `conductor-gemini ${args.join(' ')}`;
            (0, child_process_1.exec)(command, { cwd }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(stderr || stdout || error.message));
                }
                else {
                    resolve(stdout);
                }
            });
        });
    }
    function runConductorCommand(args) {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage("No workspace folder open.");
            return;
        }
        const cwd = workspaceFolders[0].uri.fsPath;
        const command = `conductor-gemini ${args.join(' ')}`;
        outputChannel.appendLine(`Running: ${command}`);
        outputChannel.show();
        (0, child_process_1.exec)(command, { cwd }, (error, stdout, stderr) => {
            if (stdout)
                outputChannel.append(stdout);
            if (stderr)
                outputChannel.append(stderr);
            if (error) {
                vscode.window.showErrorMessage(`Conductor error: ${error.message}`);
            }
        });
    }
    context.subscriptions.push(vscode.commands.registerCommand('conductor.setup', async () => {
        const goal = await vscode.window.showInputBox({ prompt: "Enter project goal" });
        if (goal)
            runConductorCommand(['setup', '--goal', goal]);
    }), vscode.commands.registerCommand('conductor.newTrack', async () => {
        const desc = await vscode.window.showInputBox({ prompt: "Enter track description" });
        if (desc)
            runConductorCommand(['new-track', `"${desc}"`]);
    }), vscode.commands.registerCommand('conductor.status', () => {
        runConductorCommand(['status']);
    }), vscode.commands.registerCommand('conductor.implement', async () => {
        const desc = await vscode.window.showInputBox({ prompt: "Enter track description (optional)" });
        const args = ['implement'];
        if (desc)
            args.push(`"${desc}"`);
        runConductorCommand(args);
    }), vscode.commands.registerCommand('conductor.revert', async () => {
        const trackId = await vscode.window.showInputBox({ prompt: "Enter track ID" });
        const taskDesc = await vscode.window.showInputBox({ prompt: "Enter task description to revert" });
        if (trackId && taskDesc)
            runConductorCommand(['revert', trackId, `"${taskDesc}"`]);
    }));
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map