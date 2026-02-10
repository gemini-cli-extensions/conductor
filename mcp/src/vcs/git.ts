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
    Reference,
    Vcs,
    VcsType,
    VcsCapabilities
} from './types.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

export class GitVcs implements Vcs {
    private shellEscape(arg: string): string {
        return "'" + arg.replace(/'/g, "'\\''") + "'";
    }

    private runCommand(command: string, options?: ExecSyncOptions): string {
        try {
            return (execSync(command, { stdio: 'pipe', encoding: 'utf-8', ...options }) as string).trim();
        } catch (error: any) {
            // Define stderr once at the beginning of the catch block
            const stderr = error.stderr?.toString().toLowerCase() || '';
            const message = error.message?.toLowerCase() || '';

            // VCSNotFoundError: Check first, as it's a fundamental system-level error
            if (error.code === 'ENOENT' || stderr.includes('command not found') || stderr.includes('enoent')) {
                throw new VCSNotFoundError('Git executable not found');
            }
            // VCSRepositoryLockedError
            if (stderr.includes('index.lock') || stderr.includes('another git process seems to be running') || message.includes('index.lock')) {
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

        const unquote = (str: string): string => {
            if (str.startsWith('"') && str.endsWith('"')) {
                // Git quotes C-style. Simple JSON.parse might work for standard chars, but robust unescaping is needed.
                // For simplicity in this env, assuming mostly standard chars + JSON compatible or simple escapes.
                // We strip quotes and handle basic escapes.
                try {
                    return JSON.parse(str);
                } catch {
                    // Fallback strip quotes
                    return str.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
                }
            }
            return str;
        };

        output.split('\n').forEach(line => {
            const lineCode = line[0];
            const xy = line.substring(2, 4);
            // const rest = line.substring(line.indexOf(' ', 5) + 1);

            // Renamed/Copied have 2 paths
            if (lineCode === '2' && (xy[0] === 'R' || xy[1] === 'R')) {
                 let idx = 0;
                 for(let i=0; i<8; i++) {
                     idx = line.indexOf(' ', idx) + 1;
                 }
                 const content = line.substring(idx);

                 if (xy[0] === 'R' || xy[1] === 'R') {
                     const scoreEnd = content.indexOf(' ');
                     const pathsPart = content.substring(scoreEnd + 1);
                     const [to, from] = pathsPart.split('\t');
                     status.renamed.push({ from: unquote(from), to: unquote(to) });
                 }
                 // Removing redundant else block that contained the conflicting check
            } else if (lineCode === '1') {
                // 1 XY sub mH mI mW hH hI path
                // const fields = line.split(' ');
                let idx = 0;
                for(let i=0; i<8; i++) {
                     idx = line.indexOf(' ', idx) + 1;
                }
                const path = line.substring(idx);
                if (xy[0] === 'M' || xy[1] === 'M') status.modified.push(unquote(path));
                if (xy[0] === 'A' || xy[1] === 'A') status.added.push(unquote(path));
                if (xy[0] === 'D' || xy[1] === 'D') status.deleted.push(unquote(path));
            } else if (lineCode === '?') {
                 // ? path
                 const path = line.substring(2);
                 status.untracked.push(unquote(path));
            } else if (lineCode === 'u') {
                 // u XY sub m1 m2 m3 mW h1 h2 h3 path
                 // const fields = line.split(' ');
                 let idx = 0;
                 for(let i=0; i<10; i++) { // u has more fields?
                     // u <XY> <sub> <m1> <m2> <m3> <mW> <h1> <h2> <h3> <path>
                     idx = line.indexOf(' ', idx) + 1;
                 }
                 const path = line.substring(idx);
                 status.conflicted.push(unquote(path));
            }
        });
        return status;
    }

    // ... (rest of methods)

    get_log(repoPath: string, limit: number, revisionRange?: string, filePath?: string): { commit_id: string, message: string, date: string, author: string }[] {
        const range = revisionRange ? ` ${revisionRange}` : '';
        const file = filePath ? ` -- ${this.shellEscape(filePath)}` : '';
        // Use %x00 as delimiter
        const output = this.runCommand(`git -C "${repoPath}" log --pretty=format:"%H%x00%s%x00%aI%x00%an" -n ${limit}${range}${file}`);
        return output.split('\n').filter(Boolean).map(line => {
            const [commit_id, message, date, author] = line.split('\0');
            return { commit_id, message, date, author };
        });
    }

    search_history(repoPath: string, query: string, limit: number, filePath?: string): { commit_id: string, message: string, date: string, author: string }[] {
        const file = filePath ? ` -- ${this.shellEscape(filePath)}` : '';
        // Use %x00 as delimiter
        const output = this.runCommand(`git -C "${repoPath}" log --grep=${query} --pretty=format:"%H%x00%s%x00%aI%x00%an" -n ${limit}${file}`);
        return output.split('\n').filter(Boolean).map(line => {
             const [commit_id, message, date, author] = line.split('\0');
             return { commit_id, message, date, author };
        });
    }

    is_repository(repoPath: string): VcsType | null {
        try {
            const output = execSync('git rev-parse --is-inside-work-tree', {
                cwd: repoPath,
                stdio: ['ignore', 'pipe', 'ignore'], // Suppress stderr
                encoding: 'utf-8'
            });
            return output.trim() === 'true' ? VcsType.Git : null;
        } catch (error) {
            return null;
        }
    }

    init(repoPath: string): void {
        execSync('git init', { cwd: repoPath, stdio: 'pipe' });
    }

    get_root_path(repoPath: string): string {
        return this.runCommand(`git -C "${repoPath}" rev-parse --show-toplevel`);
    }

    get_capabilities(): VcsCapabilities {
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
            // Check if HEAD is valid (not an empty repo)
            let hasHead = false;
            try {
                this.runCommand(`git rev-parse HEAD`, { ...options, stdio: 'ignore' });
                hasHead = true;
            } catch (e) {
                // HEAD not valid, initial commit
            }

            // Initialize the temporary index from the current HEAD if it exists
            if (hasHead) {
                this.runCommand('git read-tree HEAD', options);
            }

            if (files && files.length > 0) {
                // Use -- to separate paths from revisions to handle files that may be named like revisions
                const escapedFiles = files.map(f => this.shellEscape(f)).join(' ');
                this.runCommand(`git add -- ${escapedFiles}`, options);
            } else if (files === undefined) {
                 // If files is undefined, it implies adding all changes (git add .)
                 this.runCommand(`git add .`, options);
            }

            const allowEmpty = (files && files.length === 0) ? ' --allow-empty' : '';
            this.runCommand(`git commit${allowEmpty} -m "${message}"`, options);
            const commitId = this.runCommand(`git rev-parse HEAD`, options);

            // Update the actual branch HEAD
            let currentBranch = 'master'; // Default fallback
            try {
                 currentBranch = this.runCommand(`git -C "${repoPath}" rev-parse --abbrev-ref HEAD`);
            } catch (e) {
                // Maybe no branch yet? Try symbol ref or just assume master/main if HEAD is unborn
                // If HEAD is unborn, rev-parse --abbrev-ref HEAD returns "HEAD" or fails depending on git version
            }

            // If we are on an unborn branch (initial commit), update-ref might fail if we don't know the branch name.
            // But we can just use the commitId we just created.
            // Wait, we committed to a TEMP index. We need to point the current branch to this new commit.
            // If it's the first commit, we need to create the branch ref.

            // Actually, if it's the first commit, `git commit` in a temp index might create a root commit.
            // Then `update-ref` creates the branch.

            // We need to know the target branch name.
            if (!hasHead) {
                 // Try to get the default branch name (e.g. master or main)
                 // git symbolic-ref HEAD returns "refs/heads/master" usually
                 try {
                     const headRef = this.runCommand(`git symbolic-ref HEAD`, options); // e.g., refs/heads/master
                     this.runCommand(`git update-ref ${headRef} ${commitId}`, { cwd: repoPath });
                 } catch (e) {
                     // Fallback
                     this.runCommand(`git update-ref refs/heads/master ${commitId}`, { cwd: repoPath });
                 }
            } else {
                 this.runCommand(`git update-ref refs/heads/${currentBranch} ${commitId}`, { cwd: repoPath });
            }

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

    is_binary(repoPath: string, filePath: string): boolean {
        const fullPath = path.join(repoPath, filePath);

        // 1. Check gitattributes
        const attrOutput = this.runCommand(`git -C "${repoPath}" check-attr binary -- ${this.shellEscape(filePath)}`);

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
            this.runCommand(`git -C "${repoPath}" check-ignore --quiet ${this.shellEscape(filePath)}`);
            return true; // If command succeeds, it's ignored
        } catch (e: any) {
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
        } catch (e: any) {
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

    get_config(repoPath: string, key: string): string | null {
        try {
            return this.runCommand(`git -C "${repoPath}" config ${key}`);
        } catch (e) {
            return null;
        }
    }

    get_user_identity(repoPath: string): { name: string, email: string } | null {
        try {
            const name = this.get_config(repoPath, 'user.name');
            const email = this.get_config(repoPath, 'user.email');
            if (name && email) return { name, email };
            return null;
        } catch (e) {
            return null;
        }
    }

    get_ignored_files(repoPath: string): string[] {
        try {
            const output = this.runCommand(`git -C "${repoPath}" status --ignored --porcelain=v2`);
            const ignored: string[] = [];
            output.split('\n').forEach(line => {
                if (line.startsWith('! ')) {
                    ignored.push(line.substring(2));
                }
            });
            return ignored;
        } catch (e) {
            return [];
        }
    }

    get_file_content(repoPath: string, revision: string, filePath: string): string {
        return this.runCommand(`git -C "${repoPath}" show ${revision}:${this.shellEscape(filePath)}`);
    }

    get_diff(repoPath: string, revisionRange: string | undefined, filePath?: string): string | null {
        if (filePath && this.is_binary(repoPath, filePath)) return null;
        const range = revisionRange || '';
        const file = filePath ? ` -- ${this.shellEscape(filePath)}` : '';
        try {
            return this.runCommand(`git -C "${repoPath}" diff ${range}${file}`);
        } catch (e: any) {
            return null;
        }
    }

    get_binary_diff_info(repoPath: string, filePath: string, revisionRange?: string): { is_binary: boolean, old_size: number, new_size: number } | null {
        if (!this.is_binary(repoPath, filePath)) return null;

        let oldRev = 'HEAD';
        let newRev: string | null = null;

        if (revisionRange) {
            if (revisionRange.includes('..')) {
                const parts = revisionRange.split('..');
                oldRev = parts[0];
                newRev = parts[1];
            } else {
                oldRev = revisionRange;
            }
        }

        try {
            const escapedPath = this.shellEscape(filePath);
            const oldSize = parseInt(this.runCommand(`git -C "${repoPath}" cat-file -s ${oldRev}:${escapedPath}`));
            let newSize = 0;
            if (newRev && newRev !== 'HEAD') { // If newRev is explicit and not working copy (simplified assumption: only HEAD or range)
                 // If range is HEAD~1..HEAD, newRev is HEAD.
                 // If newRev is HEAD, use cat-file.
                 // If newRev is not provided (null), use stat.
                 newSize = parseInt(this.runCommand(`git -C "${repoPath}" cat-file -s ${newRev}:${escapedPath}`));
            } else if (newRev === 'HEAD') {
                 newSize = parseInt(this.runCommand(`git -C "${repoPath}" cat-file -s HEAD:${escapedPath}`));
            } else {
                 const stat = fs.statSync(path.join(repoPath, filePath));
                 newSize = stat.size;
            }
            return { is_binary: true, old_size: oldSize, new_size: newSize };
        } catch (e) {
            return null;
        }
    }

    get_changed_files(repoPath: string, revisionRange: string): string[] {
        const output = this.runCommand(`git -C "${repoPath}" diff --name-only ${revisionRange}`);
        return output.split('\n').filter(Boolean);
    }

    get_merge_base(repoPath: string, revisionA: string, revisionB: string): string | null {
        try {
            return this.runCommand(`git -C "${repoPath}" merge-base ${revisionA} ${revisionB}`);
        } catch (e) {
            return null;
        }
    }

    revert_commit(repoPath: string, commitId: string, waitForLock?: boolean): string {
        this.runCommand(`git -C "${repoPath}" revert --no-edit ${commitId}`);
        return this.runCommand(`git -C "${repoPath}" rev-parse HEAD`);
    }
}
