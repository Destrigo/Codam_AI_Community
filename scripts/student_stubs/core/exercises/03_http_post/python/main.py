"""Exercise 03 — HTTP POST."""

import json
import urllib.request


def main() -> None:
    url = "https://httpbin.org/post"
    payload = {"name": "codam"}
    # TODO: POST JSON, print ECHO_OK:<name>
    pass


if __name__ == "__main__":
    main()
