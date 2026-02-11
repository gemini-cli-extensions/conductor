# How to contribute

We'd love to accept your patches and contributions to this project.

## Before you begin

### Sign our Contributor License Agreement

Contributions to this project must be accompanied by a
[Contributor License Agreement](https://cla.developers.google.com/about) (CLA).
You (or your employer) retain the copyright to your contribution; this simply
gives us permission to use and redistribute your contributions as part of the
project.

If you or your current employer have already signed the Google CLA (even if it
was for a different project), you probably don't need to do it again.

Visit <https://cla.developers.google.com/> to see your current agreements or to
sign a new one.

### Review our community guidelines

This project follows
[Google's Open Source Community Guidelines](https://opensource.google/conduct/).

## Contribution process

### Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

### Elite Code Quality Standards

This project enforces the "Elite Code Quality" standard to ensure maximum reliability and maintainability.

#### 1. 100% Code Coverage
- All code in `conductor-core` MUST have 100% unit test coverage.
- All adapter code (e.g., `conductor-gemini`) MUST maintain at least 99% coverage.
- Use `# pragma: no cover` sparingly and ONLY with a comment explaining why (e.g., OS-specific branches).

#### 2. Strict Static Typing
- All Python code MUST pass `mypy --strict`.
- `mypy` is used for strict type checking and must pass.

#### 3. Linting and Formatting
- We use `ruff` for both linting and formatting.
- The `ruff.toml` defines the project's rule set (based on `ALL`).

#### 4. Pre-commit Hooks
- You MUST install and use `pre-commit` hooks locally.
- Run `pre-commit install` after cloning the repository.
- Commits that fail pre-commit checks will be blocked.
