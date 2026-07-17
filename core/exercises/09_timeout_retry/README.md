# 09 — Timeout and Retry

## Theory

External APIs fail. Networks hiccup, rate limits (`429`) kick in, servers return transient `503`s. A production-grade client **does not give up on the first error** — but it also doesn't retry forever, or retry the wrong things.

### Timeout

The maximum time you'll wait for a response before giving up on that attempt. Without one, a stalled connection can hang your program indefinitely.

- Python `urllib`: pass `timeout=<seconds>` to `urlopen`.
- libcurl: `CURLOPT_TIMEOUT`.

### Retry with backoff

A common, simple strategy:

1. Attempt 1 → fails (`503`).
2. Wait 1 second.
3. Attempt 2 → fails again.
4. Wait 2 seconds.
5. Attempt 3 → succeeds.

**Exponential backoff** (doubling the wait each time) spaces out retries so you don't hammer an already-struggling server.

### What you should *not* retry

- `400 Bad Request` — the payload itself is wrong; retrying sends the same broken request again.
- `401 Unauthorized` — the key is invalid; retrying won't fix authentication.

Only retry **transient** failures: `429`, `500`, `502`, `503`, and network-level timeouts. Blindly retrying everything (including your own bugs) hides real problems.

### Why this matters for LLM pipelines specifically

Rate limiting is routine with cloud LLM providers, especially under load. Retry + backoff isn't an optional nicety here — it's close to mandatory for any pipeline that runs unattended.

---

## Assignment

Implement a function that calls `GET {MISTRAL_API_BASE}/fail_twice` (a mock-only endpoint — see below).

- Maximum **3 attempts**.
- The first 2 attempts return `503`; retry on that status.
- On the 3rd attempt (success), print:

```
RETRY_OK
```

## Files to modify

- `python/main.py` — implement `fetch_with_retry(url, max_attempts=3)`

## Verify

```bash
codam-labs --mock verify 09_timeout_retry
```

`--mock` is not optional here: `/fail_twice` **only exists on the `codam-labs` mock server**. The real Mistral API has no such endpoint — running this exercise live will just 404 forever, which has nothing to do with your retry logic being right or wrong.

## Troubleshooting

- **Running this against the live API** — there is no `/fail_twice` route on `api.mistral.ai`. If you skip `--mock`, every attempt gets a `404`, not a `503`, and your retry-on-503 logic (correctly) won't kick in. This exercise is mock-only by design.
- **Not catching `urllib.error.HTTPError` at all** — an uncaught `HTTPError` on the first `503` crashes the whole script before a second attempt ever happens.
- **Off-by-one attempt counting** — `for attempt in range(max_attempts - 1)` only tries twice total, which means you never reach the 3rd (successful) call. Loop over the full `range(max_attempts)`.
- **Retrying non-transient errors too** — a bare `except Exception: continue` will happily retry a `401` or a malformed-URL `400` forever, masking bugs instead of recovering from real transient failures. Check the status code (`exc.code == 503`) before deciding to retry.
- **Missing a timeout on the request itself** — even with retry logic, a hung connection with no `timeout=` set can block indefinitely on a single attempt, never even reaching your retry loop's next iteration. Set `timeout=10` (or similar) on every `urlopen` call.

## Docs & further reading

- [Google SRE Book — Addressing Cascading Failures (retry & backoff)](https://sre.google/sre-book/addressing-cascading-failures/)
- [Python docs — `urllib.error`](https://docs.python.org/3/library/urllib.error.html)
- [AWS Architecture Blog — Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
