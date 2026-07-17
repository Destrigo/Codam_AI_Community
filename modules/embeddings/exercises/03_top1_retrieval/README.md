# Top-1 Retrieval

## Theory

This is the core operation behind every "semantic search" and RAG system: given a **query vector** and a small corpus of **document vectors**, find the single document whose embedding is closest to the query. At scale, this is done with approximate nearest-neighbor indexes (FAISS, HNSW, pgvector); at the scale of this exercise (2 documents), it's just a linear scan taking the `max`.

```python
def sim(a, b):
    return sum(x * y for x, y in zip(a, b))   # dot product

query = [1.0, 0.0]
docs = {"doc_a": [1.0, 0.0], "doc_b": [0.0, 1.0]}
best = max(docs, key=lambda k: sim(query, docs[k]))   # -> "doc_a"
```

Note the solution uses a raw **dot product** rather than full cosine similarity (see `02_cosine_similarity`) — for retrieval *ranking* (as opposed to reporting an absolute similarity score), that's a valid shortcut when all vectors are the same length, since dividing every candidate by the same query norm doesn't change which one is the maximum... though it still matters if document vectors have different magnitudes. `max(docs, key=...)` is the idiomatic Python way to find the *key* with the highest score, rather than the score itself.

## Assignment

Given query `[1, 0]` and two documents, `doc_a: [1, 0]` and `doc_b: [0, 1]`:

- Score every document against the query.
- Print the key of the best-scoring document as `TOP1:doc_a`.

Expected stdout:

```text
TOP1:doc_a
```

## Files to modify

- `python/main.py` — implement the similarity scoring function and the `max(..., key=...)` selection.
- `cpp/main.cpp` — implement the equivalent loop over a document map, tracking the best score/key.

## Verify

```bash
codam-labs --mock verify embeddings/03_top1_retrieval
```

Pure local math, no network calls — `--mock` is a no-op here but kept for command consistency.

## Troubleshooting

- **`max(docs.values())` instead of `max(docs, key=...)`**: `max(docs.values())` finds the highest-scoring *vector*, and `max(docs)` alone (no key) just does alphabetical string comparison on the keys — you need `max(docs, key=lambda k: sim(query, docs[k]))` to select by *computed score* while returning the *key*.
- **Off-by-one confusion between "score" and "similarity"**: this exercise's reference solution scores with a plain dot product, not normalized cosine — don't assume you must divide by norms here; both approaches happen to agree for this specific query/doc setup, but they aren't interchangeable in general (see the theory note above).
- **Iterating in a way that loses the key**: if you compute scores into a plain list without keeping track of which document each score belongs to, you can find the max *value* but not print which doc it came from.
- **Printing the score instead of the doc name**: the expected output is `TOP1:doc_a` — the document identifier, not the similarity number.

## Docs

- [Wikipedia — Cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) (background on the scoring metric family)
- [Pinecone learning center — What is a Vector Database?](https://www.pinecone.io/learn/vector-database/) — how this linear-scan idea scales to millions of documents
- [Mistral embeddings capability guide](https://docs.mistral.ai/capabilities/embeddings/)
