"""Shared Mistral HTTP helpers for capstones and business cases."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from codam_ai_labs.config import mistral_api_base, mistral_api_key, mistral_model


def _request(method: str, path: str, payload: dict | None = None, timeout: int = 60) -> dict:
    base = mistral_api_base()
    url = f"{base}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    key = mistral_api_key()
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def chat_completion(
    messages: list[dict[str, str]],
    *,
    tools: list[dict] | None = None,
    max_tokens: int | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model or mistral_model(),
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    body = _request("POST", "/chat/completions", payload)
    return body["choices"][0]["message"]


def chat_text(messages: list[dict[str, str]], **kwargs: Any) -> str:
    msg = chat_completion(messages, **kwargs)
    return (msg.get("content") or "").strip()


def embed_text(text: str, model: str = "mistral-embed") -> list[float]:
    body = _request("POST", "/embeddings", {"model": model, "input": text})
    return body["data"][0]["embedding"]


def extract_json_object(text: str) -> dict:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object in response")
    return json.loads(text[start : end + 1])


def is_mock_mode() -> bool:
    return bool(os.environ.get("CODAM_LABS_MOCK"))
