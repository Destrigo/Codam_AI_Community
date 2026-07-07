"""One-off rename: codamlings -> Codam AI Labs (package codam_ai_labs, CLI codam-labs)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "__pycache__", "build", ".egg-info", "node_modules"}
SKIP_SUFFIXES = {".exe", ".pyc", ".o", ".obj", ".lib", ".a", ".dll", ".so"}

REPLACEMENTS = [
    ("CODAMLINGS_", "CODAM_LABS_"),
    (".codamlings", ".codam-ai-labs"),
    ("codamlings.", "codam_ai_labs."),
    ("from codamlings", "from codam_ai_labs"),
    ('include = ["codamlings*"]', 'include = ["codam_ai_labs*"]'),
    ('name = "codamlings"', 'name = "codam-ai-labs"'),
    ("Codamlings", "Codam AI Labs"),
    ("codamlings", "codam-labs"),
    ("APP_NAME=codam-labs", "APP_NAME=codam-ai-labs"),  # fix double if any
]

# Ensure APP_NAME check uses hyphenated app id
REPLACEMENTS.append(('APP_NAME=codam-labs"', 'APP_NAME=codam-ai-labs"'))


def should_process(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    if path.name in {"rename_to_codam_ai_labs.py"}:
        return False
    return path.is_file()


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not should_process(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(ROOT)}")
    print(f"Done: {changed} files updated.")


if __name__ == "__main__":
    main()
