# Ollama — local LLM runtime

[Ollama](https://ollama.com) runs open-weight models on your own machine and exposes them
over a small HTTP API (see the [official API reference](https://github.com/ollama/ollama/blob/main/docs/api.md)).
This module mirrors the Mistral-cloud exercises in `core/` and `prompt_engineering/` but
against a **local** daemon — same idea of chat/completion, different transport and response
shape (`message.content`, not OpenAI-style `choices`).

| # | Exercise | Topic |
|---|----------|-------|
| 01 | check_version | Daemon health — `GET /api/version` |
| 02 | list_models | Installed models — `GET /api/tags` |
| 03 | chat | Completion — `POST /api/chat` |
| 04 | model_env | Choosing a model via `OLLAMA_MODEL` |
| 05 | stream_chat | NDJSON streaming — `POST /api/chat` with `stream: true` |
| 06 | embeddings | Local embeddings — `POST /api/embeddings` |

## Setup (live Ollama — optional)

`--mock` fakes every endpoint below, so a real Ollama install is **not required** to pass
these exercises. If you want to run against the real daemon:

```bash
# Install: https://ollama.com/download
ollama serve
ollama pull llama3.2            # used by 03, 04, 05
ollama pull nomic-embed-text    # used by 06
```

Code reads the daemon address from **`CODAM_LABS_OLLAMA_BASE`** — note the `CODAM_LABS_`
prefix; there is no plain `OLLAMA_BASE` anywhere in this repo:

```python
base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
```

Exercise 04 is the odd one out: it reads **`OLLAMA_MODEL`** (no `CODAM_LABS_` prefix, no HTTP
call at all) to pick a model name. 03 and 05 hardcode `"llama3.2"` in their solutions instead
of reading `OLLAMA_MODEL` — that's deliberate so 04 has something new to teach; don't expect
changing `OLLAMA_MODEL` to change what 03/05 print.

Optional repo-root `.env` for live runs:

```bash
# CODAM_LABS_OLLAMA_BASE=http://localhost:11434   # optional; this is already the default
OLLAMA_MODEL=llama3.2
```

**Verify offline (recommended for class / CI):**

```bash
codam-labs --mock --module ollama verify all
```

## Troubleshooting

- **`ConnectionRefusedError` in live mode** — `ollama serve` isn't running, or you're on the
  default port but the daemon bound to a different one. Confirm with
  `Invoke-WebRequest http://localhost:11434/api/version` (PowerShell) before blaming your code.
- **`404` / `"model not found"` in live mode** — you haven't `ollama pull`ed the model you're
  requesting. 06 needs an *embedding* model (`nomic-embed-text`), not a chat model — pulling
  `llama3.2` alone won't fix it.
- **05 prints nothing / hangs** — Ollama's streaming responses are **newline-delimited JSON**
  (`{"message": {...}}\n{"message": {...}}\n...`), not Server-Sent Events (`data: ...`) like
  the Mistral streaming exercise in `core/08_streaming`. Read the response line-by-line and
  `json.loads` each line; do **not** strip a `data:` prefix, there isn't one.
- **05's last line breaks `json.loads`** — the final NDJSON chunk is `{"done": true}` with no
  `"message"` key at all; guard with `chunk.get("message") or {}` before indexing `.content`.
- **Env var typo** — using `OLLAMA_BASE` instead of `CODAM_LABS_OLLAMA_BASE` silently falls
  back to `http://localhost:11434` and either times out (no daemon) or hits your real local
  Ollama instead of the mock, which is confusing during `--mock` runs.

Prerequisites: `core/`, `modules/local_llm`
