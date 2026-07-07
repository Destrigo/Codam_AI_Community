import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
    payload = {
        "model": "llama3.2",
        "messages": [{"role": "user", "content": "ollama chat hello"}],
        "stream": False,
    }
    req = urllib.request.Request(
        f"{base}/api/chat",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    print(data["message"]["content"])

if __name__ == "__main__":
    main()
