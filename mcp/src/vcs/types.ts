// mcp/src/vcs/types.ts

// --- (Interfaces) ---
export interface VcsStatus {
    modified: string[];
    untracked: string[];
    added: string[];
    deleted: string[];
    conflicted: string[];
    renamed: { from: string, to: string }[];
    is_operation_in_progress: { type: 'merge' | 'rebase' | 'none' };
}

export interface CommitParams {
    path: string;
    message: string;
    files?: string[];
}

export interface Reference {
    name: string | null;
    commit_id: string;
    change_id: string;
    type: 'branch' | 'tag' | 'detached';
}

// --- (Error Classes) ---
export class VCSNotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'VCSNotFoundError';
  }
}

export class NotARepositoryError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NotARepositoryError';
  }
}

export class VCSRepositoryLockedError extends Error {
  public lockFile: string;
  constructor(message: string, lockFile: string) {
    super(message);
    this.name = 'VCSRepositoryLockedError';
    this.lockFile = lockFile;
  }
}

export class DirtyWorkingDirectoryError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'DirtyWorkingDirectoryError';
  }
}

export class AuthenticationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

export class MergeConflictError extends Error {
  public files: string[];
  constructor(message: string, files: string[]) {
    super(message);
    this.name = 'MergeConflictError';
    this.files = files;
  }
}

export class GenericVCSError extends Error {
  public command: string;
  public exitCode: number;
  constructor(message: string, command: string, exitCode: number) {
    super(message);
    this.name = 'GenericVCSError';
    this.command = command;
    this.exitCode = exitCode;
  }
}
