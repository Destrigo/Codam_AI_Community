# Ollama — local LLM runtime

Run open models on your machine with the [Ollama HTTP API](https://github.com/ollama/ollama/blob/main/docs/api.md).

| # | Exercise | Topic |
|---|----------|-------|
| 01 | check_version | Daemon health |
| 02 | list_models | Installed models |
| 03 | chat | `/api/chat` completion |
| 04 | model_env | `OLLAMA_MODEL` in `.env` |
| 05 | stream_chat | NDJSON streaming |
| 06 | embeddings | Local embeddings |

## Setup

```bash
# Install: https://ollama.com/download
ollama serve
ollama pull llama3.2
ollama pull nomic-embed-text   # optional, for exercise 06
```

In code, use **`CODAM_LABS_OLLAMA_BASE`** (not `OLLAMA_BASE`):

```python
base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
```

Optional in repo root `.env` for live Ollama:

```bash
# CODAM_LABS_OLLAMA_BASE=http://localhost:11434   # optional; this is the default
OLLAMA_MODEL=llama3.2
```

**Verify offline (recommended for class / CI):**

```bash
codam-labs --mock --module ollama verify all
```

No Ollama install required with `--mock`.

Prerequisites: `core/`, `modules/local_llm`
