"""Shared subprocess environment for capstones and business cases."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from codam_ai_labs.config import load_dotenv_if_present
from codam_ai_labs.mock_server import mock_api_base, start_mock_server
from codam_ai_labs.verify import exercise_env


@contextmanager
def subprocess_env(*, use_mock: bool = False) -> Iterator[dict[str, str]]:
    """Build env for child Python processes; starts mock server when use_mock=True."""
    load_dotenv_if_present()
    server = None
    try:
        if use_mock:
            server = start_mock_server(0)
            env = exercise_env(True, mock_api_base(server))
            env["CODAM_LABS_AUTO_CONFIRM"] = "1"
        else:
            env = exercise_env(False)
        yield env
    finally:
        if server:
            server.shutdown()
