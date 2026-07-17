# Human-in-the-Loop

## Theory

Some actions are too risky to let an agent execute autonomously — sending an email,
deleting a file, spending money. **Human-in-the-loop (HITL)** gating adds a checkpoint:
the agent proposes an action but doesn't actually run it until a human explicitly
confirms. This is the same pattern behind Cursor's own "approve this command" prompts
and CI systems that require manual approval before deploying to production — the agent
does the reasoning, a human keeps veto power over the consequential step.

## Assignment

Gate a (simulated) destructive action behind a `confirmed` flag: only "act" and print
success if the flag is `True`.

**Expected output:**

```
CONFIRM_OK
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify agents/06_human_confirm
```

No LLM call — this is control-flow logic around a boolean gate, so `--mock` and live
mode check the same output.

## Troubleshooting

- **Printing `BLOCKED` instead of `CONFIRM_OK`?** Check that `confirmed` is actually set
  to `True` before the conditional runs — this exercise hardcodes the confirmation for
  simplicity, but the branch that prints `BLOCKED` is exactly what should fire in
  production when a human has *not* yet approved.
- **Only implemented the "always confirmed" happy path?** Try extending it: flip
  `confirmed = False` locally and verify you get `BLOCKED` instead of `CONFIRM_OK` — a
  gate that can't actually block anything isn't a gate.
- **How would this look with a real prompt for confirmation?** In an interactive CLI,
  you'd replace the hardcoded flag with something like
  `input("Proceed? [y/N] ").lower() == "y"` before gating the action — the important
  part for this exercise is that the *action itself* (the risky side effect) only runs
  inside the `if confirmed:` branch, never before it.

## Further reading

- [LangChain — Human-in-the-loop guide](https://python.langchain.com/docs/how_to/human_in_the_loop/)
- [LangGraph — human-in-the-loop breakpoints](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/breakpoints/)
