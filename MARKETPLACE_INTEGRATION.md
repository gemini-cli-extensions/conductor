# Marketplace Integration Guide

This document outlines the process for publishing Conductor to various marketplaces and package managers.

## Current Status

✅ **mise Integration**: Complete - Available via `mise install edithatogo/conductor-next`
✅ **install.cat Integration**: Complete - Available via `curl install.cat/edithatogo/conductor-next | sh`
✅ **Smithery Manifest**: Complete - Ready for Smithery publication
✅ **PyPI Preparation**: Complete - setup.cfg ready for publication
✅ **npm Preparation**: Complete - package.json ready for publication
✅ **Homebrew Preparation**: Complete - Formula template ready
✅ **Chocolatey Preparation**: Complete - .nuspec and install script ready
✅ **Scoop Preparation**: Complete - Manifest ready

## Publication Steps

### 1. Smithery Publication

To publish to Smithery:

```bash
# 1. Install Smithery CLI
npm install -g @smithery/cli

# 2. Login to Smithery
smithery login

# 3. Validate your manifest
smithery validate

# 4. Publish
smithery publish
```

### 2. PyPI Publication

To publish to PyPI:

```bash
# 1. Install build tools
pip install build twine

# 2. Build the package
python -m build

# 3. Test upload to test PyPI first
twine upload --repository testpypi dist/*

# 4. Upload to PyPI
twine upload dist/*
```

### 3. npm Publication

To publish to npm:

```bash
# 1. Login to npm
npm login

# 2. Publish
npm publish --access public
```

### 4. Homebrew Formula

To submit to Homebrew:

1. Fork <https://github.com/Homebrew/homebrew-core>
2. Create formula in `Formula/conductor.rb`:

```ruby
class Conductor < Formula
  desc "Context-Driven Development tool for AI-assisted workflows"
  homepage "https://github.com/edithatogo/conductor-next"
  url "https://github.com/edithatogo/conductor-next/archive/v0.2.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"
  license "MIT"

  depends_on "python@3.9"
  depends_on "node"
  depends_on "git"

  def install
    # Install core components
    system "pip3", "install", *std_pip_args.add_test_deps.add_development_deps, buildpath
  end

  test do
    system "#{bin}/conductor", "--version"
  end
end
```

3. Run audit: `brew audit --new-formula Formula/conductor.rb`
4. Submit pull request

### 5. Chocolatey Package

To publish to Chocolatey:

1. Build the package:

```powershell
choco pack chocolatey/conductor.nuspec
```

2. Test locally:

```powershell
choco install conductor -s . -fdv
```

3. Push to Chocolatey:

```powershell
choco apikey -k YOUR_API_KEY -source https://push.chocolatey.org/
choco push conductor.0.2.0.nupkg -s https://push.chocolatey.org/
```

### 6. Scoop Bucket

To add to Scoop:

1. Fork <https://github.com/ScoopInstaller/Main>
2. Add manifest to `/bucket/conductor.json`
3. Submit pull request

Or create a personal bucket:

```bash
# Create your bucket
mkdir -p ~/scoop-buckets/conductor/bucket
cp scoop/conductor.json ~/scoop-buckets/conductor/bucket/
```

Users can then add your bucket:

```bash
scoop bucket add conductor https://github.com/YOUR_USERNAME/scoop-buckets
scoop install conductor
```

## Automation Scripts

### Marketplace Publication Script

```bash
#!/bin/bash
# publish_to_marketplaces.sh

set -e

VERSION="0.2.0"

echo "Publishing Conductor v$VERSION to marketplaces..."

# Build artifacts
echo "Building release artifacts..."
mkdir -p dist/
tar -czf "dist/conductor-$VERSION.tar.gz" --exclude=".*" --exclude="dist" --exclude="*.egg-info" .

# Calculate checksums
SHA256=$(shasum -a 256 "dist/conductor-$VERSION.tar.gz" | cut -d' ' -f1)
echo "SHA256: $SHA256"

# Update manifests with actual checksums
sed -i.bak "s/TODO_REPLACE_WITH_ACTUAL_SHA256/$SHA256/g" HOMEBREW.md
sed -i.bak "s/TODO_REPLACE_WITH_ACTUAL_HASH/$SHA256/g" scoop/conductor.json

echo "Marketplace manifests updated with correct checksums."

# Instructions for publishing
echo ""
echo "Next steps:"
echo "1. Upload dist/conductor-$VERSION.tar.gz to GitHub Releases"
echo "2. Update Homebrew formula with correct SHA256"
echo "3. Follow publication steps for each marketplace"
```

## Verification Checklist

Before publishing to each marketplace, verify:

- [ ] Version number is correct
- [ ] Dependencies are properly declared
- [ ] Installation works on clean systems
- [ ] All required files are included
- [ ] License information is correct
- [ ] Homepage and repository URLs are valid
- [ ] Descriptions are accurate and compelling
- [ ] Installation instructions are tested

## Maintenance

- Update version numbers in all manifests when releasing new versions
- Monitor marketplace feedback and issues
- Keep dependencies up-to-date
- Test installations regularly across platforms
- Update documentation as needed

## Benefits of Multi-Marketplace Presence

1. **Broader Reach**: Available to users of different package managers
2. **Easier Discovery**: Findable through familiar channels
3. **Reduced Friction**: No need to learn new installation methods
4. **Professional Appearance**: Listed alongside other professional tools
5. **Community Trust**: Following established distribution patterns
