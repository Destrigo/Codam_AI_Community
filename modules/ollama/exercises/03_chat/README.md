# Ollama Chat

## Theory

Ollama's non-streaming chat endpoint is
[`POST /api/chat`](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion)
with `"stream": false`. The response shape is **not** OpenAI/Mistral-style
`choices[0].message.content` — it is a top-level object:

```json
{
  "model": "llama3.2",
  "message": {"role": "assistant", "content": "..."},
  "done": true
}
```

That mismatch is the #1 bug when students copy `core/04_llm_first_call` patterns here.
The labs mock only returns the magic string when the user message contains
`ollama chat` — so the prompt text is part of the contract, not decoration.

## Assignment

`POST {CODAM_LABS_OLLAMA_BASE}/api/chat` with:

- `model`: `"llama3.2"`
- `messages`: one user message whose content is exactly `ollama chat hello`
- `stream`: `false`

Print only `message.content` from the JSON response.

## Files to modify

- `python/main.py`
- `cpp/main.cpp`

## Verify

```bash
codam-labs --mock verify ollama/03_chat
```

Expected (mock): stdout contains `OLLAMA_CHAT_OK`.

## Troubleshooting

- **`KeyError: 'choices'`** — you used the Mistral/OpenAI response path. Ollama puts the
  reply at `data["message"]["content"]`, not `data["choices"][0]["message"]["content"]`.
- **Mock prints a generic `MOCK_RESPONSE:...` (or empty / wrong text)** — the user content
  must include the substring `ollama chat`. Rewording to `"hello from ollama"` breaks the
  mock matcher even if your HTTP client is perfect.
- **`stream: true` by accident** — then the body is NDJSON (exercise 05), and a single
  `json.loads(r.read())` fails or returns only the first chunk. Keep `"stream": False`.
- **Hardcoded `http://localhost:11434`** — under `--mock` the daemon is on a dynamic port.
  Always use `CODAM_LABS_OLLAMA_BASE`.

## Docs

- [Ollama API — chat](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion)
- Contrast with [Mistral chat completions](https://docs.mistral.ai/api/#tag/chat) (`/v1/chat/completions`)
