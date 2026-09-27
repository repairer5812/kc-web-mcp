"""Generate SpaceDock config without printing its owner token."""
import argparse
import json
import os
from pathlib import Path
import secrets
from urllib.parse import urlparse

def configure(origin, state, workspace, port=8766):
    parsed = urlparse(origin)
    if (parsed.scheme not in ("http", "https") or not parsed.hostname
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or parsed.path not in ("", "/")
        or (parsed.scheme == "http" and parsed.hostname not in ("localhost", "127.0.0.1"))):
        raise ValueError("Expected HTTPS origin (HTTP is allowed only on loopback)")
    origin = origin.rstrip("/")
    state, workspace = Path(state).resolve(), Path(workspace).resolve()
    state.mkdir(parents=True, exist_ok=True)
    workspace.mkdir(parents=True, exist_ok=True)
    token_path = state / "oauth-owner.token"
    if not token_path.exists():
        fd = os.open(token_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(secrets.token_hex(32) + "\n")
    config = {
        "state_dir": str(state),
        "server": {"host": "127.0.0.1", "port": port, "public_base_url": origin,
            "allowed_hosts": [parsed.hostname, "localhost", "127.0.0.1"],
            "trust_proxy": False,
            "oauth": {"owner_token_file": str(token_path), "scopes": ["spacedock"],
                      "allowed_redirect_hosts": ["chatgpt.com", "localhost", "127.0.0.1"]}},
        "worktree": {"root": str(state / "worktrees")},
        "agents": {"max_concurrent": 1},
        "allowed_roots": [{"id": "projects", "name": "KC Development Projects",
                           "path": str(workspace),
                           "permissions": ["fs.read", "fs.write", "command.execute", "git.read",
                                           "workspace.manage", "recall.read", "recall.write"]}],
    }
    # JSON is valid YAML; use stdlib to avoid another deployment dependency.
    config_path = state / "config.yaml"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    os.chmod(config_path, 0o600)
    (state / "connection-url.txt").write_text(origin + "/mcp\n", encoding="utf-8")
    return config_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("origin")
    parser.add_argument("--state", default="/state")
    parser.add_argument("--workspace", default="/workspace")
    args = parser.parse_args()
    configure(args.origin, args.state, args.workspace)
