# Ollama Embeddings

## Theory

Chat models and embedding models are different artifacts. Ollama exposes embeddings on
[`POST /api/embeddings`](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings)
with a body like `{"model": "nomic-embed-text", "prompt": "..."}` and a response that is a
flat vector:

```json
{"embedding": [0.1, 0.2, 0.3]}
```

Contrast with Mistral's `/v1/embeddings` (used in `modules/embeddings`): there the vector lives
at `data[0].embedding`. Copying that path here yields `KeyError`. Live Ollama also needs an
*embedding* model pulled (`nomic-embed-text`); having only `llama3.2` is not enough.

The labs mock returns a 3-dimensional vector so verify can assert `EMBED_DIM:3`.

## Assignment

`POST {CODAM_LABS_OLLAMA_BASE}/api/embeddings` with:

- `model`: `"nomic-embed-text"` (or any string under `--mock`)
- `prompt`: `"codam ollama embed"`

Print `EMBED_DIM:` followed by `len(embedding)`.

## Files to modify

- `python/main.py`
- `cpp/main.cpp`

## Verify

```bash
codam-labs --mock verify ollama/06_embeddings
```

Expected (mock): `EMBED_DIM:3`.

## Troubleshooting

- **`KeyError: 'data'`** — Mistral-shaped parsing. Ollama returns `data["embedding"]` at the
  top level, not `data["data"][0]["embedding"]`.
- **Live `model not found`** — run `ollama pull nomic-embed-text`. Chat models do not serve
  this endpoint.
- **Printing the whole vector** — verify wants the **dimension** line `EMBED_DIM:N`, not the
  float list.
- **Wrong field name `input`** — Ollama's historical embeddings API uses **`prompt`**, not
  OpenAI's `input`. Check the payload keys against the Ollama docs linked below.
- **Forgetting `CODAM_LABS_OLLAMA_BASE`** — same dynamic-port issue as the other HTTP
  exercises in this module.

## Docs

- [Ollama API — embeddings](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings)
- [Mistral embeddings](https://docs.mistral.ai/capabilities/embeddings/) (different response
  envelope — useful contrast with `modules/embeddings/01_generate_embedding`)
