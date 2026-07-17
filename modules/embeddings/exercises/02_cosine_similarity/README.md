# Cosine Similarity

## Theory

Once you have two embedding vectors, you need a number that says "how similar are these?" Cosine similarity measures the **angle** between two vectors, ignoring their magnitude — which is exactly what you want for embeddings, where direction encodes meaning but length is often just an artifact of the model.

$$\text{cosine}(a, b) = \frac{a \cdot b}{\lVert a \rVert \, \lVert b \rVert}$$

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb)
```

The result ranges from `-1.0` (opposite direction) through `0.0` (orthogonal / unrelated) to `1.0` (identical direction — same or highly similar meaning). Two identical vectors always give exactly `1.0`, which is the sanity-check case this exercise verifies: `cosine([1,0,0], [1,0,0]) == 1.0`. This is pure math — no API calls, no model involved — the kind of function you'd unit test in isolation before wiring it into a real similarity search.

## Assignment

Implement `cosine(a, b)`:

- Compute the dot product of `a` and `b`.
- Divide by the product of their Euclidean norms.
- For `a = [1, 0, 0]`, `b = [1, 0, 0]`, print `SIMILARITY:1.0` (one decimal place).

Expected stdout:

```text
SIMILARITY:1.0
```

## Files to modify

- `python/main.py` — implement `cosine(a: list[float], b: list[float]) -> float` and print the formatted result.
- `cpp/main.cpp` — implement the equivalent dot-product/norm computation over `std::vector<double>`.

## Verify

```bash
codam-labs --mock verify embeddings/02_cosine_similarity
```

Purely local computation — `--mock` has nothing to intercept here, but keep the flag for consistency with the rest of the module's verify commands.

## Troubleshooting

- **Division by zero on a zero vector**: if either `a` or `b` is all zeros, `na` or `nb` is `0.0` and you get a `ZeroDivisionError` — not exercised by this exact input, but worth knowing before reusing this function elsewhere.
- **Forgetting to divide by both norms**: a common bug is `dot / na` (dividing only by one vector's norm) — that's *projection*, not cosine similarity, and gives the wrong scale.
- **Formatting precision**: the expected output is `SIMILARITY:1.0`, exactly one decimal digit — printing the raw float (`0.9999999999999998` due to floating point, or `1.0` with more/fewer digits) can fail an exact-string check; use `f"{value:.1f}"`.
- **`zip(a, b)` silently truncating**: if `a` and `b` have different lengths, `zip` stops at the shorter one without raising an error — fine for this exercise's equal-length inputs, but a subtle bug source if reused with mismatched vectors.

## Docs

- [Wikipedia — Cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Mistral embeddings capability guide](https://docs.mistral.ai/capabilities/embeddings/) — mentions cosine similarity as the standard comparison metric for `mistral-embed` vectors
- [Python `math` module docs](https://docs.python.org/3/library/math.html) (`math.sqrt`)
