"""Exercise 05 — System and user prompts."""

import json
import os
import urllib.request


def chat_completion(messages: list[dict]) -> str:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    url = f"{base}/chat/completions"
    payload = {"model": "mistral-small-latest", "messages": messages}
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    if api_key:
        request.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> None:
    messages = [
        {"role": "system", "content": "Always respond in UPPERCASE"},
        {"role": "user", "content": "hello"},
    ]
    print(chat_completion(messages))


if __name__ == "__main__":
    main()
