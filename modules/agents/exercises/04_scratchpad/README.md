# Scratchpad

## Theory

Not every piece of an agent's intermediate state belongs in the chat history sent back
to the model — a scratchpad is a place for the agent to jot notes, partial results, or
working memory *outside* the conversation, then selectively pull from it when
constructing the next prompt. This keeps the actual message history focused on what
the model needs to see, rather than bloating it with every intermediate calculation or
observation the agent made along the way.

## Assignment

Write a note into a scratchpad variable and print it with the `SCRATCH:` prefix.

**Expected output:**

```
SCRATCH:note
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify agents/04_scratchpad
```

No LLM call — purely local state, so `--mock` and live mode check the same output.

## Troubleshooting

- **Printing `SCRATCH:` with nothing after it?** Make sure the `scratch` variable is
  assigned the string `"note"` *before* the f-string is built — an empty or
  uninitialized variable prints as `SCRATCH:` with no value.
- **Storing the scratchpad as a list but printing the whole list?** `SCRATCH:['note']`
  won't match the substring check `"SCRATCH:note"` — if your scratchpad holds multiple
  entries, print a specific entry (`scratch[-1]`) or `.join()` them, not the raw
  container's `repr()`.
- **How is this different from a regular variable?** For this toy exercise, not much —
  the concept becomes meaningful once an agent loop appends to the scratchpad across
  multiple steps (e.g. "step 1 found X, step 2 found Y") and later reads it back to
  decide what to do next, without replaying the entire raw tool output history.

## Further reading

- [LangChain — `agent_scratchpad` in prompt construction](https://python.langchain.com/docs/how_to/agent_executor/#adding-in-memory)
- [ReAct paper — intermediate reasoning traces](https://arxiv.org/abs/2210.03629)
