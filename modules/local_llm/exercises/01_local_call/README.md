# Local LLM Call

## Theory
Tools like Ollama and llama.cpp's server expose an OpenAI/Mistral-*shaped* HTTP API
(`POST /chat/completions` or `/api/chat`, same `messages` array) even though the model is running
entirely on your own machine. That means the same client code that talks to `api.mistral.ai` can
talk to `localhost:11434` — the only thing that changes is the base URL.

**Worked example — swapping providers without touching client code:**

```text
Cloud:  MISTRAL_API_BASE=https://api.mistral.ai/v1
Local:  MISTRAL_API_BASE=http://localhost:11434/v1   (or an Ollama/llama.cpp gateway)
```

Same `payload = {"model": ..., "messages": [...]}`, same response parsing
(`choices[0].message.content`). This exercise verifies that shape against the lab's mock, which
stands in for "local endpoint" here.

## Assignment
`POST {MISTRAL_API_BASE}/chat/completions` with a user message containing `"local llm"`, parse the
response, and print it (`LOCAL_OK`).

## Files
- `python/main.py` — stub with the payload/request already drafted; wire up the print.
- `hint.md` — `Same chat API, different base URL`.
- `solution/python/main.py` — reference implementation.

## Verify
```bash
codam-labs --mock verify local_llm/01_local_call
```
Expected stdout: `LOCAL_OK`.

## Troubleshooting
- **Assuming a different API shape** — a common mistake when moving to "local" is reaching for
  Ollama's native `/api/chat` format (`message.content` singular, not `choices[...]`) when the
  exercise actually targets the Mistral-shaped `/chat/completions` path; check which base/path
  you're actually calling. (See `modules/ollama/` for the native Ollama-shape exercises.)
- **Forgetting to change the base URL at all** — if `MISTRAL_API_BASE` is left pointing at the
  cloud default, you're not testing "local" behavior even though the code runs.
- **Trailing slash mismatches** — `http://localhost:11434/v1/` + `/chat/completions` can produce
  a double slash depending on how you concatenate; `rstrip("/")` the base before joining, as the
  solution does.
- **Real local servers need to actually be running** — outside `--mock`, a local exercise assumes
  Ollama/llama.cpp is already serving on the configured port; a connection-refused error usually
  means the local server isn't started, not a code bug.

## Docs
- [Ollama: OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility) — same request/response shape as cloud chat APIs.
- [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- Related: `modules/ollama/exercises/03_chat/README.md` for the native Ollama API shape.
