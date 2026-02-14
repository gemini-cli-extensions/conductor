#requires -Version 5.1
<#
.SYNOPSIS
    Conductor Universal Installer for Windows

.DESCRIPTION
    Installs conductor-next on Windows systems using PowerShell.
    Supports both native PowerShell and WSL.

.EXAMPLE
    # One-liner install:
    irm install.cat/edithatogo/conductor-next | iex

    # Or download and run:
    .\install.ps1
#>

[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$SkipWSLCheck,
    [string]$InstallDir = "$env:USERPROFILE\.local\share\conductor-next"
)

# Configuration
$script:RepoUrl = "https://github.com/edithatogo/conductor-next.git"
$script:ConductorVersion = "0.2.0"
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

# Check if running as administrator
function Test-Administrator {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Detect Windows version
function Get-WindowsVersion {
    $os = Get-CimInstance Win32_OperatingSystem
    return @{
        Name = $os.Caption
        Version = $os.Version
        Build = $os.BuildNumber
    }
}

# Check if WSL is available
function Test-WSL {
    try {
        $wsl = Get-Command wsl -ErrorAction SilentlyContinue
        if ($wsl) {
            $wslVersion = wsl --version 2>$null
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Check if a command exists
function Test-Command($Command) {
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Install mise using PowerShell
function Install-Mise {
    Write-Info "Checking for mise..."

    if (Test-Command "mise") {
        Write-Success "mise is already installed"
        return $true
    }

    Write-Info "Installing mise..."

    try {
        # Download and install mise
        $installScript = Invoke-RestMethod -Uri "https://mise.run"
        Invoke-Expression $installScript

        # Add to PATH for current session
        $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"

        if (Test-Command "mise") {
            Write-Success "mise installed successfully"
            return $true
        }
        else {
            Write-Error "mise installation failed"
            return $false
        }
    }
    catch {
        Write-Error "Failed to install mise: $_"
        return $false
    }
}

# Clone or update repository
function Install-Repository {
    Write-Info "Setting up conductor-next repository..."

    if (Test-Path $InstallDir) {
        Write-Info "Repository already exists at $InstallDir, updating..."
        Push-Location $InstallDir
        try {
            git pull origin main 2>$null || git pull origin master 2>$null
        }
        catch {
            Write-Warning "Could not update repository: $_"
        }
        Pop-Location
    }
    else {
        Write-Info "Cloning repository to $InstallDir..."
        $parentDir = Split-Path -Parent $InstallDir
        if (!(Test-Path $parentDir)) {
            New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        }

        git clone --depth 1 $script:RepoUrl $InstallDir
    }

    Write-Success "Repository ready at $InstallDir"
    return $true
}

# Setup mise environment
function Setup-MiseEnvironment {
    Write-Info "Setting up mise environment..."

    Push-Location $InstallDir
    try {
        # Install tools
        mise install
        Write-Success "mise environment ready"
    }
    catch {
        Write-Error "Failed to setup mise environment: $_"
        Pop-Location
        return $false
    }
    Pop-Location

    return $true
}

# Install components using Python installer
function Install-Components {
    Write-Info "Installing conductor components..."

    Push-Location $InstallDir
    try {
        if (Test-Path "scripts\conductor_install.py") {
            python scripts\conductor_install.py --all
        }
        else {
            Write-Warning "conductor_install.py not found, using mise tasks..."
            mise run install-all
        }

        Write-Success "Components installed"
    }
    catch {
        Write-Error "Failed to install components: $_"
        Pop-Location
        return $false
    }
    Pop-Location

    return $true
}

# Setup PowerShell profile
function Setup-PowerShellProfile {
    Write-Info "Setting up PowerShell profile..."

    $profileDir = Split-Path -Parent $PROFILE
    if (!(Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    if (!(Test-Path $PROFILE)) {
        New-Item -ItemType File -Path $PROFILE -Force | Out-Null
    }

    # Add mise activation if not present
    $miseLine = 'if (Get-Command mise -ErrorAction SilentlyContinue) { mise activate pwsh | Out-String | Invoke-Expression }'
    $profileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue

    if ($profileContent -notmatch "mise activate") {
        Add-Content -Path $PROFILE -Value "`n# Conductor-next (mise)`n$miseLine"
        Write-Success "Added mise activation to PowerShell profile"
    }

    # Add conductor to PATH
    $pathLine = "`$env:PATH = `'$InstallDir\scripts;`' + `$env:PATH"
    if ($profileContent -notmatch [regex]::Escape($InstallDir)) {
        Add-Content -Path $PROFILE -Value "`n# Conductor-next`n$pathLine"
        Write-Success "Added conductor scripts to PATH"
    }

    return $true
}

# Install using WSL as fallback
function Install-UsingWSL {
    Write-Info "Attempting installation via WSL..."

    if (!(Test-WSL)) {
        Write-Error "WSL is not available. Please install WSL or use manual installation."
        return $false
    }

    Write-Info "WSL detected, running Linux installer..."

    # Download and run the shell script in WSL
    $wslCommand = @"
curl -fsSL install.cat/edithatogo/conductor-next | bash
"@

    try {
        wsl bash -c $wslCommand
        Write-Success "Installation via WSL completed"
        Write-Info "Note: Conductor is installed in WSL. Use 'wsl' to access it."
        return $true
    }
    catch {
        Write-Error "WSL installation failed: $_"
        return $false
    }
}

# Print installation summary
function Show-Summary {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Installation Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "✓ mise installed and configured" -ForegroundColor Green
    Write-Host "✓ conductor-next installed to $InstallDir" -ForegroundColor Green
    Write-Host "✓ All components installed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Restart PowerShell or run: . `$PROFILE`"
    Write-Host "  2. Run 'mise doctor' to verify installation"
    Write-Host "  3. Run 'mise run verify' to verify conductor components"
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  mise run sync-upstream    # Sync with upstream repos"
    Write-Host "  mise run update-all       # Check for updates"
    Write-Host "  mise run verify           # Verify installation"
    Write-Host ""
    Write-Host "Documentation:" -ForegroundColor Cyan
    Write-Host "  $InstallDir\README.md"
    Write-Host ""
    Write-Success "Enjoy using conductor-next!"
}

# Main installation flow
function Main {
    Write-Host ""
    Write-Host "🚀 Conductor Universal Installer for Windows" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    $windowsVersion = Get-WindowsVersion
    Write-Info "Detected Windows: $($windowsVersion.Name) ($($windowsVersion.Build))"

    # Check prerequisites
    if (!(Test-Command "git")) {
        Write-Error "git is required but not installed. Please install Git for Windows."
        exit 1
    }

    # Check if we should use WSL
    if ((Test-WSL) -and !$SkipWSLCheck) {
        $useWSL = Read-Host "WSL is available. Install via WSL for better compatibility? (Y/n)"
        if ($useWSL -eq '' -or $useWSL -eq 'Y' -or $useWSL -eq 'y') {
            if (Install-UsingWSL) {
                Show-Summary
                exit 0
            }
            else {
                Write-Warning "WSL installation failed, trying native PowerShell..."
            }
        }
    }

    # Run native PowerShell installation
    Write-Info "Installing via PowerShell..."

    # Install mise
    if (!(Install-Mise)) {
        Write-Error "Failed to install mise"
        exit 1
    }

    # Clone repository
    if (!(Install-Repository)) {
        Write-Error "Failed to setup repository"
        exit 1
    }

    # Setup mise environment
    if (!(Setup-MiseEnvironment)) {
        Write-Error "Failed to setup mise environment"
        exit 1
    }

    # Install components
    if (!(Install-Components)) {
        Write-Error "Failed to install components"
        exit 1
    }

    # Setup PowerShell profile
    Setup-PowerShellProfile

    # Show summary
    Show-Summary
}

# Run main function
Main
