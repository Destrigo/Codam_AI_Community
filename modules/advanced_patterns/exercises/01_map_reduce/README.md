# Map-Reduce Summarization

## Theory
A model's context window is finite. A 50-page contract won't fit in one prompt alongside your
instructions and a useful answer budget. Map-reduce sidesteps the limit:

1. **Map** — split the document into chunks, summarize each chunk *independently* (these calls
   can run in parallel — no chunk needs to see another).
2. **Reduce** — feed the per-chunk summaries (much shorter than the originals) into one final
   call that merges them into a single coherent summary.

**Worked example — summarizing a two-section incident report:**

```text
Chunk 1: "aa"  → map → length 2
Chunk 2: "bb"  → map → length 2
Reduce:  sum([2, 2]) = 4
```

This exercise uses `len()` as a stand-in "summary" so you can verify the map/reduce *shape*
without needing real model calls for every chunk.

## Assignment
Map two chunks (`"aa"`, `"bb"`) to their lengths, reduce with `sum`, and print `MAP_REDUCE_OK`
when the total is `4`.

## Files
- `python/main.py` — stub with `chunks = ["aa", "bb"]` predefined.
- `hint.md` — `map sum len, reduce`.
- `solution/python/main.py` — reference: list comprehension (map) + `sum()` (reduce).

## Verify
```bash
codam-labs --mock verify advanced_patterns/01_map_reduce
```
Expected stdout: `MAP_REDUCE_OK`.

## Troubleshooting
- **Off-by-one on chunk count** — verify you're mapping *both* chunks, not just the first; a
  common bug is indexing `chunks[0]` twice.
- **Reduce runs before map finishes** — in a real (async) implementation, gather all map results
  before starting the reduce call; don't reduce partial results.
- **Chunk boundaries cut mid-sentence** — with real text (not this exercise's toy strings), naive
  fixed-size chunking can split a sentence across two chunks and confuse the per-chunk summary;
  prefer paragraph/sentence-aware splitting (see `rag/01_chunk_fixed` vs `rag/02_chunk_paragraph`).
- **Skipping the reduce step entirely** — printing the map results directly (`["aa", "bb"]`)
  isn't a summary; the reduce call is what actually merges them into one answer.

## Docs
- [LangChain: summarization map-reduce guide](https://python.langchain.com/docs/tutorials/summarization/)
- [Mistral: context window sizes by model](https://docs.mistral.ai/getting-started/models/)
- Related: `modules/rag/exercises/01_chunk_fixed`, `modules/rag/exercises/02_chunk_paragraph`
