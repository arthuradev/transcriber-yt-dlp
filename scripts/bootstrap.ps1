#Requires -Version 5.1
<#
.SYNOPSIS
    Set up Transcriber for development on Windows.

.DESCRIPTION
    Checks prerequisites (uv, ffmpeg, GPU/CUDA), installs Python dependencies via
    `uv sync`, and creates a local .env from .env.example. The script is safe: it
    performs no destructive actions and never installs software silently — it
    prints the exact winget command for anything missing.

.PARAMETER Run
    After a successful bootstrap, launch the app (`uv run transcriber`).

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
#>
[CmdletBinding()]
param(
    [switch]$Run
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Test-CommandExists {
    param([Parameter(Mandatory)][string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Write-Step { param([string]$Message) Write-Host "==> $Message" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Message) Write-Host "[ ok ] $Message" -ForegroundColor Green }
function Write-Warn { param([string]$Message) Write-Host "[warn] $Message" -ForegroundColor Yellow }

# Repository root is the parent of this scripts/ folder.
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Step "Checking uv"
if (-not (Test-CommandExists 'uv')) {
    Write-Warn "uv was not found. Install it, then re-run this script:"
    Write-Warn "    winget install --id=astral-sh.uv -e"
    Write-Warn "    (or see https://docs.astral.sh/uv/ )"
    exit 1
}
Write-Ok "uv found"

Write-Step "Installing dependencies (uv sync)"
uv sync
Write-Ok "Dependencies installed (Python 3.12 is provisioned by uv)"

Write-Step "Checking ffmpeg"
if (Test-CommandExists 'ffmpeg') {
    Write-Ok "ffmpeg found"
}
else {
    Write-Warn "ffmpeg not found. Audio extraction and some merges need it:"
    Write-Warn "    winget install --id=Gyan.FFmpeg -e"
}

Write-Step "Checking GPU / CUDA (transcription is GPU-only)"
if (Test-CommandExists 'nvidia-smi') {
    Write-Ok "NVIDIA GPU detected. Enable transcription with the optional extra:"
    Write-Ok "    uv sync --extra transcription"
}
else {
    Write-Warn "No NVIDIA GPU detected. Transcription will be unavailable (no CPU fallback)."
}

Write-Step "Checking .env"
$envExample = Join-Path $root '.env.example'
$envFile = Join-Path $root '.env'
if (Test-Path $envFile) {
    Write-Ok ".env already exists"
}
elseif (Test-Path $envExample) {
    Copy-Item -Path $envExample -Destination $envFile
    Write-Ok "Created .env from .env.example (fill in your API keys)"
}
else {
    Write-Warn ".env.example not found; skipping .env creation"
}

Write-Ok "Bootstrap complete."
Write-Host "Run the app with:  uv run transcriber" -ForegroundColor Cyan

if ($Run) {
    Write-Step "Starting Transcriber"
    uv run transcriber
}
