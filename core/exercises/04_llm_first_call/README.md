# 04 — First LLM Call

## Theory

A **Large Language Model (LLM)** is a model that predicts text. Cloud APIs expose it as an HTTP service.

### Chat Completions API

Standard endpoint (Mistral-compatible): `POST /v1/chat/completions`

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

### Authentication

Header `Authorization: Bearer <API_KEY>`.

The key comes from `MISTRAL_API_KEY`. The endpoint from `MISTRAL_API_BASE` (default: `https://api.mistral.ai/v1`).

### Why this API shape

[Mistral's API](https://docs.mistral.ai/api/) follows the same chat-completions format used by many providers. Write the client once; swap base URL and model as needed.

### codam-labs verify

In verify mode, `MISTRAL_API_BASE` points to a local mock — no real API key needed.

---

## Assignment

Call the chat completions API with:

- `model`: `"mistral-small-latest"` (or any string with the mock)
- `messages`: a single user message `"hello"`

Print **only** the assistant response content (`choices[0].message.content`).

With the mock, the output contains `MOCK_RESPONSE:hello`.

## Verify

```bash
codam-labs verify 04_llm_first_call
codam-labs run 04 --mock   # manual offline test
```
