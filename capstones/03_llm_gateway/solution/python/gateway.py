"""Capstone 03 — LLM Gateway library (reference solution)."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from codamlings.config import mistral_api_base, mistral_api_key, mistral_model

INJECTION_PHRASES = ("ignore instructions",)


class Gateway:
    def __init__(self) -> None:
        self.calls = 0
        self.cache_hits = 0
        self.retries = 0
        self.fallbacks = 0
        self._cache: dict[str, str] = {}
        cache_dir = os.environ.get("GATEWAY_CACHE_DIR")
        self._cache_file = Path(cache_dir) / "responses.json" if cache_dir else None
        if self._cache_file and self._cache_file.exists():
            self._cache = json.loads(self._cache_file.read_text(encoding="utf-8"))

    def _cache_key(self, prompt: str, system: str) -> str:
        payload = json.dumps({"system": system, "prompt": prompt}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    def _save_cache(self) -> None:
        if self._cache_file:
            self._cache_file.parent.mkdir(parents=True, exist_ok=True)
            self._cache_file.write_text(json.dumps(self._cache), encoding="utf-8")

    def _redact(self, text: str) -> str:
        return re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED]", text)

    def _post(self, model: str, messages: list[dict]) -> str:
        base = mistral_api_base()
        payload = {"model": model, "messages": messages}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(f"{base}/chat/completions", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        key = mistral_api_key()
        if key:
            req.add_header("Authorization", f"Bearer {key}")

        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"].strip()
            except urllib.error.HTTPError as exc:
                if exc.code == 503 and attempt < 2:
                    self.retries += 1
                    time.sleep(2**attempt)
                    continue
                raise
        raise RuntimeError("chat failed after retries")

    def complete(self, prompt: str, *, system: str = "") -> str:
        combined = f"{system}\n{prompt}".lower()
        if any(p in combined for p in INJECTION_PHRASES):
            return "BLOCKED:injection"

        key = self._cache_key(prompt, system)
        if key in self._cache:
            self.cache_hits += 1
            print("CACHE_HIT", file=__import__("sys").stderr)
            return self._cache[key]

        self.calls += 1
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        primary = mistral_model()
        fallback = os.environ.get("MISTRAL_FALLBACK_MODEL", primary)
        try:
            out = self._post(primary, messages)
        except Exception:
            if fallback != primary:
                self.fallbacks += 1
                print("FALLBACK_OK", file=__import__("sys").stderr)
                out = self._post(fallback, messages)
            else:
                raise

        log_line = self._redact(f"call model={primary} prompt_len={len(prompt)}")
        print(f"LOG:{log_line}", file=__import__("sys").stderr)
        if "REDACTED" in log_line:
            print("LOG_REDACTED", file=__import__("sys").stderr)

        self._cache[key] = out
        self._save_cache()
        return out

    def stats(self) -> dict:
        return {
            "calls": self.calls,
            "cache_hits": self.cache_hits,
            "retries": self.retries,
            "fallbacks": self.fallbacks,
        }
