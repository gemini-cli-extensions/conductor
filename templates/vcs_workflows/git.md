# VCS Workflow Definition: Git

This file defines the specific shell commands for Conductor to use when operating within a Git repository.

## Command Definitions

### initialize_repository
```bash
git init
```

### get_repository_status
```bash
# This command outputs a list of modified/untracked files.
# An empty output means the repository is clean.
git status --porcelain
```

### list_relevant_files
```bash
# Lists all tracked files and other non-ignored files in the repo.
git ls-files --exclude-standard -co
```

### get_latest_commit_hash
```bash
git log -1 --format="%H"
```

### get_changed_files_since
```bash
# Expects {{hash}} to be replaced with the target commit hash.
git diff --name-only {{hash}} HEAD
```

### store_commit_metadata
```bash
# Expects {{hash}} and {{message}} to be replaced.
git notes add -m "{{message}}" {{hash}}
```

### revert_commit
```bash
# Expects {{hash}} to be replaced.
git revert --no-edit {{hash}}
```
