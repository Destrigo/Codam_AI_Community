"""Exercise 10 — Dirty JSON."""

import json
import os
import re
import urllib.request


def chat_completion(messages: list[dict]) -> str:
    raise NotImplementedError


def extract_json_block(text: str) -> dict:
    # TODO: extract JSON from markdown or dirty text
    raise NotImplementedError


def main() -> None:
    response = chat_completion([{"role": "user", "content": "Return JSON in markdown"}])
    data = extract_json_block(response)
    print(f"PARSED:name={data['name']}")
    print(f"PARSED:score={data['score']}")


if __name__ == "__main__":
    main()
