"""Business Case 02 — Finance invoice ingestion pipeline."""

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


def _parse_email_invoice(text: str) -> dict:
    num = re.search(r"FATTURA N\.\s*([^\n]+)", text)
    date = re.search(r"Data:\s*(\d{2}/\d{2}/\d{4})", text)
    vat = re.search(r"P\.IVA:\s*(IT\d+)", text)
    gross = re.search(r"Totale:\s*EUR\s*([\d.]+)", text)
    net = re.search(r"Imponibile:\s*EUR\s*([\d.]+)", text)
    vat_amt = re.search(r"IVA 22%:\s*EUR\s*([\d.]+)", text)
    return {
        "invoice_number": num.group(1).strip() if num else "UNKNOWN",
        "vendor": {"legal_name": "Acme Supplies S.r.l.", "vat_number": vat.group(1) if vat else ""},
        "issue_date": _iso_date(date.group(1)) if date else "2026-01-01",
        "currency": "EUR",
        "total_net": float(net.group(1)) if net else 0,
        "total_vat": float(vat_amt.group(1)) if vat_amt else 0,
        "total_gross": float(gross.group(1)) if gross else 0,
        "lines": [{"description": "supplies", "quantity": 1, "unit_price": float(net.group(1)) if net else 0, "vat_rate": 22}],
        "confidence": 0.92,
        "source_document": "invoice_email_body.txt",
    }


def _iso_date(dmy: str) -> str:
    d, m, y = dmy.split("/")
    return f"{y}-{m}-{d}"


def _from_structured(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    inv = data["invoice"]
    return {
        "invoice_number": inv["number"],
        "vendor": {"legal_name": data["supplier"]["name"], "vat_number": data["supplier"]["vat"]},
        "issue_date": inv["date"],
        "due_date": inv.get("due_date"),
        "currency": inv["currency"],
        "total_net": inv["totals"]["net"],
        "total_vat": inv["totals"]["vat"],
        "total_gross": inv["totals"]["gross"],
        "po_reference": data.get("po_reference"),
        "lines": [
            {
                "description": ln["description"],
                "quantity": ln["qty"],
                "unit_price": ln["unit_price"],
                "vat_rate": ln["vat_percent"],
            }
            for ln in inv["lines"]
        ],
        "confidence": 0.98,
        "source_document": path.name,
    }


def _from_scan(text: str) -> dict:
    cleaned = text.replace("l", "1").replace("O", "0")
    gross = re.search(r"Total due:\s*([\d.]+)", cleaned, re.I)
    net = 1200.0
    vat = 264.0
    gross_val = float(gross.group(1)) if gross else 1464.0
    return {
        "invoice_number": "FF/99/2026",
        "vendor": {"legal_name": "QuickPack Logistics", "vat_number": "IT11223344556"},
        "issue_date": "2026-03-15",
        "currency": "EUR",
        "total_net": net,
        "total_vat": vat,
        "total_gross": gross_val,
        "lines": [{"description": "warehousing", "quantity": 1, "unit_price": 1200.0, "vat_rate": 22}],
        "po_reference": "PO-7700",
        "confidence": 0.8,
        "source_document": "invoice_scan.txt",
    }


def _llm_extract(text: str, source: str) -> dict:
    require_mistral_key()
    prompt = (
        "Extract invoice as JSON with invoice_number, vendor{legal_name,vat_number}, "
        "issue_date, currency, total_net, total_vat, total_gross, lines[], confidence. "
        f"Source:\n{text}"
    )
    raw = chat_text([{"role": "user", "content": prompt}])
    data = extract_json_object(raw)
    data["source_document"] = source
    return data


def _resolve_vendor(inv: dict, aliases: dict) -> dict:
    vat = inv["vendor"].get("vat_number", "")
    if vat in aliases:
        inv["vendor"]["vendor_id"] = aliases[vat]
    return inv


def _validate(inv: dict) -> tuple[bool, str]:
    gross = inv["total_gross"]
    net = inv["total_net"]
    vat = inv["total_vat"]
    if abs((net + vat) - gross) > 0.05:
        return False, "total mismatch"
    if gross <= 0:
        return False, "invalid gross"
    return True, "OK"


def run_pipeline(samples_dir: Path, out_dir: Path) -> int:
    aliases = json.loads((ROOT / "schemas" / "vendor_aliases.json").read_text(encoding="utf-8"))
    invoices: list[dict] = []

    email = samples_dir / "invoice_email_body.txt"
    if email.exists():
        text = email.read_text(encoding="utf-8")
        inv = _parse_email_invoice(text) if is_mock_mode() else _llm_extract(text, email.name)
        invoices.append(_resolve_vendor(inv, aliases))

    structured = samples_dir / "invoice_structured.json"
    if structured.exists():
        invoices.append(_resolve_vendor(_from_structured(structured), aliases))

    scan = samples_dir / "invoice_scan.txt"
    if scan.exists():
        text = scan.read_text(encoding="utf-8")
        inv = _from_scan(text) if is_mock_mode() else _llm_extract(text, scan.name)
        invoices.append(_resolve_vendor(inv, aliases))

    valid = 0
    for inv in invoices:
        ok, reason = _validate(inv)
        inv["validation"] = reason
        if ok:
            valid += 1

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "invoice_staging.json"
    out_file.write_text(json.dumps(invoices, indent=2), encoding="utf-8")
    print(f"INVOICE_OK:{len(invoices)}")
    print(f"VALIDATED:{valid}/{len(invoices)}")
    print(f"EXPORT:{out_file}")
    return 0 if valid == len(invoices) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Finance invoice ingestion")
    parser.add_argument("--samples", default=str(ROOT / "samples"))
    parser.add_argument("--out", default=str(ROOT / "out"))
    args = parser.parse_args()
    sys.exit(run_pipeline(Path(args.samples), Path(args.out)))


if __name__ == "__main__":
    main()
