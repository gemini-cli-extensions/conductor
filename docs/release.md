# Release Packaging Guide

This repository publishes releases via **GitHub Releases**. That is the canonical distribution point for the VSIX and bundled artifacts.

## Recommended Release Flow

1. Ensure artifacts are current:
   ```bash
   python scripts/sync_skills.py
   python scripts/validate_artifacts.py --require-vsix
   ```
2. Build the VSIX (if not already built):
   ```bash
   ./scripts/build_vsix.sh
   # or on Windows:
   ./scripts/build_vsix.ps1
   ```
3. Create a GitHub Release:
   - Use the existing release automation (`release-please`) or create a tag manually.
   - The workflows will upload `conductor.vsix` and `conductor-release.tar.gz` to the release.

## Automation References

- `.github/workflows/release-please.yml` (creates release + uploads assets)
- `.github/workflows/package-and-upload-assets.yml` (packages VSIX + tarball)

## Tooling Note: npx vs Python/PowerShell

Python/PowerShell remains the primary local automation path.
Node tooling (`npx vsce package`) is used only for VSIX packaging. A Node‑based CLI
wrapper could be added later, but it is not required for releases.
