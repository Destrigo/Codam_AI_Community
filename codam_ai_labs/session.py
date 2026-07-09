"""Rustlings-style interactive watch session."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

from codam_ai_labs.exercises import (
    ROOT,
    Exercise,
    exercise_pool,
    exercise_status_label,
    is_complete,
    is_exercise_complete,
    load_session_state,
    resolve_session_index,
    save_session_state,
    track_done_count,
    unmark_complete,
)
from codam_ai_labs.terminal_viewer import (
    build_hint_document,
    open_hint_in_new_terminal,
    open_in_new_terminal,
)
from codam_ai_labs.verify import format_run_summary, run_exercise, verify_exercise

from codam_ai_labs.terminal_ui import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    RESET,
    RETURN_MENU,
    YELLOW,
    alternate_screen,
    draw_screen,
    progress_bar,
    raw_keys,
    read_key,
    terminal_size,
)


class ScreenMode(Enum):
    WATCH = auto()
    LIST = auto()
    HELP = auto()


@dataclass
class WatchSession:
    lang: str
    module: str | None
    use_mock: bool
    both_langs: bool = False
    pool: list[Exercise] = field(init=False)
    index: int = field(init=False)
    mode: ScreenMode = ScreenMode.WATCH
    list_cursor: int = field(init=False)
    output_lines: list[str] = field(default_factory=list)
    last_mtime: float = 0.0
    auto_watch: bool = True

    def __post_init__(self) -> None:
        self.pool = exercise_pool(self.module)
        if not self.pool:
            raise SystemExit("No exercises found for this track.")
        saved = load_session_state()
        if (
            saved.get("lang") == self.lang
            and saved.get("module", "all") == (self.module or "all")
            and bool(saved.get("both_langs", False)) == self.both_langs
        ):
            self.index = resolve_session_index(self.pool, saved)
        else:
            self.index = 0
        self.list_cursor = self.index

    def apply_start_index(self, start_index: int | None) -> None:
        if start_index is not None:
            self.set_index(start_index)

    @property
    def exercise(self) -> Exercise:
        return self.pool[self.index]

    @property
    def source_file(self) -> Path:
        ext = "main.py" if self.lang == "python" else "main.cpp"
        return self.exercise.path / self.lang / ext

    def done_count(self) -> int:
        return track_done_count(self.pool, self.lang, both_langs=self.both_langs)

    def persist(self) -> None:
        save_session_state(
            index=self.index,
            slug=self.exercise.slug,
            lang=self.lang,
            module=self.module,
            use_mock=self.use_mock,
            both_langs=self.both_langs,
        )

    def switch_lang(self) -> None:
        self.lang = "cpp" if self.lang == "python" else "python"
        self.last_mtime = self.source_file.stat().st_mtime if self.source_file.exists() else 0.0
        self.persist()
        self.log(f"Switched to {self.lang}.")

    def log(self, message: str) -> None:
        for line in message.rstrip().splitlines():
            self.output_lines.append(line.rstrip())
        self.output_lines = self.output_lines[-40:]

    def set_index(self, index: int) -> None:
        self.index = max(0, min(index, len(self.pool) - 1))
        self.list_cursor = self.index
        self.last_mtime = self.source_file.stat().st_mtime if self.source_file.exists() else 0.0
        self.persist()

    def move(self, delta: int) -> None:
        self.set_index(self.index + delta)

    def run_current(self) -> None:
        result = run_exercise(self.exercise, self.lang, use_mock=self.use_mock, capture=True)
        if not isinstance(result, tuple):
            self.log("$ run [error — unexpected result]")
            return
        code, stdout, stderr = result
        if stdout.strip():
            self.log(stdout.rstrip())
        if stderr.strip():
            self.log("--- stderr ---")
            self.log(stderr.rstrip())
        for line in format_run_summary(
            self.exercise,
            returncode=code,
            stdout=stdout,
            stderr=stderr,
            use_mock=self.use_mock,
        ):
            self.log(line)

    def verify_current(self) -> bool:
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            ok = verify_exercise(self.exercise, self.lang, use_mock=self.use_mock)
        output = buf.getvalue().strip()
        if output:
            self.log(output)
        if ok:
            self._log_verify_success()
        return ok

    def _log_verify_success(self) -> None:
        if not self.both_langs:
            self.log("Press n for next exercise.")
            return
        if is_exercise_complete(self.exercise.slug, self.lang, both_langs=True):
            self.log("Python and C++ done. Press n for next exercise.")
            return
        other = "cpp" if self.lang == "python" else "python"
        if not is_complete(self.exercise.slug, other):
            self.log(f"{self.lang} done. Press 3 to switch to {other}, then verify again.")
            return
        self.log("Press n for next exercise.")

    def show_hint(self) -> None:
        if open_hint_in_new_terminal(self.exercise.path, slug=self.exercise.slug):
            self.log("Opened hint + peer review in new terminal (paginated).")
            return
        document = build_hint_document(self.exercise.path)
        if document:
            self.log("Could not open a new terminal. Showing hint here instead.")
            self.log(document)
        else:
            self.log("No hint available.")

    def show_readme(self) -> None:
        readme = self.exercise.path / "README.md"
        if not readme.exists():
            self.log("README not found.")
            return
        title = f"Codam — {self.exercise.slug}"
        if open_in_new_terminal(readme, title=title):
            self.log(f"Opened README in new terminal (paginated): {readme.name}")
        else:
            self.log("Could not open a new terminal. Showing README here instead.")
            self.log(readme.read_text(encoding="utf-8"))

    def reset_current(self) -> None:
        unmark_complete(self.exercise.slug, self.lang)
        self.log(f"Reset progress for {self.exercise.slug}.")

    def maybe_auto_verify(self) -> None:
        if not self.auto_watch or not self.source_file.exists():
            return
        mtime = self.source_file.stat().st_mtime
        if mtime == self.last_mtime:
            return
        self.last_mtime = mtime
        self.log(f"--- saved {self.source_file.name}, verifying ---")
        self.verify_current()

    def progress_bar(self, width: int = 30) -> str:
        return progress_bar(self.done_count(), len(self.pool), width)

    def _lang_status_line(self, slug: str) -> str:
        if not self.both_langs:
            done = is_complete(slug, self.lang)
            return f"{GREEN}done{RESET}" if done else f"{YELLOW}pending{RESET}"
        py = f"{GREEN}done{RESET}" if is_complete(slug, "python") else f"{YELLOW}todo{RESET}"
        cpp = f"{GREEN}done{RESET}" if is_complete(slug, "cpp") else f"{YELLOW}todo{RESET}"
        return f"python: {py}  |  cpp: {cpp}"

    def header_lines(self) -> list[str]:
        ex = self.exercise
        status = self._lang_status_line(ex.slug)
        mode = "mock" if self.use_mock else "live"
        track = "python+cpp" if self.both_langs else self.lang
        pct = int(100 * self.done_count() / len(self.pool))
        rel = self.source_file.relative_to(ROOT)
        return [
            f"{BOLD}Codam AI Labs{RESET}  {DIM}watch session{RESET}",
            self.progress_bar() + f"  {pct}%",
            "",
            f"{CYAN}{self.index + 1}/{len(self.pool)}{RESET}  {ex.slug}",
            f"{DIM}{ex.title}{RESET}",
            f"status: {status}  |  track: {track}  |  editing: {self.lang}  |  mode: {mode}",
            f"edit: {rel}",
        ]

    def watch_footer(self) -> str:
        return (
            f"{DIM}n{RESET}:next  {DIM}p{RESET}:prev  {DIM}s{RESET}:skip  {DIM}3{RESET}:lang  "
            f"{DIM}r{RESET}:run  {DIM}v{RESET}:verify  {DIM}h{RESET}:hint  "
            f"{DIM}o{RESET}:readme  {DIM}l{RESET}:list  {DIM}m{RESET}:menu  "
            f"{DIM}?{RESET}:help  {DIM}q{RESET}:quit"
        )

    def list_footer(self) -> str:
        return (
            f"{DIM}j/k{RESET}:move  {DIM}Enter{RESET}:open  "
            f"{DIM}Esc{RESET}:back  {DIM}m{RESET}:menu  {DIM}q{RESET}:quit"
        )

    def help_lines(self) -> list[str]:
        return [
            "Watch session commands (Rustlings-style):",
            "",
            "  n       next exercise (when current track is done)",
            "  p       previous exercise",
            "  s       skip forward without completing",
            "  3       switch language (python / cpp)",
            "  r       run your code (shows output + rubric preview)",
            "  v       verify against rubric",
            "  h       open hint + peer review in a new terminal",
            "  o       open exercise README in a new terminal",
            "  l       browse all exercises",
            "  x       reset progress on current exercise",
            "  m       back to main menu",
            "  ?       this help",
            "  q       quit session",
            "",
            "Saving your source file auto-runs verify.",
        ]

    def list_lines(self, height: int) -> list[str]:
        page_size = max(5, height - 2)
        start = max(0, min(self.list_cursor - page_size // 2, len(self.pool) - page_size))
        start = max(0, start)
        end = min(len(self.pool), start + page_size)
        lines = [f"{BOLD}Exercises{RESET}  (j/k move, Enter select, Esc back)", ""]
        for idx in range(start, end):
            ex = self.pool[idx]
            marker = ">" if idx == self.list_cursor else " "
            if idx == self.index:
                marker = "*" if idx != self.list_cursor else ">"
            state = exercise_status_label(ex.slug, self.lang, both_langs=self.both_langs)
            color = GREEN if state == "done" else (CYAN if state == "partial" else YELLOW)
            lines.append(
                f" {marker} {DIM}{idx + 1:>2}{RESET} [{color}{state:5}{RESET}] {ex.slug}"
            )
        return lines

    def render(self) -> None:
        _, rows = terminal_size()
        if self.mode == ScreenMode.HELP:
            body = self.help_lines()
            footer = f"{DIM}any key{RESET}:back  {DIM}m{RESET}:menu  {DIM}q{RESET}:quit"
        elif self.mode == ScreenMode.LIST:
            body = self.list_lines(rows - 12)
            footer = self.list_footer()
        else:
            body = list(self.output_lines)
            if not body:
                body = [
                    f"{DIM}Edit the file above, then save to auto-verify.{RESET}",
                    f"{DIM}Or press v to verify, o for README, m for menu.{RESET}",
                ]
            footer = self.watch_footer()
        draw_screen(self.header_lines(), body, footer)

    def handle_watch_key(self, key: str) -> str | None:
        """Return 'quit', 'menu', or None."""
        if key == "q":
            return "quit"
        if key == "m":
            return "menu"
        if key == "?":
            self.mode = ScreenMode.HELP
            return None
        if key == "n":
            if is_exercise_complete(self.exercise.slug, self.lang, both_langs=self.both_langs):
                if self.index + 1 < len(self.pool):
                    self.move(1)
                    self.log(f"Now at {self.exercise.slug}")
                else:
                    self.log("Track complete!")
            elif self.both_langs:
                missing = []
                if not is_complete(self.exercise.slug, "python"):
                    missing.append("python")
                if not is_complete(self.exercise.slug, "cpp"):
                    missing.append("cpp")
                self.log(
                    f"Complete both languages first ({', '.join(missing)}). "
                    "Press 3 to switch, or s to skip."
                )
            else:
                self.log("Finish or skip (s) before moving on.")
            return None
        if key == "3":
            self.switch_lang()
            return None
        if key == "p":
            if self.index > 0:
                self.move(-1)
                self.log(f"Now at {self.exercise.slug}")
            return None
        if key == "s":
            if self.index + 1 < len(self.pool):
                self.move(1)
                self.log(f"Skipped to {self.exercise.slug}")
            else:
                self.log("Already at last exercise.")
            return None
        if key == "r":
            self.run_current()
            return None
        if key == "v":
            self.verify_current()
            return None
        if key == "h":
            self.show_hint()
            return None
        if key == "o":
            self.show_readme()
            return None
        if key == "l":
            self.mode = ScreenMode.LIST
            self.list_cursor = self.index
            return None
        if key == "x":
            self.reset_current()
            return None
        return None

    def handle_list_key(self, key: str) -> str | None:
        if key == "q":
            return "quit"
        if key == "m":
            return "menu"
        if key in {"\x1b", "\x03"}:
            self.mode = ScreenMode.WATCH
            return None
        if key == "j":
            self.list_cursor = min(self.list_cursor + 1, len(self.pool) - 1)
            return None
        if key == "k":
            self.list_cursor = max(self.list_cursor - 1, 0)
            return None
        if key in {"\r", "\n"}:
            self.set_index(self.list_cursor)
            self.mode = ScreenMode.WATCH
            self.log(f"Opened {self.exercise.slug}")
            return None
        return None

    def handle_help_key(self, key: str) -> str | None:
        if key == "q":
            return "quit"
        if key == "m":
            return "menu"
        self.mode = ScreenMode.WATCH
        return None

    def handle_key(self, key: str) -> str | None:
        if self.mode == ScreenMode.LIST:
            return self.handle_list_key(key)
        if self.mode == ScreenMode.HELP:
            return self.handle_help_key(key)
        return self.handle_watch_key(key)


def run_session(
    lang: str,
    module: str | None,
    use_mock: bool,
    *,
    both_langs: bool = False,
    start_index: int | None = None,
) -> int:
    if not sys.stdout.isatty():
        print(
            "Interactive session needs a TTY. Use: codam-labs watch",
            file=sys.stderr,
        )
        return 1

    session = WatchSession(
        lang=lang,
        module=module,
        use_mock=use_mock,
        both_langs=both_langs,
    )
    session.apply_start_index(start_index)
    session.persist()
    session.log(f"Session started at {session.exercise.slug}.")

    with alternate_screen(), raw_keys():
        try:
            while True:
                session.maybe_auto_verify()
                session.render()
                key = read_key(0.25)
                if key is None:
                    continue
                action = session.handle_key(key)
                if action == "quit":
                    break
                if action == "menu":
                    return RETURN_MENU
        except KeyboardInterrupt:
            pass

    print(f"\nSession closed at {session.exercise.slug}. Resume with: codam-labs")
    return 0
