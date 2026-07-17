# Batch Compare

## Theory

Real retrieval systems don't compare a query against one document at a time interactively — they iterate over a **batch** (potentially thousands) of documents in one pass, scoring or transforming each. This exercise is deliberately minimal: it isolates the "loop over N items" shape from the actual similarity math, so you can be sure your iteration logic is solid before combining it with `cosine()` (from `02_cosine_similarity`) in a real batch-scoring pipeline.

```python
docs = ["a", "b", "c"]
lengths = [len(d) for d in docs]   # process every doc in the batch
```

In a full embeddings pipeline, this pattern generalizes to: embed every document once (ideally in a single batched API call, since most embedding APIs — including Mistral's — accept a *list* of strings in one request rather than requiring N separate round trips), then score each against the query using the same `cosine()` or `sim()` function from the retrieval exercises. Batching like this is also a major performance/cost lever: one API call with 50 inputs is far cheaper than 50 separate calls.

## Assignment

Given the document list `["a", "b", "c"]`:

- Process every document in the batch (e.g. compute something per-item, such as its length).
- Print `BATCH_OK` once the batch has been processed.

Expected stdout:

```text
BATCH_OK
```

## Files to modify

- `python/main.py` — iterate over the 3-item document list and print `BATCH_OK` after processing.
- `cpp/main.cpp` — implement the equivalent loop over a `std::vector<std::string>`.

## Verify

```bash
codam-labs --mock verify embeddings/04_batch_compare
```

No network call in this exercise — `--mock` is a no-op but consistent with the rest of the module.

## Troubleshooting

- **Skipping the loop entirely**: since the exercise doesn't check the per-item computation's output, it's tempting to just `print("BATCH_OK")` with no loop at all — that technically passes the check, but misses the point; actually iterate over all 3 documents to build the habit for when this scales up to real embedding batches.
- **Off-by-one in a manual loop**: if you use `for i in range(len(docs) - 1)` or similar instead of `for d in docs`, you'll silently skip the last document — prefer iterating directly over the collection rather than manually indexing.
- **Printing `BATCH_OK` before the loop runs**: make sure the print statement is *after* the batch processing, not a placeholder before it (this doesn't affect the current check but is the correct pattern to build on).
- **Confusing "batch" with "top-1"**: this exercise doesn't require comparing against a query or picking a winner (that's `03_top1_retrieval`) — it's just about processing every item in a collection.

## Docs

- [Mistral API reference — Embeddings](https://docs.mistral.ai/api/#tag/embeddings) (note the `input` field accepts a list of strings for batched embedding requests)
- [Mistral embeddings capability guide](https://docs.mistral.ai/capabilities/embeddings/)
- [Python docs — list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
