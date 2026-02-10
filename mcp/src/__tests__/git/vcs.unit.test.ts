import { describe, it, expect, vi, beforeEach } from 'vitest';
import { GitVcs } from '../../vcs/git';
import { NotARepositoryError, DirtyWorkingDirectoryError, GenericVCSError, VCSRepositoryLockedError, AuthenticationError, MergeConflictError, VCSNotFoundError, VcsStatus } from '../../vcs/types';
import { execSync } from 'child_process';
import * as fs from 'fs';

vi.mock('child_process', () => ({
    execSync: vi.fn(),
}));

vi.mock('fs');

describe('VCS Abstraction Layer - Unit Tests', () => {
    let vcs: GitVcs;
    let mockExecSync: vi.Mock;

    beforeEach(() => {
        vcs = new GitVcs();
        vi.resetAllMocks();
        mockExecSync = execSync as vi.Mock;
        mockExecSync.mockImplementation((command: string, options?: any) => {
            if (command.includes('rev-parse --is-inside-work-tree')) return 'true';
            return '';
        });
    });

    describe('is_repository()', () => {
        it("should return 'git' for a valid git repository", () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --is-inside-work-tree')) return 'true';
                throw { stderr: 'fatal: not a git repository', status: 128 };
            });
            expect(vcs.is_repository('/path/to/repo')).toBe('git');
        });

        it('should return null if not a repository', () => {
            mockExecSync.mockImplementation((command: string) => {
                throw { stderr: 'fatal: not a git repository (or any of the parent directories)', status: 128 };
            });
            expect(vcs.is_repository('/path/to/non-repo')).toBeNull();
        });
    });

    describe('get_root_path()', () => {
        it('should return the root path for a valid git repository', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --show-toplevel')) return '/path/to/repo';
                throw { stderr: 'fatal: not a git repository (or any of the parent directories)', status: 128 };
            });
            expect(vcs.get_root_path('/path/to/repo/subdir')).toBe('/path/to/repo');
        });

        it('should throw NotARepositoryError if not a repository', () => {
            mockExecSync.mockImplementation(() => {
                throw { stderr: 'fatal: not a git repository (or any of the parent directories)', status: 128 };
            });
            expect(() => vcs.get_root_path('/path/to/non-repo')).toThrow(NotARepositoryError);
        });
    });

    describe('get_capabilities()', () => {
        it('should return the correct capabilities for Git', () => {
            const capabilities = vcs.get_capabilities();
            expect(capabilities).toEqual({
                has_staging_area: true,
                supports_rewrite_history: true,
                distinguishes_change_id: false,
            });
        });
    });

    describe('is_binary()', () => {
        it('should return true if file is binary', () => {
            mockExecSync.mockReturnValue('path/to/file.png: binary: set');
            expect(vcs.is_binary('/path/to/repo', 'path/to/file.png')).toBe(true);
        });
        it('should return false if file is not binary', () => {
            mockExecSync.mockReturnValue('path/to/file.txt: binary: unspecified');
            expect(vcs.is_binary('/path/to/repo', 'path/to/file.txt')).toBe(false);
        });
    });

    describe('is_ignored()', () => {
        it('should return true if a file is ignored', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('check-ignore')) return '/path/to/repo/ignored-file.txt';
                return '';
            });
            expect(vcs.is_ignored('/path/to/repo', 'ignored-file.txt')).toBe(true);
        });

        it('should return false if a file is not ignored', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('check-ignore')) throw { status: 1 };
                return '';
            });
            expect(vcs.is_ignored('/path/to/repo', 'non-ignored-file.txt')).toBe(false);
        });
    });

    describe('get_current_reference()', () => {
        it('should return the current branch name when on a branch', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --abbrev-ref HEAD')) return 'main';
                if (command.includes('rev-parse HEAD')) return 'branch_commit_id';
                return '';
            });
            expect(vcs.get_current_reference('/path/to/repo')).toEqual({
                name: 'main',
                commit_id: 'branch_commit_id',
                change_id: 'branch_commit_id',
                type: 'branch',
            });
        });

        it('should return the commit hash when in detached HEAD state', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --abbrev-ref HEAD')) return 'HEAD';
                if (command.includes('rev-parse HEAD')) return 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0';
                if (command.includes('describe --exact-match --tags HEAD')) throw new Error('not a tag');
                return '';
            });
            expect(vcs.get_current_reference('/path/to/repo')).toEqual({
                name: null,
                commit_id: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
                change_id: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
                type: 'detached',
            });
        });

        it('should return the tag name when on a tag', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --abbrev-ref HEAD')) return 'HEAD';
                if (command.includes('rev-parse HEAD')) return 'tag_commit_id';
                if (command.includes('describe --exact-match --tags HEAD')) return 'v1.0.0';
                return '';
            });
            expect(vcs.get_current_reference('/path/to/repo')).toEqual({
                name: 'v1.0.0',
                commit_id: 'tag_commit_id',
                change_id: 'tag_commit_id',
                type: 'tag',
            });
        });
    });

    describe('get_upstream_buffer()', () => {
        it('should return correct ahead/behind counts when upstream is present', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-list --left-right --count @{u}...HEAD')) return '1\t2'; // 1 ahead, 2 behind
                if (command.includes('rev-parse --abbrev-ref @{u}')) return 'origin/main';
                return '';
            });
            const buffer = vcs.get_upstream_buffer('/path/to/repo');
            expect(buffer).toEqual({ ahead: 2, behind: 1 });
        });

        it('should return 0 ahead/behind when no upstream is configured', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --abbrev-ref @{u}')) throw new Error('no upstream');
                return '';
            });
            const buffer = vcs.get_upstream_buffer('/path/to/repo');
            expect(buffer).toEqual({ ahead: 0, behind: 0 });
        });
    });

    describe('get_parent_ids()', () => {
        it('should return a single parent ID for a normal commit', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('git log --pretty=%P -n 1 HEAD')) return 'parent1_id';
                return '';
            });
            expect(vcs.get_parent_ids('/path/to/repo', 'HEAD')).toEqual(['parent1_id']);
        });

        it('should return multiple parent IDs for a merge commit', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('git log --pretty=%P -n 1 MERGE_COMMIT_ID')) return 'parent1_id parent2_id';
                return '';
            });
            expect(vcs.get_parent_ids('/path/to/repo', 'MERGE_COMMIT_ID')).toEqual(['parent1_id', 'parent2_id']);
        });

        it('should return an empty array for the initial commit', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --parents INITIAL_COMMIT_ID')) return 'INITIAL_COMMIT_ID';
                return '';
            });
            expect(vcs.get_parent_ids('/path/to/repo', 'INITIAL_COMMIT_ID')).toEqual([]);
        });
    });

    describe('Remote Operations', () => {
        describe('fetch()', () => {
            it('should execute git fetch successfully', () => {
                vcs.fetch('/path/to/repo');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('fetch'), expect.any(Object));
            });

            it('should throw AuthenticationError on authentication failure', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'authentication failed', status: 1 };
                });
                expect(() => vcs.fetch('/path/to/repo')).toThrow(AuthenticationError);
            });

            it('should throw GenericVCSError for other fetch errors', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'some other fetch error', status: 1 };
                });
                expect(() => vcs.fetch('/path/to/repo')).toThrow(GenericVCSError);
            });
        });

        describe('pull()', () => {
            it('should execute git pull successfully', () => {
                vcs.pull('/path/to/repo');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('pull'), expect.any(Object));
            });

            it('should throw AuthenticationError on authentication failure', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'authentication failed', status: 1 };
                });
                expect(() => vcs.pull('/path/to/repo')).toThrow(AuthenticationError);
            });

            it('should throw GenericVCSError for other pull errors', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'some other pull error', status: 1 };
                });
                expect(() => vcs.pull('/path/to/repo')).toThrow(GenericVCSError);
            });

            it('should throw MergeConflictError on merge conflict', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'conflict: Merge conflict in file.txt', status: 1 };
                });
                vi.spyOn(vcs, 'list_conflicts').mockReturnValue(['file.txt']);
                expect(() => vcs.pull('/path/to/repo')).toThrow(MergeConflictError);
            });
        });

        describe('push()', () => {
            it('should execute git push successfully', () => {
                vcs.push('/path/to/repo');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('push'), expect.any(Object));
            });

            it('should throw AuthenticationError on authentication failure', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'authentication failed', status: 1 };
                });
                expect(() => vcs.push('/path/to/repo')).toThrow(AuthenticationError);
            });

            it('should throw GenericVCSError for other push errors', () => {
                mockExecSync.mockImplementation(() => {
                    throw { stderr: 'some other push error', status: 1 };
                });
                expect(() => vcs.push('/path/to/repo')).toThrow(GenericVCSError);
            });
        });
    });

    describe('get_status() comprehensive unit tests', () => {
        it('should return correct status for untracked files', () => {
            const porcelainOutput = `? untracked.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            const status = vcs.get_status('/path/to/repo');
            expect(status.untracked).toEqual(['untracked.txt']);
        });

        it('should return correct status for added files', () => {
            const porcelainOutput = `1 A. N... 100644 100644 100644 cbc4e2e35b801b151db095c8bf8e687cb92420c7 cbc4e2e35b801b151db095c8bf8e687cb92420c7 added.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            const status = vcs.get_status('/path/to/repo');
            expect(status.added).toEqual(['added.txt']);
        });

        it('should return correct status for deleted files', () => {
            const porcelainOutput = `1 .D N... 100644 100644 100644 cbc4e2e35b801b151db095c8bf8e687cb92420c7 cbc4e2e35b801b151db095c8bf8e687cb92420c7 deleted.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            const status = vcs.get_status('/path/to/repo');
            expect(status.deleted).toEqual(['deleted.txt']);
        });

        it('should return correct status for renamed files', () => {
            const porcelainOutput = `2 R. N... 100644 100644 100644 cbc4e2e35b801b151db095c8bf8e687cb92420c7 cbc4e2e35b801b151db095c8bf8e687cb92420c7 R100 to.txt\tfrom.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            const status = vcs.get_status('/path/to/repo');
            expect(status.renamed).toEqual([{ from: 'from.txt', to: 'to.txt' }]);
        });

        it('should return correct status for conflicted files', () => {
            const porcelainOutput = `u UU N 0 0 0 0 0 0 0 conflict.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            const status = vcs.get_status('/path/to/repo');
            expect(status.conflicted).toEqual(['conflict.txt']);
        });

        it('should return is_operation_in_progress: merge when a merge is in progress', () => {
            vi.mocked(fs).existsSync.mockImplementation((p: string) => {
                if (p.includes('.git/MERGE_HEAD')) return true;
                return false;
            });
            mockExecSync.mockReturnValue(''); // No other status changes
            const status = vcs.get_status('/path/to/repo');
            expect(status.is_operation_in_progress).toEqual({ type: 'merge' });
        });

        it('should return is_operation_in_progress: rebase when a rebase is in progress', () => {
            vi.mocked(fs).existsSync.mockImplementation((p: string) => {
                if (p.includes('.git/rebase-merge') || p.includes('.git/rebase-apply')) return true;
                return false;
            });
            mockExecSync.mockReturnValue(''); // No other status changes
            const status = vcs.get_status('/path/to/repo');
            expect(status.is_operation_in_progress).toEqual({ type: 'rebase' });
        });

        it('should return is_operation_in_progress: none when no operation is in progress', () => {
            vi.mocked(fs).existsSync.mockReturnValue(false);
            mockExecSync.mockReturnValue('');
            const status = vcs.get_status('/path/to/repo');
            expect(status.is_operation_in_progress).toEqual({ type: 'none' });
        });
    });

    describe('switch_reference()', () => {
        it('should execute git checkout', () => {
            vcs.switch_reference({ path: '/path/to/repo', reference: 'my-branch' });
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('checkout my-branch'), expect.any(Object));
        });
        it('should throw DirtyWorkingDirectoryError', () => {
            mockExecSync.mockImplementation(() => {
                throw { stderr: 'Your local changes would be overwritten' };
            });
            expect(() => vcs.switch_reference({ path: '/path/to/repo', reference: 'my-branch' }))
                .toThrow(DirtyWorkingDirectoryError);
        });
    });

    describe('list_conflicts()', () => {
        it('should return conflicted files', () => {
            const porcelainOutput = `u UU N 0 0 0 0 0 0 0 file1.txt\nu UU N 0 0 0 0 0 0 0 file2.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            expect(vcs.list_conflicts('/path/to/repo')).toEqual(['file1.txt', 'file2.txt']);
        });
    });

    describe('resolve_conflict()', () => {
        it('should execute git add', () => {
            vcs.resolve_conflict({ path: '/path/to/repo', files: ['file1.txt', 'file2.txt'] });
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('add file1.txt file2.txt'), expect.any(Object));
        });
    });

    describe('abort_operation()', () => {
        it('should abort a merge', () => {
            vi.spyOn(vcs, 'get_status').mockReturnValue({ is_operation_in_progress: { type: 'merge' } } as any);
            vcs.abort_operation('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('merge --abort'), expect.any(Object));
        });

        it('should abort a rebase', () => {
            vi.spyOn(vcs, 'get_status').mockReturnValue({ is_operation_in_progress: { type: 'rebase' } } as any);
            vcs.abort_operation('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('rebase --abort'), expect.any(Object));
        });
    });

    describe('create_commit()', () => {
        it('should commit all if no files specified', () => {
            vcs.create_commit({ path: '/path/to/repo', message: 'Commit all' });
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('commit -m "Commit all"'), expect.any(Object));
        });

        it('should commit a specific list of files', () => {
            vcs.create_commit({
                path: '/path/to/repo',
                message: 'Commit specific files',
                files: ['file1.txt', 'file2.txt'],
            });
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("add -- 'file1.txt' 'file2.txt'"), expect.any(Object));
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('commit -m "Commit specific files"'), expect.any(Object));
        });

        it('should return commit_id and change_id', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse HEAD')) return 'test_commit_id';
                return '';
            });
            const { commit_id, change_id } = vcs.create_commit({ path: '/path/to/repo', message: 'Test commit' });
            expect(commit_id).toBe('test_commit_id');
            expect(change_id).toBe('test_commit_id');
        });

        it('should use a temporary index file for transactional safety', () => {
            let capturedOptions: any;
            mockExecSync.mockImplementation((command: string, options: any) => {
                if (command.includes('rev-parse --git-dir')) return '/mock/repo/.git';
                // Capture options from any command that uses the custom environment
                if (options?.env?.GIT_INDEX_FILE) {
                    capturedOptions = options;
                }
                if (command.includes('rev-parse HEAD')) return 'test_commit_id';
                return '';
            });
            // We also need to mock Date.now() to ensure a consistent temp file name for the assertion.
            vi.spyOn(Date, 'now').mockReturnValue(12345);
            vcs.create_commit({ path: '/mock/repo', message: 'Test transactional commit' });
            expect(capturedOptions).toBeDefined();
            expect(capturedOptions.env.GIT_INDEX_FILE).toContain('temp_index_12345');
        });

        it('should handle initial commit on empty repository (regression test)', () => {
            let commitCalled = false;
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('rev-parse --git-dir')) return '/mock/repo/.git';

                if (command.includes('rev-parse HEAD')) {
                    if (!commitCalled) {
                        throw new Error('fatal: Not a valid object name HEAD');
                    } else {
                        return 'new_commit_id';
                    }
                }

                if (command.includes('read-tree')) {
                    throw new Error('git read-tree HEAD should not be called for initial commit');
                }

                if (command.includes('commit')) {
                    commitCalled = true;
                    return '';
                }

                if (command.includes('symbolic-ref HEAD')) return 'refs/heads/master';

                return '';
            });

            const { commit_id } = vcs.create_commit({ path: '/mock/repo', message: 'Initial commit' });
            expect(commit_id).toBe('new_commit_id');
            expect(commitCalled).toBe(true);
        });
    });

    describe('Error Handling', () => {
        it('should throw VCSRepositoryLockedError', () => {
            mockExecSync.mockImplementation(() => { throw { stderr: '.git/index.lock' }; });
            expect(() => vcs.get_root_path('/path/to/repo')).toThrow(VCSRepositoryLockedError);
        });

        it('should throw NotARepositoryError when command fails for non-repo with specific error', () => {
            mockExecSync.mockImplementation(() => {
                throw { stderr: 'fatal: not a git repository (or any of the parent directories)', status: 128 };
            });
            expect(() => vcs.get_root_path('/path/to/non-repo')).toThrow(NotARepositoryError);
        });

        it('should throw GenericVCSError for unexpected errors', () => {
            mockExecSync.mockImplementation(() => { throw new Error('something bad happened'); });
            expect(() => vcs.get_root_path('/path/to/repo')).toThrow(GenericVCSError);
        });

        it('should throw GenericVCSError when execSync throws an object without stderr', () => {
            mockExecSync.mockImplementation(() => { throw { message: 'some error', status: 1 }; });
            expect(() => vcs.get_root_path('/path/to/repo')).toThrow(GenericVCSError);
        });

        it('should throw VCSNotFoundError when git executable is not found', () => {
            mockExecSync.mockImplementation(() => {
                throw { code: 'ENOENT' }; // Simulate 'git: command not found' with only code
            });
            expect(() => vcs.get_root_path('/path/to/repo')).toThrow(VCSNotFoundError);
        });
    });

    describe('Extended API Methods', () => {
        describe('get_config()', () => {
            it('should return config value', () => {
                mockExecSync.mockReturnValue('Test User');
                expect(vcs.get_config('/path/to/repo', 'user.name')).toBe('Test User');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('config user.name'), expect.any(Object));
            });
            it('should return null if not set', () => {
                mockExecSync.mockImplementation(() => { throw { status: 1 }; });
                expect(vcs.get_config('/path/to/repo', 'user.unknown')).toBeNull();
            });
        });

        describe('get_user_identity()', () => {
            it('should return user identity', () => {
                mockExecSync.mockImplementation((cmd: string) => {
                    if (cmd.includes('user.name')) return 'Test User';
                    if (cmd.includes('user.email')) return 'test@example.com';
                    return '';
                });
                expect(vcs.get_user_identity('/path/to/repo')).toEqual({ name: 'Test User', email: 'test@example.com' });
            });
            it('should return null if not configured', () => {
                mockExecSync.mockImplementation(() => { throw { status: 1 }; });
                expect(vcs.get_user_identity('/path/to/repo')).toBeNull();
            });
        });

    describe('get_ignored_files()', () => {
        it('should return list of ignored files', () => {
            mockExecSync.mockReturnValue('! ignored1.txt\n! ignored2.log');
            expect(vcs.get_ignored_files('/path/to/repo')).toEqual(['ignored1.txt', 'ignored2.log']);
            // Assuming implementation uses something like git ls-files -o -i --exclude-standard
            // or git status --ignored --porcelain=v2
        });
    });

        describe('get_file_content()', () => {
            it('should return file content', () => {
                mockExecSync.mockReturnValue('content');
                expect(vcs.get_file_content('/path/to/repo', 'HEAD', 'file.txt')).toBe('content');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("show HEAD:'file.txt'"), expect.any(Object));
            });
        });

        describe('get_diff()', () => {
            it('should return diff output', () => {
                mockExecSync.mockReturnValue('diff output');
                expect(vcs.get_diff('/path/to/repo', 'HEAD~1..HEAD', 'file.txt')).toBe('diff output');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("diff HEAD~1..HEAD -- 'file.txt'"), expect.any(Object));
            });
             it('should return null if binary', () => {
                 // The implementation should check is_binary or handle the binary diff output
                 // If mocking checking is_binary internally:
                 vi.spyOn(vcs, 'is_binary').mockReturnValue(true);
                 expect(vcs.get_diff('/path/to/repo', 'HEAD~1..HEAD', 'file.png')).toBeNull();
            });
        });

        describe('get_binary_diff_info()', () => {
             it('should return binary info', () => {
                // Mocking underlying calls.
                // Implementation might check attributes and size.
                // We assume it might use 'git cat-file -s' for size.
                mockExecSync.mockImplementation((cmd: string) => {
                    if (cmd.includes('check-attr')) return 'binary: set';
                    if (cmd.includes('cat-file -s')) return '1024';
                    return '';
                });

                const info = vcs.get_binary_diff_info('/path/to/repo', 'file.bin', 'HEAD~1..HEAD');
                expect(info).toEqual({ is_binary: true, old_size: 1024, new_size: 1024 });
                // Note: The logic for old_size/new_size in git might require two calls.
                // We just check basic structure here.
            });
        });

        describe('get_changed_files()', () => {
            it('should return list of changed files', () => {
                mockExecSync.mockReturnValue('file1.txt\nfile2.txt');
                expect(vcs.get_changed_files('/path/to/repo', 'HEAD~1..HEAD')).toEqual(['file1.txt', 'file2.txt']);
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('diff --name-only HEAD~1..HEAD'), expect.any(Object));
            });
        });

        describe('get_log()', () => {
            it('should return parsed log', () => {
                // Format: %H|||%s|||%aI|||%an
                const logOutput = 'hash1\x00msg1\x002023-01-01T00:00:00Z\x00Author1\nhash2\x00msg2\x002023-01-02T00:00:00Z\x00Author2';
                mockExecSync.mockReturnValue(logOutput);
                const log = vcs.get_log('/path/to/repo', 2);
                expect(log).toEqual([
                    { commit_id: 'hash1', message: 'msg1', date: '2023-01-01T00:00:00Z', author: 'Author1' },
                    { commit_id: 'hash2', message: 'msg2', date: '2023-01-02T00:00:00Z', author: 'Author2' }
                ]);
            });

            it('should filter log by file path', () => {
                mockExecSync.mockReturnValue('');
                vcs.get_log('/path/to/repo', 2, undefined, 'file.txt');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("log --pretty=format:\"%H%x00%s%x00%aI%x00%an\" -n 2 -- 'file.txt'"), expect.any(Object));
            });
        });

        describe('search_history()', () => {
            it('should return matching commits', () => {
                const logOutput = 'hash1|||msg1|||2023-01-01T00:00:00Z|||Author1';
                mockExecSync.mockReturnValue(logOutput);
                const results = vcs.search_history('/path/to/repo', 'query', 10);
                expect(results).toHaveLength(1);
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('--grep=query'), expect.any(Object));
            });

            it('should filter search by file path', () => {
                mockExecSync.mockReturnValue('');
                vcs.search_history('/path/to/repo', 'query', 10, 'file.txt');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("--grep=query --pretty=format:\"%H%x00%s%x00%aI%x00%an\" -n 10 -- 'file.txt'"), expect.any(Object));
            });
        });

        describe('get_merge_base()', () => {
            it('should return merge base commit id', () => {
                mockExecSync.mockReturnValue('base_commit_id');
                expect(vcs.get_merge_base('/path/to/repo', 'branch1', 'branch2')).toBe('base_commit_id');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('merge-base branch1 branch2'), expect.any(Object));
            });
        });

        describe('revert_commit()', () => {
            it('should revert commit and return new commit id', () => {
                mockExecSync.mockImplementation((cmd: string) => {
                    if (cmd.includes('revert')) return '';
                    if (cmd.includes('rev-parse HEAD')) return 'revert_commit_id';
                    return '';
                });
                expect(vcs.revert_commit('/path/to/repo', 'commit_to_revert')).toBe('revert_commit_id');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('revert --no-edit commit_to_revert'), expect.any(Object));
            });
        });
    });
});
