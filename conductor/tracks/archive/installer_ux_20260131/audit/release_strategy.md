# Release Strategy & Versioning Guidance

## Release Channels

- **Primary:** GitHub Releases (VSIX + PyPI + tarball)
- **Secondary:** PyPI for `conductor-core`
- **Deferred:** npm package for installer wrapper (revisit after installer parity stabilizes)

## Versioning

- Use `release-please` as the canonical version source.
- Keep `conductor-core` version aligned with repository release tags.
- Bump VSIX version as part of the release pipeline (no manual edits).

## Required Release Assets

- `conductor.vsix`
- `conductor-core/dist/*.whl`
- `conductor-core/dist/*.tar.gz`
- `conductor-release.tar.gz`

## Publishing Flow

1. Merge to `main` and allow `release-please` to open a release PR.
2. Merge release PR to cut tag.
3. GitHub Actions publishes artifacts and PyPI package on tag.
4. Verify VSIX installation and Antigravity workflows using `scripts/install_local.py --verify`.
