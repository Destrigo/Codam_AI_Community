# MCP + LLM Bridge

## Theory

01–05 built the raw MCP plumbing by hand. In a real agent, the *LLM* is the one deciding
which MCP tool to call, based on the user's request and the manifest it was shown (the
"model-controlled" nature of tools —
[Understanding MCP servers → Tools](https://modelcontextprotocol.io/docs/learn/server-concepts)).
This exercise stands in for that decision step with a single chat call: send Mistral a
prompt that clearly signals an MCP-tool-selection scenario, and let the model's reply be the
"bridge" between the two worlds. See the
[Mistral chat completions API](https://docs.mistral.ai/api/#tag/chat) for the request shape
this exercise builds on top of (same pattern as `core/04_llm_first_call`).

## Assignment

Call Mistral with the user message `mcp bridge select tool search`. Print the assistant's
reply — it will contain `MCP_BRIDGE_OK`.

## Verify

```bash
codam-labs --mock verify mcp/06_bridge_llm
```

Expected: output containing `MCP_BRIDGE_OK`

## Troubleshooting

- **`401 Unauthorized`** — `MISTRAL_API_KEY` is missing or invalid. Set it in the repo-root
  `.env` (never hardcode it in `main.py`), or use `--mock` while you iterate — the mock
  doesn't check the key at all.
- **Response is `MOCK_RESPONSE:...` instead of `MCP_BRIDGE_OK`** — the mock's canned reply
  logic only recognizes the exact phrase `mcp bridge` (case-insensitive) inside the user
  message. Rephrasing to "use MCP to find a tool" or similar will *not* trigger it — this is
  unlike a live model, which would respond sensibly to any phrasing.
- **`KeyError: 'choices'`** — this exercise talks to Mistral (OpenAI-shaped response:
  `choices[0].message.content`), not the Ollama or MCP-mock endpoints from the rest of this
  module, which use `message.content` or `result`/`content` directly. Mixing up the response
  shape across modules is the most common bug here.
- **Peer review flags a hardcoded key** — see `peer_review.md` in this exercise: API keys
  belong only in the repo-root `.env`, read via `os.environ.get("MISTRAL_API_KEY", "")`.
