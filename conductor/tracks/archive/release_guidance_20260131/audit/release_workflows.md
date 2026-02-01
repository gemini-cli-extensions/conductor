# Release Workflow Audit

## Existing Workflows

- `.github/workflows/release-please.yml`
  - Uses `release-please` to create GitHub releases and upload `conductor-release.tar.gz`.
  - Packages the repository and uploads assets on release creation.

- `.github/workflows/package-and-upload-assets.yml`
  - Packages VSIX via `npx vsce package`.
  - Archives repo into `conductor-release.tar.gz`.
  - Uploads `conductor.vsix` and tarball to the release.

## Build Scripts

- `scripts/build_vsix.sh` and `scripts/build_vsix.ps1` package VSIX using `npx vsce package`.

## Notes

- GitHub Releases are already the canonical distribution point (README references Releases).
- Python/PowerShell scripts are the primary local automation path; Node tooling is used only for VSIX packaging.
