"""Exercise 02 — few-shot."""
import json, os, urllib.request

def few_shot(prompt: str) -> str:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    key = os.environ.get("MISTRAL_API_KEY", "")
    payload = {"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    if key: req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def main() -> None:
    p = "Example 1: hi -> friendly\nExample 2: bye -> friendly\nClassify: hello"
    print(few_shot(p))

if __name__ == "__main__":
    main()
