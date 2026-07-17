# Agent Loop

## Theory

A "tool call" (previous module) is a single request/response. An **agent** repeats that
cycle — think, act, observe, think again — until the task is actually done, not just
until one API call returns. This is the **ReAct** pattern (Reason + Act): the model
reasons about what to do next, takes an action (often a tool call), observes the
result, and loops. Everything else in this module (`02_max_steps`, `03_planner`,
`04_scratchpad`) is a refinement bolted onto this same basic loop.

## Assignment

Simulate an agent that runs for exactly 3 steps and print how many steps it completed.

**Expected output:**

```
AGENT_DONE:3
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify agents/01_agent_loop
```

No LLM call in this exercise — it's the loop *mechanics*, so `--mock` and live mode
check the same output.

## Troubleshooting

- **Printing `AGENT_DONE:0` or nothing?** Make sure the step counter is incremented
  *inside* the loop body and the final printed value reflects the loop actually having
  run 3 times, not a hardcoded variable that never changes.
- **Off-by-one from `range(3)`?** `range(3)` yields 3 iterations (`0, 1, 2`) — that's
  correct here; the bug to watch for is printing the *last index* (`2`) instead of the
  *count* (`3`).
- **This looks trivial — where's the "agent"?** Deliberately so: this exercise isolates
  the loop-termination bookkeeping before any tool calls or LLM reasoning get added on
  top in `05_two_tools`. Get the step counting right first.

## Further reading

- [Yao et al. — ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [LangChain — Agent concepts overview](https://python.langchain.com/docs/concepts/agents/)
