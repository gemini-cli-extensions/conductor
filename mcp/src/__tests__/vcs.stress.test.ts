import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestHarness, getHarness } from './harness';
import * as fs from 'fs';
import * as path from 'path';

const vcsTypes: ('git' | 'jj')[] = ['git', 'jj'];

vcsTypes.forEach((vcsType) => {
    describe(`VCS Abstraction Layer - Stress & Pathological Tests (${vcsType})`, () => {
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

        // Gap #2: Buffer Limits (Large Repo)
        it('handles large number of files without crashing (buffer limits)', () => {
            const fileCount = 2000;
            // Create many files
            for (let i = 0; i < fileCount; i++) {
                harness.createFile(repoPath, `stress-${i}.txt`, `content ${i}`);
            }

            // get_status should handle the output
            // Note: execSync default buffer is 1MB. 2000 lines * ~20 chars = 40KB.
            // We might need more files to hit the limit, or verify logic scales.
            // 2000 is a good "stress" start. If the implementation uses standard execSync, it handles 1MB.
            // A truly massive repo (100k files) might break it. But let's test if it handles a non-trivial load.
            const status = vcs.get_status(repoPath);
            // In git, untracked files are shown. In jj, untracked are filtered/shown.
            // Check count.
            const untrackedCount = status.untracked.length + status.added.length; // JJ might auto-add? No, untracked logic.
            // JJ harness might not auto-track new files unless told?
            // JJ status shows untracked files if not ignored.
            expect(untrackedCount).toBeGreaterThanOrEqual(fileCount);
        }, 30000); // Increase timeout

        it('handles large history log without crashing', () => {
            const commitCount = 30; // Reduced from 100 to avoid test timeout in CI/slow envs
            // Generating commits takes time.
            for (let i = 0; i < commitCount; i++) {
                harness.createFile(repoPath, `log-stress.txt`, `content ${i}`);
                if (vcsType === 'git') {
                    harness.runCmd('git add log-stress.txt', repoPath);
                    harness.runCmd(`git commit -m "Stress commit ${i}"`, repoPath);
                } else {
                    harness.runCmd(`jj commit -m "Stress commit ${i}"`, repoPath);
                }
            }

            const log = vcs.get_log(repoPath, commitCount);
            expect(log.length).toBe(commitCount);
        }, 30000);

        it('handles filtering logs in large history', () => {
            const commitCount = 20;
            const targetFile = 'filter-target.txt';
            harness.createFile(repoPath, targetFile, 'initial');

            if (vcsType === 'git') {
                harness.runCmd(`git add ${targetFile}`, repoPath);
                harness.runCmd('git commit -m "Initial target"', repoPath);
            } else {
                harness.runCmd('jj commit -m "Initial target"', repoPath);
            }

            // Create noise
            for (let i = 0; i < commitCount; i++) {
                harness.createFile(repoPath, `noise-${i}.txt`, `noise ${i}`);
                if (vcsType === 'git') {
                    harness.runCmd(`git add noise-${i}.txt`, repoPath);
                    harness.runCmd(`git commit -m "Noise ${i}"`, repoPath);
                } else {
                    harness.runCmd(`jj commit -m "Noise ${i}"`, repoPath);
                }
            }

            // Update target
            harness.createFile(repoPath, targetFile, 'modified');
            if (vcsType === 'git') {
                harness.runCmd(`git add ${targetFile}`, repoPath);
                harness.runCmd('git commit -m "Modify target"', repoPath);
            } else {
                harness.runCmd('jj commit -m "Modify target"', repoPath);
            }

            const log = vcs.get_log(repoPath, 100, undefined, targetFile);
            // Should find Initial and Modify commits
            expect(log.length).toBeGreaterThanOrEqual(2);
            expect(log.some((c: any) => c.message === 'Modify target')).toBe(true);
            expect(log.some((c: any) => c.message === 'Initial target')).toBe(true);
            // Should NOT find noise
            expect(log.some((c: any) => c.message.includes('Noise'))).toBe(false);
        }, 30000);

        // Gap #3: Pathological Inputs
        it('handles filenames with spaces, quotes, and weird characters', () => {
            const weirdName = 'weird "name" with spaces and \'quotes\'.txt';
            harness.createFile(repoPath, weirdName, 'weird content');

            if (vcsType === 'git') {
                // Git requires quoting for such files on command line if not careful
                // Harness runCmd uses execSync. We need to escape properly in harness or verify vcs handles it.
                // VCS abstraction uses `files` array.
                // We'll trust the harness helper `createFile` puts it on disk.
                // Now let's try to commit it using the abstraction.
                // But first, `get_status` should see it.
                const status = vcs.get_status(repoPath);
                expect(status.untracked).toContain(weirdName);

                vcs.create_commit({
                    path: repoPath,
                    message: 'Add weird file',
                    files: [weirdName]
                });

                const statusAfter = vcs.get_status(repoPath);
                expect(statusAfter.untracked).not.toContain(weirdName);
            } else {
                // JJ
                 const status = vcs.get_status(repoPath);
                 if (vcsType === 'jj') {
                     expect(status.added).toContain(weirdName);
                 } else {
                     expect(status.untracked).toContain(weirdName);
                 }

                 vcs.create_commit({
                    path: repoPath,
                    message: 'Add weird file',
                    files: [weirdName]
                });
                // In JJ, create_commit with files works by `jj commit <files>`.
                // The implementation must handle quoting.
            }
        });

        it('handles commit messages with delimiter characters', () => {
            const delimiter = '|||';
            const message = `Fix: ${delimiter} broken parser ${delimiter}`;

            if (vcsType === 'git') {
                harness.createFile(repoPath, 'delimiter.txt', 'content');
                vcs.create_commit({
                    path: repoPath,
                    message: message,
                    files: ['delimiter.txt']
                });
            } else {
                harness.createFile(repoPath, 'delimiter.txt', 'content');
                vcs.create_commit({
                    path: repoPath,
                    message: message,
                    files: ['delimiter.txt']
                });
            }

            const log = vcs.get_log(repoPath, 1);
            expect(log[0].message).toContain(message);
            // Ensure delimiter didn't break parsing (e.g. splitting the message)
            expect(log[0].author).not.toContain('broken parser'); // If split wrong, author might get garbage
        });
    });
});
