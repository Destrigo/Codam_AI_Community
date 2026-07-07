# Business Case 01 — Retail / Marketplace Catalog Harmonization

## Executive summary

**Client (fictional):** MarketHub EU — B2B marketplace with 120 suppliers uploading product data daily.

**Pain:** Each supplier uses different formats (CSV, Excel, PDF datasheets, legacy API). Categories, attributes, SKUs, and prices are inconsistent. Manual cleanup delays listing by 3–5 days; pricing errors caused two incidents last quarter.

**Solution:** AI-assisted **ingestion + normalization pipeline** that lands raw files unchanged, extracts product records via LLM with a fixed schema, normalizes to a canonical catalog, and routes exceptions to human reviewers.

---

## Business context

| Stakeholder | Need |
|-------------|------|
| Marketplace ops | Publish listings within 24h of feed receipt |
| Suppliers | Minimal format change on their side |
| Finance | Correct VAT and price units |
| Search team | Consistent categories and facets |

**Volume (typical):** 50–200 feeds/day, 5–50k SKU updates/day.

---

## Architecture

```
┌─────────────┐   SFTP/API/Email   ┌──────────────────┐
│  Suppliers  │ ─────────────────► │  Landing zone    │
│  (50+)      │                    │  (raw, immutable)│
└─────────────┘                    └────────┬─────────┘
                                              │
                    ┌─────────────────────────▼─────────────────────────┐
                    │  Router: by MIME / filename / supplier profile   │
                    └─────────────────────────┬─────────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
   ┌───────────┐                      ┌───────────────┐                    ┌────────────┐
   │ CSV/Excel │                      │ PDF datasheet │                    │ JSON API   │
   │  parser   │                      │  OCR + LLM    │                    │  snapshot  │
   └─────┬─────┘                      └───────┬───────┘                    └──────┬─────┘
         │                                    │                                    │
         └────────────────────────────────────┼────────────────────────────────────┘
                                              ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │  AI EXTRACT — LLM → draft ProductRecord (see schema)         │
                    │  Prompt: supplier context + raw text + output JSON schema    │
                    └─────────────────────────┬───────────────────────────────────┘
                                              ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │  AI NORMALIZE — category mapping, UOM, brand aliases         │
                    │  "cell phone" → category_id: electronics.mobile.phones       │
                    └─────────────────────────┬───────────────────────────────────┘
                                              ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │  VALIDATE — deterministic rules + confidence thresholds      │
                    └───────────────┬─────────────────────────────┬───────────────┘
                                    ▼                             ▼
                          ┌─────────────────┐           ┌──────────────────┐
                          │ Canonical PIM   │           │ Exception queue  │
                          │ + search index  │           │ (human review)   │
                          └─────────────────┘           └──────────────────┘
```

---

## Canonical schema

See `schemas/product.canonical.json`.

Key fields:

| Field | Type | Notes |
|-------|------|-------|
| `supplier_id` | string | From feed metadata |
| `supplier_sku` | string | Original SKU |
| `canonical_sku` | string | `hash(supplier_id + supplier_sku)` |
| `title` | string | Normalized display name |
| `brand` | string | Resolved via alias table |
| `category_path` | string[] | e.g. `["electronics","mobile","phones"]` |
| `price` | object | `{amount, currency}` — ISO 4217 |
| `attributes` | object | Color, storage, weight, … |
| `confidence` | float | 0–1 from extraction |
| `source_ref` | string | Pointer to raw file + line/page |

---

## AI vs deterministic split

| Step | AI (LLM) | Code |
|------|----------|------|
| Read PDF layout | Extract fields from unstructured text | OCR trigger, page split |
| Category guess | Map free text → taxonomy | Taxonomy lookup table |
| Brand normalization | Fuzzy match suggestions | Golden brand registry |
| Price validation | Flag anomalies in description | `price > 0`, currency whitelist |
| Dedup | Suggest same-as existing SKU | Hash on GTIN / canonical_sku |

**Rule:** never publish to PIM without passing deterministic validation. AI proposes; code disposes.

---

## Sample inputs

| File | Format | Issue |
|------|--------|-------|
| `samples/feed_supplier_a.csv` | CSV | English headers, EUR |
| `samples/feed_supplier_b.xlsx.json` | Excel export as JSON | German headers, mixed categories |
| `samples/datasheet_supplier_c.txt` | PDF text extract | Unstructured specs |

---

## Exception queue (human-in-the-loop)

Route to review when:

- `confidence < 0.85`
- Category not in taxonomy
- Price deviates > 30% from historical median for similar SKU
- Duplicate GTIN with different title

Reviewer UI shows: raw snippet | draft JSON | suggested fix.

---

## KPIs

| Metric | Target |
|--------|--------|
| Straight-through processing (STP) | ≥ 75% of line items |
| Time feed → publishable | < 24 hours |
| Category accuracy (sample audit) | ≥ 95% |
| Pricing error rate | < 0.1% of active SKUs |

---

## Workshop exercise (Codam AI Labs extension)

**Build in 1 day:**

1. Ingest `samples/feed_supplier_a.csv`
2. LLM extract → `ProductRecord` JSON per row
3. Normalize brand + category using `schemas/category_map.json`
4. Validate required fields
5. Export `out/catalog.json`

**Modules used:** `structured_output`, `prompt_engineering`, `production/02_cache` (cache extractions by row hash).

---

## Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Hallucinated attributes | Require `source_ref` quote per attribute |
| Taxonomy drift | Versioned category map, eval set per release |
| Cost at scale | Cache by content hash; batch small rows |
| Supplier PII in feeds | Landing zone access controls; redact in logs |

---

## Legal / compliance

- Supplier contracts must allow automated processing
- GDPR: no consumer PII expected in B2B catalog feeds
- Audit trail: retain raw files 7 years (finance policy)
