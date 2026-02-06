# Roadmap: Marketplace Deployment

This document outlines the steps required to publish the Conductor VS Code Extension to public registries.

## 1. Prerequisites

### VS Code Marketplace (Visual Studio Marketplace)
- **Publisher Account:** Register at [marketplace.visualstudio.com](https://marketplace.visualstudio.com/).
- **Personal Access Token (PAT):** Create a PAT in Azure DevOps with "Marketplace (Publish)" scope.
- **`vsce` CLI:** Installed via `npm install -g @vscode/vsce`.

### OpenVSX Registry
- **Account:** Register at [open-vsx.org](https://open-vsx.org/).
- **Access Token:** Generate a token in your OpenVSX profile.
- **`ovsx` CLI:** Installed via `npm install -g ovsx`.

## 2. Release Workflow

### Step 1: Versioning
Ensure `package.json` version follows semantic versioning (SemVer).
```bash
# Example: Bump to a new minor version
npm version minor
```

### Step 2: Build & Package
Use the established build script to generate the `.vsix`.
```bash
./scripts/build_vsix.ps1
```

### Step 3: Publish to VS Code Marketplace
```bash
# Login (first time only)
vsce login <publisher-name>

# Publish
vsce publish
```

### Step 4: Publish to OpenVSX Registry
```bash
# Publish using the token
ovsx publish conductor.vsix -p <open-vsx-token>
```

## 3. Automation Plan (GitHub Actions)

We should implement a GitHub Action to automate this process on every tagged release.

- **Trigger:** `on: push: tags: ['v*']`
- **Steps:**
    1. Checkout code.
    2. Setup Node.js.
    3. Install dependencies.
    4. Run `npm run compile`.
    5. Build VSIX.
    6. Publish to VS Code Marketplace (using `VSCE_PAT` secret).
    7. Publish to OpenVSX (using `OVSX_TOKEN` secret).

## 4. Quality Gates for Release
- [ ] All unit and contract tests pass.
- [ ] Smoke test passes on built VSIX.
- [ ] `CHANGELOG.md` updated with new version details.
- [ ] Documentation (`README.md`, `SKILL.md`) aligned with features.
