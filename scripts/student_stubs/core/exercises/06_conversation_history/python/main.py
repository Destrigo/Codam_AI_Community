"""Exercise 06 — Conversation history."""

import json
import os
import urllib.request


def chat_completion(messages: list[dict]) -> str:
    raise NotImplementedError


def main() -> None:
    messages = [
        # TODO: 4 messages as described in the README
    ]
    print(chat_completion(messages))


if __name__ == "__main__":
    main()
