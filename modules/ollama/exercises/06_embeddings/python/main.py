"""Exercise stub."""

import json
import os
import urllib.request


def main() -> None:
    base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
    # TODO: implement — prefer: codam-labs --mock verify <slug>
    pass


if __name__ == "__main__":
    main()
