"""Minimal LinkReacher MCP client (no SDK, MCP is just JSON-RPC 2.0).

Run: LINKREACHER_API_KEY=lr_... python examples/python_client.py
"""
import json
import os
import urllib.request

URL = os.environ.get("LINKREACHER_MCP_URL", "https://api.linkreacher.com/mcp")
KEY = os.environ.get("LINKREACHER_API_KEY", "")


def rpc(method: str, params: dict | None = None, auth: bool = False, _id: int = 1):
    headers = {"Content-Type": "application/json"}
    if auth:
        if not KEY:
            raise SystemExit("Set LINKREACHER_API_KEY=lr_... first.")
        headers["Authorization"] = f"Bearer {KEY}"
    body = json.dumps({"jsonrpc": "2.0", "id": _id, "method": method,
                       "params": params or {}}).encode()
    req = urllib.request.Request(URL, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def call(name: str, args: dict, _id: int = 1):
    out = rpc("tools/call", {"name": name, "arguments": args}, auth=True, _id=_id)
    result = out["result"]
    # `content` is markdown for the model; `structuredContent` is the same data for code.
    return result.get("structuredContent"), result["content"][0]["text"]


if __name__ == "__main__":
    info = rpc("initialize", {"protocolVersion": "2025-06-18"})["result"]
    print("server   :", info["serverInfo"])
    print("caps     :", info["capabilities"])
    print("tools    :", len(rpc("tools/list")["result"]["tools"]))
    print("prompts  :", [p["name"] for p in rpc("prompts/list")["result"]["prompts"]])

    structured, markdown = call("get_me", {}, _id=2)
    print("\n--- get_me (markdown) ---\n" + markdown)
    print("\n--- get_me (structured) ---\n" + json.dumps(structured, indent=2)[:400])

    structured, markdown = call("list_prospects", {}, _id=3)
    print("\n--- list_prospects (markdown) ---\n" + markdown)
