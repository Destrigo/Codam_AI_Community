"""Interactive start menu for Codam AI Labs."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum, auto

from codam_ai_labs.business_cases import CASES
from codam_ai_labs.capstones import CAPSTONES
from codam_ai_labs.config import load_dotenv_if_present, mistral_api_key
from codam_ai_labs.exercises import (
    ALL_EXERCISES,
    CORE_EXERCISES,
    MODULE_NAMES,
    Exercise,
    exercise_pool,
    exercise_status_label,
    exercises_for,
    is_complete,
    is_exercise_complete,
    load_preferences,
    next_incomplete,
    reset_progress,
    resolve_session_index,
    save_preferences,
    save_session_state,
    track_done_count,
)
from codam_ai_labs.session import run_session
from codam_ai_labs.terminal_ui import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    MAGENTA,
    RED,
    RESET,
    YELLOW,
    alternate_screen,
    draw_screen,
    progress_bar,
    raw_keys,
    read_key,
    RETURN_MENU,
    terminal_size,
)

ROADMAP_LINES = [
    "Suggested learning path:",
    "",
    "  core (10)  — required foundation",
    "    -> prompt_engineering (6) -> structured_output (5)",
    "    -> embeddings (5) -> rag (7)",
    "    -> tools (6) -> agents (6) -> mcp (6)",
    "    -> local_llm (4) -> ollama (6)",
    "    -> production (6) -> security (6) | advanced_patterns (5)",
    "    -> capstones (3) -> business_cases (3)",
    "",
    "Parallel tracks after core:",
    "  - local_llm / ollama  (run models on your machine)",
    "  - production / security  (reliability & safety)",
    "  - advanced_patterns  (map-reduce, routing, evals)",
    "",
    "Capstones (after relevant modules):",
    "  01 doc_assistant_rag   — mini-RAG over local docs",
    "  02 ops_agent           — tool-using agent",
    "  03 llm_gateway         — production LLM pipeline",
    "",
    "Business cases (workshop scenarios):",
    "  01 retail catalog harmonization",
    "  02 finance invoice ingestion",
    "  03 insurance claims intake",
]


class MenuMode(Enum):
    MAIN = auto()
    PROGRESS = auto()
    ROADMAP = auto()
    PICK = auto()
    EXTRAS = auto()
    HELP = auto()
    CONFIRM_RESET = auto()
    MESSAGE = auto()


@dataclass
class MenuState:
    lang: str
    module: str
    use_mock: bool
    both_langs: bool = False
    mode: MenuMode = MenuMode.MAIN
    scroll: int = 0
    pick_cursor: int = 0
    message: str = ""
    pool: list[Exercise] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.pool = exercise_pool(self.module if self.module != "all" else "all")
        prefs = load_preferences()
        if prefs.get("slug"):
            self.pick_cursor = resolve_session_index(self.pool, prefs)

    def persist(self) -> None:
        save_preferences(
            lang=self.lang,
            module=self.module,
            use_mock=self.use_mock,
            both_langs=self.both_langs,
        )

    def done_count(self) -> int:
        return track_done_count(self.pool, self.lang, both_langs=self.both_langs)

    def resume_exercise(self) -> Exercise:
        prefs = load_preferences()
        if prefs.get("slug"):
            idx = resolve_session_index(self.pool, prefs)
            return self.pool[idx]
        nxt = next_incomplete(
            self.lang,
            self.module if self.module != "all" else "all",
            both_langs=self.both_langs,
        )
        return nxt or self.pool[0]

    def resume_index(self) -> int:
        return resolve_session_index(self.pool, load_preferences())

    def header(self) -> list[str]:
        done = self.done_count()
        total = len(self.pool)
        pct = int(100 * done / total) if total else 0
        mode = f"{YELLOW}mock{RESET}" if self.use_mock else f"{GREEN}live{RESET}"
        resume = self.resume_exercise()
        key_status = (
            f"{GREEN}.env ok{RESET}"
            if self.use_mock or mistral_api_key()
            else f"{RED}no API key{RESET} (use mock or set .env)"
        )
        if self.both_langs:
            lang_label = f"{CYAN}python+cpp{RESET}"
        else:
            lang_label = f"{CYAN}{self.lang}{RESET}"
        return [
            f"{BOLD}Codam AI Labs{RESET}  {DIM}main menu{RESET}",
            progress_bar(done, total) + f"  {pct}%  |  {lang_label}  |  {mode}",
            f"resume: {resume.slug}  |  {key_status}",
        ]


def _main_body(state: MenuState) -> list[str]:
    resume = state.resume_exercise()
    mock_label = "offline" if state.use_mock else "live"
    lang_other = "cpp" if state.lang == "python" else "python"
    dual_label = "on (both required)" if state.both_langs else "off"
    return [
        "",
        f"  {BOLD}0{RESET}  Dual language track       {DIM}current: {dual_label}{RESET}",
        f"  {BOLD}1{RESET}  Resume watch session     {DIM}({resume.slug}){RESET}",
        f"  {BOLD}2{RESET}  Pick exercise            {DIM}(browse all {len(state.pool)}){RESET}",
        f"  {BOLD}3{RESET}  Switch language          {DIM}current: {state.lang} -> {lang_other}{RESET}",
        f"  {BOLD}4{RESET}  Progress by module",
        f"  {BOLD}5{RESET}  Learning roadmap",
        f"  {BOLD}6{RESET}  Toggle API mode          {DIM}current: {mock_label}{RESET}",
        f"  {BOLD}7{RESET}  Capstones & business cases",
        f"  {BOLD}8{RESET}  Reset all progress",
        f"  {BOLD}9{RESET}  Watch session help",
        "",
        f"  {DIM}Press 0-9, Enter=resume, q=quit{RESET}",
    ]


def _module_done_count(exercises: list[Exercise], state: MenuState) -> int:
    if state.both_langs:
        return sum(
            1 for ex in exercises if is_exercise_complete(ex.slug, state.lang, both_langs=True)
        )
    return sum(1 for ex in exercises if is_complete(ex.slug, state.lang))


def _progress_row(name: str, done: int, total: int, *, bar_width: int = 12) -> str:
    return f"  {name:<18} {progress_bar(done, total, width=bar_width)}"


def _progress_body(state: MenuState) -> list[str]:
    track = "python+cpp" if state.both_langs else state.lang
    lines = [f"{BOLD}Progress{RESET}  ({track})", ""]
    core_done = _module_done_count(CORE_EXERCISES, state)
    lines.append(_progress_row("core", core_done, len(CORE_EXERCISES)))
    for name in MODULE_NAMES:
        exs = exercises_for(name)
        done = _module_done_count(exs, state)
        lines.append(_progress_row(name, done, len(exs)))
    total_done = state.done_count()
    lines.extend(["", f"  {BOLD}total{RESET}{' ' * 11}{progress_bar(total_done, len(ALL_EXERCISES), width=16)}"])
    nxt = next_incomplete(state.lang, "all", both_langs=state.both_langs)
    if nxt:
        lines.append(f"  next todo: {nxt.slug}")
    else:
        lines.append(f"  {GREEN}All exercises complete!{RESET}")
    return lines


def _pick_body(state: MenuState) -> list[str]:
    lines = [f"{BOLD}Pick exercise{RESET}  (j/k move, Enter=open, Esc=back)", ""]
    _, rows = terminal_size()
    page = max(8, rows - 14)
    start = max(0, min(state.pick_cursor - page // 2, len(state.pool) - page))
    end = min(len(state.pool), start + page)
    for idx in range(start, end):
        ex = state.pool[idx]
        marker = ">" if idx == state.pick_cursor else " "
        if idx == state.resume_index():
            marker = "*" if idx != state.pick_cursor else ">"
        status = exercise_status_label(ex.slug, state.lang, both_langs=state.both_langs)
        color = GREEN if status == "done" else (CYAN if status == "partial" else YELLOW)
        lines.append(
            f" {marker} {DIM}{idx + 1:>2}{RESET} [{color}{status:5}{RESET}] {ex.slug}"
        )
    return lines


def _extras_body() -> list[str]:
    lines = [f"{BOLD}Capstones & business cases{RESET}", ""]
    lines.append(f"{MAGENTA}Capstones{RESET} (Python reference solutions):")
    for cap in CAPSTONES:
        lines.append(f"  - {cap.slug}")
    lines.extend(["", f"{MAGENTA}Business cases{RESET} (ingestion workshops):"])
    for case in CASES:
        lines.append(f"  - {case.slug}")
    lines.extend(
        [
            "",
            "Run from a separate shell:",
            "  codam-labs --mock capstone run 03_llm_gateway -- complete --prompt OK",
            "  codam-labs --mock business run 01_retail_catalog_harmonization",
        ]
    )
    return lines


def _help_body() -> list[str]:
    return [
        f"{BOLD}Watch session keys{RESET} (after Resume):",
        "",
        "  n       next (when done)     p       previous",
        "  s       skip forward         3       switch language",
        "  r       run code",
        "  v       verify               h       hint (new terminal)",
        "  o       README (new window)  l       exercise list",
        "  x       reset exercise       m       back to this menu",
        "  ?       help                 q       quit",
        "",
        "Saving your source file auto-runs verify.",
    ]


def _render(state: MenuState) -> None:
    if state.mode == MenuMode.MAIN:
        draw_screen(state.header(), _main_body(state), f"{DIM}0-9{RESET} select  {DIM}Enter{RESET} resume  {DIM}q{RESET} quit")
        return
    if state.mode == MenuMode.PROGRESS:
        body = _progress_body(state)
        draw_screen(state.header(), body, f"{DIM}Esc{RESET} back  {DIM}q{RESET} quit")
        return
    if state.mode == MenuMode.ROADMAP:
        body = ROADMAP_LINES[state.scroll : state.scroll + 20]
        draw_screen(state.header(), body, f"{DIM}j/k{RESET} scroll  {DIM}Esc{RESET} back  {DIM}q{RESET} quit")
        return
    if state.mode == MenuMode.PICK:
        draw_screen(state.header(), _pick_body(state), f"{DIM}j/k{RESET} move  {DIM}Enter{RESET} open  {DIM}Esc{RESET} back")
        return
    if state.mode == MenuMode.EXTRAS:
        draw_screen(state.header(), _extras_body(), f"{DIM}Esc{RESET} back  {DIM}q{RESET} quit")
        return
    if state.mode == MenuMode.HELP:
        draw_screen(state.header(), _help_body(), f"{DIM}Esc{RESET} back  {DIM}q{RESET} quit")
        return
    if state.mode == MenuMode.CONFIRM_RESET:
        draw_screen(
            state.header(),
            [
                "",
                f"  {RED}{BOLD}Reset all progress?{RESET}",
                "",
                "  This clears completed exercises and session position.",
                "  Your source files are NOT modified.",
                "",
                "  y = yes, reset everything",
                "  n / Esc = cancel",
            ],
            f"{DIM}y{RESET} confirm  {DIM}Esc{RESET} cancel",
        )
        return
    if state.mode == MenuMode.MESSAGE:
        draw_screen(
            state.header(),
            ["", state.message, "", f"{DIM}Press any key...{RESET}"],
            "",
        )


def _enter_watch(state: MenuState, index: int | None = None) -> int:
    idx = state.resume_index() if index is None else index
    slug = state.pool[idx].slug
    save_session_state(
        index=idx,
        slug=slug,
        lang=state.lang,
        module=state.module,
        use_mock=state.use_mock,
        both_langs=state.both_langs,
    )
    state.persist()
    return run_session(
        state.lang,
        state.module if state.module != "all" else "all",
        state.use_mock,
        both_langs=state.both_langs,
        start_index=idx,
    )


def _handle_main(state: MenuState, key: str) -> str | None:
    if key == "q":
        return "quit"
    if key == "0":
        state.both_langs = not state.both_langs
        state.persist()
        return None
    if key in {"\r", "\n", "1"}:
        return "watch"
    if key == "2":
        state.mode = MenuMode.PICK
        state.pick_cursor = state.resume_index()
        return None
    if key == "3":
        state.lang = "cpp" if state.lang == "python" else "python"
        state.persist()
        return None
    if key == "4":
        state.mode = MenuMode.PROGRESS
        return None
    if key == "5":
        state.mode = MenuMode.ROADMAP
        state.scroll = 0
        return None
    if key == "6":
        state.use_mock = not state.use_mock
        state.persist()
        return None
    if key == "7":
        state.mode = MenuMode.EXTRAS
        return None
    if key == "8":
        state.mode = MenuMode.CONFIRM_RESET
        return None
    if key == "9":
        state.mode = MenuMode.HELP
        return None
    return None


def _handle_pick(state: MenuState, key: str) -> str | None:
    if key == "q":
        return "quit"
    if key in {"\x1b", "\x03"}:
        state.mode = MenuMode.MAIN
        return None
    if key == "j":
        state.pick_cursor = min(state.pick_cursor + 1, len(state.pool) - 1)
        return None
    if key == "k":
        state.pick_cursor = max(state.pick_cursor - 1, 0)
        return None
    if key in {"\r", "\n"}:
        save_session_state(
            index=state.pick_cursor,
            slug=state.pool[state.pick_cursor].slug,
            lang=state.lang,
            module=state.module,
            use_mock=state.use_mock,
            both_langs=state.both_langs,
        )
        return "watch_pick"
    return None


def _handle_sub(state: MenuState, key: str) -> str | None:
    if key == "q":
        return "quit"
    if key in {"\x1b", "\x03"}:
        state.mode = MenuMode.MAIN
        return None
    if state.mode == MenuMode.ROADMAP:
        if key == "j":
            state.scroll = min(state.scroll + 1, max(0, len(ROADMAP_LINES) - 1))
        if key == "k":
            state.scroll = max(state.scroll - 1, 0)
    if state.mode == MenuMode.CONFIRM_RESET:
        if key == "y":
            reset_progress()
            state.message = "Progress cleared."
            state.mode = MenuMode.MESSAGE
            state.pick_cursor = 0
        if key == "n":
            state.mode = MenuMode.MAIN
    if state.mode == MenuMode.MESSAGE:
        state.mode = MenuMode.MAIN
    return None


def run_menu(
    lang: str = "python",
    module: str = "all",
    use_mock: bool | None = None,
    both_langs: bool | None = None,
) -> int:
    if not sys.stdout.isatty():
        print("Interactive menu needs a TTY. Use: codam-labs watch", file=sys.stderr)
        return 1

    load_dotenv_if_present()
    prefs = load_preferences()
    state = MenuState(
        lang=lang if lang else prefs["lang"],
        module=module or prefs.get("module", "all"),
        use_mock=prefs["use_mock"] if use_mock is None else use_mock,
        both_langs=prefs.get("both_langs", False) if both_langs is None else both_langs,
    )
    state.persist()

    with alternate_screen(), raw_keys():
        try:
            while True:
                _render(state)
                key = read_key(0.25)
                if key is None:
                    continue

                action: str | None = None
                if state.mode == MenuMode.MAIN:
                    action = _handle_main(state, key)
                elif state.mode == MenuMode.PICK:
                    action = _handle_pick(state, key)
                else:
                    action = _handle_sub(state, key)

                if action == "quit":
                    return 0
                if action == "watch":
                    code = _enter_watch(state)
                    if code != RETURN_MENU:
                        return code
                    state.mode = MenuMode.MAIN
                if action == "watch_pick":
                    code = _enter_watch(state, index=state.pick_cursor)
                    if code != RETURN_MENU:
                        return code
                    state.mode = MenuMode.MAIN
        except KeyboardInterrupt:
            pass
    return 0
