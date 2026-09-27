"""Exercise real OAuth+HTTP MCP. All credentials stay in process memory."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from configure import configure

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def main(binary, output):
    with tempfile.TemporaryDirectory(prefix="kc-mcp-smoke-") as tmp:
        root = Path(tmp)
        workspace, state = root / "workspace", root / "state"
        workspace.mkdir()
        shutil.copytree(Path(__file__).parent / "demo", workspace / "demo")
        (workspace / "demo" / ".env").write_text("DUMMY_SECRET=test-only\n")
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        origin = f"http://127.0.0.1:{port}"
        config = configure(origin, state, workspace, port)
        opener = urllib.request.build_opener(NoRedirect)
        checks = []
        def request(path, body=None, token=None, form=False, headers=None):
            h = headers or {}
            if body is not None:
                body = urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode()
                h["Content-Type"] = "application/x-www-form-urlencoded" if form else "application/json"
            if token:
                h["Authorization"] = "Bearer " + token
            h["Accept"] = "application/json, text/event-stream"
            req = urllib.request.Request(origin + path, data=body, headers=h)
            try:
                response = opener.open(req, timeout=15)
            except urllib.error.HTTPError as e:
                response = e
            with response:
                raw = response.read().decode()
                try: data = json.loads(raw)
                except json.JSONDecodeError: data = raw
                return response.status, response.headers, data
        def check(name, condition):
            if not condition:
                raise AssertionError(name)
            checks.append(name)
            print("PASS", name)
        with (root / "server.log").open("w") as log:
            proc = subprocess.Popen([str(Path(binary).resolve()), "serve", "--config", str(config)],
                                    stdout=log, stderr=log)
            try:
                for _ in range(100):
                    if proc.poll() is not None:
                        raise RuntimeError("Server exited: " + (root / "server.log").read_text())
                    try:
                        if request("/healthz")[0] == 200: break
                    except urllib.error.URLError: pass
                    time.sleep(.1)
                check("health", request("/healthz")[0] == 200)
                check("unauthenticated MCP denied", request("/mcp", {})[0] == 401)
                status, _, metadata = request("/.well-known/oauth-protected-resource/mcp")
                check("OAuth discovery", status == 200 and metadata["resource"] == origin + "/mcp")
                status, _, client = request("/register", {"client_name": "KC Integration Test",
                    "redirect_uris": ["http://127.0.0.1/callback"], "grant_types": ["authorization_code", "refresh_token"],
                    "response_types": ["code"], "token_endpoint_auth_method": "none"})
                check("dynamic client registration", status in (200, 201) and "client_id" in client)
                verifier = secrets.token_urlsafe(40)
                challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
                auth = {"client_id": client["client_id"], "redirect_uri": "http://127.0.0.1/callback",
                        "response_type": "code", "resource": origin + "/mcp", "scope": "spacedock",
                        "code_challenge_method": "S256", "code_challenge": challenge, "state": "smoke"}
                status, _, _ = request("/oauth/authorize", {**auth, "owner_token": "invalid"}, form=True)
                check("wrong owner approval denied", status == 401)
                status, headers, _ = request("/oauth/authorize", {**auth, "owner_token": (state / "oauth-owner.token").read_text().strip()}, form=True)
                check("owner approval redirects", status == 302)
                code = urllib.parse.parse_qs(urllib.parse.urlparse(headers["Location"]).query)["code"][0]
                exchange = {"grant_type": "authorization_code", "client_id": client["client_id"],
                            "redirect_uri": auth["redirect_uri"], "resource": auth["resource"], "code": code,
                            "code_verifier": verifier}
                status, _, pair = request("/oauth/token", exchange, form=True)
                check("PKCE token exchange", status == 200 and "access_token" in pair)
                check("authorization code replay denied", request("/oauth/token", exchange, form=True)[0] == 400)
                token = pair["access_token"]
                sequence = 0
                def rpc(method, params):
                    nonlocal sequence
                    sequence += 1
                    status, _, data = request("/mcp", {"jsonrpc": "2.0", "id": sequence,
                        "method": method, "params": params}, token,
                        headers={"MCP-Protocol-Version": "2025-03-26"})
                    if status != 200 or "error" in data:
                        raise AssertionError(f"RPC failed: {method}: status={status}")
                    return data["result"]
                result = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                    "clientInfo": {"name": "kc-smoke", "version": "1.0"}})
                check("MCP initialize", result["serverInfo"]["name"] == "spacedock")
                names = {t["name"] for t in rpc("tools/list", {})["tools"]}
                check("file and command tools", {"workspace_open", "read_file", "file_edit", "exec_command"} <= names)
                def call(name, args): return rpc("tools/call", {"name": name, "arguments": args})
                opened = call("workspace_open", {"root_id": "projects", "path": "demo", "mode": "checkout"})
                if opened.get("isError"): raise AssertionError("open workspace")
                wid = opened["structuredContent"]["workspace_id"]
                check("workspace open", bool(wid))
                result = call("file_edit", {"workspace_id": wid, "action": "write", "path": "greeting.txt", "content": "hello kc\n"})
                check("file write", not result.get("isError") and (workspace / "demo" / "greeting.txt").read_text() == "hello kc\n")
                result = call("read_file", {"workspace_id": wid, "path": "greeting.txt"})
                check("file read", not result.get("isError") and "hello kc" in json.dumps(result))
                check("path traversal denied", call("read_file", {"workspace_id": wid, "path": "../../state/oauth-owner.token"}).get("isError"))
                check("sensitive file denied", call("read_file", {"workspace_id": wid, "path": ".env"}).get("isError"))
                result = call("exec_command", {"workspace_id": wid, "command": "node --test", "yield_ms": 5000})
                check("command and test execution", not result.get("isError") and result["structuredContent"].get("exit_code") == 0)
                status, _, refreshed = request("/oauth/token", {"grant_type": "refresh_token", "client_id": client["client_id"],
                    "refresh_token": pair["refresh_token"], "resource": auth["resource"]}, form=True)
                check("refresh token exchange", status == 200 and "access_token" in refreshed)
                check("unexpected Host denied", request("/healthz", headers={"Host": "attacker.example"})[0] == 421)
            finally:
                proc.terminate()
                try: proc.wait(timeout=8)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(json.dumps({"runtime": "SpaceDock 0.1.6", "passed": checks,
            "scope": "local HTTP OAuth+MCP; excludes remote Docker and ChatGPT UI"}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("binary")
    parser.add_argument("--output", default="test-results/smoke.json")
    args = parser.parse_args()
    main(args.binary, args.output)
