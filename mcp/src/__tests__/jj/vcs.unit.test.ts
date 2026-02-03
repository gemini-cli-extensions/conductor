// mcp/src/__tests__/jj/vcs.unit.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { JjVcs } from '../../vcs/jj';
import { NotARepositoryError, GenericVCSError, VcsStatus } from '../../vcs/types';
import { execSync } from 'child_process';

vi.mock('child_process', () => ({
    execSync: vi.fn(),
}));

vi.mock('fs', () => ({
    ...vi.importActual('fs'),
    existsSync: vi.fn(),
    readdirSync: vi.fn(),
}));

describe('VCS Abstraction Layer - Jujutsu Unit Tests', () => {
    let vcs: JjVcs;
    let mockExecSync: vi.Mock;
    let currentTest: string; // To control specific mocks for get_current_reference tests

    beforeEach(() => {
        vcs = new JjVcs();
        vi.resetAllMocks();
        mockExecSync = execSync as vi.Mock;
        mockExecSync.mockImplementation((command: string) => {
            const separator = '|||';
            // Match the new delimited command structure for log
            if (command.includes(separator)) {
                if (currentTest === 'branch') return `commit1${separator}change1${separator}my-branch${separator}`;
                if (currentTest === 'tag') return `commit2${separator}change2${separator}${separator}v1.0.0`;
                if (currentTest === 'detached') return `commit3${separator}change3${separator}${separator}`;
                // Default log output for other tests
                return `hash1${separator}msg1${separator}2023-01-01T00:00:00Z${separator}Author1\nhash2${separator}msg2${separator}2023-01-02T00:00:00Z${separator}Author2`;
            }

            // A generic happy-path mock for other commands.
            if (command.includes('jj --color=never status')) return 'M modified.txt\nA added.txt\nD deleted.txt';
            if (command.includes('diff --git -r @-')) return ''; // Default no renames
            if (command.includes('jj --color=never root')) return '/path/to/repo';
            if (command.includes('git -C')) {
                // Mock for is_ignored which uses git check-ignore
                if (command.includes('ignored-file.txt')) return ''; 
                if (command.includes('status --ignored')) return '!! ignored1.txt\n!! ignored2.log';
                throw { status: 1, stderr: 'not ignored' };
            }
            if (command.includes('jj --color=never bookmark list')) return `main: rxyzabc... zyxwvut @ origin (ahead by 2, behind by 1)`;
            // Default behavior if no specific mock matches
            return '';
        });
    });

    describe('is_repository()', () => {
        it("should return 'jj' for a valid jj repository", () => {
            // The default mock should work here, as it doesn't throw.
            expect(vcs.is_repository('/path/to/repo')).toBe('jj');
            expect(mockExecSync).toHaveBeenCalledWith(
                expect.stringContaining('jj --color=never status'),
                expect.objectContaining({ cwd: '/path/to/repo' })
            );
        });

        it('should return null if not a repository', () => {
            mockExecSync.mockImplementation(() => { 
                const err = new Error('Command failed');
                (err as any).stderr = 'There is no jj repo in .';
                throw err; 
            });
            expect(vcs.is_repository('/path/to/repo')).toBeNull();
        });
    });

    describe('get_root_path()', () => {
        it('should return the root path for a valid jj repository', () => {
            mockExecSync.mockReturnValue('/path/to/repo');
            expect(vcs.get_root_path('/path/to/repo/subdir')).toBe('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(
                expect.stringContaining('jj --color=never root'),
                expect.objectContaining({ cwd: '/path/to/repo/subdir' })
            );
        });

        it('should throw NotARepositoryError if not a repository', () => {
            mockExecSync.mockImplementation(() => {
                throw { stderr: 'There is no jj repo in' };
            });
            expect(() => vcs.get_root_path('/path/to/non-repo')).toThrow(NotARepositoryError);
        });
    });

    describe('get_capabilities()', () => {
        it('should return the correct capabilities for Jujutsu', () => {
            const capabilities = vcs.get_capabilities();
            expect(capabilities).toEqual({
                has_staging_area: false,
                supports_rewrite_history: true,
                distinguishes_change_id: true,
            });
        });
    });

    describe('get_status()', () => {
        it('should correctly parse status output', () => {
            // This tests the private `parseStatus` method via `get_status`
            mockExecSync.mockReturnValue('M modified.txt\nA added.txt\nD deleted.txt\n? untracked.txt');
            vi.spyOn(vcs as any, 'getAllFilesInDir').mockReturnValue(['untracked.txt']);
            vi.spyOn(vcs as any, 'is_ignored').mockReturnValue(false);
            vi.spyOn(vcs as any, 'list_conflicts').mockReturnValue([]);
            
            const status = vcs.get_status('/path/to/repo');

            expect(status.modified).toEqual(['modified.txt']);
            expect(status.added).toEqual(['added.txt']);
            expect(status.deleted).toEqual(['deleted.txt']);
        });

        it('should identify untracked files', () => {
            mockExecSync.mockReturnValue('M modified.txt'); // jj status doesn't show untracked
            vi.spyOn(vcs as any, 'getAllFilesInDir').mockReturnValue(['modified.txt', 'untracked.txt']);
            vi.spyOn(vcs as any, 'is_ignored').mockReturnValue(false);
            vi.spyOn(vcs as any, 'list_conflicts').mockReturnValue([]);

            const status = vcs.get_status('/path/to/repo');
            expect(status.untracked).toEqual(['untracked.txt']);
        });

        it('should detect renamed files', () => {
            // Mock status showing add/delete
            mockExecSync.mockImplementation((cmd: string) => {
                if (cmd.includes('jj --color=never status')) return 'A new.txt\nD old.txt';
                if (cmd.includes('diff --git')) return 'diff --git a/old.txt b/new.txt\nrename from old.txt\nrename to new.txt';
                return '';
            });
            vi.spyOn(vcs as any, 'getAllFilesInDir').mockReturnValue([]);
            vi.spyOn(vcs as any, 'is_ignored').mockReturnValue(false);
            vi.spyOn(vcs as any, 'list_conflicts').mockReturnValue([]);

            const status = vcs.get_status('/path/to/repo');
            expect(status.renamed).toEqual([{ from: 'old.txt', to: 'new.txt' }]);
            expect(status.added).not.toContain('new.txt');
            expect(status.deleted).not.toContain('old.txt');
        });
    });

    describe('create_commit()', () => {
        it('should describe the current commit and create a new one', () => {
            mockExecSync.mockReturnValueOnce(''); // status
            mockExecSync.mockReturnValueOnce(''); // describe
            mockExecSync.mockReturnValueOnce('commit_id change_id'); // log
            mockExecSync.mockReturnValueOnce(''); // new

            const { commit_id, change_id } = vcs.create_commit({ path: '/path/to/repo', message: 'Test commit' });

            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('status'), expect.any(Object));
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("describe -m 'Test commit'"), expect.any(Object));
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("log -r '@'"), expect.any(Object));
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('new'), expect.any(Object));
            expect(commit_id).toBe('commit_id');
            expect(change_id).toBe('change_id');
        });
    });
    
    describe('get_current_reference()', () => {
        it('should return branch info if on a branch', () => {
            currentTest = 'branch';
            const ref = vcs.get_current_reference('/path/to/repo');
            expect(ref).toEqual({
                name: 'my-branch',
                commit_id: 'commit1',
                change_id: 'change1',
                type: 'branch',
            });
        });

        it('should return tag info if on a tag but not a branch', () => {
            currentTest = 'tag';
            const ref = vcs.get_current_reference('/path/to/repo');
            expect(ref).toEqual({
                name: 'v1.0.0',
                commit_id: 'commit2',
                change_id: 'change2',
                type: 'tag',
            });
        });

        it('should return detached info if not on a branch or tag', () => {
            currentTest = 'detached';
            const ref = vcs.get_current_reference('/path/to/repo');
            expect(ref).toEqual({
                name: null,
                commit_id: 'commit3',
                change_id: 'change3',
                type: 'detached',
            });
        });
    });
    
    describe('get_parent_ids()', () => {
        it('should return a single parent ID for a normal commit', () => {
            mockExecSync.mockReturnValue('parent_abc');
            const parents = vcs.get_parent_ids('/path/to/repo', 'commit_xyz');
            expect(parents).toEqual(['parent_abc']);
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining(`log -r 'commit_xyz'`), expect.any(Object));
        });

        it('should return multiple parent IDs for a merge commit', () => {
            mockExecSync.mockReturnValue('parent1_abc\nparent2_def');
            const parents = vcs.get_parent_ids('/path/to/repo', 'merge_commit');
            expect(parents).toEqual(['parent1_abc', 'parent2_def']);
        });

        it('should return an empty array for the root commit', () => {
            mockExecSync.mockReturnValue('');
            const parents = vcs.get_parent_ids('/path/to/repo', 'root_commit');
            expect(parents).toEqual([]);
        });
    });

    describe('is_ignored()', () => {
        it('should return true if a file is ignored by git', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('git -C ')) return ''; // Success means ignored
                throw new Error('should not happen');
            });
            expect(vcs.is_ignored('/path/to/repo', 'ignored-file.txt')).toBe(true);
        });

        it('should return false if a file is not ignored by git', () => {
            mockExecSync.mockImplementation((command: string) => {
                if (command.includes('git -C ')) throw { status: 1 }; // Exit code 1 means not ignored
                throw new Error('should not happen');
            });
            expect(vcs.is_ignored('/path/to/repo', 'non-ignored-file.txt')).toBe(false);
        });
    });

    describe('Error Handling', () => {
        it('should throw NotARepositoryError for jj commands in a non-repo directory', () => {
            mockExecSync.mockImplementation(() => {
                throw { stderr: 'There is no jj repo in /path/to/non-repo' };
            });
            expect(() => vcs.get_root_path('/path/to/non-repo')).toThrow(NotARepositoryError);
        });

        it('should throw GenericVCSError for other errors', () => {
            mockExecSync.mockImplementation(() => {
                throw { message: 'some other error', status: 1 };
            });
            expect(() => vcs.get_root_path('/path/to/repo')).toThrow(GenericVCSError);
        });
    });

    describe('Extended API Methods', () => {
        describe('get_config()', () => {
            it('should return config value', () => {
                mockExecSync.mockReturnValue('Test User');
                expect(vcs.get_config('/path/to/repo', 'user.name')).toBe('Test User');
                // Updated to match implementation (no --user)
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('config get user.name'), expect.any(Object));
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
        });

        describe('get_file_content()', () => {
            it('should return file content', () => {
                mockExecSync.mockReturnValue('content');
                expect(vcs.get_file_content('/path/to/repo', 'HEAD', 'file.txt')).toBe('content');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("file show -r @ 'file.txt'"), expect.any(Object));
            });
        });

        describe('get_diff()', () => {
            it('should return diff output', () => {
                mockExecSync.mockReturnValue('diff output');
                expect(vcs.get_diff('/path/to/repo', 'HEAD~1..HEAD', 'file.txt')).toBe('diff output');
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("diff -r \"HEAD~1..HEAD\" 'file.txt'"), expect.any(Object));
            });
        });

        describe('get_changed_files()', () => {
            it('should return list of changed files', () => {
                mockExecSync.mockReturnValue('file1.txt\nfile2.txt');
                expect(vcs.get_changed_files('/path/to/repo', 'HEAD~1..HEAD')).toEqual(['file1.txt', 'file2.txt']);
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('diff --name-only -r @~1..@'), expect.any(Object));
            });
        });

        describe('get_log()', () => {
            it('should return parsed log', () => {
                const logOutput = 'hash1\x00msg1\x002023-01-01T00:00:00Z\x00Author1\nhash2\x00msg2\x002023-01-02T00:00:00Z\x00Author2';
                mockExecSync.mockReturnValue(logOutput);
                const log = vcs.get_log('/path/to/repo', 2);
                expect(log).toEqual([
                    { commit_id: 'hash1', message: 'msg1', date: '2023-01-01T00:00:00Z', author: 'Author1' },
                    { commit_id: 'hash2', message: 'msg2', date: '2023-01-02T00:00:00Z', author: 'Author2' }
                ]);
            });
        });

        describe('search_history()', () => {
            it('should return matching commits', () => {
                const logOutput = 'hash1\x00msg1\x002023-01-01T00:00:00Z\x00Author1';
                mockExecSync.mockReturnValue(logOutput);
                const results = vcs.search_history('/path/to/repo', 'query', 10);
                expect(results).toHaveLength(1);
                // Spec: jj log -r "description(~<query>)"
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("log -r \"description(~'query') & ::@-\" "), expect.any(Object));
            });
        });

        describe('get_merge_base()', () => {
            it('should return merge base commit id', () => {
                mockExecSync.mockReturnValue('base_commit_id');
                expect(vcs.get_merge_base('/path/to/repo', 'rev1', 'rev2')).toBe('base_commit_id');
                // Updated to use heads(::A & ::B) which is valid in current JJ
                expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('heads(::rev1 & ::rev2)'), expect.any(Object));
            });
        });

        describe('revert_commit()', () => {
            it('should throw error (not implemented)', () => {
                expect(() => vcs.revert_commit('/path/to/repo', 'commit_id')).toThrow('Not implemented');
            });
        });
    });

    describe('Implemented Methods', () => {
        it('switch_reference() should call jj new', () => {
            vcs.switch_reference({ path: '/path/to/repo', reference: 'my-branch' });
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("jj --color=never new 'my-branch'"), expect.any(Object));
        });

        describe('is_binary()', () => {
            it('should return true if git check-attr says a file is binary', () => {
                mockExecSync.mockImplementation((command: string) => {
                    if (command.includes('git -C')) return 'file.bin: binary: set';
                    return '';
                });
                expect(vcs.is_binary('/path/to/repo', 'file.bin')).toBe(true);
            });

            it('should return false if git check-attr says a file is not binary', () => {
                mockExecSync.mockImplementation((command: string) => {
                    if (command.includes('git -C')) return 'file.txt: binary: unspecified';
                    return '';
                });
                expect(vcs.is_binary('/path/to/repo', 'file.txt')).toBe(false);
            });

            it('should return false if git check-attr fails', () => {
                mockExecSync.mockImplementation((command: string) => {
                    if (command.includes('git -C')) throw { status: 1 };
                    return '';
                });
                expect(vcs.is_binary('/path/to/repo', 'file.txt')).toBe(false);
            });
        });

        describe('get_upstream_buffer()', () => {
            it('should return correct ahead/behind counts when upstream is present', () => {
                const mockBookmarkList = `main: ykvzty... @ origin (ahead by 2, behind by 1)`;
                mockExecSync.mockImplementation((command: string) => {
                    if (command.includes('jj --color=never bookmark list')) return mockBookmarkList;
                    if (command.includes('|||')) return 'commit1|||change1|||main|||';
                    return '';
                });
                const buffer = vcs.get_upstream_buffer('/path/to/repo');
                expect(buffer).toEqual({ ahead: 2, behind: 1 });
            });

            it('should return 0 for ahead/behind when not on a branch', () => {
                 mockExecSync.mockImplementation((command: string) => {
                    if (command.includes('|||')) return 'commit3|||change3||||||';
                    return '';
                });
                const buffer = vcs.get_upstream_buffer('/path/to/repo');
                expect(buffer).toEqual({ ahead: 0, behind: 0 });
            });
        });

        it('fetch() should call jj git fetch', () => {
            vcs.fetch('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('jj --color=never git fetch'), expect.any(Object));
        });

        it('pull() should call jj git fetch', () => {
            vcs.pull('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('jj --color=never git fetch'), expect.any(Object));
        });

        it('push() should call jj git push', () => {
            vcs.push('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('jj --color=never git push'), expect.any(Object));
        });

        it('list_conflicts() should parse conflicted files', () => {
            mockExecSync.mockReturnValue('file1.txt\nfile2.txt');
            const conflicts = vcs.list_conflicts('/path/to/repo');
            expect(conflicts).toEqual(['file1.txt', 'file2.txt']);
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('jj --color=never resolve --list'), expect.any(Object));
        });

        it('resolve_conflict() should call jj resolve with files', () => {
            vcs.resolve_conflict({ path: '/path/to/repo', files: ['file1.txt', 'file2.txt'] });
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining("jj --color=never resolve 'file1.txt' 'file2.txt'"), expect.any(Object));
        });

        it('abort_operation() should call jj undo', () => {
            vcs.abort_operation('/path/to/repo');
            expect(mockExecSync).toHaveBeenCalledWith(expect.stringContaining('jj --color=never undo'), expect.any(Object));
        });
    });
});