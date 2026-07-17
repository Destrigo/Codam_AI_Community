"""Exercise stub."""

import json
import os
import urllib.request


def main() -> None:
    base = os.environ.get("CODAM_LABS_MCP_BASE", "http://127.0.0.1:8765/mcp").rstrip("/")
    # TODO: implement — prefer: codam-labs --mock verify <slug>
    pass


if __name__ == "__main__":
    main()
