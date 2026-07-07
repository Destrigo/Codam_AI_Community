"""Exercise 07 — Temperature and max_tokens."""

import json
import os
import urllib.request


def chat_completion(messages: list[dict], max_tokens: int | None = None) -> str:
    # TODO: add max_tokens to the payload
    raise NotImplementedError


def main() -> None:
    print(chat_completion([{"role": "user", "content": "hello"}], max_tokens=5))


if __name__ == "__main__":
    main()
