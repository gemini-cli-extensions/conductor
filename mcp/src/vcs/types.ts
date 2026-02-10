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

export enum VcsType {
    Git = 'git',
    Jj = 'jj',
}

export interface VcsCapabilities {
    has_staging_area: boolean;
    supports_rewrite_history: boolean;
    distinguishes_change_id: boolean;
}

export interface Vcs {
    is_repository(repoPath: string): VcsType | null;
    get_root_path(repoPath: string): string;
    get_capabilities(): VcsCapabilities;
    get_status(repoPath: string): VcsStatus;
    switch_reference(params: { path: string, reference: string }): void;
    create_commit(params: CommitParams): { commit_id: string, change_id: string };
    is_binary(repoPath: string, filePath: string): boolean;
    is_ignored(repoPath: string, filePath: string): boolean;
    get_ignored_files(repoPath: string): string[];
    get_file_content(repoPath: string, revision: string, filePath: string): string;
    get_diff(repoPath: string, revisionRange: string | undefined, filePath?: string): string | null;
    get_binary_diff_info(repoPath: string, filePath: string, revisionRange?: string): { is_binary: boolean, old_size: number, new_size: number } | null;
    get_changed_files(repoPath: string, revisionRange: string): string[];
    get_log(repoPath: string, limit: number, revisionRange?: string, filePath?: string): { commit_id: string, message: string, date: string, author: string }[];
    search_history(repoPath: string, query: string, limit: number, filePath?: string): { commit_id: string, message: string, date: string, author: string }[];
    get_merge_base(repoPath: string, revisionA: string, revisionB: string): string | null;
    revert_commit(repoPath: string, commitId: string, waitForLock?: boolean): string;
    get_config(repoPath: string, key: string): string | null;
    get_user_identity(repoPath: string): { name: string, email: string } | null;
    get_current_reference(repoPath: string): Reference;
    get_upstream_buffer(repoPath: string): { ahead: number, behind: number };
    get_parent_ids(repoPath: string, commitId: string): string[];
    fetch(repoPath: string): void;
    pull(repoPath: string): void;
    push(repoPath: string): void;
    list_conflicts(repoPath: string): string[];
    resolve_conflict(params: { path: string, files: string[] }): void;
    abort_operation(repoPath: string): void;
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