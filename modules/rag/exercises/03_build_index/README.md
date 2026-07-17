# Build an Index

## Theory

Once you have chunks, you need somewhere to put them. A production system reaches for
FAISS, pgvector, or a managed vector DB, but conceptually an **index** is just a
collection of records — each holding an id, the chunk text, and (eventually) its
embedding — that you can search over later. This exercise builds the simplest possible
version: an in-memory list of records. Exercises `04_top_k` and `05_rag_pipeline` will
search and consume this structure, so getting the shape right here matters even though
the storage itself is trivial.

## Assignment

Build an in-memory index containing 3 chunk records and print its size.

**Expected output:**

```
INDEX_SIZE:3
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify rag/03_build_index
```

Purely local logic — no network calls, no API key needed, `--mock` or live give
identical results.

## Troubleshooting

- **`INDEX_SIZE:0`?** Make sure you're appending records inside the loop/comprehension
  and not re-initializing the list after populating it.
- **Counting embedding dimensions instead of records?** `INDEX_SIZE` refers to the
  number of *chunks* stored, not the length of an embedding vector — don't confuse
  `len(index)` with `len(index[0]["embedding"])`.
- **Using a `dict` keyed by id instead of a `list`?** Both work for this check since
  `len()` applies to either, but a `list` of record dicts scales more naturally once you
  add metadata (source file, offset, score) in later modules.

## Further reading

- [FAISS — Getting started](https://github.com/facebookresearch/faiss/wiki/Getting-started)
- [LlamaIndex — Index concepts](https://docs.llamaindex.ai/en/stable/module_guides/indexing/index_guide/)
