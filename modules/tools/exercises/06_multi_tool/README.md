# Multi-Tool Router

## Theory

Real assistants juggle more than one capability — a `search` tool for lookups, a
`calculator` for math, maybe a `fetch_url` for live data. **Routing** is the model's job
of picking the *right* tool from several candidates based on what the user actually
asked for, which only works if every candidate tool is described in the same request so
the model has real options to choose between (contrast with `02_tool_select`, where only
one tool existed).

## Assignment

Send a request offering **two** tools — `search` and `calculator` — with a user
message asking to search documentation. Print the assistant's response.

**Expected output:**

```
ROUTER:search
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify tools/06_multi_tool
```

Calls an LLM — prefer `--mock` in class. Live check with your own key:

```bash
codam-labs verify tools/06_multi_tool
```

## Troubleshooting

- **Getting the default `MOCK_RESPONSE:...` instead of `ROUTER:search`?** The mock
  requires **both** a non-empty `tools` array **and** the exact contiguous substring
  `"search docs"` (case-insensitive) in the user message. A message like `"can you
  search the docs"` has the words in the wrong order and won't match — use something
  like `"search docs for RAG"`.
- **Only sent one tool?** Even with the right trigger phrase, if `tools` only contains
  `calculator` (not `search`), the mock's `tools and "search docs" in ul` condition is
  still true (it only checks that *some* tools were sent) — but a real router prompt
  should offer every tool the model might plausibly pick, or the "routing" is fake.
- **Confusing this with `02_tool_select`?** That exercise expects `TOOL_CALL:calculator`
  triggered by the word `"calculate"`; this one expects `ROUTER:search` triggered by
  `"search docs"` — same endpoint, different trigger phrase and a longer `tools` list.

## Further reading

- [Mistral AI — Function calling guide (multiple tools)](https://docs.mistral.ai/capabilities/function_calling/)
- [Anthropic — Tool use with multiple tools](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
