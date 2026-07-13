"""Verify exercises using reference solutions (dev / CI check)."""

from __future__ import annotations

import argparse
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from codam_ai_labs.config import load_dotenv_if_present
from codam_ai_labs.exercises import ALL_EXERCISES, exercises_for
from codam_ai_labs.verify import verify_exercise

load_dotenv_if_present()


@contextmanager
def temporary_student_overlay(dst: Path, solution: Path):
    """Run verification with solution code without leaving student folders dirty."""
    original = dst.read_text(encoding="utf-8") if dst.exists() else None
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(solution.read_text(encoding="utf-8"), encoding="utf-8")
    try:
        yield
    finally:
        if original is not None:
            dst.write_text(original, encoding="utf-8")
        elif dst.exists():
            dst.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["python", "cpp"], default="python")
    parser.add_argument("--module", default="all")
    parser.add_argument("--mock", action="store_true", help="Use offline mock (CI default)")
    args = parser.parse_args()

    pool = ALL_EXERCISES if args.module == "all" else exercises_for(args.module)
    passed = 0
    lang = args.lang
    ext = "py" if lang == "python" else "cpp"

    for exercise in pool:
        src = exercise.path / "solution" / lang / f"main.{ext}"
        dst = exercise.path / lang / f"main.{ext}"
        if not src.exists():
            print(f"MISSING {src}")
            continue
        with temporary_student_overlay(dst, src):
            if verify_exercise(exercise, lang, use_mock=args.mock, record_progress=False):
                passed += 1

    total = len(pool)
    print(f"\nSolutions check: {passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
