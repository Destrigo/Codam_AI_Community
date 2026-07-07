# Codam AI Community — Codamlings

Interactive [Rustlings](https://github.com/rust-lang/rustlings)-style exercises to learn AI/LLM with **Python** and **C++**.

## Structure

```
core/           ← common track (10 exercises)
modules/        ← 12 stand-alone categories (68 exercises)
capstones/      ← 3 final projects (after modules)
business_cases/ ← 3 real-world ingestion scenarios (workshops)
codamlings/     ← terminal CLI
```

**78 exercises** + **3 capstones** + **3 business cases**.

## System requirements

Codamlings runs on **Windows, macOS, and Linux**. No administrator privileges are required.

| Component | Python track | C++ track (`--lang cpp`) |
|-----------|--------------|---------------------------|
| Python | **3.10+** | Same (CLI + verify) |
| Build tools | — | **CMake 3.16+**, C++17 compiler |
| Compiler | — | MSVC (Windows), gcc/clang (Linux/macOS) |

**Optional (live mode, by module):**

| Service | Used for | Notes |
|---------|----------|-------|
| [Mistral API](https://console.mistral.ai) | Most exercises | Personal `MISTRAL_API_KEY` in repo-root `.env` |
| [Ollama](https://ollama.com/download) | `modules/ollama` | `ollama serve` + `ollama pull llama3.2` (and `nomic-embed-text` for embeddings) |
| Internet | Live HTTP / API calls | `jsonplaceholder.typicode.com`, `httpbin.org`, cloud APIs |

**Offline / CI:** `codamlings verify --mock` starts a local mock server on `127.0.0.1` — no API keys, no Ollama install, no internet (after the first C++ build, which may download header-only deps via CMake).

**Environment constraints:** corporate firewalls or proxies may block cloud APIs or GitHub downloads. If live verify fails but `--mock` passes, check network access first.

Official CI runs on **Ubuntu** (GitHub Actions). Student machines on Windows or macOS are supported; report platform-specific issues if C++ builds fail.

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
# One .env at repo root — your personal Mistral key for every exercise:
export MISTRAL_API_KEY=sk-...
export MISTRAL_API_BASE=https://api.mistral.ai/v1
export MISTRAL_MODEL=mistral-small-latest
```

Each student manages their own key in `.env` (never commit it). Live mode uses that key for all `codamlings run` / `verify` commands. Use `--mock` only for offline testing.

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
