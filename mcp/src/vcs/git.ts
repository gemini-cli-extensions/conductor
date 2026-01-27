import { execSync, ExecSyncOptions } from 'child_process';
import { 
    NotARepositoryError, 
    DirtyWorkingDirectoryError, 
    GenericVCSError, 
    VCSRepositoryLockedError, 
    AuthenticationError, 
    MergeConflictError, 
    VCSNotFoundError,
    VcsStatus,
    CommitParams,
    Reference
} from './types';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

export class Vcs {
    private runCommand(command: string, options?: ExecSyncOptions): string {
        try {
            return execSync(command, { stdio: 'pipe', encoding: 'utf-8', ...options }).trim();
        } catch (error: any) {
            // Define stderr once at the beginning of the catch block
            const stderr = error.stderr?.toString().toLowerCase() || '';

            // VCSNotFoundError: Check first, as it's a fundamental system-level error
            if (error.code === 'ENOENT' || stderr.includes('command not found') || stderr.includes('enoent')) {
                throw new VCSNotFoundError('Git executable not found');
            }
            // VCSRepositoryLockedError
            if (stderr.includes('index.lock')) {
                throw new VCSRepositoryLockedError('Repo locked', '.git/index.lock');
            }
            // NotARepositoryError
            if (stderr.includes('fatal: not a git repository')) {
                throw new NotARepositoryError('Not a git repository');
            }
            // DirtyWorkingDirectoryError
            if (stderr.includes('overwritten by checkout') || stderr.includes('local changes would be overwritten') || stderr.includes('your local changes to the following files would be overwritten')) {
                throw new DirtyWorkingDirectoryError('Dirty working directory');
            }
            // AuthenticationError
            if (stderr.includes('authentication failed') || stderr.includes('bad username or password')) {
                throw new AuthenticationError('Authentication failed');
            }
            // MergeConflictError
            if (stderr.includes('conflict: merge conflict') || stderr.includes('merging is not possible because you have unmerged files')) {
                throw new MergeConflictError('Merge conflict', []); // Files will be determined by list_conflicts
            }
            // GenericVCSError for all other unexpected errors
            throw new GenericVCSError(error.message, command, error.status);
        }
    }

    private parseStatus(output: string): VcsStatus {
        const status: VcsStatus = { modified:[], untracked:[], added:[], deleted:[], conflicted:[], renamed:[], is_operation_in_progress:{type:'none'} };
        if (!output) return status;
        output.split('\n').forEach(line => {
            const lineCode = line[0];
            const contentRaw = line.substring(line.indexOf(' ', 5) + 1);
            let contentProcessed = contentRaw; // Initialize here

            const xy = line.substring(2, 4);

            if (lineCode === '?') {
                status.untracked.push(contentRaw.substring(2)); // Remove '? '
            } else if (lineCode === 'u') {
                status.conflicted.push(contentRaw.split(' ').pop()!);
            } else if (lineCode === '1') {
                // For other '1' codes (modified, added, deleted)
                const parts = contentRaw.split(/\s+/);
                contentProcessed = parts[parts.length - 1];
                if (xy[0] === 'M' || xy[1] === 'M') status.modified.push(contentProcessed);
                if (xy[0] === 'A' || xy[1] === 'A') status.added.push(contentProcessed);
                if (xy[0] === 'D' || xy[1] === 'D') status.deleted.push(contentProcessed);
            } else if (lineCode === '2') {
                // Renamed or copied files (start with '2')
                if (xy[0] === 'R' || xy[1] === 'R') {
                    const parts = contentRaw.split('\t');
                    const to = parts[parts.length - 2].split(' ').pop();
                    const from = parts[parts.length - 1];
                    status.renamed.push({ from, to });
                }
            }
        });
        return status;
    }

    is_repository(repoPath: string): 'git' | null {
        try {
            this.runCommand(`git -C "${repoPath}" rev-parse --is-inside-work-tree`);
            return 'git';
        } catch (e) {
            if (e instanceof NotARepositoryError) return null;
            throw e;
        }
    }
    
    get_root_path(repoPath: string): string {
        return this.runCommand(`git -C "${repoPath}" rev-parse --show-toplevel`);
    }

    get_capabilities() {
        return {
            has_staging_area: true, // Git has a staging area
            supports_rewrite_history: true, // Git supports history rewrite (e.g., rebase)
            distinguishes_change_id: false, // In Git, commit_id and change_id are the same
        };
    }

    get_status(repoPath: string): VcsStatus {
        const output = this.runCommand(`git -C "${repoPath}" status --porcelain=v2`);
        const status = this.parseStatus(output);

        // Check for merge in progress
        if (fs.existsSync(path.join(repoPath, '.git/MERGE_HEAD'))) {
            status.is_operation_in_progress.type = 'merge';
        }
        // Check for rebase in progress
        else if (fs.existsSync(path.join(repoPath, '.git/rebase-merge')) || fs.existsSync(path.join(repoPath, '.git/rebase-apply'))) {
            status.is_operation_in_progress.type = 'rebase';
        }

        return status;
    }
    
    switch_reference({ path: repoPath, reference }: { path: string, reference: string }): void {
        this.runCommand(`git -C "${repoPath}" checkout ${reference}`);
    }

