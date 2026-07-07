"""Exercise 01 — clear vs ambiguous."""
import json, os, urllib.request

def classify_sentiment(text: str) -> str:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    key = os.environ.get("MISTRAL_API_KEY", "")
    payload = {"model": os.environ.get("MISTRAL_MODEL", "mistral-small-latest"),
               "messages": [{"role": "user", "content": f"Classify as positive or negative: {text}"}]}
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    if key: req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def main() -> None:
    print(classify_sentiment("I love this product"))

if __name__ == "__main__":
    main()
