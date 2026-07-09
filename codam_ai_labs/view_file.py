"""Paginated file viewer for a separate terminal window."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

PAGE_LINES = 30


def _win32_expand_buffer(lines: int = 9999, cols: int = 120) -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)

        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        kernel32.SetConsoleScreenBufferSize(handle, COORD(cols, lines))
    except Exception:
        pass


def _print_paged(lines: list[str]) -> None:
    total = len(lines)
    if total == 0:
        return

    height = max(20, shutil.get_terminal_size((80, 24)).lines - 6)
    page = max(PAGE_LINES, height)

    index = 0
    while index < total:
        end = min(index + page, total)
        print("\n".join(lines[index:end]))
        index = end
        if index < total:
            try:
                reply = input(f"\n[{index}/{total} lines] Enter=next, q=quit ")
            except EOFError:
                break
            if reply.strip().lower() == "q":
                break


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m codam_ai_labs.view_file <path> [title]")
        return 1

    path = Path(args[0]).resolve()
    title = args[1] if len(args) > 1 else path.parent.name

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        input("Press Enter to close...")
        return 1

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Could not read {path}: {exc}", file=sys.stderr)
        input("Press Enter to close...")
        return 1

    _win32_expand_buffer()
    width = max(60, min(shutil.get_terminal_size((80, 24)).columns, 100))

    lines = text.splitlines()
    print()
    print("=" * width)
    print(title)
    print(path)
    print(f"{len(lines)} lines")
    print("=" * width)
    print()

    height = max(16, shutil.get_terminal_size((80, 24)).lines - 8)
    if len(lines) <= height:
        print(text.rstrip())
        print()
        print("-" * width)
        input("Press Enter to close...")
        return 0

    _print_paged(lines)
    print()
    print("-" * width)
    input("Press Enter to close...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
