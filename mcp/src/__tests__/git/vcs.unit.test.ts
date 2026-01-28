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
            const porcelainOutput = `2 R. N... 100644 100644 100644 cbc4e2e35b801b151db095c8bf8e687cb92420c7 cbc4e2e35b801b151db095c8bf8e687cb92420c7 R100\tto.txt\tfrom.txt`;
            mockExecSync.mockReturnValue(porcelainOutput);
            const status = vcs.get_status('/path/to/repo');
            expect(status.renamed).toEqual([{ from: 'from.txt', to: 'to.txt' }]);
        });

        it('should return correct status for conflicted files', () => {
            const porcelainOutput = `u UU N... 100644 100644 100644 100644 fce2a2b... 7914439... 937b003... conflict.txt`;
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
            const porcelainOutput = `u UU N... file1.txt\nu UU N... file2.txt`;
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
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('add file1.txt file2.txt'), expect.any(Object));
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
            let gitIndexFile: string | undefined;
            mockExecSync.mockImplementation((command: string, options: any) => {
                if (command.includes('rev-parse --git-dir')) return '/mock/repo/.git';
                if (command.includes('add') || command.includes('commit')) {
                    gitIndexFile = '/mock/repo/.git/temp_index_12345'; // Directly set the expected path
                }
                if (command.includes('rev-parse HEAD')) return 'test_commit_id';
                return '';
            });
            // We also need to mock Date.now() to ensure a consistent temp file name for the assertion.
            vi.spyOn(Date, 'now').mockReturnValue(12345);
            vcs.create_commit({ path: '/mock/repo', message: 'Test transactional commit' });
            expect(gitIndexFile).toBeDefined();
            expect(gitIndexFile).toBe('/mock/repo/.git/temp_index_12345'); // Exact match now
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
});
