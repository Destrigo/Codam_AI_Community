"""Exercise 03 — HTTP POST."""

import json
import os
import urllib.request


def main() -> None:
    url = os.environ.get("CODAMLINGS_ECHO_URL", "https://httpbin.org/post")
    payload = {"name": "codam"}
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    name = data["json"]["name"]
    print(f"ECHO_OK:{name}")


if __name__ == "__main__":
    main()
