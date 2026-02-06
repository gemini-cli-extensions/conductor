param(
  [switch]$Verify,
  [switch]$DryRun,
  [switch]$PrintLocations,
  [switch]$RepoOnly,
  [switch]$InstallVsix,
  [switch]$SyncWorkflows,
  [switch]$SyncSkills,
  [switch]$SyncCopilot
)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptRoot "..")
$python = Join-Path $env:USERPROFILE "AppData\Local\miniconda3\python.exe"
if (-not (Test-Path $python)) {
  $python = "python"
}

$argsList = @()
if ($Verify) { $argsList += "--verify" }
if ($DryRun) { $argsList += "--dry-run" }
if ($PrintLocations) { $argsList += "--print-locations" }
if ($RepoOnly) { $argsList += "--repo-only" }
if ($InstallVsix) { $argsList += "--install-vsix" }
if ($SyncWorkflows) { $argsList += "--sync-workflows" }
if ($SyncSkills) { $argsList += "--sync-skills" }
if ($SyncCopilot) { $argsList += "--sync-copilot" }

& $python (Join-Path $repoRoot "scripts\install_local.py") @argsList
exit $LASTEXITCODE