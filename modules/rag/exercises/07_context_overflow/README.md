# Context Overflow

## Theory

Retrieval doesn't stop being useful just because you found 5 relevant chunks and your
model only has room for 2. Every LLM has a finite **context window**, and stuffing in
too many chunks either gets truncated silently by the API, blows your token budget, or
dilutes the prompt so much that the model can't tell what matters. The fix is to select
or truncate *before* the API call — keep the highest-priority chunks (from `04_top_k`)
and drop or summarize the rest, rather than hoping everything fits.

## Assignment

Given 5 candidate chunks, select only the first 2 that fit the (simulated) context
budget and print a success marker.

**Expected output:**

```
TRUNCATED_OK
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify rag/07_context_overflow
```

No LLM call here either — included with `--mock` purely for a consistent verify
workflow across the module; live mode checks the exact same string.

## Troubleshooting

- **Printing `FAIL`?** The check only cares that your selected list has exactly length
  2 — if you sliced `chunks[:3]` or forgot to slice at all (keeping all 5), the length
  guard fails and prints `FAIL` instead of `TRUNCATED_OK`.
- **Picking the wrong 2 chunks?** For *this* toy example (`list(range(5))`) any 2
  elements satisfy the length check, but in real pipelines you should keep the chunks
  with the highest retrieval score (from top-k), not just the first N by index —
  otherwise you're throwing away your best matches to save space.
- **Thinking in tokens, not chunks?** Real truncation logic usually accumulates chunks
  until a running token count would exceed the model's context limit, rather than
  hard-coding "keep 2" — this exercise simplifies that to a fixed count so you can focus
  on the selection mechanic first.

## Further reading

- [Mistral AI — Models overview (context window sizes)](https://docs.mistral.ai/getting-started/models/)
- [OpenAI Cookbook — Managing context window length](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
