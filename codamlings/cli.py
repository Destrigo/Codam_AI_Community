"""Codamlings CLI — rustlings-style."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from codamlings.exercises import (
    CORE_EXERCISES,
    MODULE_NAMES,
    find_exercise,
    is_complete,
    next_incomplete,
    exercises_for,
)
from codamlings.verify import run_exercise, verify_all, verify_exercise


def _print_list(lang: str, module: str | None) -> None:
    if module in (None, "core"):
        print("Core exercises:\n")
        for ex in CORE_EXERCISES:
            status = "done" if is_complete(ex.slug, lang) else "todo"
            print(f"  [{status}] {ex.id} {ex.slug} — {ex.title}")
    if module is None:
        print("\nModules:\n")
        for name in MODULE_NAMES:
            exs = exercises_for(name)
            done = sum(1 for e in exs if is_complete(e.slug, lang))
            print(f"  {name}: {done}/{len(exs)}")
        print("\nUse: codamlings list --module rag")
        return
    if module != "core":
        print(f"\n{module} exercises:\n")
        for ex in exercises_for(module):
            status = "done" if is_complete(ex.slug, lang) else "todo"
            print(f"  [{status}] {ex.id} {ex.slug} — {ex.title}")


def _show_hint(exercise_path: Path) -> None:
    hint = exercise_path / "hint.md"
    readme = exercise_path / "README.md"
    if hint.exists():
        print(hint.read_text(encoding="utf-8"))
    elif readme.exists():
        print("(hint.md missing — read the Assignment section in README.md)\n")
        print(readme.read_text(encoding="utf-8"))
    else:
        print("No hint found.")


def _watch(lang: str, module: str | None) -> int:
    exercise = next_incomplete(lang, module=module)
    if not exercise:
        print("All exercises complete for this track!")
        return 0
    target = exercise.path / lang / ("main.py" if lang == "python" else "main.cpp")
    print(f"Watching {target.name} — save to re-run verify.")
    print(f"Current: {exercise.slug}\n")
    last_mtime = target.stat().st_mtime if target.exists() else 0
    while True:
        if target.exists():
            mtime = target.stat().st_mtime
            if mtime != last_mtime:
                last_mtime = mtime
                print(f"\n--- verify {exercise.slug} [{lang}] ---")
                if verify_exercise(exercise, lang):
                    nxt = next_incomplete(lang, module=module)
                    if nxt:
                        exercise = nxt
                        target = exercise.path / lang / ("main.py" if lang == "python" else "main.cpp")
                        last_mtime = target.stat().st_mtime if target.exists() else 0
                        print(f"\nNext: {exercise.slug}")
                    else:
                        print("\nTrack complete!")
                        return 0
        time.sleep(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="codamlings", description="Interactive AI exercises")
    parser.add_argument("--lang", choices=["python", "cpp"], default="python")
    parser.add_argument("--module", choices=["core", *MODULE_NAMES, "all"], default=None)

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list", help="List exercises and progress")
    run_p = sub.add_parser("run", help="Run an exercise")
    run_p.add_argument("exercise", nargs="?", help="Exercise slug or id")
    run_p.add_argument("--mock", action="store_true", help="Use local mock")
    hint_p = sub.add_parser("hint", help="Show hint")
    hint_p.add_argument("exercise", nargs="?", help="Exercise slug or id")
    verify_p = sub.add_parser("verify", help="Verify exercises")
    verify_p.add_argument("exercise", nargs="?", help="Slug, id, or 'all'")
    sub.add_parser("watch", help="Verify on save")

    args = parser.parse_args(argv)
    lang: str = args.lang
    module: str | None = args.module

    if args.command is None:
        exercise = next_incomplete(lang, module=module or "core")
        if exercise:
            print(f"Next: {exercise.slug} — {exercise.title}\n")
            readme = exercise.path / "README.md"
            if readme.exists():
                print(readme.read_text(encoding="utf-8"))
            print("\nUseful commands:")
            print(f"  codamlings run {exercise.path.name} --lang {lang}")
            print(f"  codamlings verify {exercise.path.name} --lang {lang}")
        else:
            print("Core complete! Try: codamlings list --module rag")
        return

    if args.command == "list":
        _print_list(lang, module)
        return

    if args.command == "run":
        exercise = find_exercise(args.exercise, module=module) or next_incomplete(lang, module)
        if not exercise:
            print("No exercise found.")
            sys.exit(1)
        sys.exit(run_exercise(exercise, lang, use_mock=args.mock))

    if args.command == "hint":
        exercise = find_exercise(args.exercise, module=module) or next_incomplete(lang, module)
        if not exercise:
            print("No exercise found.")
            sys.exit(1)
        _show_hint(exercise.path)
        return

    if args.command == "verify":
        if args.exercise in (None, "all"):
            sys.exit(verify_all(lang, module=module or ("all" if args.exercise == "all" else "core")))
        exercise = find_exercise(args.exercise, module=module)
        if not exercise:
            print(f"Exercise not found: {args.exercise}")
            sys.exit(1)
        sys.exit(0 if verify_exercise(exercise, lang) else 1)

    if args.command == "watch":
        sys.exit(_watch(lang, module=module or "core"))


if __name__ == "__main__":
    main()
