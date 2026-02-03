import { execSync, ExecSyncOptions } from 'child_process';
import { VcsStatus, CommitParams, Reference, NotARepositoryError, GenericVCSError, Vcs, VcsType, VcsCapabilities } from './types';
import * as fs from 'fs';
import * as path from 'path';

export class JjVcs implements Vcs {
    private shellEscape(arg: string): string {
        return "'" + arg.replace(/'/g, "'\\''") + "'";
    }

    private runCommand(command: string, options?: ExecSyncOptions): string {
        try {
            return execSync(`jj --color=never ${command}`, { stdio: 'pipe', encoding: 'utf-8', ...options }).trim();
        } catch (error: any) {
            if (error.stderr) {
                const stderr = error.stderr.toString();
                if (stderr.includes('no repo found') || stderr.includes('not a jj repository') || stderr.includes('no jj repo')) {
                     throw new NotARepositoryError('Not a jj repository');
                }
            }
            throw new GenericVCSError(error.message, command, error.exitCode ?? error.status);
        }
    }

    private getSize(repoPath: string, revision: string, filePath: string): number {
        try {
            if (revision === '@') {
                 const fullPath = path.join(repoPath, filePath);
                 if (fs.existsSync(fullPath)) {
                     return fs.statSync(fullPath).size;
                 }
                 return 0;
            }

            const commitId = this.runCommand(`log -r "${revision}" --no-graph -T commit_id`, { cwd: repoPath });
            if (!commitId) return 0;
            
            // Use git cat-file -s which is reliable for size
            const output = execSync(`git -C "${repoPath}" cat-file -s ${commitId}:${this.shellEscape(filePath)}`, { stdio: 'pipe', encoding: 'utf-8' }).trim();
            return parseInt(output, 10);
        } catch (e) {
            return 0;
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

        const unquote = (str: string): string => {
            if (str.startsWith('"') && str.endsWith('"')) {
                try {
                    return JSON.parse(str);
                } catch {
                    return str.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
                }
            }
            return str;
        };

        const lines = output.split('\n');
        for (const line of lines) {
            if (line.length > 2 && line[1] === ' ') {
                const statusChar = line[0];
                const filePath = unquote(line.substring(2));
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

        status.conflicted = this.list_conflicts(repoPath);
        
        try {
            const diffOutput = this.runCommand('diff --git -r @-', { cwd: repoPath });
            const lines = diffOutput.split('\n');
            let currentFrom: string | null = null;
            let currentTo: string | null = null;
            
            for (const line of lines) {
                if (line.startsWith('diff --git')) {
                    if (currentFrom && currentTo) {
                        status.renamed.push({ from: currentFrom, to: currentTo });
                    }
                    currentFrom = null;
                    currentTo = null;
                } else if (line.startsWith('rename from ')) {
                    currentFrom = line.substring('rename from '.length).trim();
                } else if (line.startsWith('rename to ')) {
                    currentTo = line.substring('rename to '.length).trim();
                }
            }
            if (currentFrom && currentTo) {
                status.renamed.push({ from: currentFrom, to: currentTo });
            }
        } catch (e) {
        }

        status.renamed.forEach(({ from, to }) => {
            status.deleted = status.deleted.filter(f => f !== from);
            status.added = status.added.filter(f => f !== to);
            status.modified = status.modified.filter(f => f !== from && f !== to);
        });

        status.modified = status.modified.filter(f => !status.conflicted.includes(f));
        status.added = status.added.filter(f => !status.conflicted.includes(f));
        status.deleted = status.deleted.filter(f => !status.conflicted.includes(f));

        const trackedFilesOutput = this.runCommand(`file list`, { cwd: repoPath });
        const trackedFiles = trackedFilesOutput.split('\n').filter(Boolean);
        
        const allFilesInWorkingDir = this.getAllFilesInDir(repoPath);

        status.untracked = allFilesInWorkingDir.filter(file => {
            if (trackedFiles.includes(file)) return false;
            
            const isReportedByStatus = status.modified.includes(file) || 
                                       status.added.includes(file) || 
                                       status.deleted.includes(file) ||
                                       status.conflicted.includes(file) ||
                                       status.renamed.some(r => r.to === file);
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
                if (fullPath === '.jj' || fullPath === '.git') continue;
                files = files.concat(this.getAllFilesInDir(dirPath, fullPath));
            } else {
                files.push(fullPath);
            }
        }
        return files;
    }

    switch_reference({ path: repoPath, reference }: { path: string, reference: string }): void {
        this.runCommand(`new ${this.shellEscape(reference)}`, { cwd: repoPath });
    }

    create_commit({ path: repoPath, message, files }: CommitParams): { commit_id: string, change_id: string } {
        this.runCommand('status', { cwd: repoPath });
        this.runCommand(`describe -m ${this.shellEscape(message)}`, { cwd: repoPath });
        const logOutput = this.runCommand(`log -r '@' -T 'commit_id ++ " " ++ change_id'`, { cwd: repoPath });
        const [commit_id, change_id] = logOutput.split(' ');
        this.runCommand(`new`, { cwd: repoPath });
        return { commit_id, change_id };
    }

    is_binary(repoPath: string, filePath: string): boolean {
        try {
            const output = execSync(`git -C "${repoPath}" check-attr binary -- ${this.shellEscape(filePath)}`, { stdio: 'pipe', encoding: 'utf-8' }).trim();
            return output.endsWith(': set');
        } catch (e: any) {
            if (e.status === 1) return false;
            throw e;
        }
    }

    is_ignored(repoPath: string, filePath: string): boolean {
        try {
            execSync(`git -C "${repoPath}" check-ignore --quiet ${this.shellEscape(filePath)}`, { stdio: 'pipe', encoding: 'utf-8' });
            return true;
        } catch (e: any) {
            if (e.status === 1) return false;
            throw e;
        }
    }

    get_current_reference(repoPath: string): Reference {
        const separator = '|||';
        const template = `commit_id ++ "${separator}" ++ change_id ++ "${separator}" ++ bookmarks ++ "${separator}" ++ tags`;
        const output = this.runCommand(`log -r @ --no-graph -T '${template}'`, { cwd: repoPath });
        const parts = output.split(separator);
        
        const commit_id = parts[0] ? parts[0].trim() : '';
        const change_id = parts[1] ? parts[1].trim() : '';
        const bookmarksStr = parts[2] ? parts[2].trim() : '';
        const tagsStr = parts[3] ? parts[3].trim() : '';

        let type: 'branch' | 'tag' | 'detached' = 'detached';
        let name: string | null = null;

        if (bookmarksStr) {
            const bookmarks = bookmarksStr.split(/\s+/);
            if (bookmarks.length > 0) {
                name = bookmarks[0].replace(/[?*@]+$/, '');
                type = 'branch';
            }
        }

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

        return { name, commit_id, change_id, type }
    }

    get_upstream_buffer(repoPath: string) {
        let branchName = this.get_current_reference(repoPath).name;

        if (!branchName) {
             const parentBookmarks = this.runCommand('log -r @- --no-graph -T "bookmarks"', {cwd: repoPath});
             if (parentBookmarks && parentBookmarks.trim()) {
                 branchName = parentBookmarks.trim().split(' ')[0]; 
             }
        }

        if (!branchName) {
            return { ahead: 0, behind: 0 };
        }
        
        const output = this.runCommand('bookmark list', { cwd: repoPath });
        const lines = output.split('\n');
        
        let foundBranch = false;
        for (const line of lines) {
            if (line.startsWith(branchName)) {
                foundBranch = true;
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
                if (line.startsWith(' ') || line.startsWith('\t')) {
                     const aheadMatch = line.match(/ahead by (\d+)/);
                     const behindMatch = line.match(/behind by (\d+)/);
                     if (aheadMatch || behindMatch) {
                         const ahead = aheadMatch ? parseInt(aheadMatch[1], 10) : 0;
                         const behind = behindMatch ? parseInt(behindMatch[1], 10) : 0;
                         return { ahead, behind };
                     }
                } else {
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
            // JJ returns non-zero exit code if no conflicts found? Or just prints to stderr?
            if (error.message?.includes('No conflicts found') || error.message?.includes('no conflicts found')) {
                return [];
            }
            const exitCode = error.exitCode ?? error.status;
            if (exitCode === 2 || exitCode === 1) return [];
            throw error;
        }
    }

    resolve_conflict({ path: repoPath, files }: { path: string, files: string[] }): void {
        if (files.length > 0) {
            try {
                this.runCommand(`resolve ${files.map(f => this.shellEscape(f)).join(' ')}`, { cwd: repoPath });
            } catch (error: any) {
            }
        }
    }

    abort_operation(repoPath: string): void { 
        this.runCommand('undo', { cwd: repoPath });
    }

    get_config(repoPath: string, key: string): string | null {
        try {
            return this.runCommand(`config get ${key}`, { cwd: repoPath });
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
            const output = execSync(`git -C "${repoPath}" status --ignored --porcelain`, { stdio: 'pipe', encoding: 'utf-8' });
            return output.split('\n')
                .filter(line => line.startsWith('!! '))
                .map(line => line.substring(3));
        } catch (e) {
            return [];
        }
    }

    get_file_content(repoPath: string, revision: string, filePath: string): string {
        const rev = revision === 'HEAD' ? '@' : revision;
        return this.runCommand(`file show -r ${rev} ${this.shellEscape(filePath)}`, { cwd: repoPath });
    }

    get_diff(repoPath: string, revisionRange: string | undefined, filePath?: string): string | null {
        if (filePath && this.is_binary(repoPath, filePath)) return null;
        const rangeArg = revisionRange ? `-r "${revisionRange}"` : ''; 
        const fileArg = filePath ? ` ${this.shellEscape(filePath)}` : '';
        try {
            return this.runCommand(`diff ${rangeArg}${fileArg}`, { cwd: repoPath });
        } catch (e) {
            return null;
        }
    }

    get_binary_diff_info(repoPath: string, filePath: string, revisionRange?: string): { is_binary: boolean, old_size: number, new_size: number } | null {
         if (!this.is_binary(repoPath, filePath)) return null;
         let oldRev = '@-';
         let newRev = '@';

         if (revisionRange) {
             if (revisionRange.includes('..')) {
                 const parts = revisionRange.split('..');
                 oldRev = parts[0] || '@-';
                 newRev = parts[1] || '@';
             } else {
                 oldRev = revisionRange; 
                 newRev = '@';
             }
         }
         
         if (oldRev === 'HEAD') oldRev = '@';
         if (newRev === 'HEAD') newRev = '@';
         
         try {
             const oldSize = this.getSize(repoPath, oldRev, filePath);
             const newSize = this.getSize(repoPath, newRev, filePath);
             return { is_binary: true, old_size: oldSize, new_size: newSize };
         } catch (e) {
             return null;
         }
    }

    get_changed_files(repoPath: string, revisionRange: string): string[] {
        const range = revisionRange.replace(/HEAD/g, '@');
        const output = this.runCommand(`diff --name-only -r ${range}`, { cwd: repoPath });
        return output.split('\n').filter(Boolean);
    }

    get_merge_base(repoPath: string, revisionA: string, revisionB: string): string | null {
        try {
            const output = this.runCommand(`log --no-graph -T "commit_id" -r "heads(::${revisionA} & ::${revisionB})"`, { cwd: repoPath });
            return output.split('\n')[0]?.trim() || null;
        } catch (e) {
            return null;
        }
    }

    revert_commit(repoPath: string, commitId: string, waitForLock?: boolean): string {
        throw new Error('Not implemented: jj backout not supported in this version');
    }

    get_log(repoPath: string, limit: number, revisionRange?: string): { commit_id: string, message: string, date: string, author: string }[] {
        // Default to ancestors of working copy parent (effectively committed history)
        const range = revisionRange ? ` -r "${revisionRange}"` : ' -r "::@-"';
        const delimiter = '\\0'; 
        const jsDelimiter = '\0';
        
        // Use author.email() as it appears to be a method in this JJ version. 
        // Using timestamp directly usually formats to string, but if issues arise, we might need .format().
        const template = `commit_id ++ "${delimiter}" ++ description.first_line() ++ "${delimiter}" ++ author.timestamp() ++ "${delimiter}" ++ author.email() ++ "\\n"`;
        const output = this.runCommand(`log -n ${limit}${range} -T '${template}' --no-graph`, { cwd: repoPath });
        return output.split('\n').filter(Boolean).map(line => {
            const [commit_id, message, date, author] = line.split(jsDelimiter);
            return { commit_id, message, date, author };
        });
    }

    search_history(repoPath: string, query: string, limit: number): { commit_id: string, message: string, date: string, author: string }[] {
        const delimiter = '\\0';
        const jsDelimiter = '\0';
        const template = `commit_id ++ "${delimiter}" ++ description.first_line() ++ "${delimiter}" ++ author.timestamp() ++ "${delimiter}" ++ author.email() ++ "\\n"`;
        // Search within committed history
        const output = this.runCommand(`log -r "description(~'${query}') & ::@-" -n ${limit} -T '${template}' --no-graph`, { cwd: repoPath });
        return output.split('\n').filter(Boolean).map(line => {
             const [commit_id, message, date, author] = line.split(jsDelimiter);
             return { commit_id, message, date, author };
        });
    }}
