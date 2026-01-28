import { execSync, ExecSyncOptions } from 'child_process';
import { VcsStatus, CommitParams, Reference, NotARepositoryError, GenericVCSError, Vcs, VcsType, VcsCapabilities } from './types';
import * as fs from 'fs';
import * as path from 'path';

export class JjVcs implements Vcs {
    private runCommand(command: string, options?: ExecSyncOptions): string {
        try {
            // Ensure EDITOR is set to something non-interactive for commands that might open an editor.
            const env = { ...process.env, EDITOR: 'true' };
            return execSync(`jj ${command}`, { stdio: 'pipe', encoding: 'utf-8', ...options, env }).trim();
        } catch (error: any) {
            const stderr = error.stderr?.toString().toLowerCase() || '';
            if (stderr.includes('there is no jj repo in')) {
                throw new NotARepositoryError('Not a jj repository');
            }
            throw new GenericVCSError(error.message, command, error.exitCode ?? error.status);
        }
    }

    private parseStatus(output: string): VcsStatus {
        const status: VcsStatus = { 
            modified:[], 
            untracked:[], 
            added:[], 
            deleted:[], 
            conflicted:[], 
            renamed:[], 
            is_operation_in_progress:{type:'none'} 
        };
        if (!output) return status;

        const lines = output.split('\n');
        for (const line of lines) {
            if (line.length > 2 && line[1] === ' ') {
                const statusChar = line[0];
                const filePath = line.substring(2);
                switch (statusChar) {
                    case 'A':
                        status.added.push(filePath);
                        break;
                    case 'M':
                        status.modified.push(filePath);
                        break;
                    case 'D':
                        status.deleted.push(filePath);
                        break;
                }
            }
        }
        return status;
    }

    is_repository(repoPath: string): VcsType | null {
        try {
            this.runCommand(`status`, { cwd: repoPath });
            return VcsType.Jj;
        } catch (e) {
            if (e instanceof NotARepositoryError) return null;
            throw e;
        }
    }
    
    get_root_path(repoPath: string): string {
        return this.runCommand(`root`, { cwd: repoPath });
    }

    get_capabilities(): VcsCapabilities {
        return {
            has_staging_area: false,
            supports_rewrite_history: true,
            distinguishes_change_id: true,
        };
    }

    get_status(repoPath: string): VcsStatus {
        const statusOutput = this.runCommand(`status`, { cwd: repoPath });
        const status = this.parseStatus(statusOutput);

        // Populate conflicts
        status.conflicted = this.list_conflicts(repoPath);
        // Remove conflicted files from modified to avoid duplication
        status.modified = status.modified.filter(f => !status.conflicted.includes(f));
        status.added = status.added.filter(f => !status.conflicted.includes(f));
        status.deleted = status.deleted.filter(f => !status.conflicted.includes(f));

        const trackedFilesOutput = this.runCommand(`file list`, { cwd: repoPath });
        const trackedFiles = trackedFilesOutput.split('\n').filter(Boolean);
        
        const allFilesInWorkingDir = this.getAllFilesInDir(repoPath);

        status.untracked = allFilesInWorkingDir.filter(file => {
            // A file is untracked if it's not tracked by jj and not ignored.
            if (trackedFiles.includes(file)) return false;
            
            // Also check if it's reported as added/modified/deleted/conflicted in status, just in case
            const isReportedByStatus = status.modified.includes(file) || 
                                       status.added.includes(file) || 
                                       status.deleted.includes(file) ||
                                       status.conflicted.includes(file);
            if (isReportedByStatus) return false;

            const isIgnored = this.is_ignored(repoPath, file);
            return !isIgnored;
        });

        return status;
    }

