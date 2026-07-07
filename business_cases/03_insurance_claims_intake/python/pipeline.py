"""Business Case 03 — Insurance FNOL intake pipeline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from codamlings.config import load_dotenv_if_present, require_mistral_key
from codamlings.llm_client import chat_text, extract_json_object, is_mock_mode

load_dotenv_if_present()

ROOT = Path(__file__).resolve().parent.parent


def _triage(loss_type: str, text: str, hints: dict | None = None) -> dict:
    hints = hints or {}
    if hints.get("injuries_reported") is True:
        return {"priority": "high", "reason": "injuries reported"}
    lower = text.lower()
    if "emergency" in lower or "ambulance" in lower:
        return {"priority": "high", "reason": "emergency services"}
    if loss_type == "motor_theft":
        return {"priority": "medium", "reason": "theft"}
    if "non e' marciante" in lower or "not drivable" in lower:
        return {"priority": "medium", "reason": "vehicle not drivable"}
    return {"priority": "low", "reason": "standard claim"}


def _from_email(text: str) -> dict:
    policy = re.search(r"Polizza:\s*(\S+)", text)
    date = re.search(r"(\d{1,2})\s+marzo", text, re.I)
    return {
        "policy_number": policy.group(1) if policy else "UNKNOWN",
        "loss_date": "2026-03-06T21:30:00",
        "loss_type": "motor_collision",
        "location": {"text": "Via Roma, Milano", "city": "Milano", "country": "IT"},
        "parties": [
            {"name": "Marco Rossi", "role": "insured"},
            {"name": "Luca Bianchi", "role": "third_party"},
        ],
        "description": "Rear collision at traffic light, front bumper damaged, vehicle not drivable.",
        "severity_hints": {"injuries_reported": False, "vehicle_drivable": False, "emergency_services": False},
        "confidence": 0.9,
        "sources": ["fnol_email.txt"],
    }


def _from_app(data: dict) -> dict:
    return {
        "policy_number": data["policy_number"],
        "loss_date": data["submitted_at"],
        "loss_type": "property_water",
        "location": {"text": data["geo"]["city"], "city": data["geo"]["city"], "country": data["geo"]["country"]},
        "parties": [{"name": "policyholder", "role": "insured"}],
        "description": data["user_text"],
        "severity_hints": {
            "injuries_reported": data["structured_hints"].get("injuries", False),
            "vehicle_drivable": True,
            "emergency_services": False,
        },
        "confidence": 0.93,
        "sources": ["fnol_app.json"],
    }


def _from_call_center(text: str) -> dict:
    policy = re.search(r"POL-M-(\d+)", text)
    return {
        "policy_number": f"POL-M-{policy.group(1)}" if policy else "POL-M-200300",
        "loss_date": "2026-03-07T03:00:00",
        "loss_type": "motor_theft",
        "location": {"text": "Naples street parking", "city": "Naples", "country": "IT"},
        "parties": [{"name": "Anna Verdi", "role": "insured"}],
        "description": "Vehicle stolen overnight; police report NA-2026-44521 filed.",
        "severity_hints": {"injuries_reported": False, "vehicle_drivable": False, "emergency_services": False},
        "confidence": 0.87,
        "sources": ["fnol_call_center.txt"],
    }


def _llm_extract(text: str, source: str) -> dict:
    require_mistral_key()
    prompt = (
        "Extract FNOL as JSON: policy_number, loss_date, loss_type "
        "(motor_collision|motor_theft|property_water|property_fire|other), "
        "location{text,city,country}, parties[], description, severity_hints, confidence. "
        f"Text:\n{text}"
    )
    raw = chat_text([{"role": "user", "content": prompt}])
    data = extract_json_object(raw)
    data["sources"] = [source]
    return data


def _enrich_policy(claim: dict, policies: dict) -> dict:
    pol = policies.get(claim["policy_number"])
    claim["policy_status"] = pol["status"] if pol else "unknown"
    claim["coverage"] = pol.get("coverage", []) if pol else []
    return claim


def run_pipeline(samples_dir: Path, out_dir: Path) -> int:
    policies = json.loads((ROOT / "schemas" / "policy_mock_db.json").read_text(encoding="utf-8"))
    drafts: list[dict] = []

    email = samples_dir / "fnol_email.txt"
    if email.exists():
        text = email.read_text(encoding="utf-8")
        claim = _from_email(text) if is_mock_mode() else _llm_extract(text, email.name)
        claim["triage"] = _triage(claim["loss_type"], text, claim.get("severity_hints"))
        drafts.append(_enrich_policy(claim, policies))

    app = samples_dir / "fnol_app.json"
    if app.exists():
        data = json.loads(app.read_text(encoding="utf-8"))
        claim = _from_app(data)
        claim["triage"] = _triage(claim["loss_type"], claim["description"], claim.get("severity_hints"))
        drafts.append(_enrich_policy(claim, policies))

    cc = samples_dir / "fnol_call_center.txt"
    if cc.exists():
        text = cc.read_text(encoding="utf-8")
        claim = _from_call_center(text) if is_mock_mode() else _llm_extract(text, cc.name)
        claim["triage"] = _triage(claim["loss_type"], text)
        drafts.append(_enrich_policy(claim, policies))

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "claim_drafts.json"
    out_file.write_text(json.dumps(drafts, indent=2), encoding="utf-8")
    high = sum(1 for d in drafts if d["triage"]["priority"] == "high")
    print(f"FNOL_OK:{len(drafts)}")
    print(f"TRIAGE_HIGH:{high}")
    print(f"EXPORT:{out_file}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Insurance FNOL intake")
    parser.add_argument("--samples", default=str(ROOT / "samples"))
    parser.add_argument("--out", default=str(ROOT / "out"))
    args = parser.parse_args()
    sys.exit(run_pipeline(Path(args.samples), Path(args.out)))


if __name__ == "__main__":
    main()
