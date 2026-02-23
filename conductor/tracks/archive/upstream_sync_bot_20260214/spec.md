# Track Specification: Upstream Sync Bot & Issue Triage

## Summary

Create an automated recurring workflow that synchronizes from upstream repositories, analyzes GitHub issues, creates conductor tracks for applicable issues, and manages the repository rename from "conductor" to "conductor-next". This bot will ensure the fork stays current with upstream while systematically addressing community issues.

## Goals

- Automated daily sync from upstream repositories (gemini-cli-extensions/conductor and jnorthrup/conductor2)
- Intelligent GitHub issue analysis and triage
- Automatic conductor track creation for applicable upstream issues
- Repository rename coordination (conductor → conductor-next)
- Reduced manual overhead for maintaining fork synchronization

## Upstream Sources

1. **gemini-cli-extensions/conductor** - Primary upstream repository
2. **jnorthrup/conductor2** - Secondary upstream with enhancements

## Key Issues to Address (from 48 analyzed, 12 relevant)

| Issue | Description | Priority |
|-------|-------------|----------|
| #113 | Auto-create .gitignore on git init | High |
| #112 | Update workflow with overwrite confirmation | High |
| #108 | Fix TOML references | Medium |
| #105 | AskUser tool integration | High |
| #103 | Auto-update metadata.json timestamps | Medium |
| #97 | Single commit option | Medium |
| #96 | Separate metadata/output commits | Low |
| #115 | Multi-agent support | High |

## Key Deliverables

- `scripts/sync_upstream.py` - Sync from both upstream repos with merge conflict handling
- `scripts/triage_issues.py` - Analyze GitHub issues and create conductor tracks
- `scripts/rename_repo.py` - Coordinate repository rename and URL updates
- `.github/workflows/sync-upstream.yml` - Daily automated sync via GitHub Actions
- `.github/ISSUE_TEMPLATE/` - Issue templates for consistent reporting
- `docs/UPSTREAM_SYNC.md` - Documentation for sync process and bot usage
- `docs/REPO_RENAME.md` - Guide for repository rename transition

## Repository Rename Details

- **From:** `edithatogo/conductor`
- **To:** `edithatogo/conductor-next`
- **Impact Areas:**
  - Git remotes in all clones
  - Documentation references
  - Install scripts and URLs
  - GitHub Actions workflows
  - Package metadata

## Acceptance Criteria

- [ ] `scripts/sync_upstream.py` successfully syncs from both upstream repos
- [ ] Sync script handles merge conflicts and creates PRs for manual review
- [ ] `scripts/triage_issues.py` analyzes issues and creates appropriate tracks
- [ ] GitHub Actions workflow runs daily and reports status
- [ ] High-priority issues (#113, #112, #105, #115) have corresponding tracks
- [ ] Repository rename documented with migration guide
- [ ] All documentation updated to reflect new repository name
- [ ] GitHub issue templates created for bug reports and feature requests
- [ ] Bot provides clear reports on sync status and created tracks

## Non-Goals

- Automatic merging of upstream changes without review
- Deletion of existing issues or tracks
- Support for repositories other than the two specified upstreams
- Real-time sync (daily is sufficient)

## References

- Previous track: [upstream_sync_20260131](../archive/upstream_sync_20260131/)
- Upstream repos:
  - <https://github.com/gemini-cli-extensions/conductor>
  - <https://github.com/jnorthrup/conductor2>
