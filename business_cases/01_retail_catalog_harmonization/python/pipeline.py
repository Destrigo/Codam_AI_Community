"""Business Case 01 — Retail catalog harmonization pipeline."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

from codam_ai_labs.config import load_dotenv_if_present, require_mistral_key
from codam_ai_labs.llm_client import chat_text, extract_json_object, is_mock_mode

load_dotenv_if_present()

ROOT = Path(__file__).resolve().parent.parent


def _canonical_sku(supplier_id: str, supplier_sku: str) -> str:
    return hashlib.sha256(f"{supplier_id}:{supplier_sku}".encode()).hexdigest()[:16]


def _map_category(raw: str, category_map: dict) -> list[str]:
    key = raw.strip().lower()
    if key in category_map:
        return category_map[key]
    for k, v in category_map.items():
        if k in key:
            return v
    return ["uncategorized"]


def _from_csv(path: Path, supplier_id: str, category_map: dict) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sku = row["supplier_sku"]
            records.append({
                "supplier_id": supplier_id,
                "supplier_sku": sku,
                "canonical_sku": _canonical_sku(supplier_id, sku),
                "title": row["product_name"],
                "brand": row["brand"],
                "category_path": _map_category(row["category"], category_map),
                "price": {"amount": float(row["price_eur"]), "currency": "EUR"},
                "attributes": {
                    k: v for k, v in row.items()
                    if k not in {"supplier_sku", "product_name", "brand", "category", "price_eur"} and v
                },
                "confidence": 0.95,
                "source_ref": f"{path.name}:{sku}",
            })
    return records


def _from_json_feed(path: Path, supplier_id: str, category_map: dict) -> list[dict]:
    records = []
    for row in json.loads(path.read_text(encoding="utf-8")):
        sku = row["Artikelnummer"]
        price = float(row["Preis"].replace(",", "."))
        records.append({
            "supplier_id": supplier_id,
            "supplier_sku": sku,
            "canonical_sku": _canonical_sku(supplier_id, sku),
            "title": row["Bezeichnung"],
            "brand": row["Hersteller"],
            "category_path": _map_category(row["Kategorie"], category_map),
            "price": {"amount": price, "currency": row.get("Waehrung", "EUR")},
            "attributes": {"storage": row.get("Speicher", "")},
            "confidence": 0.9,
            "source_ref": f"{path.name}:{sku}",
        })
    return records


def _from_datasheet(path: Path, supplier_id: str, category_map: dict) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if is_mock_mode():
        return [{
            "supplier_id": supplier_id,
            "supplier_sku": "XR-PHONE-2",
            "canonical_sku": _canonical_sku(supplier_id, "XR-PHONE-2"),
            "title": "XR-Phone 2",
            "brand": "NordMobile",
            "category_path": _map_category("smartphones", category_map),
            "price": {"amount": 749.0, "currency": "EUR"},
            "attributes": {"ean": "4012345678901"},
            "confidence": 0.88,
            "source_ref": path.name,
        }]

    require_mistral_key()
    prompt = (
        "Extract one product as JSON with keys: supplier_sku, title, brand, category, "
        f"price_amount, price_currency, attributes (object). Text:\n{text}"
    )
    raw = chat_text([{"role": "user", "content": prompt}])
    data = extract_json_object(raw)
    sku = data.get("supplier_sku", "UNKNOWN")
    return [{
        "supplier_id": supplier_id,
        "supplier_sku": sku,
        "canonical_sku": _canonical_sku(supplier_id, sku),
        "title": data["title"],
        "brand": data["brand"],
        "category_path": _map_category(str(data.get("category", "")), category_map),
        "price": {"amount": float(data["price_amount"]), "currency": data.get("price_currency", "EUR")},
        "attributes": data.get("attributes", {}),
        "confidence": 0.85,
        "source_ref": path.name,
    }]


def run_pipeline(samples_dir: Path, out_dir: Path) -> int:
    category_map = json.loads((ROOT / "schemas" / "category_map.json").read_text(encoding="utf-8"))
    catalog: list[dict] = []

    csv_path = samples_dir / "feed_supplier_a.csv"
    if csv_path.exists():
        catalog.extend(_from_csv(csv_path, "supplier_a", category_map))

    json_path = samples_dir / "feed_supplier_b.xlsx.json"
    if json_path.exists():
        catalog.extend(_from_json_feed(json_path, "supplier_b", category_map))

    txt_path = samples_dir / "datasheet_supplier_c.txt"
    if txt_path.exists():
        catalog.extend(_from_datasheet(txt_path, "supplier_c", category_map))

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "catalog.json"
    out_file.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print(f"CATALOG_OK:{len(catalog)}")
    print(f"EXPORT:{out_file}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Retail catalog harmonization")
    parser.add_argument("--samples", default=str(ROOT / "samples"))
    parser.add_argument("--out", default=str(ROOT / "out"))
    args = parser.parse_args()
    sys.exit(run_pipeline(Path(args.samples), Path(args.out)))


if __name__ == "__main__":
    main()
