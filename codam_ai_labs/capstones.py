"""Capstone projects registry and runner."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPSTONES_DIR = ROOT / "capstones"

CAPSTONE_NAMES = ("01_doc_assistant_rag", "02_ops_agent", "03_llm_gateway")


@dataclass(frozen=True)
class Capstone:
    slug: str
    title: str
    path: Path

    @property
    def solution_main(self) -> Path:
        return self.path / "solution" / "python" / "main.py"


CAPSTONES: list[Capstone] = [
    Capstone("01_doc_assistant_rag", "Doc Assistant (mini-RAG)", CAPSTONES_DIR / "01_doc_assistant_rag"),
    Capstone("02_ops_agent", "Ops Agent (mini-agent)", CAPSTONES_DIR / "02_ops_agent"),
    Capstone("03_llm_gateway", "LLM Gateway (mini-pipeline)", CAPSTONES_DIR / "03_llm_gateway"),
]


def find_capstone(name: str | None) -> Capstone | None:
    if not name:
        return None
    key = name.replace("-", "_")
    for cap in CAPSTONES:
        if cap.slug == key or cap.slug.startswith(key) or cap.slug.split("_", 1)[0] == key:
            return cap
    return None


def run_capstone(cap: Capstone, args: list[str], *, use_solution: bool = True) -> int:
    entry = cap.solution_main if use_solution else cap.path / "python" / "main.py"
    if not entry.exists():
        print(f"Not found: {entry}", file=sys.stderr)
        return 1
    return subprocess.run([sys.executable, str(entry), *args], cwd=cap.path).returncode
