#!/bin/bash
set -euo pipefail
umask 077
mkdir -p /state /workspace
tunnel_pid=''
server_pid=''
cleanup() {
    if [[ -n "$server_pid" ]]; then kill "$server_pid" 2>/dev/null || true; fi
    if [[ -n "$tunnel_pid" ]]; then kill "$tunnel_pid" 2>/dev/null || true; fi
}
trap cleanup EXIT
trap 'exit 0' TERM INT
origin="${PUBLIC_BASE_URL:-}"
if [[ -z "$origin" ]]; then
    cloudflared tunnel --no-autoupdate --protocol http2 --url http://127.0.0.1:8766 \
        --logfile /tmp/kc-cloudflared.log >/tmp/kc-cloudflared.stdout 2>&1 &
    tunnel_pid=$!
    for ((attempt=0; attempt<90; attempt++)); do
        origin=$(python3 -c 'import re,pathlib; p=pathlib.Path("/tmp/kc-cloudflared.log"); t=p.read_text() if p.exists() else ""; m=re.search(r"https://[a-z0-9-]+\.trycloudflare\.com",t); print(m.group(0) if m else "")')
        [[ -n "$origin" ]] && break
        kill -0 "$tunnel_pid" 2>/dev/null || { echo 'Tunnel startup failed' >&2; exit 1; }
        sleep 1
    done
    [[ -n "$origin" ]] || { echo 'Tunnel URL was not issued' >&2; exit 1; }
fi
python3 /opt/kc-mcp/scripts/configure.py "$origin"
if [[ ! -d /workspace/demo/.git ]]; then
    mkdir -p /workspace/demo
    cp -n /opt/kc-mcp/scripts/demo/* /workspace/demo/
    git -C /workspace/demo init -q
    git -C /workspace/demo -c user.name='KC MCP Setup' -c user.email='kc-mcp@localhost' add .
    git -C /workspace/demo -c user.name='KC MCP Setup' -c user.email='kc-mcp@localhost' commit -qm 'Initial demo'
fi
echo "ChatGPT MCP URL: $origin/mcp"
echo 'Owner token is stored in /state/oauth-owner.token (not printed).'
spacedock serve --config /state/config.yaml &
server_pid=$!
if [[ -n "$tunnel_pid" ]]; then
    wait -n "$server_pid" "$tunnel_pid"
else
    wait "$server_pid"
fi
