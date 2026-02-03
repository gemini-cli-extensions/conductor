import { GitVcs } from './git.js';
import { JjVcs } from './jj.js';
import { Vcs } from './types.js';

const strategies = [GitVcs, JjVcs];

/**
 * Factory function to get the appropriate VCS implementation.
 * @param repoPath The path to the repository.
 * @returns An instance of the VCS implementation.
 * @throws {Error} If the VCS type is unknown or no repository is found.
 */
export function getVcs(repoPath: string): Vcs {
    for (const Strategy of strategies) {
        const vcs = new Strategy();
        if (vcs.is_repository(repoPath)) {
            return vcs;
        }
    }

    throw new Error(`No supported VCS repository found at ${repoPath}`);
}