    private getAllFilesInDir(dirPath: string, relativePath = ''): string[] {
        let files: string[] = [];
        const entries = fs.readdirSync(path.join(dirPath, relativePath), { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(relativePath, entry.name);
            if (entry.isDirectory()) {
                // Exclude the .jj and .git directories themselves from recursive scanning
                if (fullPath === '.jj' || fullPath === '.git') continue;
                files = files.concat(this.getAllFilesInDir(dirPath, fullPath));
            } else {
                files.push(fullPath);
            }
        }
        return files;
    }

    switch_reference({ path: repoPath, reference }: { path: string, reference: string }): void {
        this.runCommand(`new "${reference}"`, { cwd: repoPath });
    }

    create_commit({ path: repoPath, message, files }: CommitParams): { commit_id: string, change_id: string } {
        // Force snapshot
        this.runCommand('status', { cwd: repoPath });

        // 1. Set the message for the current working-copy commit.
        this.runCommand(`describe -m "${message}"`, { cwd: repoPath });

        // 2. Get the IDs of the commit we just described.
        const logOutput = this.runCommand(`log -r '@' -T 'commit_id ++ " " ++ change_id'`, { cwd: repoPath });
        const [commit_id, change_id] = logOutput.split(' ');

        // 3. Create a new, empty working-copy commit for the user to work on next.
        this.runCommand(`new`, { cwd: repoPath });
        
        return { commit_id, change_id };
    }

    is_binary(repoPath: string, filePath: string): boolean {
        try {
            const output = execSync(`git -C "${repoPath}" check-attr binary -- "${filePath}"`, { stdio: 'pipe', encoding: 'utf-8' }).trim();
            return output.endsWith(': set');
        } catch (e: any) {
            if (e.status === 1) return false;
            throw e;
        }
    }

    is_ignored(repoPath: string, filePath: string): boolean {
        try {
            execSync(`git -C "${repoPath}" check-ignore --quiet "${filePath}"`, { stdio: 'pipe', encoding: 'utf-8' });
            return true; // If command succeeds, it's ignored
        } catch (e: any) {
            // If command fails with exit code 1, it's not ignored
            if (e.status === 1) return false;
            throw e; // Re-throw other errors
        }
    }

    get_current_reference(repoPath: string): Reference {
        const separator = '|||';
        // We use a safe separator to parse the output reliably.
        // We capture commit_id, change_id, bookmarks, and tags.
        const template = `commit_id ++ "${separator}" ++ change_id ++ "${separator}" ++ bookmarks ++ "${separator}" ++ tags`;
        const output = this.runCommand(`log -r @ --no-graph -T '${template}'`, { cwd: repoPath });
        const parts = output.split(separator);
        
        const commit_id = parts[0] ? parts[0].trim() : '';
        const change_id = parts[1] ? parts[1].trim() : '';
        const bookmarksStr = parts[2] ? parts[2].trim() : '';
        const tagsStr = parts[3] ? parts[3].trim() : '';

        let type: 'branch' | 'tag' | 'detached' = 'detached';
        let name: string | null = null;

        // Check for bookmarks (branches)
        if (bookmarksStr) {
            // Take the first bookmark as the current branch name
            const bookmarks = bookmarksStr.split(/\s+/);
            if (bookmarks.length > 0) {
                // Sanitize bookmark name (remove trailing *, ?, @ which might indicate status)
                name = bookmarks[0].replace(/[?*@]+$/, '');
                type = 'branch';
            }
        }

        // Check for tags if not on a branch
        if (!name && tagsStr) {
            const tags = tagsStr.split(/\s+/);
            if (tags.length > 0) {
                name = tags[0];
                type = 'tag';
            }
        }

        if (!name && commit_id === '0000000000000000000000000000000000000000') {
             type = 'detached';
             name = null;
        }

        return {
            name,
            commit_id,
            change_id,
            type,
        }
    }

    get_upstream_buffer(repoPath: string) {
        let branchName = this.get_current_reference(repoPath).name;

        if (!branchName) {
             // Try parent if current is detached (common in jj new workflow)
             // We look for a bookmark on the parent commit.
             const parentBookmarks = this.runCommand('log -r @- --no-graph -T "bookmarks"', {cwd: repoPath});
             if (parentBookmarks && parentBookmarks.trim()) {
                 // bookmarks can be space separated, take the first one
                 branchName = parentBookmarks.trim().split(' ')[0]; 
             }
        }

        if (!branchName) {
            return { ahead: 0, behind: 0 };
        }
        
        // Use bookmark list instead of branch list
        const output = this.runCommand('bookmark list', { cwd: repoPath });
        const lines = output.split('\n');
        
        let foundBranch = false;
        for (const line of lines) {
            // Match branchName followed by colon or space/conflicted marker
            if (line.startsWith(branchName)) {
                foundBranch = true;
                // Check if this line itself has info (sometimes it does?)
                const aheadMatch = line.match(/ahead by (\d+)/);
                const behindMatch = line.match(/behind by (\d+)/);
                if (aheadMatch || behindMatch) {
                     const ahead = aheadMatch ? parseInt(aheadMatch[1], 10) : 0;
                     const behind = behindMatch ? parseInt(behindMatch[1], 10) : 0;
                     return { ahead, behind };
                }
                continue;
            }
            
            if (foundBranch) {
                // If we found the branch, check indented lines for remote info
                if (line.startsWith(' ') || line.startsWith('\t')) {
                     const aheadMatch = line.match(/ahead by (\d+)/);
                     const behindMatch = line.match(/behind by (\d+)/);
                     if (aheadMatch || behindMatch) {
                         const ahead = aheadMatch ? parseInt(aheadMatch[1], 10) : 0;
                         const behind = behindMatch ? parseInt(behindMatch[1], 10) : 0;
                         return { ahead, behind };
                     }
                } else {
                    // Start of another bookmark, stop searching
                    break;
                }
            }
        }
        
        return { ahead: 0, behind: 0 };
    }

    get_parent_ids(repoPath: string, commitId: string): string[] {
        if (commitId === '0000000000000000000000000000000000000000') {
            return [];
        }
        const output = this.runCommand(`log -r '${commitId}' --no-graph -T 'parents.map(|c| c.commit_id() ++ "\n")'`, { cwd: repoPath });
        if (!output) {
            return [];
        }
        return output.split('\n').filter(Boolean);
    }

    fetch(repoPath: string): void {
        this.runCommand(`git fetch`, { cwd: repoPath });
    }

    pull(repoPath: string): void {
        this.runCommand(`git fetch`, { cwd: repoPath });
        this.runCommand(`rebase -d main@origin`, { cwd: repoPath });
    }

    push(repoPath: string): void {
        this.runCommand(`git push`, { cwd: repoPath });
    }

    list_conflicts(repoPath: string): string[] { 
        try {
            const output = this.runCommand('resolve --list', { cwd: repoPath });
            if (!output) {
                return [];
            }
            return output.split('\n').filter(Boolean).map(line => line.split(/\s+/)[0]);
        } catch (error: any) {
            const exitCode = error.exitCode ?? error.status;
            if (exitCode === 2 || exitCode === 1) return [];
            throw error;
        }
    }

    resolve_conflict({ path: repoPath, files }: { path: string, files: string[] }): void {
        if (files.length > 0) {
            try {
                this.runCommand(`resolve ${files.map(f => `"${f}"`).join(' ')}`, { cwd: repoPath });
            } catch (error: any) {
                // Ignore errors if conflicts are not found (already resolved)
                // jj resolve exits with non-zero if no conflicts found at path.
            }
        }
    }

    abort_operation(repoPath: string): void { 
        this.runCommand('undo', { cwd: repoPath });
    }
}
