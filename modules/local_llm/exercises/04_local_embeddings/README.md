# Local Embeddings

## Theory
RAG pipelines (`modules/rag/`) need an embeddings model to turn text into vectors. Running that
embeddings model locally (e.g. `nomic-embed-text` via Ollama, or a `sentence-transformers` model)
keeps document content from ever leaving your machine — useful for on-prem/regulated RAG over
sensitive documents, at the cost of managing the model yourself instead of calling a hosted API.

**Worked example — embedding a support-ticket for local semantic search:**

```text
Input:  "local"
Output: {"data": [{"embedding": [0.1, 0.2, 0.3], "index": 0}], "model": "mistral-embed"}
```

The request/response *shape* mirrors `modules/embeddings/exercises/01_generate_embedding` — the
difference is purely where `MISTRAL_API_BASE` points (a local gateway vs the cloud).

## Assignment
`POST {MISTRAL_API_BASE}/embeddings` with `{"model": "mistral-embed", "input": "local"}`, and print
`LOCAL_EMBED_OK` once the call succeeds.

## Files
- `python/main.py` — stub with the payload drafted; POST call and print need finishing.
- `hint.md` — `Same as embeddings exercise`.
- `solution/python/main.py` — reference implementation.

## Verify
```bash
codam-labs --mock verify local_llm/04_local_embeddings
```
Expected stdout: `LOCAL_EMBED_OK`.

## Troubleshooting
- **Wrong endpoint path** — Ollama's native embeddings path is `/api/embeddings` (singular
  `"embedding"` key in the response), while this exercise's mock uses the Mistral/OpenAI-shaped
  `/embeddings` (`"data": [{"embedding": [...]}]`, plural, list-wrapped). Confusing the two shapes
  is the single most common bug here — check `codam_ai_labs/mock_server.py`'s `do_POST` for both
  branches side by side.
- **Dimension mismatch with a real vector index** — a local embeddings model's vector dimension
  (e.g. 768) almost never matches a cloud embeddings model's (e.g. 1024+); if you swap embedding
  providers on an existing vector index, you must re-embed everything, not just new documents.
- **Timeout on first call** — a local embeddings model that isn't preloaded can be slow to respond
  to the very first request; don't mistake normal cold-start latency for a hung server.
- **Forgetting `Content-Type: application/json`** — same POST-body pitfall as the chat endpoints;
  the mock (and most real servers) will fail to parse the body without it.

## Docs
- [Ollama: embeddings API](https://docs.ollama.com/api#generate-embeddings)
- [Mistral: Embeddings API](https://docs.mistral.ai/api/#tag/embeddings)
- Related: `modules/embeddings/exercises/01_generate_embedding/README.md`
