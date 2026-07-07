"""Exercise 04 — First LLM call."""

import json
import os
import urllib.error
import urllib.request


def chat_completion(messages: list[dict]) -> str:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    url = f"{base}/chat/completions"

    payload = {
        "model": "mistral-small-latest",
        "messages": messages,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    if api_key:
        request.add_header("Authorization", f"Bearer {api_key}")

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"]


def main() -> None:
    content = chat_completion([{"role": "user", "content": "hello"}])
    print(content)


if __name__ == "__main__":
    main()
