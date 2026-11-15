$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  throw 'Docker is not installed. Install Docker Desktop, restart Windows, and run this script again.'
}

docker info *> $null
if ($LASTEXITCODE -ne 0) {
  throw 'Docker Desktop is installed but not running. Start Docker Desktop and run this script again.'
}

if (-not (Test-Path '.env')) {
  Copy-Item '.env.example' '.env'
  $secret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 48 | ForEach-Object {[char]$_})
  $content = Get-Content '.env' -Raw
  $content = $content -replace '(?m)^JWT_SECRET=.*$', "JWT_SECRET=$secret"
  Set-Content '.env' $content -NoNewline
}

Write-Host 'Building and starting SoilWise AI. First run downloads required images and packages...' -ForegroundColor Cyan
docker compose up --build
