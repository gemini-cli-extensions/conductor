import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	console.log('Conductor is now active!');
	let disposable = vscode.commands.registerCommand('conductor.newTrack', () => {
		vscode.window.showInformationMessage('Conductor: New Track command executed.');
	});
	context.subscriptions.push(disposable);
}

export function deactivate() {}
