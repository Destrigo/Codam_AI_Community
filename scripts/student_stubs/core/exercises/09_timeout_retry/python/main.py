"""Exercise 09 — Timeout and retry."""

import json
import os
import time
import urllib.error
import urllib.request


def fetch_with_retry(url: str, max_attempts: int = 3) -> None:
    # TODO: retry on 503, print RETRY_OK on success
    raise NotImplementedError


def main() -> None:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    fetch_with_retry(f"{base}/fail_twice")


if __name__ == "__main__":
    main()
