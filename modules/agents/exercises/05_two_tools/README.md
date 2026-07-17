# Two Tools

## Theory

A single-tool agent is really just the tool-execute pattern from the `tools` module
with extra ceremony. The interesting behavior starts once an agent has to **coordinate
multiple tools within one run** — e.g. search for information, then calculate something
with what it found — deciding which tool to reach for at each step rather than being
handed a single obvious choice. This exercise connects the agent loop concept to a real
LLM call for the first time in this module.

## Assignment

Send the user message **`"agent two tools"`** to the chat completions endpoint at
`MISTRAL_API_BASE` and print the assistant's response.

**Expected output:**

```
AGENT_TOOLS_OK
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify agents/05_two_tools
```

Calls an LLM — prefer `--mock` in class (no API key, no internet needed). Live check
with your own key:

```bash
codam-labs verify agents/05_two_tools
```

## Troubleshooting

- **Getting a generic `MOCK_RESPONSE:...` instead of `AGENT_TOOLS_OK`?** The mock
  matches on the exact substring `"agent two tools"` (case-insensitive) in your user
  message — check for typos like `"agent 2 tools"` or extra words that break the
  contiguous phrase.
- **Request timing out?** Confirm you're reading the base URL from `MISTRAL_API_BASE`
  (populated by `--mock`) instead of hardcoding the production Mistral endpoint —
  hardcoding it means the offline mock server is never reached.
- **Want to actually wire up two tools instead of relying on the mock string?** Combine
  this exercise with `tools/06_multi_tool`'s router: send both `search` and
  `calculator` in the `tools` array, then execute whichever one(s) the model requests
  and feed results back before printing the final answer.

## Further reading

- [Mistral AI — Chat Completion API reference](https://docs.mistral.ai/api/#tag/chat)
- [LangChain — Multi-tool agent examples](https://python.langchain.com/docs/how_to/tools_multiple/)
