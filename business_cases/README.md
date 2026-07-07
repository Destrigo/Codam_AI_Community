# Business Cases — Real-World AI Ingestion & Normalization

Three **production-style scenarios** for data ingestion from heterogeneous sources and AI-assisted normalization to a canonical schema.

These are **separate from capstones** — aimed at workshop days, client demos, or advanced cohorts.

| # | Sector | Case | Core problem |
|---|--------|------|--------------|
| 01 | Retail / Marketplace | [Catalog harmonization](01_retail_catalog_harmonization/README.md) | Multi-supplier feeds → unified product catalog |
| 02 | Finance / AP | [Invoice ingestion](02_finance_invoice_ingestion/README.md) | PDF/email invoices → ERP-ready records |
| 03 | Insurance / Claims | [FNOL intake](03_insurance_claims_intake/README.md) | Unstructured loss notices → structured claims |

## Common pattern

All three cases follow the same pipeline shape:

```
Sources (heterogeneous)
    → Landing zone (raw, immutable)
    → AI Extract (LLM + schema)
    → AI Normalize (mapping, aliases, units)
    → Validate (business rules, deterministic)
    → Canonical store (JSON / DB / API export)
    → Human-in-the-loop (exceptions queue)
```

## What AI does vs what code does

| Layer | AI (LLM) | Code (deterministic) |
|-------|----------|----------------------|
| Extract | Parse messy PDF/Excel/email layout | OCR trigger, file type routing |
| Normalize | Synonyms, categories, entity resolution | Schema validation, dedup keys |
| Validate | Ambiguity flags | Hard rules (VAT, price > 0, policy exists) |
| Export | Summaries for operators | API calls, audit logs |

## Relationship to Codam AI Labs

| Business case | Closest modules |
|---------------|-----------------|
| Retail catalog | `structured_output`, `embeddings`, `rag` |
| Finance invoices | `structured_output`, `production` |
| Insurance FNOL | `structured_output`, `agents`, `production` |

Capstones teach **how to build**; business cases teach **where to apply** in industry.

## Run pipelines

```bash
codam-labs business list
codam-labs business run 01_retail_catalog_harmonization
codam-labs business run 02_finance_invoice_ingestion
codam-labs business run 03_insurance_claims_intake
```

Output is written to `out/` inside each case folder (`catalog.json`, `invoice_staging.json`, `claim_drafts.json`).

Use `--mock` on `codam-labs` when running without a live API key (rule-based extraction). Live mode uses Mistral for unstructured sources.

## Synthetic data only

All sample files in `samples/` are **fictional**. Do not use real PII, invoices, or policy numbers.
