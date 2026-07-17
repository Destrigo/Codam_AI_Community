import json
import os
import urllib.request


def main() -> None:
    url = os.environ.get(
        "CODAM_LABS_TODO_URL",
        "https://jsonplaceholder.typicode.com/todos/1",
    )
    with urllib.request.urlopen(url, timeout=15) as r:
        title = json.loads(r.read())["title"]
    print(f"FETCH_OK:{title}")


if __name__ == "__main__":
    main()
