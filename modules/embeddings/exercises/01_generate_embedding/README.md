# Generate an Embedding

## Theory

An embedding model maps a piece of text to a fixed-length vector of floating-point numbers — a point in high-dimensional space where semantically similar texts land near each other. Unlike chat completions (`/chat/completions`, text in → text out), an embeddings call (`/embeddings`, text in → numbers out) never generates language at all; it's a pure encoding step, typically the *first* stage of any semantic search, clustering, or RAG pipeline.

```json
POST /embeddings
{"model": "mistral-embed", "input": "hello"}

Response:
{"data": [{"embedding": [0.021, -0.114, 0.008, ...]}]}
```

Real embedding models (Mistral's `mistral-embed` included) return vectors with hundreds or thousands of dimensions. In mock mode here, the fake server returns a deliberately tiny 3-dimensional vector so you can verify the request/response plumbing without needing to reason about high-dimensional output.

## Assignment

POST to the `/embeddings` endpoint with `input = "hello"`, using `MISTRAL_API_BASE` for the host.

- Read `data[0].embedding` from the JSON response.
- Print `EMBED_DIM:` followed by the length of that vector.

Expected stdout (mock mode):

```text
EMBED_DIM:3
```

## Files to modify

- `python/main.py` — build the POST request to `{MISTRAL_API_BASE}/embeddings`, parse `data[0]["embedding"]`, print its length.
- `cpp/main.cpp` — build the equivalent HTTP request and parse the response.

## Verify

```bash
codam-labs --mock verify embeddings/01_generate_embedding
```

Mock mode serves a fixed-size fake vector from a local mock server (no real Mistral credits spent, no `MISTRAL_API_KEY` required).

## Troubleshooting

- **Hitting `/chat/completions` instead of `/embeddings`**: it's an easy copy-paste mistake from the prompt_engineering exercises — double check the URL path is `/embeddings`, and that your payload key is `input` (a string), not `messages`.
- **Parsing `choices[0].message.content` instead of `data[0].embedding`**: the embeddings response shape is different from chat completions — there's no `choices`/`message` here, it's `data` (a list) with an `embedding` field.
- **Printing the vector itself instead of its length**: the expected output is `EMBED_DIM:3` (the dimension count), not the raw list of floats — use `len(vec)`, not `vec`.
- **Trailing slash issues in `MISTRAL_API_BASE`**: strip any trailing `/` before concatenating `/embeddings`, or you'll end up with a double-slash URL that some HTTP clients mishandle.

## Docs

- [Mistral API reference — Embeddings](https://docs.mistral.ai/api/#tag/embeddings)
- [Mistral embeddings capability guide](https://docs.mistral.ai/capabilities/embeddings/)
- [Python `urllib.request` docs](https://docs.python.org/3/library/urllib.request.html) (for building the raw HTTP POST without extra dependencies)
