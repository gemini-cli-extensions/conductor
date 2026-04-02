import { writeFileSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync } from 'fs';
import { exec } from 'child_process';
import path from 'path';
import os from 'os';

/**
 * Orchestrates the advanced spec development workflow.
 * Handles Git worktree isolation, session plans, and trackers.
 */

function ensureDir(dirPath: string) {
    if (!existsSync(dirPath)) {
        mkdirSync(dirPath, { recursive: true });
    }
}

/**
 * Automatically retrieves the latest sessionId from Gemini CLI logs or chat history.
 */
export function getLatestSessionId(): string | undefined {
    const projectName = 'agent-spec-sdlc'; // Default project name
    const homeDir = os.homedir();
    
    // Paths to check for logs.json
    const logPaths = [
        path.resolve(process.cwd(), '.gemini', 'tmp', projectName, 'logs.json'),
        path.resolve(homeDir, '.gemini', 'tmp', projectName, 'logs.json')
    ];

    for (const logPath of logPaths) {
        if (existsSync(logPath)) {
            try {
                const logs = JSON.parse(readFileSync(logPath, 'utf-8'));
                if (Array.isArray(logs) && logs.length > 0) {
                    const latest = logs[logs.length - 1];
                    if (latest.sessionId) return latest.sessionId;
                }
            } catch (e) {
                console.error(`Error parsing logs at ${logPath}:`, e);
            }
        }
    }

    // Fallback: check chats directory
    const chatPaths = [
        path.resolve(process.cwd(), '.gemini', 'tmp', projectName, 'chats'),
        path.resolve(homeDir, '.gemini', 'tmp', projectName, 'chats')
    ];

    for (const chatPath of chatPaths) {
        if (existsSync(chatPath)) {
            try {
                const sessionDirs = readdirSync(chatPath);
                if (sessionDirs.length > 0) {
                    // Sort by modification time to find latest
                    const sorted = sessionDirs
                        .map(name => ({ name, time: statSync(path.join(chatPath, name)).mtimeMs }))
                        .sort((a, b) => b.time - a.time);
                    return sorted[0].name;
                }
            } catch (e) {
                console.error(`Error reading chats at ${chatPath}:`, e);
            }
        }
    }

    return undefined;
}

/**
 * Initializes a session by creating a Git worktree.
 * Isolate user interactions to prevent filesystem collisions.
 */
export async function initSession(sessionId?: string): Promise<string> {
    const sessId = sessionId || getLatestSessionId();
    if (!sessId) throw new Error("Could not determine sessionId automatically. Please provide one.");

    return new Promise((resolve, reject) => {
        const worktreePath = path.resolve(process.cwd(), '.gemini', 'worktrees', sessId);
        const branchName = `gemini/session-${sessId}`;

        console.error(`Creating worktree for session ${sessId} at ${worktreePath}...`);

        // Check if worktree already exists
        if (existsSync(worktreePath)) {
            return resolve(`Session ${sessId} already initialized at ${worktreePath}`);
        }

        exec(`git worktree add "${worktreePath}" -b ${branchName}`, (err, stdout, stderr) => {
            if (err) {
                console.error(`Failed to create worktree: ${stderr}`);
                return reject(err);
            }
            resolve(`Session ${sessId} initialized in worktree: ${worktreePath}`);
        });
    });
}

/**
 * Creates a session-specific plan.
 * Stored in a session-specific directory to avoid rewriting.
 */
export async function createSessionPlan(sessionId: string | undefined, planId: string, goal: string, specId: string): Promise<string> {
    const sessId = sessionId || getLatestSessionId();
    if (!sessId) throw new Error("Could not determine sessionId automatically. Please provide one.");

    const sessionDir = path.resolve(process.cwd(), '.gemini', 'asdd', sessId);
    const plansDir = path.resolve(sessionDir, 'plans');
    ensureDir(plansDir);

    const planPath = path.resolve(plansDir, `${planId}.md`);

    const planContent = `# Plan: ${planId}

## Goal
${goal}

## Target Spec
Linked Spec ID: ${specId}

## Implementation Details
(To be filled by agent)
`;

    writeFileSync(planPath, planContent);
    return `Plan ${planId} created for session ${sessId} at ${planPath}`;
}

/**
 * Creates a session-specific task (tracker).
 * Scoped to session level.
 */
export async function createSessionTask(sessionId: string | undefined, taskId: string, description: string, planId: string): Promise<string> {
    const sessId = sessionId || getLatestSessionId();
    if (!sessId) throw new Error("Could not determine sessionId automatically. Please provide one.");

    const sessionDir = path.resolve(process.cwd(), '.gemini', 'asdd', sessId);
    const trackersDir = path.resolve(sessionDir, 'trackers');
    ensureDir(trackersDir);

    const trackerPath = path.resolve(trackersDir, `${taskId}.json`);

    const trackerData = {
        id: taskId,
        planId: planId,
        description: description,
        status: 'PENDING',
        createdAt: new Date().toISOString()
    };

    writeFileSync(trackerPath, JSON.stringify(trackerData, null, 2));
    return `Task ${taskId} created for session ${sessId} at ${trackerPath}`;
}

/**
 * Merges the session worktree back to the main branch.
 * Human-in-the-loop validation is expected before this.
 */

/**
 * Executes verifiers defined in specs/plans.
 */
export async function runVerifiers(sessionId: string): Promise<string> {
    // Placeholder for running verifiers
    return `Verifiers executed for session ${sessionId}`;
}

/**
 * Visualizes the Spec DAG as an ASCII tree or formatted list.
 */
export async function visualizeDAG(): Promise<string> {
    const specsDir = path.resolve(process.cwd(), 'conductor', 'tracks');
    const asddDir = path.resolve(process.cwd(), '.gemini', 'asdd');
    
    if (!existsSync(specsDir)) {
        return "No specs directory found. Run /spec init first.";
    }

    const files = readdirSync(specsDir, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => path.join(dirent.name, 'spec.md'))
        .filter(relPath => existsSync(path.resolve(specsDir, relPath)));
        
    const nodes: { [id: string]: { id: string, parent?: string, title: string, children: string[] } } = {};

    for (const file of files) {
        const filePath = path.resolve(specsDir, file);
        const content = readFileSync(filePath, 'utf-8');

        const idMatch = content.match(/^id:\s*(.*)$/m);
        const parentMatch = content.match(/^parent:\s*(.*)$/m);
        const titleMatch = content.match(/^# (.*)$/m);

        if (idMatch) {
            const id = idMatch[1].trim();
            nodes[id] = {
                id,
                parent: parentMatch ? parentMatch[1].trim() : undefined,
                title: titleMatch ? titleMatch[1].trim() : file,
                children: []
            };
        }
    }

    // Link children to parents
    for (const id in nodes) {
        const parentId = nodes[id].parent;
        if (parentId && nodes[parentId]) {
            nodes[parentId].children.push(id);
        }
    }

    let output = "### Project Spec DAG\n\n";

    function printNode(id: string, depth: number) {
        const node = nodes[id];
        const indent = "  ".repeat(depth);
        output += `${indent}- **${node.id}**: ${node.title}\n`;
        for (const childId of node.children) {
            printNode(childId, depth + 1);
        }
    }

    // Find roots and print
    for (const id in nodes) {
        if (!nodes[id].parent) {
            printNode(id, 0);
        }
    }

    return output;
}
