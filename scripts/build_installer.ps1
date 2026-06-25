#Requires -Version 5.1
<#
.SYNOPSIS
    Build the Transcriber installer with Inno Setup.

.DESCRIPTION
    Requires dist\Transcriber.exe (run scripts\build_exe.ps1 first) and Inno
    Setup's compiler (ISCC). If ISCC is missing, prints the winget command and
    exits. Produces dist\Transcriber-Setup-<version>.exe.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/build_installer.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-Step { param([string]$Message) Write-Host "==> $Message" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Message) Write-Host "[ ok ] $Message" -ForegroundColor Green }
function Write-Warn { param([string]$Message) Write-Host "[warn] $Message" -ForegroundColor Yellow }

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path 'dist\Transcriber.exe')) {
    Write-Warn "dist\Transcriber.exe not found. Build it first:"
    Write-Warn "    powershell -ExecutionPolicy Bypass -File scripts/build_exe.ps1"
    exit 1
}

$iscc = Get-Command 'ISCC' -ErrorAction SilentlyContinue
if ($null -eq $iscc) {
    Write-Warn "Inno Setup compiler (ISCC) not found. Install it, then re-run:"
    Write-Warn "    winget install --id=JRSoftware.InnoSetup -e"
    exit 1
}

Write-Step "Building installer (ISCC)"
& $iscc.Source 'scripts\installer.iss'
Write-Ok "Installer built in dist\"
