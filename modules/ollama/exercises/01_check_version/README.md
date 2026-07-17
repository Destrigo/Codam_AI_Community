# Ollama Health Check

## Theory

[Ollama](https://ollama.com) serves open models locally over HTTP. Before making any chat or
embedding call, it's good practice to confirm the daemon is actually up — the
[`/api/version`](https://github.com/ollama/ollama/blob/main/docs/api.md#version) endpoint is
the cheapest possible way to do that, and this exercise is the first thing every later Ollama
exercise implicitly assumes works.

```python
base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
```

`--mock` points this at the local labs mock (no Ollama install needed).

## Assignment

Call `GET {CODAM_LABS_OLLAMA_BASE}/api/version`. Print `OLLAMA_OK:` followed by the
`version` field from the JSON response.

## Verify

```bash
codam-labs --mock verify ollama/01_check_version
```

Expected: `OLLAMA_OK:0.5.7-mock`

## Troubleshooting

- **Live mode, `ConnectionRefusedError`** — `ollama serve` isn't running, or nothing is
  listening on port `11434`. This is the *first* exercise where that would show up — if it
  fails here, every later live Ollama exercise will fail the same way for the same reason.
- **`OLLAMA_OK:0.5.7-mock` looks like a fake version** — it is; the mock always reports
  `0.5.7-mock` regardless of what's installed, specifically so `MOCK_CHECKS` can assert an
  exact string. A real daemon returns whatever version you actually have installed — don't
  expect this literal string outside `--mock`.
- **Printing the whole JSON dict instead of just the version** — `data["version"]` is a
  plain string; printing `data` directly would technically also contain `0.5.7-mock` as a
  substring, but it's not what the assignment asks for and makes the output noisier for the
  exercises after this one that build on the same request pattern.
