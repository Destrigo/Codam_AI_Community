# Codam AI Community — Codamlings

Interactive [Rustlings](https://github.com/rust-lang/rustlings)-style exercises to learn AI/LLM with **Python** and **C++**.

## Structure

```
core/           ← common track (10 exercises)
modules/        ← 9 stand-alone categories (50 exercises)
codamlings/     ← terminal CLI
```

**60 exercises total** — Python and C++ for each.

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
| `codamlings run [slug]` | Run an exercise |
| `codamlings verify [slug\|all]` | Verify output |
| `codamlings verify all --module rag` | Verify a whole module |
| `codamlings list --module all` | Progress across modules |
| `codamlings hint [slug]` | Show hint |
| `codamlings watch` | Rustlings-style mode |
| `--lang python\|cpp` | Language (default: python) |
| `--mock` | Use local LLM mock (with `run`) |

## Configuration

```bash
cp .env.example .env
# For live execution:
export MISTRAL_API_KEY=sk-...
export MISTRAL_API_BASE=https://api.mistral.ai/v1
export MISTRAL_MODEL=mistral-small-latest
```

## Philosophy

Each exercise includes:

- **README** with theory + assignment
- **hint.md** with progressive hints
- **solution/** with reference answer
- **python/** and **cpp/** mirror implementations

Finish `core/`, then pick the stand-alone modules you care about.
