# List Ollama Models

## Theory

Once you know the daemon is alive (exercise 01), the next question is "what can it actually
run?" Ollama tracks installed models locally and exposes them via
[`GET /api/tags`](https://github.com/ollama/ollama/blob/main/docs/api.md#list-local-models),
returning a `models` array with one entry per pulled model (including its tag, e.g.
`llama3.2:latest`).

Use `CODAM_LABS_OLLAMA_BASE` (set by `--mock`).

## Assignment

Fetch `{CODAM_LABS_OLLAMA_BASE}/api/tags`. Print `MODELS_OK:` followed by the number of
entries in the `models` array.

## Verify

```bash
codam-labs --mock verify ollama/02_list_models
```

Expected: `MODELS_OK:2`

## Troubleshooting

- **`MODELS_OK:0` in live mode** — you haven't `ollama pull`ed anything yet. `/api/tags`
  reflects locally installed models only; it can't list models you haven't downloaded, even
  if they exist in the Ollama library online.
- **`KeyError: 'models'`** — the response is `{"models": [...]}`, a plain list under one key
  — don't confuse it with the nested `details` object *inside* each model entry (name,
  format, family, etc.), which this exercise doesn't need at all.
- **Count includes duplicates** — each `name:tag` pair (e.g. `llama3.2:latest` vs.
  `llama3.2:1b`) is a separate entry even though they're "the same model" conceptually.
  That's expected — `len(data["models"])` counts installed tags, not distinct base models.
- **Mock always reports exactly 2** — the mock's fixed list is `llama3.2:latest` and
  `nomic-embed-text:latest` (the two models used by 03/05 and 06 respectively), regardless of
  what you've actually pulled locally.