    create_commit({ path: repoPath, message, files }: CommitParams): { commit_id: string, change_id: string } {
        const gitDir = this.runCommand(`git -C "${repoPath}" rev-parse --git-dir`);
        const tempIndexFile = path.join(gitDir, `temp_index_${Date.now()}`);
        const options: ExecSyncOptions = { cwd: repoPath, stdio: 'pipe', encoding: 'utf-8', env: { ...process.env, GIT_INDEX_FILE: tempIndexFile } };

        try {
            // Initialize the temporary index from the current HEAD
            this.runCommand('git read-tree HEAD', options);

            const fileList = files ? files.join(' ') : '.';
            this.runCommand(`git add ${fileList}`, options);
            this.runCommand(`git commit -m "${message}"`, options);
            const commitId = this.runCommand(`git rev-parse HEAD`, options);

            // Update the actual branch HEAD
            const currentBranch = this.runCommand(`git -C "${repoPath}" rev-parse --abbrev-ref HEAD`);
            this.runCommand(`git update-ref refs/heads/${currentBranch} ${commitId}`, { cwd: repoPath });

            // Reset index to match the new HEAD
            this.runCommand(`git reset --mixed ${commitId}`, { cwd: repoPath });

            return { commit_id: commitId, change_id: commitId };
        } finally {
            // Clean up the temporary index file
            if (fs.existsSync(tempIndexFile)) {
                fs.unlinkSync(tempIndexFile);
            }
        }
    }

    // --- Stubs for functions not fully implemented in the last state ---
    is_binary(repoPath: string, filePath: string): boolean {
        const fullPath = path.join(repoPath, filePath);

        // 1. Check gitattributes
        const attrOutput = this.runCommand(`git -C "${repoPath}" check-attr binary -- "${filePath}"`);

        if (attrOutput.endsWith(': set')) {
            return true;
        }
        if (attrOutput.endsWith(': unset')) {
            return false;
        }

        // 2. If unspecified, check content for null bytes
        if (attrOutput.endsWith(': unspecified')) {
            if (!fs.existsSync(fullPath)) {
                return false;
            }
            const stat = fs.statSync(fullPath);
            if (stat.size === 0) {
                return false;
            }
            const buffer = Buffer.alloc(8000);
            const fd = fs.openSync(fullPath, 'r');
            try {
                const bytesRead = fs.readSync(fd, buffer, 0, 8000, 0);
                return buffer.slice(0, bytesRead).includes(0); // Check for null byte (0)
            } finally {
                fs.closeSync(fd);
            }
        }

        // Default fallback
        return false;
    }

    is_ignored(repoPath: string, filePath: string): boolean {
        try {
            this.runCommand(`git -C "${repoPath}" check-ignore --quiet "${filePath}"`);
            return true; // If command succeeds, it's ignored
        } catch (e) {
            // If command fails with exit code 1, it's not ignored
            if (e instanceof GenericVCSError && e.exitCode === 1) return false;
            throw e; // Re-throw other errors
        }
    }

    get_current_reference(repoPath: string): Reference {
        const refName = this.runCommand(`git -C "${repoPath}" rev-parse --abbrev-ref HEAD`);
        const commitId = this.runCommand(`git -C "${repoPath}" rev-parse HEAD`);
        let type: 'branch' | 'tag' | 'detached';
        let name: string | null = null;

        if (refName === 'HEAD') {
            try {
                // Check if the detached HEAD points to a tag
                const tagName = this.runCommand(`git -C "${repoPath}" describe --exact-match --tags HEAD`);
                type = 'tag';
                name = tagName;
            } catch (e) {
                // Not a tag, just a detached HEAD on a commit
                type = 'detached';
                name = null;
            }
        } else {
            type = 'branch';
            name = refName;
        }

        return { name, commit_id: commitId, change_id: commitId, type };
    }

    get_upstream_buffer(repoPath: string): { ahead: number, behind: number } {
        try {
            this.runCommand(`git -C "${repoPath}" rev-parse --abbrev-ref @{u}`);
        } catch (e) {
            // No upstream configured
            if (e instanceof GenericVCSError && e.message.includes('no upstream')) {
                return { ahead: 0, behind: 0 };
            }
            throw e;
        }

        const output = this.runCommand(`git -C "${repoPath}" rev-list --left-right --count @{u}...HEAD`);
        const [behind, ahead] = output.split('\t').map(Number);
        return { ahead, behind };
    }

        get_parent_ids(repoPath: string, commitId: string): string[] {

            const output = this.runCommand(`git log --pretty=%P -n 1 ${commitId}`, { cwd: repoPath });

            // The output will be space-separated parent IDs, or empty string for initial commit

            if (!output) return []; // No parents

            return output.split(' ');

        }

    fetch(repoPath: string): void {
        this.runCommand(`git -C "${repoPath}" fetch`);
    }

    pull(repoPath: string): void {
        this.runCommand(`git -C "${repoPath}" pull`);
    }

    push(repoPath: string): void {
        this.runCommand(`git -C "${repoPath}" push`);
    }

    list_conflicts(repoPath: string): string[] { 
        return this.get_status(repoPath).conflicted;
     }
    resolve_conflict({ path: repoPath, files }: { path: string, files: string[] }): void {
        this.runCommand(`git -C "${repoPath}" add ${files.join(' ')}`);
    }
    abort_operation(repoPath: string): void { 
        const status = this.get_status(repoPath);
        if(status.is_operation_in_progress.type === 'merge') {
            this.runCommand(`git -C "${repoPath}" merge --abort`);
        } else if (status.is_operation_in_progress.type === 'rebase') {
            this.runCommand(`git -C "${repoPath}" rebase --abort`);
        }
    }
}
