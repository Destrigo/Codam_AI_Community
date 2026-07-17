"""Exercise 02 — HTTP GET and JSON."""

import json
import os
import urllib.request


def main() -> None:
    url = os.environ.get(
        "CODAM_LABS_TODO_URL",
        "https://jsonplaceholder.typicode.com/todos/1",
    )
    with urllib.request.urlopen(url, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
    print(data["title"])


if __name__ == "__main__":
    main()
