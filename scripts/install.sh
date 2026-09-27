#!/bin/bash
# Run from the uploaded project directory on kc_server.
set -euo pipefail
cd -- "$(dirname -- "$0")/.."
command -v docker >/dev/null || { echo 'Docker is required; inspect the host before installing it.' >&2; exit 1; }
docker compose version >/dev/null
if [[ "${1:-}" == '--stable' ]]; then
    [[ -f .env && -s cloudflare-tunnel.token ]] || { echo '.env and cloudflare-tunnel.token are required.' >&2; exit 1; }
    grep -Eq '^PUBLIC_BASE_URL=https://[^[:space:]]+' .env || { echo 'PUBLIC_BASE_URL must be set in .env.' >&2; exit 1; }
    docker compose -f compose.yaml -f compose.stable.yaml up -d --build
else
    docker compose up -d --build
fi
docker compose ps
echo 'Read the connection URL with: docker compose exec -T runtime cat /state/connection-url.txt'
echo 'Read the owner token privately in your terminal; never paste it in chat.'
