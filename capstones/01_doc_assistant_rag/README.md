# Capstone 01 — Doc Assistant (mini-RAG)

## Brief (fictional client)

**Acme Internal Docs** has 200+ markdown and text files (HR policies, engineering runbooks, sales playbooks). Employees ask questions in Slack; today nobody reads the wiki.

**Your job:** build a terminal CLI that answers questions from a local document folder, cites sources, and refuses when context is insufficient.

---

## Theory

A minimal RAG system has four stages:

1. **Ingest** — load files, chunk text
2. **Index** — embed chunks, store vectors + metadata
3. **Retrieve** — embed query, find top-k similar chunks
4. **Generate** — augment prompt with chunks, call LLM, require citations

You already practiced each piece in `modules/embeddings` and `modules/rag`. This capstone wires them together with production guardrails from `modules/production`.

---

## Prerequisites

- `core/` (all 10 exercises)
- `modules/embeddings` (all 5)
- `modules/rag` (all 7)
- `modules/production` (at least 04_guardrail)

---

## Assignment

Build `doc_assistant` CLI:

```bash
# Index documents (run once or on --reindex)
python python/main.py index --docs ./data

# Ask a question
python python/main.py ask --docs ./data --question "What is the remote work policy?"

# Expected output shape:
# ANSWER: Employees may work remotely up to 3 days per week...
# CITED: hr_remote_policy#chunk_2
# CONFIDENCE: high
```

### Functional requirements

| # | Requirement |
|---|-------------|
| R1 | Chunk documents (fixed size or paragraph — your choice, document it) |
| R2 | Build in-memory index: chunk_id → text + embedding vector |
| R3 | On `ask`: retrieve top-3 chunks by cosine similarity |
| R4 | System prompt: answer **only** from retrieved context; cite chunk IDs |
| R5 | If best similarity score < threshold (e.g. 0.5), print `CONFIDENCE: low` and `ANSWER: I don't have enough information.` |
| R6 | Redact any `sk-` patterns from logs (see production/03) |
| R7 | Use `MISTRAL_API_KEY` from environment — no hardcoded secrets |

### Out of scope

- Web UI, Slack bot, cloud vector DB
- PDF parsing (use `.md` and `.txt` only)
- Multi-user auth

---

## Milestones

Complete and verify each milestone before moving on.

### Milestone 1 — Ingest & chunk

**Goal:** `index` command loads all `.md`/`.txt` under `--docs` and prints chunk count.

```
INDEX_OK:docs=5:chunks=23
```

**Hints:** reuse logic from `rag/01_chunk_fixed` or `rag/02_chunk_paragraph`.

---

### Milestone 2 — Embeddings index

**Goal:** each chunk gets an embedding via Mistral `/embeddings`.

```
EMBED_INDEX_OK:chunks=23:dim=1024
```

Store as JSON sidecar: `data/.index/chunks.json` (gitignore this in your fork).

---

### Milestone 3 — Retrieve

**Goal:** given a question, print top-3 chunk IDs and scores.

```
RETRIEVE_OK:top1=hr_remote_policy#2:score=0.82
```

---

### Milestone 4 — RAG answer with citations

**Goal:** full `ask` flow with `ANSWER:`, `CITED:`, `CONFIDENCE:` lines.

Test with `eval/gold_questions.json` — at least 4/5 must cite the correct source file.

---

### Milestone 5 — Guardrails & eval

**Goal:**

- Low-confidence path for off-topic questions
- Redacted logging to stderr: `[REDACTED]` instead of API keys
- `eval` subcommand runs gold set and prints `EVAL:4/5`

---

## Project structure

```
01_doc_assistant_rag/
├── README.md           ← you are here
├── peer_review.md
├── hint.md
├── eval/
│   └── gold_questions.json
├── data/               ← sample corpus (provided)
│   ├── hr_remote_policy.md
│   ├── engineering_oncall.md
│   └── sales_discount_rules.md
├── schemas/
│   └── answer.schema.json
├── python/
│   └── main.py         ← your implementation
└── cpp/
    └── main.cpp        ← optional C++ track
```

---

## Evaluation rubric

| Criterion | Weight |
|-----------|--------|
| Correct chunking & indexing | 20% |
| Retrieval relevance (manual check on 5 questions) | 25% |
| Citations present and accurate | 25% |
| Low-confidence / refusal behavior | 15% |
| Code quality, env vars, no secrets in source | 15% |

---

## Sample gold questions

See `eval/gold_questions.json`. Your assistant should:

- Answer from the right document
- Include `CITED:<chunk_id>` matching that document
- Refuse `"What is the CEO's salary?"` (not in corpus)

---

## CLI sketch (Python)

```python
# python/main.py — structure only, you implement
import argparse

def cmd_index(docs: str) -> None: ...
def cmd_ask(docs: str, question: str) -> None: ...
def cmd_eval(docs: str) -> None: ...

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    # index, ask, eval ...
```

---

## Time estimate

| Phase | Hours |
|-------|-------|
| Milestones 1–2 | 4–6 |
| Milestones 3–4 | 6–8 |
| Milestone 5 + peer review | 4–6 |
| **Total** | **14–20** |

---

## Further reading

- RAG module README: when retrieval beats fine-tuning
- `rag/06_citations` — citation format
- `production/04_guardrail` — refusal patterns
