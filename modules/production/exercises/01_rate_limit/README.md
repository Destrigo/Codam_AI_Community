# Rate Limiting & Retry

## Theory
LLM APIs throttle you under load and occasionally hiccup with transient `503`s. A production
client treats these as *expected* events, not crashes.

**Worked example — a support-bot at 9am Monday:**

| Attempt | Result | Wait before next try |
|---------|--------|----------------------|
| 1       | `503 Service Unavailable` | 1s |
| 2       | `503 Service Unavailable` | 2s (exponential) |
| 3       | `200 OK`                  | — |

If attempt 3 also failed, a well-behaved client gives up and surfaces the error — it does **not**
retry forever and does **not** retry `4xx` client errors (those mean *your request* is wrong, and
retrying a bad request just repeats the mistake).

This exercise mirrors `core/09_timeout_retry`, but against a dedicated endpoint that exists only
in the lab's mock server.

## Assignment
Call `GET {MISTRAL_API_BASE}/fail_twice`:
- Up to **3 attempts total**.
- Retry only on `503`, sleeping between attempts.
- On success, print `RATE_OK`.

> **Mock-only endpoint — read this before you go looking for it on Mistral's docs.**
> `/fail_twice` is served by `codam_ai_labs/mock_server.py`. It fails with `503` for the first
> two calls it receives (per process), then returns `200`. It does **not** exist on
> `https://api.mistral.ai/v1` — running this exercise without `--mock` will 404. This is
> intentional: it lets you practice retry logic offline, deterministically, without burning a
> real rate limit.

## Files
- `python/main.py` — your stub (has a `TODO` where the success print goes).
- `cpp/main.cpp` — C++ track stub, builds via `cpp/CMakeLists.txt`.
- `solution/python/main.py`, `solution/cpp/main.cpp` — reference implementations.
- `hint.md` — points back to `core/09_timeout_retry` if you're stuck on the backoff shape.

## Verify
```bash
codam-labs --mock verify production/01_rate_limit
```
Runs against the in-process mock (`--mock` spins up `mock_server.py` and rewrites
`MISTRAL_API_BASE` for the subprocess). Expected stdout: `RATE_OK`.

## Troubleshooting
- **Connection refused / 404 without `--mock`** — expected. `/fail_twice` only lives on the mock.
- **Only 1 attempt runs** — check your loop bound; you need up to 3 attempts, not 1 retry (2 total).
- **Retrying forever** — cap attempts. An unbounded retry loop against a real outage will hang CI.
- **Swallowing non-503 errors** — if the error is a `403` (bad key) or `400`, re-raise immediately;
  only `503` (and generally `429`) should trigger a retry+sleep.
- **Flaky first run** — the mock's fail counter is per-server-process; running the exercise twice
  in the same `codam-labs` session without restarting the mock can change which attempt succeeds.

## Docs
- [Mistral API errors reference](https://docs.mistral.ai/api/) — status codes you'll actually see live.
- [MDN: HTTP 503 Service Unavailable](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/503)
- [Python `urllib.error.HTTPError`](https://docs.python.org/3/library/urllib.error.html)
- Related: `core/exercises/09_timeout_retry/README.md` for the exponential-backoff derivation.
