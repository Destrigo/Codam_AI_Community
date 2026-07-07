"""Verify exercises using reference solutions (dev check)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from codamlings.exercises import ALL_EXERCISES, exercises_for
from codamlings.verify import verify_exercise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["python", "cpp"], default="python")
    parser.add_argument("--module", default="all")
    args = parser.parse_args()

    pool = ALL_EXERCISES if args.module == "all" else exercises_for(args.module)
    passed = 0
    backups: list[tuple[Path, str | None]] = []

    try:
        for exercise in pool:
            lang = args.lang
            ext = "py" if lang == "python" else "cpp"
            src = exercise.path / "solution" / lang / f"main.{ext}"
            dst = exercise.path / lang / f"main.{ext}"
            if not src.exists():
                print(f"MISSING {src}")
                continue
            backups.append((dst, dst.read_text(encoding="utf-8") if dst.exists() else None))
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            if verify_exercise(exercise, lang):
                passed += 1
    finally:
        for dst, original in backups:
            if original is not None:
                dst.write_text(original, encoding="utf-8")

    total = len(pool)
    print(f"\nSolutions check: {passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
