#!/usr/bin/env python3
"""Minimal read-only MCP-over-HTTP health check.

Use only against endpoints you own or are authorized to test.
No credentials are stored and no tool is executed.
"""

import json
import sys
import urllib.error
import urllib.request
import uuid

TIMEOUT = 10

def rpc(url, method, params=None, session_id=None):
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params or {},
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "naif-gravity-mcp-health-check/1.0",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
        body = res.read().decode("utf-8", errors="replace")
        return res.status, dict(res.headers.items()), body

def summarize(label, result):
    status, headers, body = result
    print(f"\n[{label}] HTTP {status}")
    session = headers.get("Mcp-Session-Id") or headers.get("mcp-session-id")
    if session:
        print("session: present")
    try:
        data = json.loads(body)
        if "error" in data:
            err = data["error"]
            print("json-rpc: error", err.get("code"), err.get("message"))
        elif "result" in data:
            print("json-rpc: result")
            if label == "tools/list":
                tools = data.get("result", {}).get("tools", [])
                print("tools:", len(tools))
        else:
            print("json-rpc: unexpected JSON shape")
    except json.JSONDecodeError:
        print("body: non-JSON or streaming response")
        print(body[:300].replace("\n", " "))

def main():
    if len(sys.argv) != 2:
        print("usage: python3 tools/mcp_health_check.py https://your-server.example/mcp")
        return 2
    url = sys.argv[1]
    if not url.startswith(("http://", "https://")):
        print("error: URL must start with http:// or https://")
        return 2

    init_params = {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "naif-gravity-health-check", "version": "1.0"},
    }
    try:
        init = rpc(url, "initialize", init_params)
        summarize("initialize", init)
        session = init[1].get("Mcp-Session-Id") or init[1].get("mcp-session-id")
        tools = rpc(url, "tools/list", {}, session)
        summarize("tools/list", tools)
        print("\nNo tools were executed.")
        return 0
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
        return 1
    except urllib.error.URLError as e:
        print(f"connection error: {e.reason}")
        return 1
    except Exception as e:
        print(f"error: {type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
