"""Shared terminal UI helpers for interactive screens."""

from __future__ import annotations

import shutil
import sys
import time
from contextlib import contextmanager

ALT_SCREEN_ON = "\033[?1049h"
ALT_SCREEN_OFF = "\033[?1049l"
CLEAR = "\033[2J\033[H"
DIM = "\033[2m"
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

RETURN_MENU = 2


@contextmanager
def alternate_screen():
    try:
        sys.stdout.write(ALT_SCREEN_ON)
        sys.stdout.flush()
        yield
    finally:
        sys.stdout.write(ALT_SCREEN_OFF)
        sys.stdout.flush()


@contextmanager
def raw_keys():
    if sys.platform == "win32":
        yield
        return
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_key(timeout: float = 0.2) -> str | None:
    if sys.platform == "win32":
        import msvcrt

        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("\x00", "\xe0"):
                ch2 = msvcrt.getwch()
                if ch2 == "H":
                    return "k"
                if ch2 == "P":
                    return "j"
                return None
            return ch
        time.sleep(timeout)
        return None

    import select

    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if not ready:
        return None
    return sys.stdin.read(1)


def terminal_size(default: tuple[int, int] = (100, 24)) -> tuple[int, int]:
    cols, rows = shutil.get_terminal_size(default)
    return max(60, cols), max(16, rows)


def draw_screen(header: list[str], body: list[str], footer: str) -> None:
    cols, rows = terminal_size()
    width = min(cols, 78)
    out: list[str] = [CLEAR]
    out.extend(header)
    out.append("─" * width)
    max_body = rows - len(out) - 3
    if len(body) > max_body:
        body = body[:max_body]
    out.extend(body)
    out.append("─" * width)
    out.append(footer)
    sys.stdout.write("\n".join(out) + "\n")
    sys.stdout.flush()


def progress_bar(done: int, total: int, width: int = 28) -> str:
    if total <= 0:
        return "[" + " " * width + "]"
    filled = int(width * done / total)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {done}/{total}"
