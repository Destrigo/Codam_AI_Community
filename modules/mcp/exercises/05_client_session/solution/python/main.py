import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAM_LABS_MCP_BASE", "http://127.0.0.1:8765/mcp").rstrip("/")
    req = urllib.request.Request(f"{base}/initialize", data=b"{}", method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    print(f"SESSION_OK:{data['session_id']}")

if __name__ == "__main__":
    main()
