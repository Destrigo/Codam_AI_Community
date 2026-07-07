import json, os, urllib.request

def main() -> None:
    base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
    with urllib.request.urlopen(f"{base}/api/tags", timeout=10) as r:
        data = json.loads(r.read())
    print(f"MODELS_OK:{len(data['models'])}")

if __name__ == "__main__":
    main()
