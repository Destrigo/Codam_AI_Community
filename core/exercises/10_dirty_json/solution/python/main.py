"""Exercise 10 — Dirty JSON."""

import json
import os
import re
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


def extract_json_block(text: str) -> dict:
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError("JSON not found in response")


def main() -> None:
    response = chat_completion([{"role": "user", "content": "Return JSON in markdown"}])
    data = extract_json_block(response)
    print(f"PARSED:name={data['name']}")
    print(f"PARSED:score={data['score']}")


if __name__ == "__main__":
    main()
