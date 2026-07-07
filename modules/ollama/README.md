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

Add to repo root `.env`:

```bash
OLLAMA_BASE=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

`codam-labs verify --mock` uses a built-in mock — no Ollama install required for CI.

Prerequisites: `core/`, `modules/local_llm`
