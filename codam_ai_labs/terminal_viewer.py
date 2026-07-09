"""Open exercise docs in a separate terminal window."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

VIEW_CACHE_DIR = Path(__file__).resolve().parent.parent / ".codam-ai-labs" / "view"


def _launch(command: list[str], *, shell: bool = False) -> None:
    subprocess.Popen(command, shell=shell, close_fds=False)


def _viewer_command(path: Path, title: str) -> list[str]:
    py = sys.executable
    module = "codam_ai_labs.view_file"
    return [py, "-m", module, str(path.resolve()), title]


def _open_viewer(path: Path, *, title: str) -> bool:
    command = _viewer_command(path, title)

    if sys.platform == "win32":
        if shutil.which("wt"):
            _launch(["wt", "-w", "0", "nt", "--title", title, "--", *command])
            return True

        _launch(
            [
                "cmd",
                "/c",
                "start",
                title,
                "cmd",
                "/k",
                *command,
            ],
        )
        return True

    if sys.platform == "darwin":
        cmd = " ".join(f'"{part}"' if " " in part else part for part in command)
        _launch(
            [
                "osascript",
                "-e",
                f'tell application "Terminal" to do script "{cmd}"',
            ],
        )
        return True

    runners = [
        ["gnome-terminal", "--title", title, "--", *command],
        ["konsole", "--new-tab", "-p", f"tabtitle={title}", "-e", *command],
        ["xfce4-terminal", "--title", title, "-e", " ".join(command)],
        ["xterm", "-T", title, "-e", *command],
    ]
    for runner in runners:
        if shutil.which(runner[0]):
            _launch(runner)
            return True

    return False


def open_in_new_terminal(path: Path, *, title: str) -> bool:
    """Print a file in a new terminal window. Returns True if launch was attempted."""
    path = path.resolve()
    if not path.exists():
        return False
    return _open_viewer(path, title=title)


def open_text_in_new_terminal(text: str, *, title: str, cache_name: str) -> bool:
    """Write text to the local view cache and open it in a new terminal."""
    VIEW_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = VIEW_CACHE_DIR / cache_name
    path.write_text(text, encoding="utf-8")
    return _open_viewer(path, title=title)


def build_hint_document(exercise_path: Path) -> str | None:
    """Combine peer review checklist and hints for one exercise."""
    peer = exercise_path / "peer_review.md"
    hint = exercise_path / "hint.md"
    readme = exercise_path / "README.md"
    parts: list[str] = []

    if peer.exists():
        parts.append(peer.read_text(encoding="utf-8").rstrip())
    if hint.exists():
        if parts:
            parts.append("\n\n---\n\n")
        parts.append(hint.read_text(encoding="utf-8").rstrip())
    if not parts and readme.exists():
        parts.append(readme.read_text(encoding="utf-8").rstrip())

    if not parts:
        return None
    return "\n".join(parts) + "\n"


def open_hint_in_new_terminal(exercise_path: Path, *, slug: str) -> bool:
    document = build_hint_document(exercise_path)
    if not document:
        return False
    title = f"Codam — {slug} — hint"
    safe_name = slug.replace("/", "__") + ".md"
    return open_text_in_new_terminal(document, title=title, cache_name=safe_name)
