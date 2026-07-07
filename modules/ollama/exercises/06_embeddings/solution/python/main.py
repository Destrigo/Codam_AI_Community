import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAMLINGS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
    payload = {"model": "nomic-embed-text", "prompt": "codam ollama embed"}
    req = urllib.request.Request(
        f"{base}/api/embeddings",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    print(f"EMBED_DIM:{len(data['embedding'])}")

if __name__ == "__main__":
    main()
