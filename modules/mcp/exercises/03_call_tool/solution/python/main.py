import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAMLINGS_MCP_BASE", "http://127.0.0.1:8765/mcp").rstrip("/")
    body = json.dumps({"name": "search", "arguments": {"query": "docs"}}).encode()
    req = urllib.request.Request(f"{base}/call", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=10) as r:
        out = json.loads(r.read())["result"]
    print(out)

if __name__ == "__main__":
    main()
