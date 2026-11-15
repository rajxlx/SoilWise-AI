#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo 'Docker is not installed. Install Docker Desktop (or Docker Engine + Compose plugin), then retry.' >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo 'Docker is installed but not running. Start Docker and retry.' >&2
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
  if [[ "$(uname -s)" == "Darwin" ]]; then
    sed -i '' "s|^JWT_SECRET=.*|JWT_SECRET=${SECRET}|" .env
  else
    sed -i "s|^JWT_SECRET=.*|JWT_SECRET=${SECRET}|" .env
  fi
fi

echo 'Building and starting SoilWise AI. First run downloads required images and packages...'
docker compose up --build
