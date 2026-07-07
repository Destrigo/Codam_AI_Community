"""Peer review workflow — alternative to reading static solutions."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from codamlings.exercises import Exercise, mark_complete

ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = ROOT / ".codamlings" / "reviews"
REVIEWS_INDEX = REVIEWS_DIR / "index.json"


def _load_index() -> dict:
    if not REVIEWS_INDEX.exists():
        return {"submissions": [], "approvals": []}
    return json.loads(REVIEWS_INDEX.read_text(encoding="utf-8"))


def _save_index(data: dict) -> None:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_INDEX.write_text(json.dumps(data, indent=2), encoding="utf-8")


def show_rubric(exercise: Exercise) -> None:
    path = exercise.path / "peer_review.md"
    if path.exists():
        print(path.read_text(encoding="utf-8"))
        return
    print(f"No peer_review.md for {exercise.slug}")


def submit_for_review(exercise: Exercise, lang: str, author: str = "student") -> str:
    """Copy student code to pending review folder."""
    ext = "py" if lang == "python" else "cpp"
    src = exercise.path / lang / f"main.{ext}"
    if not src.exists():
        raise FileNotFoundError(f"Submission not found: {src}")

    submission_id = f"{exercise.slug.replace('/', '__')}__{lang}__{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    dest_dir = REVIEWS_DIR / "pending" / submission_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest_dir / f"main.{ext}")

    data = _load_index()
    data["submissions"].append({
        "id": submission_id,
        "slug": exercise.slug,
        "lang": lang,
        "author": author,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    })
    _save_index(data)
    return submission_id


def list_pending() -> list[dict]:
    data = _load_index()
    return [s for s in data.get("submissions", []) if s.get("status") == "pending"]


def approve_review(exercise: Exercise, lang: str, reviewer: str = "peer") -> None:
    """Mark exercise complete via peer review (alternative to verify)."""
    data = _load_index()
    data.setdefault("approvals", []).append({
        "slug": exercise.slug,
        "lang": lang,
        "reviewer": reviewer,
        "approved_at": datetime.now(timezone.utc).isoformat(),
    })
    for sub in data.get("submissions", []):
        if sub.get("slug") == exercise.slug and sub.get("lang") == lang and sub.get("status") == "pending":
            sub["status"] = "approved"
    _save_index(data)
    mark_complete(exercise.slug, lang, via="peer_review")
    print(f"Peer review approved: {exercise.slug} [{lang}] by {reviewer}")
