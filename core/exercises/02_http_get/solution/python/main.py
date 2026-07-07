"""Exercise 02 — HTTP GET and JSON."""

import json
import urllib.request


def main() -> None:
    url = "https://jsonplaceholder.typicode.com/todos/1"
    with urllib.request.urlopen(url, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
    print(data["title"])


if __name__ == "__main__":
    main()
