"""Discover and manage exercise progress."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "core" / "exercises"
MODULES_DIR = ROOT / "modules"
PROGRESS_FILE = ROOT / ".codam-ai-labs" / "progress.json"
SESSION_FILE = ROOT / ".codam-ai-labs" / "session.json"
TRACK_LANGS = ("python", "cpp")


@dataclass(frozen=True)
class Exercise:
    id: str
    title: str
    path: Path
    module: str = "core"

    @property
    def slug(self) -> str:
        if self.module == "core":
            return self.path.name
        return f"{self.module}/{self.path.name}"


def _title_from_readme(path: Path) -> str:
    readme = path / "README.md"
    if readme.exists():
        first = readme.read_text(encoding="utf-8").splitlines()[0]
        if first.startswith("#"):
            return first.lstrip("# ").strip()
    return path.name


def _discover_module_exercises(module: str) -> list[Exercise]:
    base = MODULES_DIR / module / "exercises"
    if not base.exists():
        return []
    exercises: list[Exercise] = []
    for folder in sorted(base.iterdir()):
        if not folder.is_dir():
            continue
        ex_id = folder.name.split("_", 1)[0]
        exercises.append(Exercise(ex_id, _title_from_readme(folder), folder, module=module))
    return exercises


MODULE_NAMES = [
    "prompt_engineering",
    "structured_output",
    "embeddings",
    "rag",
    "tools",
    "agents",
    "local_llm",
    "production",
    "advanced_patterns",
    "mcp",
    "security",
    "ollama",
]

CORE_EXERCISES: list[Exercise] = [
    Exercise("01", "Environment variables", CORE_DIR / "01_env_vars"),
    Exercise("02", "HTTP GET and JSON", CORE_DIR / "02_http_get"),
    Exercise("03", "HTTP POST", CORE_DIR / "03_http_post"),
    Exercise("04", "First LLM call", CORE_DIR / "04_llm_first_call"),
    Exercise("05", "System and user prompts", CORE_DIR / "05_system_user_prompts"),
    Exercise("06", "Conversation history", CORE_DIR / "06_conversation_history"),
    Exercise("07", "Temperature and max_tokens", CORE_DIR / "07_output_control"),
    Exercise("08", "Streaming", CORE_DIR / "08_streaming"),
    Exercise("09", "Timeout and retry", CORE_DIR / "09_timeout_retry"),
    Exercise("10", "Dirty JSON", CORE_DIR / "10_dirty_json"),
]

MODULE_EXERCISES: list[Exercise] = []
for name in MODULE_NAMES:
    MODULE_EXERCISES.extend(_discover_module_exercises(name))

ALL_EXERCISES: list[Exercise] = CORE_EXERCISES + MODULE_EXERCISES


def exercises_for(module: str | None = None) -> list[Exercise]:
    if module is None or module == "core":
        return CORE_EXERCISES
    if module == "all":
        return ALL_EXERCISES
    return _discover_module_exercises(module)


def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {"completed": {}}
    return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))


def save_progress(data: dict) -> None:
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def mark_complete(slug: str, lang: str, via: str = "verify") -> None:
    data = load_progress()
    completed = data.setdefault("completed", {})
    langs = set(completed.get(slug, []))
    langs.add(lang)
    completed[slug] = sorted(langs)
    if via == "peer_review":
        peer = data.setdefault("peer_reviewed", {})
        plangs = set(peer.get(slug, []))
        plangs.add(lang)
        peer[slug] = sorted(plangs)
    save_progress(data)


def exercise_pool(module: str | None = None) -> list[Exercise]:
    """Ordered exercise list for the interactive session."""
    if module in (None, "all"):
        return ALL_EXERCISES
    return exercises_for(module)


def unmark_complete(slug: str, lang: str) -> None:
    data = load_progress()
    completed = data.setdefault("completed", {})
    langs = [value for value in completed.get(slug, []) if value != lang]
    if langs:
        completed[slug] = langs
    else:
        completed.pop(slug, None)
    peer = data.setdefault("peer_reviewed", {})
    plangs = [value for value in peer.get(slug, []) if value != lang]
    if plangs:
        peer[slug] = plangs
    else:
        peer.pop(slug, None)
    save_progress(data)


def load_session_state() -> dict:
    if not SESSION_FILE.exists():
        return {}
    return json.loads(SESSION_FILE.read_text(encoding="utf-8"))


def save_session_state(
    *,
    index: int,
    slug: str,
    lang: str,
    module: str | None,
    use_mock: bool = False,
    both_langs: bool = False,
) -> None:
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_FILE.write_text(
        json.dumps(
            {
                "index": index,
                "slug": slug,
                "lang": lang,
                "module": module or "all",
                "use_mock": use_mock,
                "both_langs": both_langs,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def load_preferences() -> dict:
    data = load_session_state()
    return {
        "lang": data.get("lang", "python"),
        "module": data.get("module", "all"),
        "use_mock": bool(data.get("use_mock", False)),
        "both_langs": bool(data.get("both_langs", False)),
        "slug": data.get("slug"),
        "index": int(data.get("index", 0)),
    }


def save_preferences(
    *,
    lang: str,
    module: str | None,
    use_mock: bool,
    both_langs: bool = False,
) -> None:
    existing = load_session_state()
    pool = exercise_pool(module if module != "all" else "all")
    index = int(existing.get("index", 0))
    slug = existing.get("slug", pool[0].slug if pool else "")
    if slug and pool:
        index = resolve_session_index(pool, {"slug": slug, "index": index})
    save_session_state(
        index=index,
        slug=slug or (pool[index].slug if pool else ""),
        lang=lang,
        module=module,
        use_mock=use_mock,
        both_langs=both_langs,
    )


def resolve_session_index(pool: list[Exercise], saved: dict) -> int:
    slug = saved.get("slug")
    if slug:
        for idx, exercise in enumerate(pool):
            if exercise.slug == slug:
                return idx
    index = int(saved.get("index", 0))
    if not pool:
        return 0
    return max(0, min(index, len(pool) - 1))


def reset_progress() -> None:
    """Clear local exercise completion state (student progress only)."""
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


def is_complete(slug: str, lang: str) -> bool:
    data = load_progress()
    return lang in data.get("completed", {}).get(slug, [])


def is_exercise_complete(slug: str, lang: str, *, both_langs: bool = False) -> bool:
    """True when the exercise is done for the active track (one or both languages)."""
    if both_langs:
        return all(is_complete(slug, track) for track in TRACK_LANGS)
    return is_complete(slug, lang)


def track_done_count(
    pool: list[Exercise],
    lang: str,
    *,
    both_langs: bool = False,
) -> int:
    return sum(
        1 for ex in pool if is_exercise_complete(ex.slug, lang, both_langs=both_langs)
    )


def exercise_status_label(slug: str, lang: str, *, both_langs: bool = False) -> str:
    if not both_langs:
        return "done" if is_complete(slug, lang) else "todo"
    py = is_complete(slug, "python")
    cpp = is_complete(slug, "cpp")
    if py and cpp:
        return "done"
    if py or cpp:
        return "partial"
    return "todo"


def find_exercise(query: str | None, module: str | None = None) -> Exercise | None:
    if not query:
        return next_incomplete(module=module)
    query = query.strip().lower()
    pool = exercises_for(module if module and module != "all" else None)
    if module == "all":
        pool = ALL_EXERCISES
    for ex in pool:
        candidates = {
            ex.id,
            ex.slug,
            ex.path.name,
            ex.slug.replace("_", "-"),
            f"core/{ex.slug}" if ex.module == "core" else ex.slug,
        }
        if query in candidates or query.endswith(ex.path.name):
            return ex
    # search all if not found in pool
    for ex in ALL_EXERCISES:
        if query in {ex.slug, ex.path.name, f"{ex.module}/{ex.path.name}"}:
            return ex
    return None


def next_incomplete(
    lang: str = "python",
    module: str | None = None,
    *,
    both_langs: bool = False,
) -> Exercise | None:
    for ex in exercises_for(module):
        if not is_exercise_complete(ex.slug, lang, both_langs=both_langs):
            return ex
    return None
