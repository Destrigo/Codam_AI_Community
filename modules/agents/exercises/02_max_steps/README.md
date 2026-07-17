# Max Steps

## Theory

An agent loop with no exit condition other than "the model says it's done" is one bad
reasoning step away from running forever — burning API calls and money while it
oscillates between two tool calls that never resolve. **Max-steps** is the seatbelt: a
hard iteration cap that forces the loop to stop and report failure gracefully instead of
looping indefinitely. Production agent frameworks (LangChain's `AgentExecutor`,
LangGraph's recursion limit) all implement some version of this same guard.

## Assignment

Run a loop that would iterate up to 10 times, but enforce a hard cap of **5 steps** and
break out once that cap is reached.

**Expected output:**

```
MAX_STEPS_OK
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify agents/02_max_steps
```

Purely local loop logic — no API call, so `--mock` and live mode check the identical
output.

## Troubleshooting

- **Loop runs all 10 iterations anyway?** Your `break` condition probably compares the
  wrong variable — check `if step + 1 >= max_steps: break` (comparing the *next* step
  count, since `step` itself is 0-indexed) rather than `if step >= max_steps`, which
  would let it run one extra iteration.
- **Breaks after only 4 iterations?** Classic off-by-one in the other direction — if
  you compare `step >= max_steps` with `step` starting at 0, you break when `step == 5`
  (the 6th iteration), one too many; if you compare `step > max_steps` you might break
  one too late. Trace through `step = 0, 1, 2, 3, 4` and confirm the break fires exactly
  when 5 steps have run.
- **Where does this fit with `01_agent_loop`?** `01` counts *completed* steps with no
  upper bound; this exercise adds the *cap* — the difference matters once a real agent
  loop consults the LLM each iteration and can't be trusted to stop on its own.

## Further reading

- [LangChain — AgentExecutor `max_iterations` parameter](https://python.langchain.com/docs/how_to/agent_executor/)
- [LangGraph — recursion limit for graph-based agents](https://langchain-ai.github.io/langgraph/how-tos/recursion-limit/)
