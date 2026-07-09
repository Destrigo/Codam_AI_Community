"""Codam AI Labs CLI — rustlings-style."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from codam_ai_labs.config import load_dotenv_if_present
from codam_ai_labs.exercises import (
    CORE_EXERCISES,
    MODULE_NAMES,
    find_exercise,
    is_complete,
    load_preferences,
    next_incomplete,
    exercises_for,
    reset_progress,
)
from codam_ai_labs.review import approve_review, list_pending, show_rubric, submit_for_review
from codam_ai_labs.capstones import CAPSTONES, find_capstone, run_capstone
from codam_ai_labs.business_cases import CASES, find_case, run_case
from codam_ai_labs.menu import run_menu
from codam_ai_labs.terminal_viewer import build_hint_document, open_hint_in_new_terminal
from codam_ai_labs.session import run_session
from codam_ai_labs.verify import format_run_summary, run_exercise, verify_all, verify_exercise

load_dotenv_if_present()


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
        print("\nUse: codam-labs --module rag list")
        return
    if module != "core":
        print(f"\n{module} exercises:\n")
        for ex in exercises_for(module):
            status = "done" if is_complete(ex.slug, lang) else "todo"
            print(f"  [{status}] {ex.id} {ex.slug} — {ex.title}")


def _show_hint(exercise_path: Path, slug: str, *, show_solution: bool = False) -> None:
    if show_solution:
        sol_py = exercise_path / "solution" / "python" / "main.py"
        if sol_py.exists():
            print("=== Instructor solution (do not share) ===\n")
            print(sol_py.read_text(encoding="utf-8"))
            return
    if sys.stdout.isatty() and open_hint_in_new_terminal(exercise_path, slug=slug):
        print(f"Opened hint + peer review in new terminal: {slug}")
        return
    document = build_hint_document(exercise_path)
    if document:
        print(document)
    else:
        print("No hint available.")


def _watch(lang: str, module: str | None, use_mock: bool, *, both_langs: bool) -> int:
    return run_session(lang, module or "all", use_mock, both_langs=both_langs)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="codam-labs", description="Interactive AI exercises")
    parser.add_argument("--lang", choices=["python", "cpp"], default="python")
    parser.add_argument("--module", choices=["core", *MODULE_NAMES, "all"], default=None)
    parser.add_argument("--mock", action="store_true", help="Offline mock (CI only)")
    parser.add_argument(
        "--both-langs",
        action="store_true",
        help="Require both python and cpp before advancing to the next exercise",
    )

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list", help="List exercises and progress")

    run_p = sub.add_parser("run", help="Run an exercise (live Mistral by default)")
    run_p.add_argument("exercise", nargs="?", help="Exercise slug or id")

    hint_p = sub.add_parser("hint", help="Peer review rubric + hint (not solution)")
    hint_p.add_argument("exercise", nargs="?", help="Exercise slug or id")
    hint_p.add_argument("--solution", action="store_true", help="Show instructor solution")

    verify_p = sub.add_parser("verify", help="Verify exercises (live Mistral by default)")
    verify_p.add_argument("exercise", nargs="?", help="Slug, id, or 'all'")

    sub.add_parser("watch", help="Interactive watch session (Rustlings-style)")

    sub.add_parser("menu", help="Interactive start menu (default)")

    session_p = sub.add_parser("session", help="Same as watch — interactive exercise session")

    sub.add_parser("reset", help="Clear local progress (.codam-ai-labs/progress.json)")

    review_p = sub.add_parser("review", help="Peer review workflow")
    review_sub = review_p.add_subparsers(dest="review_cmd")
    rubric_p = review_sub.add_parser("rubric", help="Show peer review checklist")
    rubric_p.add_argument("exercise", nargs="?", help="Exercise slug")
    submit_p = review_sub.add_parser("submit", help="Submit code for peer review")
    submit_p.add_argument("exercise", nargs="?", help="Exercise slug")
    submit_p.add_argument("--author", default="student")
    review_sub.add_parser("pending", help="List pending submissions")
    approve_p = review_sub.add_parser("approve", help="Approve peer review (marks complete)")
    approve_p.add_argument("exercise", help="Exercise slug")
    approve_p.add_argument("--reviewer", default="peer")

    cap_p = sub.add_parser("capstone", help="Capstone projects")
    cap_sub = cap_p.add_subparsers(dest="cap_cmd")
    cap_sub.add_parser("list", help="List capstones")
    cap_run = cap_sub.add_parser("run", help="Run capstone solution CLI")
    cap_run.add_argument("name", help="Capstone slug or id")
    cap_run.add_argument("args", nargs=argparse.REMAINDER, help="Args passed to capstone main.py")
    cap_sol = cap_sub.add_parser("solution", help="Show capstone reference entrypoint path")
    cap_sol.add_argument("name", help="Capstone slug")

    bus_p = sub.add_parser("business", help="Business case pipelines")
    bus_sub = bus_p.add_subparsers(dest="bus_cmd")
    bus_sub.add_parser("list", help="List business cases")
    bus_run = bus_sub.add_parser("run", help="Run business case pipeline")
    bus_run.add_argument("name", help="Case slug or id")
    bus_run.add_argument("args", nargs=argparse.REMAINDER, help="Extra args for pipeline")

    args = parser.parse_args(argv)
    lang: str = args.lang
    module: str | None = args.module
    use_mock: bool = args.mock
    prefs = load_preferences()
    both_langs: bool = args.both_langs or bool(prefs.get("both_langs", False))

    if args.command is None:
        sys.exit(
            run_menu(
                lang=lang,
                module=module or "all",
                use_mock=use_mock if use_mock else None,
                both_langs=both_langs if args.both_langs else None,
            )
        )
        return

    if args.command == "menu":
        sys.exit(
            run_menu(
                lang=lang,
                module=module or "all",
                use_mock=use_mock if use_mock else None,
                both_langs=both_langs if args.both_langs else None,
            )
        )
        return

    if args.command == "reset":
        reset_progress()
        print("Progress cleared. Run codam-labs to open the menu.")
        return

    if args.command == "list":
        _print_list(lang, module)
        return

    if args.command == "run":
        exercise = find_exercise(args.exercise, module=module) or next_incomplete(lang, module)
        if not exercise:
            print("No exercise found.")
            sys.exit(1)
        result = run_exercise(exercise, lang, use_mock=use_mock, capture=True)
        if not isinstance(result, tuple):
            sys.exit(1)
        code, stdout, stderr = result
        if stdout:
            print(stdout, end="" if stdout.endswith("\n") else "\n")
        if stderr:
            print(stderr, file=sys.stderr, end="" if stderr.endswith("\n") else "\n")
        for line in format_run_summary(
            exercise,
            returncode=code,
            stdout=stdout,
            stderr=stderr,
            use_mock=use_mock,
        ):
            print(line)
        sys.exit(code)

    if args.command == "hint":
        exercise = find_exercise(args.exercise, module=module) or next_incomplete(lang, module)
        if not exercise:
            print("No exercise found.")
            sys.exit(1)
        _show_hint(exercise.path, exercise.slug, show_solution=getattr(args, "solution", False))
        return

    if args.command == "verify":
        if args.exercise in (None, "all"):
            sys.exit(verify_all(lang, module=module or ("all" if args.exercise == "all" else "core"), use_mock=use_mock))
        exercise = find_exercise(args.exercise, module=module)
        if not exercise:
            print(f"Exercise not found: {args.exercise}")
            sys.exit(1)
        sys.exit(0 if verify_exercise(exercise, lang, use_mock=use_mock) else 1)

    if args.command == "watch":
        sys.exit(_watch(lang, module=module, use_mock=use_mock, both_langs=both_langs))

    if args.command == "session":
        sys.exit(run_session(lang, module or "all", use_mock=use_mock, both_langs=both_langs))

    if args.command == "review":
        if args.review_cmd == "rubric":
            exercise = find_exercise(args.exercise, module=module) or next_incomplete(lang, module)
            if not exercise:
                sys.exit(1)
            show_rubric(exercise)
            return
        if args.review_cmd == "submit":
            exercise = find_exercise(args.exercise, module=module) or next_incomplete(lang, module)
            if not exercise:
                sys.exit(1)
            sid = submit_for_review(exercise, lang, author=args.author)
            print(f"Submitted: {sid}")
            print("Ask a peer to run: codam-labs review rubric", exercise.path.name)
            return
        if args.review_cmd == "pending":
            pending = list_pending()
            if not pending:
                print("No pending submissions.")
                return
            for item in pending:
                print(f"  {item['id']} — {item['slug']} [{item['lang']}] by {item['author']}")
            return
        if args.review_cmd == "approve":
            exercise = find_exercise(args.exercise, module=module)
            if not exercise:
                sys.exit(1)
            approve_review(exercise, lang, reviewer=args.reviewer)
            return
        review_p.print_help()
        return

    if args.command == "capstone":
        if args.cap_cmd == "list":
            print("Capstones:\n")
            for cap in CAPSTONES:
                print(f"  {cap.slug} — {cap.title}")
            return
        cap = find_capstone(getattr(args, "name", None))
        if not cap:
            print("Capstone not found.")
            sys.exit(1)
        if args.cap_cmd == "solution":
            print(cap.solution_main)
            return
        if args.cap_cmd == "run":
            extra = [a for a in getattr(args, "args", []) if a != "--"]
            sys.exit(run_capstone(cap, extra, use_solution=True, use_mock=use_mock))
        cap_p.print_help()
        return

    if args.command == "business":
        if args.bus_cmd == "list":
            print("Business cases:\n")
            for case in CASES:
                print(f"  {case.slug} — {case.title}")
            return
        case = find_case(getattr(args, "name", None))
        if not case:
            print("Business case not found.")
            sys.exit(1)
        if args.bus_cmd == "run":
            extra = [a for a in getattr(args, "args", []) if a != "--"]
            sys.exit(run_case(case, extra, use_mock=use_mock))
        bus_p.print_help()
        return


if __name__ == "__main__":
    main()
