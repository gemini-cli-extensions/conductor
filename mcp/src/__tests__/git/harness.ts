import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import { tmpdir } from 'os';
import { TestHarness } from '../harness';
import { GitVcs } from '../../vcs/git';
import { Vcs as VcsInterface } from '../../vcs/types';

function setupRepo(vcsType: 'git' | 'jj', remoteUrl?: string): string {
    const repoPath = fs.mkdtempSync(path.join(tmpdir(), 'mcp-test-repo-'));
    
    if (remoteUrl) {
        execSync(`git clone ${remoteUrl} .`, { cwd: repoPath });
    } else {
        execSync('git init', { cwd: repoPath });
        execSync('git config user.email "test@example.com"', { cwd: repoPath });
        execSync('git config user.name "Test User"', { cwd: repoPath });
        
        // Setup .gitattributes
        fs.writeFileSync(path.join(repoPath, '.gitattributes'), '*.bin binary');
        execSync('git add .gitattributes', { cwd: repoPath });
        execSync('git commit -m "Add gitattributes"', { cwd: repoPath });

        fs.writeFileSync(path.join(repoPath, 'initial.txt'), 'initial content');
        execSync('git add initial.txt', { cwd: repoPath });
        execSync('git commit -m "Initial commit"', { cwd: repoPath });
        fs.writeFileSync(path.join(repoPath, 'second.txt'), 'second content');
        execSync('git add second.txt', { cwd: repoPath });
        execSync('git commit -m "Second commit"', { cwd: repoPath });
    }
    
    return repoPath;
}

function createFile(repoPath: string, filePath: string, content: string | Buffer): void {
    fs.writeFileSync(path.join(repoPath, filePath), content);
}

function setupRemoteRepo(vcsType: 'git' | 'jj'): string {
    const bareRepoPath = fs.mkdtempSync(path.join(tmpdir(), 'mcp-test-bare-repo-'));
    const workingRepoPath = fs.mkdtempSync(path.join(tmpdir(), 'mcp-test-working-repo-'));

    execSync('git init --bare', { cwd: bareRepoPath });

    execSync('git init', { cwd: workingRepoPath });
    execSync('git config user.email "test-remote@example.com"', { cwd: workingRepoPath });
    execSync('git config user.name "Test Remote User"', { cwd: workingRepoPath });
    
    // Setup .gitattributes for the remote repo
    fs.writeFileSync(path.join(workingRepoPath, '.gitattributes'), '*.bin binary');
    execSync('git add .gitattributes', { cwd: workingRepoPath });
    execSync('git commit -m "Add gitattributes"', { cwd: workingRepoPath });

    fs.writeFileSync(path.join(workingRepoPath, 'initial.txt'), 'initial content in remote');
    execSync('git add initial.txt', { cwd: workingRepoPath });
    execSync('git commit -m "Initial commit in remote"', { cwd: workingRepoPath });

    fs.writeFileSync(path.join(workingRepoPath, 'second.txt'), 'second content in remote');
    execSync('git add second.txt', { cwd: workingRepoPath });
    execSync('git commit -m "Second commit in remote"', { cwd: workingRepoPath });

    execSync(`git remote add origin ${bareRepoPath}`, { cwd: workingRepoPath });
    execSync('git push -u origin main', { cwd: workingRepoPath });
    
    teardownRepo(workingRepoPath);
    return bareRepoPath;
}

function teardownRepo(repoPath: string): void {
    fs.rmSync(repoPath, { recursive: true, force: true });
}

function runCmd(command: string, repoPath: string): string {
    return execSync(command, { cwd: repoPath }).toString().trim();
}

export const harness: TestHarness = {
    setupRepo: (vcsType: 'git' | 'jj', remoteUrl?: string) => setupRepo('git', remoteUrl),
    setupRemoteRepo: (vcsType: 'git' | 'jj') => setupRemoteRepo('git'),
    teardownRepo,
    runCmd,
    createFile,
    getVcs: (repoPath: string): VcsInterface => new GitVcs(),
};
