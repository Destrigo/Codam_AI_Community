import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
    payload = {
        "model": "llama3.2",
        "messages": [{"role": "user", "content": "ollama stream hello"}],
        "stream": True,
    }
    req = urllib.request.Request(
        f"{base}/api/chat",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    parts: list[str] = []
    with urllib.request.urlopen(req, timeout=60) as r:
        for line in r:
            line = line.decode("utf-8").strip()
            if not line:
                continue
            chunk = json.loads(line)
            msg = chunk.get("message") or {}
            if content := msg.get("content"):
                parts.append(content)
    print("".join(parts))

if __name__ == "__main__":
    main()
