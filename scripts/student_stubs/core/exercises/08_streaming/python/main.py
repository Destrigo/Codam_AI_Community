"""Exercise 08 — Streaming."""

import json
import os
import urllib.request


def chat_stream(messages: list[dict]) -> str:
    # TODO: stream=true, accumulate delta.content
    raise NotImplementedError


def main() -> None:
    print(chat_stream([{"role": "user", "content": "hello"}]), end="")


if __name__ == "__main__":
    main()
