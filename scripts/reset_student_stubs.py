"""Reset student exercise files (python/ and cpp/) to canonical stubs.

Use before distributing exercises to students or after local dev/CI left
solution code in student folders.

  py -3 scripts/reset_student_stubs.py apply          # restore all stubs
  py -3 scripts/reset_student_stubs.py apply --slug 01_env_vars
  py -3 scripts/reset_student_stubs.py export         # refresh snapshots from current stubs
  py -3 scripts/reset_student_stubs.py check          # fail if any student file == solution
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUBS_ROOT = Path(__file__).resolve().parent / "student_stubs"
LANGS = ("python", "cpp")
EXT = {"python": "py", "cpp": "cpp"}


def exercise_dirs() -> list[Path]:
    dirs: list[Path] = []
    for pattern in ("core/exercises/*", "modules/*/exercises/*"):
        dirs.extend(sorted(ROOT.glob(pattern)))
    return [d for d in dirs if d.is_dir() and (d / "README.md").exists()]


def student_file(exercise: Path, lang: str) -> Path:
    return exercise / lang / f"main.{EXT[lang]}"


def solution_file(exercise: Path, lang: str) -> Path:
    return exercise / "solution" / lang / f"main.{EXT[lang]}"


def stub_snapshot(exercise: Path, lang: str) -> Path:
    rel = exercise.relative_to(ROOT)
    return STUBS_ROOT / rel / lang / f"main.{EXT[lang]}"


def identical_to_solution(exercise: Path, lang: str) -> bool:
    student = student_file(exercise, lang)
    solution = solution_file(exercise, lang)
    if not student.exists() or not solution.exists():
        return False
    return student.read_text(encoding="utf-8").strip() == solution.read_text(encoding="utf-8").strip()


def export_stubs(*, slug: str | None = None) -> int:
    STUBS_ROOT.mkdir(parents=True, exist_ok=True)
    count = 0
    for exercise in exercise_dirs():
        if slug and exercise.name != slug and not str(exercise).endswith(slug.replace("/", "\\")):
            rel_slug = str(exercise.relative_to(ROOT)).replace("\\", "/")
            if slug not in rel_slug:
                continue
        for lang in LANGS:
            src = student_file(exercise, lang)
            if not src.exists():
                continue
            dst = stub_snapshot(exercise, lang)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            count += 1
            print(f"exported {dst.relative_to(ROOT)}")
    print(f"Exported {count} stub file(s) to {STUBS_ROOT.relative_to(ROOT)}")
    return 0


def apply_stubs(*, slug: str | None = None, clean_build: bool = True) -> int:
    if not STUBS_ROOT.exists():
        print("No stub snapshots found. Run: py -3 scripts/reset_student_stubs.py export", file=sys.stderr)
        return 1

    restored = 0
    missing = 0
    for exercise in exercise_dirs():
        rel_slug = str(exercise.relative_to(ROOT)).replace("\\", "/")
        if slug and slug not in rel_slug and exercise.name != slug:
            continue
        if clean_build:
            build_dir = exercise / "cpp" / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)
        for lang in LANGS:
            snapshot = stub_snapshot(exercise, lang)
            dst = student_file(exercise, lang)
            if not snapshot.exists():
                if dst.exists() and solution_file(exercise, lang).exists():
                    missing += 1
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(snapshot.read_text(encoding="utf-8"), encoding="utf-8")
            restored += 1
            print(f"restored {dst.relative_to(ROOT)}")

    if missing:
        print(f"Warning: {missing} student file(s) have no snapshot", file=sys.stderr)
    print(f"Restored {restored} student stub file(s)")
    return 0


def check_stubs() -> int:
    problems: list[str] = []
    for exercise in exercise_dirs():
        rel = exercise.relative_to(ROOT)
        for lang in LANGS:
            if identical_to_solution(exercise, lang):
                problems.append(f"{rel}/{lang}/main.{EXT[lang]} is identical to solution/")
    if problems:
        print("Student files must be stubs, not solutions:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"OK: {len(exercise_dirs())} exercises — no student file matches its solution")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    export_p = sub.add_parser("export")
    export_p.add_argument("--slug", help="Limit to one exercise slug or path fragment")
    apply_p = sub.add_parser("apply")
    apply_p.add_argument("--slug", help="Limit to one exercise slug or path fragment")
    apply_p.add_argument("--keep-build", action="store_true", help="Do not delete cpp/build/")
    check_p = sub.add_parser("check")
    check_p.add_argument("--slug", help="Limit to one exercise slug or path fragment")
    args = parser.parse_args()

    if args.command == "export":
        return export_stubs(slug=args.slug)
    if args.command == "apply":
        return apply_stubs(slug=args.slug, clean_build=not args.keep_build)
    return check_stubs()


if __name__ == "__main__":
    raise SystemExit(main())
