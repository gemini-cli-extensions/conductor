# VCS Workflow Definition: Git

This file defines the specific shell commands and their expected behaviors for Conductor to use when operating within a Git repository. Each command includes details about its execution, expected successful exit codes, and structured error handlers for common failure scenarios.

---

## Command Definitions

### initialize_repository
# Purpose: Initializes a new, empty Git repository in the current directory.
command: git init
success_code: 0
error_handlers:
  - exit_code: 128
    stderr_contains: "already exists and is not an empty directory"
    agent_action: "A Git repository already exists here. Conductor will proceed, but no new repository was initialized."

### get_repository_status
# Purpose: Checks the status of the working tree to detect uncommitted changes.
# Expected Output: A list of modified/untracked files (one per line). Empty if clean.
command: git status --porcelain
success_code: 0
error_handlers: []

### list_relevant_files
# Purpose: Lists all files tracked by Git, plus any other non-ignored files.
# Expected Output: A list of file paths (one per line).
command: git ls-files --exclude-standard -co
success_code: 0
error_handlers: []

### get_latest_commit_hash
# Purpose: Retrieves the full SHA hash of the most recent commit (HEAD).
# Expected Output: A single 40-character commit SHA.
command: git log -1 --format="%H"
success_code: 0
error_handlers:
  - exit_code: 128
    stderr_contains: "does not have any commits yet"
    agent_action: "The repository has no commits yet. Unable to retrieve a hash."

### get_changed_files_since
# Purpose: Lists all files that have been changed between a specified commit and HEAD.
# Placeholders:
#   - {{hash}}: The starting commit hash to compare against.
# Expected Output: A list of file paths that have changed (one per line).
command: git diff --name-only {{hash}} HEAD
success_code: 0
error_handlers:
  - exit_code: 128
    stderr_contains: "bad object"
    agent_action: "The provided hash '{{hash}}' is not a valid Git object."

### store_commit_metadata
# Purpose: Appends a JSON object containing metadata about a commit to the project's metadata log.
# Placeholders:
#   - {{hash}}: The hash of the commit to log.
#   - {{message}}: The detailed summary/message to associate with the commit.
command: echo "{\"hash\": \"{{hash}}\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"message\": \"{{message}}\"}" >> conductor/metadata.json
success_code: 0
error_handlers:
  - exit_code: "*" # Catch any non-zero exit code
    agent_action: "Failed to write metadata to conductor/metadata.json. This might indicate a permissions issue or file system problem."

### get_commit_metadata
# Purpose: Searches the metadata log and retrieves the full JSON line for a specific commit hash.
# Placeholders:
#   - {{hash}}: The commit hash to search for.
# Expected Output: The full JSON string corresponding to the commit if found, otherwise empty.
command: grep ""hash": "{{hash}}"" conductor/metadata.json
success_code: 0
error_handlers:
  - exit_code: 1 # grep returns 1 if no lines were selected
    agent_action: "No metadata found for commit hash '{{hash}}' in conductor/metadata.json."

### revert_commit
# Purpose: Creates a new commit that reverts the changes from a specified commit.
# Placeholders:
#   - {{hash}}: The hash of the commit to revert.
command: git revert --no-edit {{hash}}
success_code: 0
error_handlers:
  - exit_code: 1
    stderr_contains: "could not revert"
    agent_action: "A merge conflict occurred while reverting commit '{{hash}}'. The revert has been initiated, but you must now resolve the conflicts manually. Once resolved, use 'git commit' to finalize the revert process."
  - exit_code: 128
    stderr_contains: "unknown revision"
    agent_action: "The commit hash '{{hash}}' was not found in the repository history. The revert could not be started."
  - exit_code: 128
    stderr_contains: "is a merge but no -m option was given"
    agent_action: "The commit '{{hash}}' is a merge commit. Conductor cannot automatically revert merge commits. Please revert it manually specifying a parent number (e.g., 'git revert -m 1 {{hash}}')."

### get_commit_history_for_file
# Purpose: Retrieves the commit history for a specific file.
# Placeholders:
#   - {{file}}: The path to the file to get the history for.
# Expected Output: The standard `git log` output for the specified file.
command: git log -- {{file}}
success_code: 0
error_handlers:
  - exit_code: 128
    stderr_contains: "ambiguous argument"
    agent_action: "The file path '{{file}}' is ambiguous or does not exist."

### search_commit_history
# Purpose: Searches the entire commit history for commits whose messages match a specific pattern.
# Placeholders:
#   - {{pattern}}: The regex pattern to search for in commit messages.
# Expected Output: The standard `git log` output for any matching commits.
command: git log --grep="{{pattern}}"
success_code: 0
error_handlers: []
