# Top-k Retrieval

## Theory

Returning only the single best-matching chunk is fragile — the "right" answer is often
spread across two or three chunks, or the top match is merely *close* rather than
*correct*. **Top-k retrieval** returns the `k` highest-scoring chunks instead of just
one, giving the generation step more context to work with at the cost of a slightly
noisier prompt. Choosing `k` is a real tuning knob in production RAG systems: too small
and you miss relevant context, too large and you waste context-window budget (see
`07_context_overflow`) or dilute the signal with irrelevant chunks.

## Assignment

Given three scored chunks:

```python
scores = [("a", 0.9), ("b", 0.8), ("c", 0.1)]
```

sort by score (descending) and keep the top **2**.

**Expected output:**

```
TOPK:2
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify rag/04_top_k
```

No LLM involved — this is pure sorting/slicing logic, identical under `--mock` or live.

## Troubleshooting

- **`TOPK:3`?** You sliced `[:2]` after sorting *ascending* by mistake, which still
  gives 2 items but if you instead forgot to slice at all you'd keep all 3 — check that
  your slice comes after the sort, not before.
- **Sorted the wrong direction?** `sorted(scores, key=lambda x: -x[1])` (or
  `reverse=True`) is required — sorting ascending puts `"c"` (lowest score) first,
  which would silently retrieve the *worst* matches instead of the best ones. The count
  check here won't catch that bug, so double check the actual chunk ids you keep.
- **Ties in score:** Python's `sorted()` is stable, so equal scores keep their original
  relative order — useful to know once you plug in real cosine-similarity floats that
  rarely tie exactly, but can matter with rounded scores.

## Further reading

- [LangChain — Vector store retrievers (similarity_search top-k)](https://python.langchain.com/docs/how_to/vectorstore_retriever/)
- [Pinecone — What is a vector database (top-k search)](https://www.pinecone.io/learn/vector-database/)
