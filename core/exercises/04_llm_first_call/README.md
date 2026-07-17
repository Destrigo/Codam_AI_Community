# 04 — First LLM Call

## Theory

A **Large Language Model (LLM)** predicts text, one token at a time. Cloud providers expose that capability as a plain HTTP service — which is exactly why exercises `02` and `03` made you practice GET and POST first. There's no new networking concept here, just a new endpoint shape.

### The Chat Completions API

Standard endpoint (Mistral-compatible, and shared by most providers today): `POST /v1/chat/completions`

Request:

```json
{
  "model": "mistral-small-latest",
  "messages": [
    {"role": "user", "content": "hello!"}
  ]
}
```

Response:

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      }
    }
  ]
}
```

The text you want is buried at `choices[0].message.content` — `choices` is a list because some providers support returning several candidate completions in one call (you'll only ever ask for one here).

### Authentication

Header `Authorization: Bearer <API_KEY>`. The key comes from `MISTRAL_API_KEY`, the endpoint from `MISTRAL_API_BASE` (default `https://api.mistral.ai/v1`). Both are environment variables — exactly the pattern from exercise `01`, now protecting something that actually costs money if leaked.

### Why this exact API shape

[Mistral's API](https://docs.mistral.ai/api/) follows the same `chat/completions` contract used by OpenAI and most other providers. Write the client once against this shape, and swapping providers later is mostly a matter of changing `MISTRAL_API_BASE` and the `model` field.

### `codam-labs verify`

In `--mock` mode, `MISTRAL_API_BASE` points at a local mock server — no real API key required, no network call leaves your machine, and no cost.

---

## Assignment

Write a reusable `chat_completion(messages)` function, then call the API with:

- `model`: `"mistral-small-latest"` (the mock ignores the exact value, but always send one)
- `messages`: a single user message, `"hello"`

Print **only** the assistant's response content (`choices[0]["message"]["content"]`) — no labels, no extra formatting.

With `--mock`, the output contains `MOCK_RESPONSE` (exact mock text: `MOCK_RESPONSE:hello`).

## Files to modify

- `python/main.py` — implement `chat_completion(messages)`
- `cpp/main.cpp` — same, using libcurl + nlohmann/json

## Verify

```bash
codam-labs --mock verify 04_llm_first_call
```

To try it against the real Mistral API (needs `MISTRAL_API_KEY` in your `.env`):

```bash
codam-labs verify 04_llm_first_call
```

## Troubleshooting

- **`401 Unauthorized` on live mode** — `MISTRAL_API_KEY` is missing, empty, or malformed in your `.env`. Not needed at all for `--mock`.
- **`404 Not Found` on the endpoint** — check you're posting to `{MISTRAL_API_BASE}/chat/completions`, and that you stripped a trailing slash from `MISTRAL_API_BASE` before concatenating (`.rstrip("/")`) — otherwise you get a URL like `.../v1//chat/completions`.
- **Missing `Authorization` header entirely** — even with a key set in `.env`, forgetting `request.add_header("Authorization", f"Bearer {api_key}")` means the server never sees it. `--mock` won't catch this since it ignores auth; live mode will 401.
- **Printing the wrong nesting level** — `print(data["choices"])` prints the whole list of dicts; you need `data["choices"][0]["message"]["content"]` specifically.
- **`chat_completion` raising `NotImplementedError`** — that's the starter stub; nothing "breaks", it's just not implemented yet. Replace the `raise` with the real POST logic.

## Docs & further reading

- [Mistral API reference — Chat Completions](https://docs.mistral.ai/api/#tag/chat)
- [Mistral — Quickstart](https://docs.mistral.ai/getting-started/quickstart/)
- [Python docs — `urllib.request`](https://docs.python.org/3/library/urllib.request.html)
