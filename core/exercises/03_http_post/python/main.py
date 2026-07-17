"""Exercise 03 — HTTP POST."""

import json
import os
import urllib.request


def main() -> None:
    # Prefer CODAM_LABS_ECHO_URL (set automatically with --mock).
    # Live fallback: httpbin — may return 503 / rate-limit; use --mock if so.
    url = os.environ.get("CODAM_LABS_ECHO_URL", "https://httpbin.org/post")
    payload = {"name": "codam"}
    # TODO: POST JSON with Content-Type application/json, print ECHO_OK:<name>
    # Response shape: {"json": {"name": "codam"}, ...}  → use data["json"]["name"]
    pass


if __name__ == "__main__":
    main()
