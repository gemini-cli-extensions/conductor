import * as vscode from 'vscode';
import { exec, execFile } from 'child_process';
import { normalizeCommand, readSkillContent, SkillCommand } from './skills';

export function activate(context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel("Conductor");
    const cliName = 'conductor-gemini';
    let cliCheckPromise: Promise<boolean> | null = null;

    const getWorkspaceCwd = (): string | null => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        return workspaceFolders?.[0]?.uri.fsPath ?? null;
    };

    const buildCliArgsFromPrompt = (command: SkillCommand, prompt: string): string[] => {
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

    const hasConductorCli = (): Promise<boolean> => {
        if (process.env.CONDUCTOR_VSCODE_FORCE_SKILLS === '1') {
            return Promise.resolve(false);
        }

        if (!cliCheckPromise) {
            const checkCommand = process.platform === 'win32'
                ? `where ${cliName}`
                : `command -v ${cliName}`;

            cliCheckPromise = new Promise((resolve) => {
                exec(checkCommand, (error, stdout) => {
                    resolve(!error && stdout.trim().length > 0);
                });
            });
        }

        return cliCheckPromise;
    };

    const runCli = (args: string[], cwd: string): Promise<string> => {
        return new Promise((resolve, reject) => {
            execFile(cliName, args, { cwd }, (error, stdout, stderr) => {
                if (error) {
                    reject(new Error(stderr || stdout || error.message));
                    return;
                }
                resolve(stdout || '');
            });
        });
    };

    const formatSkillFallback = (command: SkillCommand, prompt: string, skillContent: string, hasWorkspace: boolean): string => {
        const sections: string[] = [
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

    const runConductor = async (
        command: SkillCommand,
        prompt: string,
        cliArgs?: string[],
    ): Promise<string> => {
        const cwd = getWorkspaceCwd();
        const args = cliArgs ?? buildCliArgsFromPrompt(command, prompt);

        if (await hasConductorCli()) {
            if (!cwd) {
                throw new Error("No workspace folder open.");
            }
            return runCli(args, cwd);
        }

        const skillContent = await readSkillContent(context.extensionPath, command);
        if (!skillContent) {
            throw new Error(`Conductor CLI not found and skill content is missing for /${command}.`);
        }

        return formatSkillFallback(command, prompt, skillContent, Boolean(cwd));
    };

    // Copilot Chat Participant
    const handler: vscode.ChatRequestHandler = async (request: vscode.ChatRequest, chatContext: vscode.ChatContext, stream: vscode.ChatResponseStream, token: vscode.CancellationToken) => {
        const commandKey = normalizeCommand(request.command);
        const prompt = request.prompt || '';

        stream.progress(`Conductor is processing /${commandKey}...`);

        try {
            const result = await runConductor(commandKey, prompt);
            stream.markdown(result);
        } catch (err: any) {
            stream.markdown(`**Error:** ${err.message}`);
        }

        return { metadata: { command: commandKey } };
    };

    const agent = vscode.chat.createChatParticipant('conductor.agent', handler);
    agent.iconPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'icon.png');

    async function runConductorCommand(command: SkillCommand, prompt: string, cliArgs?: string[]) {
        try {
            const result = await runConductor(command, prompt, cliArgs);
            outputChannel.appendLine(result);
            outputChannel.show();
        } catch (error: any) {
            let message = error?.message ?? String(error);

            // Try to parse structured error from core if it's JSON
            try {
                const parsed = JSON.parse(message);
                if (parsed.error) {
                    message = `[${parsed.error.category.toUpperCase()}] ${parsed.error.message}`;
                }
            } catch (e) {
                // Not JSON, use original message
            }

            outputChannel.appendLine(message);
            outputChannel.show();
            vscode.window.showErrorMessage(`Conductor: ${message}`);
        }
    }

    context.subscriptions.push(
        vscode.commands.registerCommand('conductor.setup', async () => {
            const goal = await vscode.window.showInputBox({ prompt: "Enter project goal" });
            if (goal) {
                runConductorCommand('setup', goal, ['setup', '--goal', goal]);
            }
        }),
        vscode.commands.registerCommand('conductor.newTrack', async () => {
            const desc = await vscode.window.showInputBox({ prompt: "Enter track description" });
            if (desc) {
                runConductorCommand('newtrack', desc, ['new-track', desc]);
            }
        }),
        vscode.commands.registerCommand('conductor.status', () => {
            runConductorCommand('status', '', ['status']);
        }),
        vscode.commands.registerCommand('conductor.implement', async () => {
            const desc = await vscode.window.showInputBox({ prompt: "Enter track description (optional)" });
            const args = ['implement'];
            if (desc) args.push(desc);
            runConductorCommand('implement', desc ?? '', args);
        }),
        vscode.commands.registerCommand('conductor.revert', async () => {
            const trackId = await vscode.window.showInputBox({ prompt: "Enter track ID" });
            const taskDesc = await vscode.window.showInputBox({ prompt: "Enter task description to revert" });
            if (trackId && taskDesc) {
                runConductorCommand('revert', `${trackId} ${taskDesc}`, ['revert', trackId, taskDesc]);
            }
        })
    );
}

export function deactivate() {}
