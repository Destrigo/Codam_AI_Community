# Codam AI Community — Codam AI Labs

Interactive [Rustlings](https://github.com/rust-lang/rustlings)-style exercises to learn AI/LLM with **Python** and **C++**.

> New here? Start with the **[Student Onboarding Guide](ONBOARDING.md)**.

## Structure

```
core/           ← common track (10 exercises)
modules/        ← 12 stand-alone categories (68 exercises)
capstones/      ← 3 final projects (after modules)
business_cases/ ← 3 real-world ingestion scenarios (workshops)
codam_ai_labs/  ← terminal CLI (package)
```

**78 exercises** + **3 capstones** + **3 business cases**.

## System requirements

Codam AI Labs runs on **Windows, macOS, and Linux**. No administrator privileges are required.

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

**Offline / CI:** `codam-labs --mock verify` starts a local mock server on `127.0.0.1` — no API keys, no Ollama install, no internet (after the first C++ build, which may download header-only deps via CMake).

**Environment constraints:** corporate firewalls or proxies may block cloud APIs or GitHub downloads. If live verify fails but `--mock` passes, check network access first.

Official CI runs on **Ubuntu** (GitHub Actions). Student machines on Windows or macOS are supported; report platform-specific issues if C++ builds fail.

## Quick start

```bash
pip install -e .
cp .env.example .env   # add your MISTRAL_API_KEY

# Linux / macOS
codam-labs list
codam-labs --mock --lang python verify 01_env_vars

# Windows (if `codam-labs` is not on PATH)
py -m codam_ai_labs list
py -m codam_ai_labs --mock --lang python verify 01_env_vars
```

**CLI flag order:** global options (`--mock`, `--lang`, `--module`) go **before** the subcommand:

```bash
codam-labs --mock verify ollama/03_chat        # ✅
codam-labs verify ollama/03_chat --mock        # ❌
```

## Commands

| Command | Description |
|---------|-------------|
| `codam-labs` | Next incomplete exercise + README |
| `codam-labs list` | List exercises and status |
| `codam-labs --module <name> list` | List one module |
| `codam-labs --lang python run <slug>` | Run an exercise (live Mistral by default) |
| `codam-labs --mock verify <slug>` | Verify offline (no API key) |
| `codam-labs --mock verify all` | Verify every exercise offline |
| `codam-labs --mock --module rag verify all` | Verify a whole module offline |
| `codam-labs hint <slug>` | Peer review rubric + hint (not solution) |
| `codam-labs hint <slug> --solution` | Instructor solution only |
| `codam-labs review rubric [slug]` | Show peer review checklist |
| `codam-labs review submit [slug]` | Submit code for peer review |
| `codam-labs review approve [slug]` | Approve peer review (marks complete) |
| `codam-labs watch` | Rustlings-style verify on save |
| `codam-labs capstone list` | List capstone projects |
| `codam-labs --mock capstone run <name> -- <args>` | Run capstone offline |
| `codam-labs --mock business run <name>` | Run business case offline |
| `--lang python\|cpp` | Language (default: python) — place before subcommand |
| `--mock` | Offline mock server (CI / no API key) — place before subcommand |

## Configuration

```bash
cp .env.example .env
# One .env at repo root — your personal Mistral key for every exercise:
export MISTRAL_API_KEY=sk-...
export MISTRAL_API_BASE=https://api.mistral.ai/v1
export MISTRAL_MODEL=mistral-small-latest
```

Each student manages their own key in `.env` (never commit it). Live mode uses that key for all `codam-labs run` / `verify` commands. Use `--mock` only for offline testing.

## Completing exercises

Two paths to mark an exercise **done**:

1. **Automated verify** — `codam-labs verify <slug>` (checks output against rubric)
2. **Peer review** — `codam-labs review submit` → peer runs `review rubric` → `review approve`

Students should use `codam-labs hint` (shows `peer_review.md`), not `solution/`.

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

```bash
codam-labs capstone list
codam-labs --mock capstone run 03_llm_gateway -- complete --prompt "Reply OK"
codam-labs --mock business run 01_retail_catalog_harmonization
```
