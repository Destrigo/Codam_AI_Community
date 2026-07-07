# Codam AI Community — Codamlings

Interactive [Rustlings](https://github.com/rust-lang/rustlings)-style exercises to learn AI/LLM with **Python** and **C++**.

## Structure

```
core/           ← common track (10 exercises)
modules/        ← 9 stand-alone categories (50 exercises)
capstones/      ← 3 final projects (after modules)
business_cases/ ← 3 real-world ingestion scenarios (workshops)
codamlings/     ← terminal CLI
```

**60 exercises** + **3 capstones** + **3 business cases**.

## Quick start

```bash
pip install -e .
codamlings          # show next exercise
codamlings watch    # verify loop on save
codamlings list     # progress
codamlings verify all
```

## Commands

| Command | Description |
|---------|-------------|
| `codamlings` | Next incomplete exercise + README |
| `codamlings list` | List exercises and status |
| `codamlings run [slug]` | Run an exercise (live Mistral by default) |
| `codamlings verify [slug\|all]` | Verify output (live Mistral by default) |
| `codamlings verify all --module rag` | Verify a whole module |
| `codamlings list --module all` | Progress across modules |
| `codamlings hint [slug]` | Peer review rubric + hint (not solution) |
| `codamlings hint [slug] --solution` | Instructor solution only |
| `codamlings review rubric [slug]` | Show peer review checklist |
| `codamlings review submit [slug]` | Submit code for peer review |
| `codamlings review approve [slug]` | Approve peer review (marks complete) |
| `codamlings watch` | Rustlings-style mode |
| `--lang python\|cpp` | Language (default: python) |
| `--mock` | Offline mock server (CI / no API key) |

## Configuration

```bash
cp .env.example .env
# Required for live verify/run (default):
export MISTRAL_API_KEY=sk-...
export MISTRAL_API_BASE=https://api.mistral.ai/v1
export MISTRAL_MODEL=mistral-small-latest
```

Live mode uses your real Mistral key. Use `--mock` only for offline testing.

## Completing exercises

Two paths to mark an exercise **done**:

1. **Automated verify** — `codamlings verify <slug>` (checks output against rubric)
2. **Peer review** — `codamlings review submit` → peer runs `review rubric` → `review approve`

Students should use `codamlings hint` (shows `peer_review.md`), not `solution/`.

## Philosophy

Each exercise includes:

- **README** with theory + assignment
- **hint.md** with progressive hints
- **peer_review.md** with checklist (alternative to reading `solution/`)
- **solution/** with instructor reference (use `hint --solution`)
- **python/** and **cpp/** mirror implementations

Finish `core/`, then pick the stand-alone modules you care about.

## Capstones & business cases

| Track | Path | Description |
|-------|------|-------------|
| Capstones | [`capstones/`](capstones/README.md) | 3 medium projects: RAG assistant, ops agent, LLM gateway |
| Business cases | [`business_cases/`](business_cases/README.md) | Retail catalog, AP invoices, insurance FNOL |

Capstones require completing relevant modules. Business cases are workshop-style scenarios with sample data and canonical JSON schemas.
