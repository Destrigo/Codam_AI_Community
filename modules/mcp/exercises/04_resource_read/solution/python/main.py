import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAM_LABS_MCP_BASE", "http://127.0.0.1:8765/mcp").rstrip("/")
    with urllib.request.urlopen(f"{base}/resources/policy", timeout=10) as r:
        data = json.loads(r.read())
    print(data["content"])

if __name__ == "__main__":
    main()
