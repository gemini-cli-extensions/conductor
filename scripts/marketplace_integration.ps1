<#
.SYNOPSIS
    Conductor Marketplace Integration Script
    This script demonstrates how to publish Conductor to various marketplaces
#>

[CmdletBinding()]
param()

# Configuration
$script:ErrorActionPreference = "Stop"

# Colors for PowerShell
function Write-Info($Message) {
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success($Message) {
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning($Message) {
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error($Message) {
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if command exists
function Test-Command($Command) {
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Prepare release artifacts
function Prepare-Release {
    Write-Info "Preparing release artifacts..."

    # Create distribution directory
    if (!(Test-Path "dist")) {
        New-Item -ItemType Directory -Path "dist" -Force | Out-Null
    }

    # Build core components
    if (Test-Path "conductor-core") {
        Write-Info "Building conductor-core..."
        try {
            Push-Location "conductor-core"
            if (Test-Command "python") {
                python -m build --outdir ../dist 2>$null
            }
            Pop-Location
        }
        catch {
            Write-Warning "Build skipped for conductor-core: $_"
        }
    }

    # Build VS Code extension
    if (Test-Path "conductor-vscode") {
        Write-Info "Building VS Code extension..."
        try {
            Push-Location "conductor-vscode"
            if (Test-Command "npm") {
                npm run package 2>$null
                Copy-Item "*.vsix" "../dist/" -Force 2>$null
            }
            Pop-Location
        }
        catch {
            Write-Warning "VS Code build skipped: $_"
        }
    }

    Write-Success "Release artifacts prepared in dist/"
}

# Publish to Smithery (conceptual)
function Publish-To-Smithery {
    Write-Info "Preparing Smithery publication..."

    $smitheryFile = "smithery.toml"
    if (!(Test-Path $smitheryFile)) {
        Write-Warning "smithery.toml not found, creating template..."

        $smitheryContent = @"
# Smithery Manifest for Conductor
id = "conductor"
name = "Conductor"
version = "0.2.0"
description = "Context-Driven Development tool for AI-assisted workflows"
homepage = "https://github.com/edithatogo/conductor-next"
repository = "https://github.com/edithatogo/conductor-next"
license = "MIT"

[installation]
primary = "mise"
methods = ["pip", "npm"]

[installation.mise]
enabled = true
config_file = "mise.toml"

[platforms]
linux = true
macos = true
windows = true

[dependencies]
python = ">=3.9"
node = ">=18"
git = ">=2.0"

tags = [
    "ai",
    "development-tool",
    "cli",
    "automation",
    "context-driven",
    "project-management",
    "workflow"
]
"@

        Set-Content -Path $smitheryFile -Value $smitheryContent
        Write-Success "smithery.toml created"
    }

    Write-Info "To publish to Smithery:"
    Write-Host "1. Register at https://smithery.dev" -ForegroundColor Yellow
    Write-Host "2. Authenticate: smithery login" -ForegroundColor Yellow
    Write-Host "3. Publish: smithery publish" -ForegroundColor Yellow
    Write-Host "4. More info: https://smithery.dev/docs/publishing" -ForegroundColor Yellow
}

# Publish to Chocolatey (conceptual)
function Publish-To-Chocolatey {
    Write-Info "Preparing Chocolatey publication..."

    Write-Host "To publish to Chocolatey:" -ForegroundColor Yellow
    Write-Host "1. Create account at https://chocolatey.org" -ForegroundColor Yellow
    Write-Host "2. Install Chocolatey CLI: choco install chocolatey" -ForegroundColor Yellow
    Write-Host "3. Create package template with: choco new conductor" -ForegroundColor Yellow
    Write-Host "4. Modify nuspec file with proper metadata" -ForegroundColor Yellow
    Write-Host "5. Test package: choco pack && choco install conductor -s ." -ForegroundColor Yellow
    Write-Host "6. Submit package to Chocolatey Gallery" -ForegroundColor Yellow
}

# Publish to Scoop (conceptual)
function Publish-To-Scoop {
    Write-Info "Preparing Scoop publication..."

    Write-Host "To publish to Scoop:" -ForegroundColor Yellow
    Write-Host "1. Fork https://github.com/ScoopInstaller/Main or create a bucket" -ForegroundColor Yellow
    Write-Host "2. Create manifest in bucket: conductor.json" -ForegroundColor Yellow
    Write-Host "3. Submit pull request to ScoopInstaller/Main" -ForegroundColor Yellow
}

# Print summary
function Show-Summary {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Marketplace Integration Ready!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Supported marketplaces:" -ForegroundColor Cyan
    Write-Host "  1. $(if (Test-Command "mise")) { Write-Output "$([char]27)[0;32m" } else { Write-Output "$([char]27)[1;33m" })mise$([char]27)[0m - $(if (Test-Command "mise") { "✓ Already integrated" } else { "Setup required" })" -ForegroundColor White
    Write-Host "  2. Smithery - Config prepared" -ForegroundColor Yellow
    Write-Host "  3. Chocolatey - Windows package manager" -ForegroundColor Yellow
    Write-Host "  4. Scoop - Windows package manager" -ForegroundColor Yellow
    Write-Host "  5. pip - Python package manager" -ForegroundColor Yellow
    Write-Host "  6. npm - Node.js package manager" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  - Review and customize configuration files" -ForegroundColor White
    Write-Host "  - Test installations in different environments" -ForegroundColor White
    Write-Host "  - Publish to desired marketplaces" -ForegroundColor White
    Write-Host "  - Update documentation with new installation methods" -ForegroundColor White
    Write-Host ""
}

# Main function
function Main {
    Write-Host ""
    Write-Host "🚀 Conductor Marketplace Integration" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""

    Prepare-Release
    Publish-To-Smithery
    Publish-To-Chocolatey
    Publish-To-Scoop
    Show-Summary
}

Main
