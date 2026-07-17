"""Exercise stub."""

import json
import os
import urllib.request


def main() -> None:
    url = os.environ.get(
        "CODAM_LABS_TODO_URL",
        "https://jsonplaceholder.typicode.com/todos/1",
    )
    # TODO: GET title, print FETCH_OK:<title>
    pass


if __name__ == "__main__":
    main()
