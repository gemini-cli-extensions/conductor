# PowerShell script to build Conductor VS Code Extension
$ErrorActionPreference = "Stop"

Write-Host "Building Conductor VS Code Extension..."
Set-Location conductor-vscode
npm install
npx vsce package -o ../conductor.vsix
Set-Location ..
Write-Host "Build complete: conductor.vsix"
