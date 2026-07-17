# Query Router

## Theory
Not every user query needs the same pipeline. A router looks at the query first and dispatches it
to the cheapest/most-accurate pipeline for that *type* of question, instead of running every
query through the most expensive path "just in case."

**Worked example — a product-support assistant:**

| Query | Type | Route |
|-------|------|-------|
| `"what is your return window?"` | factual, needs grounded docs | `rag` |
| `"lol thanks, you're the best"`  | small talk | `chat` |

Routing can be a cheap heuristic (keyword/prefix match, like this exercise), a small classifier
model, or the primary model itself doing function-calling to pick a route (see `tools/02_tool_select`
for the function-calling flavor of the same idea).

## Assignment
Route a query starting with `"what"` to `rag`; print `ROUTE:rag` for the query
`"what is RAG"`.

## Files
- `python/main.py` — stub with `route(q)` partially defined.
- `hint.md` — `if what/when/how -> rag`.
- `solution/python/main.py` — reference: `q.startswith("what")`.

## Verify
```bash
codam-labs --mock verify advanced_patterns/02_router
```
Expected stdout: `ROUTE:rag`.

## Troubleshooting
- **Case sensitivity** — `"What is RAG"` (capital W) won't match `startswith("what")`; lowercase
  the query before routing.
- **Overlapping heuristics** — as you add more route types (`chat`, `tool`, `rag`), keyword rules
  can start matching more than one route; order your `if`/`elif` chain deliberately, most specific
  first.
- **No default route** — every router needs a fallback for queries that match nothing; here it's
  `chat`, but forgetting a default means unclassified queries crash instead of degrading
  gracefully.
- **Confusing routing with answering** — the router's job stops at picking a pipeline; don't have
  it also try to answer the question inline, or you lose the cost/latency benefit of routing.

## Docs
- [Mistral: function calling](https://docs.mistral.ai/capabilities/function_calling/) — model-driven routing via tool selection.
- Related: `modules/tools/exercises/02_tool_select/README.md`, `modules/rag/exercises/05_rag_pipeline/README.md`
