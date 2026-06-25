#Requires -Version 5.1
<#
.SYNOPSIS
    Build the portable Transcriber.exe with PyInstaller.

.DESCRIPTION
    Installs the optional build dependencies (`uv sync --extra build`) and runs
    PyInstaller against Transcriber.spec, producing dist\Transcriber.exe. Bundles
    assets only — never secrets or user data.

.PARAMETER Clean
    Remove the build\ and dist\ output folders before building.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/build_exe.ps1 -Clean
#>
[CmdletBinding()]
param(
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-Step { param([string]$Message) Write-Host "==> $Message" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Message) Write-Host "[ ok ] $Message" -ForegroundColor Green }

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if ($Clean) {
    foreach ($dir in @('build', 'dist')) {
        if (Test-Path $dir) {
            Write-Step "Removing $dir"
            Remove-Item -Recurse -Force -Path $dir
        }
    }
}

Write-Step "Installing build dependencies (uv sync --extra build)"
uv sync --extra build

Write-Step "Building Transcriber.exe (PyInstaller)"
uv run pyinstaller Transcriber.spec --noconfirm

$exe = Join-Path $root 'dist\Transcriber.exe'
if (Test-Path $exe) {
    Write-Ok "Built $exe"
}
else {
    throw "Build finished but $exe was not found."
}
