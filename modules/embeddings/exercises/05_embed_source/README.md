# Embedding Source (Mock vs API)

## Theory

The same `/embeddings` request shape (model name + `input` text, POST, JSON body) works whether you're pointed at Mistral's hosted API, a local mock server for testing, or a self-hosted embedding server — because `MISTRAL_API_BASE` is just a configurable host, not a hardcoded endpoint. This exercise is about writing code that's aware of *which* backend it's actually talking to, using the `CODAM_LABS_MOCK` environment variable as the signal, without changing the request logic itself.

```python
resp = call_embeddings_endpoint(base=MISTRAL_API_BASE, input="test")
source = "mock" if os.environ.get("CODAM_LABS_MOCK") else "api"
print(f"EMBED_SOURCE:{source}")
```

This mirrors a real-world concern: your embedding pipeline shouldn't need a different code path for "testing against a mock" versus "calling the real API" — only the environment configuration (`MISTRAL_API_BASE`, and here `CODAM_LABS_MOCK`) should change. Notice this exercise deliberately does **not** send an `Authorization` header — unlike `01_generate_embedding`, it works whether or not `MISTRAL_API_KEY` is set, since the mock server doesn't check it and it's harmless to omit against most local test servers.

## Assignment

Call the `/embeddings` endpoint (any input is fine, e.g. `"test"`), then:

- Check whether `CODAM_LABS_MOCK` is set in the environment.
- Print `EMBED_SOURCE:mock` if it is set, or `EMBED_SOURCE:api` if it isn't.

Expected stdout (with `CODAM_LABS_MOCK=1`, as set by the grader's mock mode):

```text
EMBED_SOURCE:mock
```

## Files to modify

- `python/main.py` — make the POST request to `/embeddings`, then branch on `os.environ.get("CODAM_LABS_MOCK")` to decide what to print.
- `cpp/main.cpp` — make the equivalent request and check the `CODAM_LABS_MOCK` environment variable (e.g. via `std::getenv`).

## Verify

```bash
codam-labs --mock verify embeddings/05_embed_source
```

The `--mock` flag is what sets `CODAM_LABS_MOCK` in the subprocess environment — running without it (a real `codam-labs verify`, no `--mock`) would legitimately hit the live Mistral API and should print `EMBED_SOURCE:api` instead.

## Troubleshooting

- **Checking the wrong environment variable**: this exercise keys off `CODAM_LABS_MOCK`, not `MISTRAL_API_BASE` or `MISTRAL_API_KEY` — those affect *where* the request goes, but the mock/api label is decided by `CODAM_LABS_MOCK` specifically.
- **Truthiness of environment variables**: `os.environ.get("CODAM_LABS_MOCK")` returns a *string* (like `"1"`) or `None` — never `True`/`False` directly. `if os.environ.get("CODAM_LABS_MOCK"):` works because any non-empty string is truthy, but don't compare it to the Python boolean `True` (`== True` will always be `False`).
- **Skipping the actual request**: even though the branch logic doesn't depend on the response body, the exercise still expects you to make the `/embeddings` call — don't shortcut straight to the print statement without hitting the endpoint.
- **Hardcoding `"mock"`**: printing `EMBED_SOURCE:mock` unconditionally passes the mock-mode check but is wrong — running the same code in live mode (no `--mock`) should correctly report `api`, which only happens if you actually read the environment variable.

## Docs

- [Mistral API reference — Embeddings](https://docs.mistral.ai/api/#tag/embeddings)
- [Python `os.environ` docs](https://docs.python.org/3/library/os.html#os.environ)
- [Twelve-Factor App — Config](https://12factor.net/config) — the general principle of driving environment-specific behavior from env vars, not code branches
