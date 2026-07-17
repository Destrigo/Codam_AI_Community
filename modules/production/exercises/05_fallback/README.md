# Fallback Model

## Theory
Even a well-retried call (see `01_rate_limit`) eventually gives up. The next layer of resilience
is a **fallback**: if the primary model/provider is unavailable, switch to a secondary one rather
than failing the whole request. This is the same "circuit breaker" idea used for any external
dependency, applied to model providers.

**Worked example — a document-summarization service:**

| Step | Model | Result |
|------|-------|--------|
| 1 | `mistral-large-latest` (primary) | times out / 500s |
| 2 | `mistral-small-latest` (fallback) | succeeds, slightly lower quality answer |

The key production discipline is **visibility**: silently falling back and returning a normal
`200` hides degraded quality from monitoring. A real system logs/metrics-tags every fallback use
so someone notices if the primary is down for hours, not months.

## Assignment
Simulate a failed primary and a successful fallback. Print `FALLBACK_OK`.

## Files
- `python/main.py` — stub with a `primary` boolean flag standing in for "did the primary succeed?".
- `hint.md` — `try primary except use fallback`.
- `solution/python/main.py` — reference: branches on the `primary` flag.

## Verify
```bash
codam-labs --mock verify production/05_fallback
```
Expected stdout: `FALLBACK_OK`.

## Troubleshooting
- **Wrong branch printed** — `FALLBACK_OK` should print when the primary *failed* (`primary =
  False` in the stub), not when it succeeded; double-check your condition isn't inverted.
- **No fallback attempted** — a `try/except` that re-raises immediately never reaches the fallback
  branch; the fallback call belongs inside the `except`, not after an unconditional `raise`.
- **Catching too broadly** — swallowing every exception (including bugs in your own code) around
  the primary call can mask real errors as "primary is down." Catch the specific
  network/API exceptions you expect.
- **No fallback logging** — in a real service, always log which model actually served the
  response so on-call engineers can tell primary outages from expected traffic.

## Docs
- [Martin Fowler: CircuitBreaker pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Mistral: available models](https://docs.mistral.ai/getting-started/models/) — for picking a realistic primary/fallback pair.
- [Python `try`/`except`/`else` docs](https://docs.python.org/3/tutorial/errors.html)
