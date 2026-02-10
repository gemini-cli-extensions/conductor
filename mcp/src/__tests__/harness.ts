
import { Vcs } from '../vcs/types';

export interface TestHarness {
    setupRepo(vcsType: 'git' | 'jj', remoteUrl?: string): string;
    setupRemoteRepo(vcsType: 'git' | 'jj'): string;
    teardownRepo(repoPath: string): void;
    runCmd(command: string, repoPath: string): string;
    createFile(repoPath: string, filePath: string, content: string | Buffer): void;
    getVcs(repoPath: string): Vcs;
}

export async function getHarness(vcsType: 'git' | 'jj'): Promise<TestHarness> {
    if (vcsType === 'git') {
        return (await import('./git/harness')).harness;
    }
    if (vcsType === 'jj') {
        return (await import('./jj/harness')).harness;
    }
    throw new Error(`Unsupported VCS type: ${vcsType}`);
}
