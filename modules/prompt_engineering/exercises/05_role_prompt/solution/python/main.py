"""Exercise 05 — role."""
import json, os, urllib.request

def with_role() -> str:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    key = os.environ.get("MISTRAL_API_KEY", "")
    payload = {"model": "mistral-small-latest", "messages": [
        {"role": "system", "content": "You are a code reviewer"},
        {"role": "user", "content": "Review: print(1)"}]}
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    if key: req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def main() -> None:
    print(with_role())

if __name__ == "__main__":
    main()
