"""Add peer_review.md to every exercise."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """# Peer Review — {title}

Use this checklist **instead of reading `solution/`**. Pair with a classmate.

## Before review
- [ ] Your code runs: `codamlings run {run_slug} --lang python`
- [ ] You tried `codamlings hint` (not `--solution`)
- [ ] Submit: `codamlings review submit {run_slug} --lang python`

## Reviewer checklist
- [ ] Code runs without errors on reviewer's machine
- [ ] Output matches the assignment in README.md
- [ ] No API keys hardcoded in source files
- [ ] Error handling present where required
- [ ] Code is readable (names, structure, no dead code)
- [ ] LLM calls use `MISTRAL_API_KEY` from environment

## Questions for the author
1. What was the hardest part?
2. What would you improve with more time?

## Approve
When all boxes are checked:
```bash
codamlings review approve {run_slug} --lang python --reviewer YOUR_NAME
```

This marks the exercise complete (alternative to `codamlings verify`).
"""


def main() -> None:
    paths = list(ROOT.glob("core/exercises/*/README.md")) + list(
        ROOT.glob("modules/*/exercises/*/README.md")
    )
    for readme in paths:
        folder = readme.parent
        title = readme.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        if folder.parent.parent.name == "exercises":
            run_slug = folder.name
        else:
            mod = folder.parent.parent.name
            run_slug = f"{mod}/{folder.name}" if mod != "core" else folder.name
        # fix slug for core
        if (ROOT / "core" / "exercises" / folder.name).exists():
            run_slug = folder.name
        else:
            mod = folder.parent.parent.name
            run_slug = folder.name  # CLI find accepts folder name

        out = folder / "peer_review.md"
        out.write_text(TEMPLATE.format(title=title, run_slug=folder.name), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
