# Release Notes Draft

## Highlights
- Context hygiene tooling and documentation (context bundle rules + report script).
- Setup/NewTrack UX guide with canonical messaging and troubleshooting.
- Release packaging guide clarifying GitHub Releases as the distribution source.

## Added
- Context report tooling: `scripts/context_report.py`.
- Context hygiene guide: `docs/context-hygiene.md`.
- Setup/NewTrack UX guide: `docs/setup-newtrack.md`.
- Release packaging guide: `docs/release.md`.

## Changed
- Optional Git helpers and VCS capability gating for opt-in workflows.
- Artifact validation and workflow sync refinement.

## Fixed
- Cross‑platform installer location validation tests (Windows/POSIX).

## Packaging
- `conductor.vsix`
- `conductor-release.tar.gz`

## Validation
- `python scripts/validate_artifacts.py`
- `python -m pytest`
