import * as vscode from 'vscode';
import { exec } from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel("Conductor");

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
            vscode.window.showInformationMessage("Revert command is handled via track plan updates.");
        })
    );
}

export function deactivate() {}