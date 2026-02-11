import { GitVcs } from './git.js';
import { JjVcs } from './jj.js';
import { Vcs, VcsType } from './types.js';

const strategies = [GitVcs, JjVcs];

/**
 * Detects the VCS type for a given path.
 * @param repoPath The path to check.
 * @returns The VcsType (e.g., 'git', 'jj') or null if not a repository.
 */
export function detectVcs(repoPath: string): VcsType | null {
  for (const Strategy of strategies) {
    const vcs = new Strategy();
    const type = vcs.is_repository(repoPath);
    if (type) {
      return type;
    }
  }
  return null;
}

/**
 * Initializes a new VCS repository.
 * @param repoPath The path where the repository should be initialized.
 * @param type The type of VCS to initialize ('git' or 'jj').
 */
export function initVcs(repoPath: string, type: VcsType): void {
  if (type === VcsType.Git) {
    new GitVcs().init(repoPath);
  } else if (type === VcsType.Jj) {
    new JjVcs().init(repoPath);
  } else {
    throw new Error(`Unsupported VCS type for initialization: ${type}`);
  }
}

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
