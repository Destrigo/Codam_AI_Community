"""Generate ASSIGNMENTS.md lookup from exercise READMEs."""

from __future__ import annotations

import re
from pathlib import Path

from codam_ai_labs.checks import MOCK_CHECKS
from codam_ai_labs.exercises import ALL_EXERCISES, CORE_EXERCISES, MODULE_NAMES, exercises_for

ROOT = Path(__file__).resolve().parent.parent


def extract_assignment(text: str) -> str:
    match = re.search(r"## Assignment\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not match:
        return ""
    lines: list[str] = []
    in_code = False
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        lines.append(stripped)
    return " ".join(lines)


def main() -> None:
    sections = [
        "# Codam AI Labs — Assignment lookup",
        "",
        "Quick reference for all **78 exercises**: slug → assignment → verify output.",
        "",
        "Verify with: `codam-labs --mock verify <slug>`",
        "",
    ]

    def add_module(title: str, pool) -> None:
        sections.extend([f"## {title}", "", "| Slug | Assignment | Verify expects |", "|------|------------|----------------|"])
        for exercise in pool:
            readme = (exercise.path / "README.md").read_text(encoding="utf-8")
            assignment = extract_assignment(readme).replace("|", "/")
            if len(assignment) > 140:
                assignment = assignment[:137] + "..."
            expected = ", ".join(f"`{item}`" for item in MOCK_CHECKS.get(exercise.slug, []))
            sections.append(f"| `{exercise.slug}` | {assignment} | {expected} |")
        sections.append("")

    add_module("Core (10)", CORE_EXERCISES)
    for name in MODULE_NAMES:
        add_module(name.replace("_", " ").title(), exercises_for(name))

    out = ROOT / "ASSIGNMENTS.md"
    out.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote {out} ({len(ALL_EXERCISES)} exercises)")


if __name__ == "__main__":
    main()
