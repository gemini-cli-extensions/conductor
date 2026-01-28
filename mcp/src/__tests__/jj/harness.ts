import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import { tmpdir } from 'os';
import { TestHarness } from '../harness';
import { JjVcs } from '../../vcs/jj';
import { Vcs as VcsInterface } from '../../vcs/types';
import { harness as gitHarness } from '../git/harness';

function setupRepo(vcsType: 'git' | 'jj', remoteUrl?: string): string {
    const repoPath = fs.mkdtempSync(path.join(tmpdir(), 'mcp-jj-test-repo-'));
    
    execSync('git init', { cwd: repoPath });
    execSync('jj git init', { cwd: repoPath });

    // Setup .gitattributes for binary file detection
    fs.writeFileSync(path.join(repoPath, '.gitattributes'), '*.bin binary');
    runCmd('jj commit -m "Add gitattributes"', repoPath);

    createFile(repoPath, 'initial.txt', 'initial content');
    runCmd('jj commit -m "Initial commit"', repoPath);

    // Ensure the main bookmark exists for tests that depend on it
    runCmd('jj bookmark create main -r @', repoPath);

    return repoPath;
}

function teardownRepo(repoPath: string): void {
    fs.rmSync(repoPath, { recursive: true, force: true });
}

function runCmd(command: string, repoPath: string): string {
    return execSync(command, { cwd: repoPath, env: { ...process.env, EDITOR: 'true' } }).toString().trim();
}

function createFile(repoPath: string, filePath: string, content: string | Buffer): void {
    fs.writeFileSync(path.join(repoPath, filePath), content);
}

// For Jujutsu, remote operations typically involve a Git remote
// so we can reuse the Git remote setup and adapt it.
function setupRemoteRepoJj(vcsType: 'git' | 'jj'): string {
    const bareGitRepoPath = gitHarness.setupRemoteRepo('git');
    // The gitHarness.setupRemoteRepo implicitly calls gitHarness.teardownRepo(workingRepoPath);
    // So, no explicit teardown is needed here for workingRepoPath.
    return bareGitRepoPath;
}

export const harness: TestHarness = {
    setupRepo: (vcsType: 'git' | 'jj', remoteUrl?: string) => setupRepo('jj', remoteUrl),
    setupRemoteRepo: (vcsType: 'git' | 'jj') => setupRemoteRepoJj('jj'),
    teardownRepo,
    runCmd,
    createFile,
    getVcs: (repoPath: string): VcsInterface => new JjVcs(),
};

// getCleanCommitId is a JJ-specific helper and not part of the generic harness interface.
// It will be used internally by JJ E2E tests for now, if needed.
// If it becomes generic, it can be moved to the shared harness and implemented for Git.
export function getCleanCommitId(repoPath: string, revset: string = '@'): string {
    const output = runCmd(`jj log -r '${revset}' -T "commit_id"`, repoPath);
    const parts = output.split(' ').filter(Boolean);
    let commitId = parts[parts.length - 1];
    commitId = commitId.replace(/[^0-9a-fA-F]/g, '');
    return commitId;
}