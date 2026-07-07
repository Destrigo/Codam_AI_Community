# 08 — Streaming

## Theory

Without streaming, the API returns the **complete** response in one shot. The user waits in silence until the entire text is ready.

### Streaming (SSE)

With `"stream": true`, the server sends **Server-Sent Events**: text fragments as the model generates them.

Typical format:

```
data: {"choices":[{"delta":{"content":"Hello"}}]}

data: {"choices":[{"delta":{"content":" world"}}]}

data: [DONE]
```

Each `data:` line is a JSON chunk. The `delta.content` field contains the new piece (not the full response).

### Why use it

- **UX**: text appears progressively (like ChatGPT)
- **Perceived latency**: the first token arrives sooner
- **Early cancel**: you can stop if the response is not good enough

### Implementation

1. POST with `stream: true`
2. Read the response line by line (do not wait for the full body)
3. Parse each `data: {...}` except `[DONE]`
4. Accumulate or print `delta.content`

---

## Assignment

Call chat completions in **stream mode** with user `"hello"`.

Print the content chunks **concatenated** without extra newlines between them.

Expected output (mock): `MOCK_RESPONSE:hello ` (or similar, must contain `MOCK_RESPONSE`)

## Verify

```bash
codamlings verify 08_streaming
```
