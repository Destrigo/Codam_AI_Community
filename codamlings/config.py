"""Shared Mistral API configuration for codamlings."""

from __future__ import annotations

import os

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
