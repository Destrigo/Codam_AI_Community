# Capstone 03 — LLM Gateway (mini-pipeline prod)

## Brief (fictional client)

**Platform team** at a fintech startup: every squad calls Mistral directly with copy-pasted code. Incidents include quota exhaustion, leaked API keys in logs, and silent prompt regressions after "quick fixes."

**Your job:** build a small **LLM gateway** — one function `gateway.complete(prompt)` that every internal tool should use.

---

## Theory

Production LLM usage is 20% prompting and 80% **reliability**:

| Concern | Module exercise |
|---------|-----------------|
| Rate limits & retry | `production/01_rate_limit`, `core/09_timeout_retry` |
| Cache identical prompts | `production/02_cache` |
| Redacted logs | `production/03_redacted_log` |
| Guardrails | `production/04_guardrail` |
| Fallback model | `production/05_fallback` |
| Output tests | `production/06_output_test` |
| Eval set | `advanced_patterns/05_eval_set` |

This capstone packages them into a reusable client — no RAG, no agents.

---

## Prerequisites

- `core/` (all 10, especially 09)
- `modules/production` (all 6)
- `modules/advanced_patterns` (05_eval_set)

---

## Assignment

Build `llm_gateway` library + CLI:

```bash
# Single call
python python/main.py complete --prompt "Summarize GDPR in one sentence"
# GATEWAY_OK:<assistant text>

# Run eval suite
python python/main.py eval
# EVAL:9/10

# Show stats
python python/main.py stats
# STATS:calls=42:cache_hits=7:retries=2:fallbacks=1
```

### `Gateway` class API

```python
class Gateway:
    def complete(self, prompt: str, *, system: str = "") -> str: ...

    def stats(self) -> dict: ...
```

### Functional requirements

| # | Requirement |
|---|-------------|
| G1 | Read `MISTRAL_API_KEY`, `MISTRAL_API_BASE`, `MISTRAL_MODEL` from env |
| G2 | **Cache:** same `(system, prompt)` hash → return cached response, print `CACHE_HIT` to stderr |
| G3 | **Retry:** on HTTP 503, retry up to 3 times with exponential backoff (1s, 2s, 4s) |
| G4 | **Redacted logging:** log request metadata to stderr; replace `sk-...` with `[REDACTED]` |
| G5 | **Guardrail:** if user prompt contains `ignore instructions` (case-insensitive), return `BLOCKED:injection` without calling API |
| G6 | **Fallback:** if primary model fails after retries, try `MISTRAL_FALLBACK_MODEL` (default `mistral-small-latest`) |
| G7 | **Eval:** run `eval/prompts.json`; each entry has `prompt`, `must_contain` (substring). Print `EVAL:N/M` |

### Out of scope

- HTTP server / REST API wrapper
- Multi-tenant billing
- Distributed cache (Redis)

---

## Milestones

### Milestone 1 — Basic complete

`complete()` calls Mistral and prints `GATEWAY_OK:`.

---

### Milestone 2 — Retry + redacted logs

Simulate failures with mock `/fail_twice` (set `MISTRAL_API_BASE` to mock). Logs must not contain raw API key.

```
RETRY_OK
LOG_REDACTED
```

---

### Milestone 3 — Cache

Second identical call prints `CACHE_HIT` on stderr; no second HTTP request (verify with mock call counter or logging).

---

### Milestone 4 — Guardrail + fallback

Injection blocked. Primary failure triggers fallback model call → `FALLBACK_OK` on stderr.

---

### Milestone 5 — Eval suite

`eval` subcommand: **≥ 90%** of `eval/prompts.json` pass `must_contain` checks.

```
EVAL:9/10
```

---

## Project structure

```
03_llm_gateway/
├── README.md
├── peer_review.md
├── hint.md
├── eval/
│   └── prompts.json
├── schemas/
│   └── stats.schema.json
├── python/
│   ├── main.py
│   └── gateway.py      ← core library (you implement)
└── cpp/
    └── main.cpp
```

---

## Configuration

```bash
# .env
MISTRAL_API_KEY=sk-...
MISTRAL_API_BASE=https://api.mistral.ai/v1
MISTRAL_MODEL=mistral-small-latest
MISTRAL_FALLBACK_MODEL=mistral-small-latest   # or different model in prod
GATEWAY_CACHE_DIR=.gateway_cache              # optional
```

---

## Evaluation rubric

| Criterion | Weight |
|-----------|--------|
| Retry/backoff correct | 20% |
| Cache hit behavior | 20% |
| Redacted logs | 15% |
| Guardrail blocks injection | 15% |
| Fallback on primary failure | 15% |
| Eval suite ≥ 90% | 15% |

---

## Time estimate

**18–24 hours** total.

---

## Design note

Keep `gateway.py` **free of CLI code** so other capstones (Doc Assistant, Ops Agent) could import it later. This is how real platform teams structure shared libraries.
