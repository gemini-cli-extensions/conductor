# Repository Rename Migration Guide

**Date:** 2026-02-23

**Old Repository:** `edithatogo/conductor`
**New Repository:** `edithatogo/conductor-next`

## Why the Rename?

The repository has been renamed to `conductor-next` to better reflect its next-generation features and architecture.

## For Users

### Update Your Installation

#### If installed via pip:
```bash
# Uninstall old version
pip uninstall conductor

# Install new version
pip install conductor-next
```

#### If installed via npm:
```bash
# Uninstall old version
npm uninstall -g conductor

# Install new version
npm install -g conductor-next
```

#### If using npx:
```bash
# Just use the new name - no installation needed
npx conductor-next <command>
```

### Update Git Remotes

If you have a local clone of the repository:

```bash
cd path/to/your/clone

# Update remote URL
git remote set-url origin https://github.com/edithatogo/conductor-next.git

# Verify the change
git remote -v

# Pull latest changes
git pull origin main
```

Or if you use SSH:

```bash
git remote set-url origin git@github.com:edithatogo/conductor-next.git
```

### Update Bookmarks and Links

Update any bookmarks or documentation links:

**Old:** `https://github.com/edithatogo/conductor`
**New:** `https://github.com/edithatogo/conductor-next`

## For Developers

### Update Import Statements

If you import from this package in your code:

```python
# Old
from conductor import something

# New
from conductor-next import something
```

### Update Dependencies

Update your `requirements.txt`, `setup.py`, `pyproject.toml`, or `package.json`:

```diff
- conductor>=1.0.0
+ conductor-next>=1.0.0
```

### Update CI/CD Pipelines

Update any CI/CD configuration that references the old repository:

```yaml
# GitHub Actions
- uses: edithatogo/conductor@v1
+ uses: edithatogo/conductor-next@v1
```

## Common Issues

### Issue: "Module not found" after update

**Solution:** Make sure you've uninstalled the old package and cleared any cached imports:

```bash
pip uninstall conductor
pip cache purge  # For pip
python -c "import sys; print(sys.path)"  # Check for old installations
```

### Issue: Git remote still points to old repository

**Solution:** Verify and update your remote:

```bash
git remote -v
git remote set-url origin https://github.com/edithatogo/conductor-next.git
```

### Issue: Old bookmarks still work

**Note:** GitHub will redirect old URLs to the new repository, but it's best to update your bookmarks to use the new URL directly.

## Timeline

- **Announcement Date:** 2026-02-23
- **Redirect Period:** Indefinite (GitHub provides automatic redirects)
- **Old Package Deprecation:** Immediate

## Questions?

If you encounter any issues during migration, please open an issue at:
https://github.com/edithatogo/conductor-next/issues

---
*Generated automatically by the Repository Rename Coordinator*
