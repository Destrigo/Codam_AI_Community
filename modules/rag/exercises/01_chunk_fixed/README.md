# Fixed-Size Chunking

## Theory

Embedding models and LLM context windows both have hard size limits, so before anything
can be indexed for retrieval it has to be cut into smaller pieces — **chunks**. The
simplest strategy is **fixed-size chunking**: walk the text in windows of `N`
characters (or tokens) and cut, regardless of where sentences or words fall. It's fast,
predictable, and a reasonable default when you don't yet know your corpus, but it can
slice a sentence (or a code block, or a table row) right down the middle. Later
exercises in this module (`02_chunk_paragraph`, `07_context_overflow`) build on this
idea with boundary-aware and budget-aware variants.

## Assignment

Chunk the string `"abcdefghij"` (10 characters) into fixed windows of size `4` and
print how many chunks you got.

Walking `"abcdefghij"` in steps of 4 characters produces `"abcd"`, `"efgh"`, `"ij"` —
three chunks, the last one shorter because 10 isn't a multiple of 4.

**Expected output:**

```
CHUNKS:3
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

Do not edit `solution/python/main.py`; it's the instructor reference (see
`codam-labs hint rag/01_chunk_fixed --solution` if you get stuck).

## Verify

```bash
codam-labs --mock verify rag/01_chunk_fixed
```

This exercise never calls an LLM, so `--mock` and live mode behave identically — it's
included here purely for consistency with the rest of the module.

## Troubleshooting

- **Getting `CHUNKS:2` or `CHUNKS:4`?** You likely used `range(0, len(text), size)` but
  computed `len(text)` wrong, or you rounded down and dropped the trailing `"ij"`
  fragment. The last (partial) chunk still counts.
- **Off-by-one on the loop bound?** Use `range(0, len(text), size)` and slice
  `text[i:i+size]` — Python slicing already clamps the upper bound, so you don't need
  a separate check for the final short chunk.
- **Empty chunks showing up?** Only happens if `size <= 0` or you slice past the string
  needlessly; not an issue here but worth guarding against for real documents.

## Further reading

- [Pinecone — Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
- [Python slice notation reference](https://docs.python.org/3/reference/expressions.html#slicings)
