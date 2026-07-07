"""Shared Mistral API configuration for codamlings."""

from __future__ import annotations

import os
import sys

MISTRAL_API_BASE_DEFAULT = "https://api.mistral.ai/v1"
MISTRAL_MODEL_DEFAULT = "mistral-small-latest"


def mistral_api_base() -> str:
    return os.environ.get("MISTRAL_API_BASE", MISTRAL_API_BASE_DEFAULT).rstrip("/")


def mistral_api_key() -> str:
    return os.environ.get("MISTRAL_API_KEY", "")


def mistral_model() -> str:
    return os.environ.get("MISTRAL_MODEL", MISTRAL_MODEL_DEFAULT)


def apply_mistral_env(env: dict[str, str], mock_base: str | None = None, mock_key: str = "mock-key") -> None:
    if mock_base:
        env["MISTRAL_API_BASE"] = mock_base
        env["MISTRAL_API_KEY"] = mock_key
        env["CODAMLINGS_MOCK"] = "1"
    else:
        env.setdefault("MISTRAL_API_BASE", MISTRAL_API_BASE_DEFAULT)
        env.pop("CODAMLINGS_MOCK", None)


def require_mistral_key() -> None:
    if not mistral_api_key():
        print(
            "MISTRAL_API_KEY is required for live exercises.\n"
            "Copy .env.example to .env and set your key from https://console.mistral.ai\n"
            "Use --mock only for offline CI/testing.",
            file=sys.stderr,
        )
        sys.exit(1)


def load_dotenv_if_present() -> None:
    """Load .env from project root when running CLI."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(root, ".env")
    if not os.path.isfile(env_file):
        return
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
