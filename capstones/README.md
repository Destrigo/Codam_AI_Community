# Capstones — Final Projects

Three **medium-sized** projects that combine 2–3 Codamlings modules into a real end-to-end system.

Complete **core + relevant modules** before starting a capstone.

| # | Project | Modules | Duration |
|---|---------|---------|----------|
| 01 | [Doc Assistant (mini-RAG)](01_doc_assistant_rag/README.md) | embeddings, rag, production | 2–3 weeks |
| 02 | [Ops Agent (mini-agent)](02_ops_agent/README.md) | tools, agents, structured_output | 2–3 weeks |
| 03 | [LLM Gateway (mini-pipeline)](03_llm_gateway/README.md) | production, advanced_patterns, core | 2–4 weeks |

## Recommended order

```
01 Doc Assistant  →  02 Ops Agent  →  03 LLM Gateway
     (RAG)            (orchestration)      (production hardening)
```

## How capstones differ from exercises

| | Exercises | Capstones |
|---|-----------|-----------|
| Scope | One concept per file | Full pipeline |
| Verify | Exact output substrings | Milestone checks + peer review |
| Data | Mock / tiny fixtures | Local corpus or eval set |
| Solution | Reference in `solution/` | Rubric only — no static solution |

## Completion

Reference implementations live in `solution/python/` (instructor). Student stubs remain in `python/main.py`.

```bash
# Run reference capstone (solution)
codamlings capstone run 01_doc_assistant_rag -- index --docs ./data
codamlings capstone run 01_doc_assistant_rag -- ask --question "How many remote days?"
codamlings capstone run 02_ops_agent -- eval
codamlings capstone run 03_llm_gateway -- complete --prompt "Hello"

# Business case pipelines
codamlings business run 01_retail_catalog_harmonization
codamlings business run 02_finance_invoice_ingestion
codamlings business run 03_insurance_claims_intake

# Verify all (mock, CI)
python scripts/verify_extended.py --mock
```

Each capstone can be marked done via:

1. **Milestone verify** — `codamlings capstone verify <name> --milestone N` (when implemented)
2. **Peer review** — `peer_review.md` checklist + demo to instructor

## Prerequisites

| Capstone | Minimum modules |
|----------|-----------------|
| 01 | `core`, `embeddings`, `rag` |
| 02 | `core`, `tools`, `agents`, `structured_output` |
| 03 | `core`, `production`, `advanced_patterns` |

## Languages

Implement in **Python** or **C++** (same assignment, idiomatic code).

```bash
codamlings capstone list          # future CLI
# For now: work inside capstones/NN_name/python or cpp/
```
