import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestHarness, getHarness } from './harness';
import * as fs from 'fs';
import * as path from 'path';

const vcsTypes: ('git' | 'jj')[] = ['git', 'jj'];

vcsTypes.forEach((vcsType) => {
    describe(`VCS Abstraction Layer - Robustness Tests (${vcsType})`, () => {
        let repoPath: string;
        let vcs: any;
        let harness: TestHarness;

        beforeEach(async () => {
            harness = await getHarness(vcsType);
            repoPath = harness.setupRepo(vcsType);
            vcs = harness.getVcs(repoPath);
        });

        afterEach(() => {
            harness.teardownRepo(repoPath);
        });

        // Gap #1: Concurrency & Locking
        it('handles locking gracefully (wait_for_lock or VCSRepositoryLockedError)', () => {
            if (vcsType === 'git') {
                const lockFile = path.join(repoPath, '.git/index.lock');
                fs.writeFileSync(lockFile, '');

                // With lock held, try to create commit.
                // Spec says create_commit(..., wait_for_lock: true) waits. 
                // If false, should fail immediately?
                // The implementation doesn't expose wait_for_lock option yet in `CommitParams`?
                // Wait, `create_commit` implementation in `git.ts` does NOT take `wait_for_lock` param.
                // It takes `CommitParams` which has `message`, `files`.
                // The spec defined `wait_for_lock`. The implementation missed it?
                // Let's assume implementation throws `VCSRepositoryLockedError` if wait is false (default).
                
                try {
                    vcs.create_commit({
                        path: repoPath,
                        message: 'Lock test',
                        files: []
                    });
                    // Should fail
                    expect.fail('Should throw locked error');
                } catch (e: any) {
                    expect(e.name).toBe('VCSRepositoryLockedError');
                } finally {
                    fs.unlinkSync(lockFile);
                }
            } else {
                // JJ locking mechanisms are different (op logs).
                // JJ handles concurrent operations better usually, or locks the repo.
                // Let's see if we can simulate lock. JJ has `.jj/lock`?
                // Skip for JJ unless we know how to lock it reliably for test.
            }
        });

        // Gap #4: Submodules
        it('handles submodules correctly (no recursion)', () => {
            if (vcsType === 'jj') return; // JJ support for git submodules is complex/different. Focus on Git.
            
            // Add a submodule using -c to allow file protocol
            const submodulePath = path.join(repoPath, 'sub');
            const submoduleRemote = harness.setupRemoteRepo('git');
            
            harness.runCmd(`git -c protocol.file.allow=always submodule add ${submoduleRemote} sub`, repoPath);
            harness.runCmd('git commit -m "Add submodule"', repoPath);
            
            // Verify status is clean
            let status = vcs.get_status(repoPath);
            expect(status.modified).not.toContain('sub');

            // Modify submodule content (dirty working directory inside submodule)
            harness.createFile(submodulePath, 'dirty.txt', 'dirty');
            
            // Verify status sees submodule as modified (but not the file inside)
            status = vcs.get_status(repoPath);
            // Git status porcelain v2 shows 'sub' as modified if it has changes?
            // Usually shows 'M' for the submodule path.
            expect(status.modified).toContain('sub');
            expect(status.modified).not.toContain('sub/dirty.txt');

            // Clean up
            harness.teardownRepo(submoduleRemote);
        });
    });
});
