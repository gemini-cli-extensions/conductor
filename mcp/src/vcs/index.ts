import { Vcs as GitVcs } from './git';
import { Vcs as JjVcs } from './jj';
import { Vcs, VcsType } from './types';

/**
 * Factory function to get the appropriate VCS implementation.
 * @param repoPath The path to the repository.
 * @returns An instance of the VCS implementation.
 * @throws {Error} If the VCS type is unknown or no repository is found.
 */
export function getVcs(repoPath: string): Vcs {
    // First, try to detect Git
    const gitVcs = new GitVcs();
    if (gitVcs.is_repository(repoPath) === VcsType.Git) {
        return gitVcs;
    }

    // If not Git, try to detect Jujutsu
    const jjVcs = new JjVcs();
    if (jjVcs.is_repository(repoPath) === VcsType.Jj) {
        return jjVcs;
    }

    throw new Error(`No supported VCS repository found at ${repoPath}`);
}