# 08 — Streaming

## Theory

Without streaming, the API waits until the **entire** response is generated, then sends it back in one shot. The user stares at a blank screen the whole time.

### Streaming with Server-Sent Events (SSE)

Set `"stream": true` and the server instead sends a sequence of small **Server-Sent Events** — text fragments as the model produces them:

```
data: {"choices":[{"delta":{"content":"Hello"}}]}

data: {"choices":[{"delta":{"content":" world"}}]}

data: [DONE]
```

Each `data: ` line carries one JSON chunk. The field is `delta.content` — a small *piece* of new text, not the accumulated response so far. `[DONE]` is a sentinel, not JSON — don't try to parse it.

### Why it's worth the extra complexity

- **UX**: text appears progressively, the way ChatGPT's interface does.
- **Perceived latency**: the first token shows up almost immediately, even if the full answer takes seconds.
- **Early cancel**: you can stop reading (and stop paying for tokens) the moment you see the response heading in the wrong direction.

### Implementation shape

1. POST with `"stream": true` in the body.
2. Read the response **line by line** instead of waiting for the full body.
3. For each line starting with `data: `, strip the prefix; if what's left is `[DONE]`, stop.
4. Otherwise `json.loads()` the remainder and read `choices[0]["delta"].get("content")`.
5. Accumulate (or print) each chunk as it arrives.

---

## Assignment

Call chat completions in **stream mode** with user message `"hello"`.

Concatenate the content chunks as they arrive, with no extra newlines inserted between them, and print the result.

Expected output (with `--mock`) contains `MOCK_RESPONSE` (the mock streams back `MOCK_RESPONSE:hello ` as a single chunk).

## Files to modify

- `python/main.py` — implement `chat_stream(messages)`

## Verify

```bash
codam-labs --mock verify 08_streaming
```

## Troubleshooting

- **Forgetting `"stream": true` in the payload** — without it, the mock (and a real provider) sends back a normal, complete JSON response instead of SSE chunks. If your code then tries to iterate the response line-by-line expecting `data: ` prefixes, it will either find nothing or crash trying to parse a plain JSON body as if it were a stream.
- **Calling `.read()` on the whole response before processing** — this defeats the purpose of streaming (you're back to waiting for everything at once), even if the mock still "passes" because it buffers the full body anyway. Iterate the response object or read incrementally instead.
- **Not handling `[DONE]`** — `json.loads("[DONE]")` doesn't crash (it happens to parse as a valid JSON array!), but treating it like a normal chunk and indexing `choices[0]` on it will `IndexError`. Check for the `[DONE]` sentinel explicitly and stop the loop.
- **Off-by-one on the `data: ` prefix strip** — `line.removeprefix("data:")` still leaves a leading space; forgetting `.strip()` afterward means `json.loads(" {...}")` (usually fine) but `json.loads(data)` where `data` still has `[DONE]` embedded oddly can misbehave. Strip whitespace after removing the prefix.
- **Introducing extra newlines while concatenating** — `print(chunk)` in a loop adds a newline after every chunk; the assignment wants chunks joined with nothing between them (`"".join(parts)`), then printed once at the end.

## Docs & further reading

- [MDN — Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Mistral / OpenAI-style streaming guide](https://docs.mistral.ai/api/#tag/chat) (`stream: true` on the chat completions endpoint)
