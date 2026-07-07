"""Exercise 04 — First LLM call."""

import json
import os
import urllib.request


def chat_completion(messages: list[dict]) -> str:
    # TODO: POST to /chat/completions, return assistant content
    raise NotImplementedError


def main() -> None:
    content = chat_completion([{"role": "user", "content": "hello"}])
    print(content)


if __name__ == "__main__":
    main()
