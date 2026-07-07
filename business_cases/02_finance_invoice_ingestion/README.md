# Business Case 02 — Finance / Accounts Payable Invoice Ingestion

## Executive summary

**Client (fictional):** LedgerFirst SpA — mid-market manufacturer, 400 suppliers, ERP on SAP Business One.

**Pain:** Invoices arrive via PEC, email, supplier portal, and scanned PDF. AP team manually keys vendor, amounts, VAT, and line items. Average **4.2 minutes per invoice**, 8% error rate, duplicate payments twice in 2025.

**Solution:** Ingestion pipeline that stores raw documents, uses OCR when needed, **LLM extraction** to a canonical invoice schema, **normalization** (vendor aliases, VAT codes, dates), deterministic validation + PO matching, export to ERP.

---

## Business context

| Stakeholder | Need |
|-------------|------|
| AP clerks | Touch only exceptions |
| Controller | Accurate accruals by month-end |
| Suppliers | Faster payment (DSO target 45 days) |
| Audit | Immutable raw document trail |

**Volume:** 800–1,200 invoices/month, peak +40% in Q4.

---

## Architecture

```
Channels                    Landing                    Processing
─────────                   ───────                    ──────────

PEC / Email ──┐
Supplier API ─┼──► Object store (WORM) ──► Classify doc type
Scan batch  ──┘         │                      │
                        │                      ▼
                        │              OCR if image/scanned
                        │                      │
                        └──────────────────────┼──► AI EXTRACT
                                               │    (header + lines)
                                               ▼
                                        AI NORMALIZE
                                        vendor_id, VAT, dates
                                               ▼
                                        VALIDATE + ENRICH
                                        PO match, duplicates, limits
                                               ▼
                         ┌─────────────────────┴─────────────────────┐
                         ▼                                           ▼
                  ERP staging JSON                            Exception desk
                  (SAP import)                               (AP reviewer)
```

---

## Canonical schema

See `schemas/invoice.canonical.json`.

| Section | Fields |
|---------|--------|
| Header | `invoice_id`, `vendor`, `issue_date`, `due_date`, `currency`, `total_net`, `total_vat`, `total_gross` |
| Vendor | `vat_number`, `legal_name`, `vendor_id` (resolved) |
| Lines | `description`, `quantity`, `unit_price`, `vat_rate`, `cost_center` (optional) |
| Meta | `confidence`, `source_document`, `po_reference` |

Aligns conceptually with **UBL / FatturaPA** but simplified for workshop.

---

## AI vs deterministic split

| Task | AI | Code |
|------|-----|------|
| Find totals on varied layouts | Extract from OCR text | — |
| Vendor name → vendor_id | Suggest match from history | Match on VAT number (exact) |
| Line item split | Parse description tables | Sum(lines) ≈ total (tolerance 0.02) |
| Date formats | Normalize "31/01/26" | ISO 8601 output |
| Duplicate detection | — | Hash(vendor_id + number + gross) |
| Approval routing | Classify cost center from text | Threshold rules (> €10k → manager) |

---

## Sample inputs

| File | Scenario |
|------|----------|
| `samples/invoice_email_body.txt` | Invoice pasted in email |
| `samples/invoice_structured.json` | e-invoice JSON |
| `samples/invoice_scan.txt` | OCR text from scanned PDF |

All data is **fictional**.

---

## Validation rules (deterministic)

1. `total_gross = total_net + total_vat` (± €0.05)
2. `vat_number` passes checksum (country-specific module)
3. `issue_date <= today`
4. No duplicate `vendor_id + invoice_number` in last 24 months
5. If `po_reference` set → PO must exist and be open

Failures → exception queue with reason code.

---

## Human-in-the-loop

| Condition | Action |
|-----------|--------|
| confidence < 0.9 | Mandatory review |
| amount > €25,000 | Manager approval |
| new vendor VAT | Master data review |
| PO mismatch | Buyer confirmation |

---

## KPIs

| Metric | Baseline | Target |
|--------|----------|--------|
| STP rate | 12% | 60% |
| Minutes per invoice | 4.2 | 0.8 (blended) |
| Duplicate payment incidents | 2/year | 0 |
| Month-end accrual lag | 3 days | Same day |

---

## Workshop exercise

1. Parse `samples/invoice_email_body.txt`
2. LLM → canonical JSON
3. Resolve vendor `IT12345678901` → `VND-0042`
4. Validate totals
5. Export `out/invoice_staging.json`

**Modules:** `structured_output`, `production/03_redacted_log`, `production/04_guardrail` (block exfiltration prompts in email body).

---

## Risks

| Risk | Mitigation |
|------|------------|
| Wrong payment amount | Dual control on exceptions; no auto-pay |
| PII in logs | Redact IBAN, tax IDs in debug output |
| Prompt injection in invoice text | Treat document as data, not instructions |
| Model drift | Monthly eval on 50 gold invoices |

---

## Compliance

- Italian **FatturaPA** / SDI for domestic B2B
- 10-year document retention
- Segregation of duties: ingest ≠ approve ≠ pay
