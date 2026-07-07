"""Exercise 09 — Timeout and retry."""

import json
import os
import time
import urllib.error
import urllib.request


def fetch_with_retry(url: str, max_attempts: int = 3) -> None:
    for attempt in range(max_attempts):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                json.loads(response.read().decode("utf-8"))
            print("RETRY_OK")
            return
        except urllib.error.HTTPError as exc:
            if exc.code == 503 and attempt < max_attempts - 1:
                time.sleep(2**attempt)
                continue
            raise


def main() -> None:
    base = os.environ.get("MISTRAL_API_BASE", "https://api.mistral.ai/v1").rstrip("/")
    fetch_with_retry(f"{base}/fail_twice")


if __name__ == "__main__":
    main()
