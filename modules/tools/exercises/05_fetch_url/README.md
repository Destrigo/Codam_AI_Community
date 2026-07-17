# Fetch URL Tool

## Theory

Some information simply isn't in the model's training data or the conversation so
far — today's weather, a live stock price, or (in this exercise) a to-do item from an
external API. A **fetch tool** gives the model a way to reach outside itself: your code
makes the actual HTTP request, and the result gets fed back as tool output. This
exercise strips away the LLM entirely and focuses on the fetch mechanics: reading the
target URL from an environment variable (so tests can point it at a mock server) rather
than hardcoding it.

## Assignment

`GET` the URL in `CODAM_LABS_TODO_URL` — falling back to
`https://jsonplaceholder.typicode.com/todos/1` if that variable isn't set — and print
the todo item's `title` field.

```python
url = os.environ.get(
    "CODAM_LABS_TODO_URL",
    "https://jsonplaceholder.typicode.com/todos/1",
)
```

**Expected output:**

```
FETCH_OK:delectus aut autem
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify tools/05_fetch_url
```

`--mock` starts a local HTTP server and points `CODAM_LABS_TODO_URL` at it, so this
works with **no internet access and no API key**. Prefer `--mock` in class; the
live/no-mock path falls back to the real `jsonplaceholder.typicode.com` and needs
outbound internet:

```bash
codam-labs verify tools/05_fetch_url
```

## Troubleshooting

- **Hardcoded the jsonplaceholder URL directly?** It'll work when you have internet,
  but breaks the point of `--mock` (offline/CI verification) and will fail entirely
  behind a firewall that blocks `jsonplaceholder.typicode.com`. Always read
  `CODAM_LABS_TODO_URL` first and fall back only when it's unset.
- **`URLError` / connection refused under `--mock`?** The mock server binds to a
  *dynamic* port each run — never hardcode `127.0.0.1:<port>`; always read the env var,
  since the port changes between runs.
- **Got a title but it's not `"delectus aut autem"`?** That's the exact title of
  `todos/1` on jsonplaceholder, which the mock also returns for consistency — if you're
  fetching a different todo id, or reading a different field (`completed`, `userId`),
  the string won't match.
- **Corporate proxy blocking the live fallback?** This is the textbook case for this
  exercise's mock — if `--mock` passes but the live command times out, it's a network
  restriction on your side, not a code bug.

## Further reading

- [JSONPlaceholder — free fake REST API for testing](https://jsonplaceholder.typicode.com/)
- [Python docs — `urllib.request` for HTTP GET](https://docs.python.org/3/library/urllib.request.html)
