# Model Selection

## Theory
"Which model?" is a tradeoff between quality, latency, and cost — and it's usually the single
biggest lever you have without changing any code. A pipeline should read the model name from
configuration (an environment variable), not hardcode it, so that swapping models is a deploy-time
decision, not a code change.

**Worked example — three tiers for the same task:**

| Model | Relative quality | Relative latency | Where it runs |
|-------|-------------------|-------------------|----------------|
| `mistral-large-latest` | highest | slowest | cloud |
| `mistral-small-latest` | good | fast | cloud |
| local quantized 7B (e.g. via Ollama) | lower | fastest (no network hop) | your machine |

This exercise checks that your code *reads configuration* correctly rather than picking a model
name arbitrarily — the same pattern that lets a real deployment switch tiers via `.env` alone.

## Assignment
Read `MISTRAL_MODEL` from the environment (default `mistral-small-latest` if unset) and print
`MODEL:mistral-small-latest`.

## Files
- `python/main.py` — stub; single `os.environ.get(...)` call plus print.
- `hint.md` — `Read MISTRAL_MODEL env`.
- `solution/python/main.py` — reference implementation.

## Verify
```bash
codam-labs --mock verify local_llm/02_model_select
```
Expected stdout: `MODEL:mistral-small-latest`. `codam-labs --mock` does not override
`MISTRAL_MODEL`, so the default from `.env.example` (`mistral-small-latest`) is what should print
unless you've set it differently in your own `.env`.

## Troubleshooting
- **Wrong default value** — if you hardcode a different fallback than `mistral-small-latest`, the
  check fails whenever `MISTRAL_MODEL` isn't set in the environment.
- **Reading the wrong env var name** — `MISTRAL_API_MODEL`, `MODEL`, and `MISTRAL_MODEL` all look
  plausible; the repo's convention (see `.env.example` and `codam_ai_labs/config.py`) is
  `MISTRAL_MODEL`.
- **Env var set in one shell but not the one running the exercise** — `export`ing a variable in
  an interactive shell doesn't propagate to a different terminal/process; use the repo's `.env`
  file (loaded automatically by `codam-labs`) instead of ad-hoc shell exports.
- **Silent typos in model names** — unlike a missing file, a misspelled model name
  (`mistral-smal-latest`) won't fail locally in this exercise (it's just a string), but will 404
  against the real API — validate against the actual model catalog before shipping.

## Docs
- [Mistral: model catalog](https://docs.mistral.ai/getting-started/models/) — current model names, context sizes, pricing tier.
- `private/codam_AI_community/codam_ai_labs/config.py` — where this repo centralizes `MISTRAL_MODEL_DEFAULT`.
