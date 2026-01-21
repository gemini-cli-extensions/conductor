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
# Appends a JSON object to the metadata log.
echo "{\"hash\": \"{{hash}}\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"message\": \"{{message}}\"}" >> conductor/metadata.json
```

### revert_commit
```bash
# Expects {{hash}} to be replaced.
git revert --no-edit {{hash}}
```

### get_commit_history_for_file
```bash
# Expects {{file}} to be replaced.
git log -- {{file}}
```

### search_commit_history
```bash
# Expects {{pattern}} to be replaced.
git log --grep="{{pattern}}"
```