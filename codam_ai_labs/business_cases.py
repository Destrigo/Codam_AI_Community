"""Business case workshop pipelines."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUSINESS_DIR = ROOT / "business_cases"


@dataclass(frozen=True)
class BusinessCase:
    slug: str
    title: str
    path: Path

    @property
    def pipeline(self) -> Path:
        return self.path / "python" / "pipeline.py"


CASES: list[BusinessCase] = [
    BusinessCase(
        "01_retail_catalog_harmonization",
        "Retail catalog harmonization",
        BUSINESS_DIR / "01_retail_catalog_harmonization",
    ),
    BusinessCase(
        "02_finance_invoice_ingestion",
        "Finance invoice ingestion",
        BUSINESS_DIR / "02_finance_invoice_ingestion",
    ),
    BusinessCase(
        "03_insurance_claims_intake",
        "Insurance FNOL intake",
        BUSINESS_DIR / "03_insurance_claims_intake",
    ),
]


def find_case(name: str | None) -> BusinessCase | None:
    if not name:
        return None
    key = name.replace("-", "_")
    for case in CASES:
        if case.slug == key or case.slug.startswith(key) or case.slug.split("_", 1)[0] == key:
            return case
    return None


def run_case(case: BusinessCase, args: list[str]) -> int:
    entry = case.pipeline
    if not entry.exists():
        print(f"Not found: {entry}", file=sys.stderr)
        return 1
    return subprocess.run([sys.executable, str(entry), *args], cwd=case.path).returncode
