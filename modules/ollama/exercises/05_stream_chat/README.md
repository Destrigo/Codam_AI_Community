# Ollama Streaming Chat

## Theory

With `"stream": true`, Ollama does **not** use Mistral-style Server-Sent Events
(`data: {...}\n\n`). It returns **NDJSON**: one JSON object per line, each carrying a
partial `message.content`, until a final object with `"done": true` (often **without** a
`message` field).

```text
{"message":{"role":"assistant","content":"OLLAMA_"},"done":false}
{"message":{"role":"assistant","content":"STREAM_OK"},"done":false}
{"done":true}
```

That is why copying `core/08_streaming` (SSE + `delta.content`) almost always fails here.
The mock only emits the stream when the user text contains `ollama stream`.

## Assignment

`POST {CODAM_LABS_OLLAMA_BASE}/api/chat` with:

- `model`: `"llama3.2"`
- `messages`: user content `ollama stream hello`
- `stream`: `true`

Read the response **line by line**, parse each non-empty line as JSON, append every
`message.content` fragment, and print the concatenated string (no extra separators).

## Files to modify

- `python/main.py`
- `cpp/main.cpp`

## Verify

```bash
codam-labs --mock verify ollama/05_stream_chat
```

Expected (mock): stdout contains `OLLAMA_STREAM_OK`.

## Troubleshooting

- **`json.JSONDecodeError` on the last line** — you assumed every line has `"message"`.
  Guard with `(chunk.get("message") or {}).get("content")` and skip empties / the final
  `done` frame.
- **Stripping a `data:` prefix** — that is SSE from Mistral. Ollama lines are raw JSON;
  stripping `data:` will corrupt the payload.
- **Printing each chunk on its own line** — verify looks for the concatenated token string.
  Join fragments with `"".join(parts)` (the mock already includes spaces inside chunks when
  needed).
- **Wrong trigger phrase** — user content must include `ollama stream`. Using the 03 phrase
  `ollama chat` routes you to the non-stream mock path.
- **Reading `r.read()` once** — that waits for the full body and fights streaming. Iterate
  `for line in r:`.

## Docs

- [Ollama API — streaming chat](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion)
  (see the `stream` flag)
- Contrast: [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
  (what `core/08_streaming` uses — different wire format)
