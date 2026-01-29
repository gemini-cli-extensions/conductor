import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel("Conductor");

    // Copilot Chat Participant
    const handler: vscode.ChatRequestHandler = async (request: vscode.ChatRequest, context: vscode.ChatContext, stream: vscode.ChatResponseStream, token: vscode.CancellationToken) => {
        const command = request.command || 'status';
        const prompt = request.prompt || '';
        
        stream.progress(`Conductor is processing /${command}...`);

        // Map Copilot commands to Conductor CLI args
        const cmdMap: Record<string, string[]> = {
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
        } catch (err: any) {
            stream.markdown(`**Error:** ${err.message}`);
        }

        return { metadata: { command } };
    };

    const agent = vscode.chat.createChatParticipant('conductor.agent', handler);
    agent.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'icon.png');

    function runConductorCommandAsync(args: string[]): Promise<string> {
        return new Promise((resolve, reject) => {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (!workspaceFolders) {
                reject(new Error("No workspace folder open."));
                return;
            }
            const cwd = workspaceFolders[0].uri.fsPath;
            const command = `conductor-gemini ${args.join(' ')}`;
            
            exec(command, { cwd }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(stderr || stdout || error.message));
                } else {
                    resolve(stdout);
                }
            });
        });
    }

    function runConductorCommand(args: string[]) {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage("No workspace folder open.");
            return;
        }
        const cwd = workspaceFolders[0].uri.fsPath;
        const command = `conductor-gemini ${args.join(' ')}`;
        
        outputChannel.appendLine(`Running: ${command}`);
        outputChannel.show();

        exec(command, { cwd }, (error, stdout, stderr) => {
            if (stdout) outputChannel.append(stdout);
            if (stderr) outputChannel.append(stderr);
            if (error) {
                vscode.window.showErrorMessage(`Conductor error: ${error.message}`);
            }
        });
    }

    context.subscriptions.push(
        vscode.commands.registerCommand('conductor.setup', async () => {
            const goal = await vscode.window.showInputBox({ prompt: "Enter project goal" });
            if (goal) runConductorCommand(['setup', '--goal', goal]);
        }),
        vscode.commands.registerCommand('conductor.newTrack', async () => {
            const desc = await vscode.window.showInputBox({ prompt: "Enter track description" });
            if (desc) runConductorCommand(['new-track', `"${desc}"`]);
        }),
        vscode.commands.registerCommand('conductor.status', () => {
            runConductorCommand(['status']);
        }),
        vscode.commands.registerCommand('conductor.implement', async () => {
            const desc = await vscode.window.showInputBox({ prompt: "Enter track description (optional)" });
            const args = ['implement'];
            if (desc) args.push(`"${desc}"`);
            runConductorCommand(args);
        }),
        vscode.commands.registerCommand('conductor.revert', async () => {
            const trackId = await vscode.window.showInputBox({ prompt: "Enter track ID" });
            const taskDesc = await vscode.window.showInputBox({ prompt: "Enter task description to revert" });
            if (trackId && taskDesc) runConductorCommand(['revert', trackId, `"${taskDesc}"`]);
        })
    );
}

export function deactivate() {}