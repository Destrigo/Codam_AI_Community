"""Exercise 08 — Streaming."""

import json
import os
import urllib.request


def chat_stream(messages: list[dict]) -> str:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    url = f"{base}/chat/completions"
    payload = {"model": "mistral-small-latest", "messages": messages, "stream": True}
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    if api_key:
        request.add_header("Authorization", f"Bearer {api_key}")

    parts: list[str] = []
    with urllib.request.urlopen(request, timeout=30) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8").strip()
            if not line or not line.startswith("data:"):
                continue
            data = line.removeprefix("data:").strip()
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            delta = chunk["choices"][0].get("delta", {})
            content = delta.get("content")
            if content:
                parts.append(content)
    return "".join(parts)


def main() -> None:
    print(chat_stream([{"role": "user", "content": "hello"}]), end="")


if __name__ == "__main__":
    main()
