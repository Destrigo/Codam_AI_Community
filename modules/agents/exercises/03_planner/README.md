# Planner

## Theory

Jumping straight into tool calls without a plan works for simple tasks but falls apart
on multi-step ones — an agent that "figures it out as it goes" tends to wander, retry
the same failed approach, or lose track of the original goal. A **planner** decomposes
the task into an ordered list of subtasks *before* execution starts, so the agent loop
has a checklist to work through instead of improvising at every step. This is the core
idea behind "plan-and-execute" agent architectures, as opposed to purely reactive
ReAct-style loops.

## Assignment

Decompose a task into exactly 3 subtasks — for example `["research", "draft",
"review"]` — and print how many subtasks the plan contains.

**Expected output:**

```
PLAN:3
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify agents/03_planner
```

No LLM call — this exercise is about the plan *data structure*, not generating it with
a model, so `--mock` and live mode are identical.

## Troubleshooting

- **`PLAN:1`?** You likely stored the whole task as one string instead of a list of
  separate subtask strings — `len("research draft review")` counts characters, not
  list items; make sure `plan` is an actual list/array.
- **Hardcoded `print("PLAN:3")` without building a real list?** Passes the check but
  defeats the point — build an actual `plan` list and print `len(plan)` so the count
  reflects real data, which matters once you extend this to have an LLM generate the
  plan dynamically.
- **Want the model to generate the plan instead of hardcoding it?** That's a natural
  extension: prompt for "break this task into an ordered list of steps," parse the
  response into a list, then feed each subtask into the agent loop from
  `01_agent_loop` one at a time.

## Further reading

- [LangChain blog — Plan-and-Execute agents](https://blog.langchain.dev/planning-agents/)
- [Wang et al. — Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
