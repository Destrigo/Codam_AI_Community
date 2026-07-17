# Response Caching

## Theory
LLM calls cost money and take hundreds of milliseconds to seconds. If two users (or the same user
twice) ask the *exact* same question, calling the model twice is pure waste.

**Worked example — an FAQ widget:**

| Call | Prompt | Cache state | Cost |
|------|--------|-------------|------|
| 1 | `"What are your business hours?"` | miss → store | 1 API call |
| 2 | `"What are your business hours?"` | **hit** → return stored | 0 API calls |
| 3 | `"What is your return policy?"`    | miss → store (different key!) | 1 API call |

A cache key should normally include everything that affects the output — not just the prompt text,
but `model`, `temperature`, and any system prompt. This exercise simplifies to prompt-only keying
so you can focus on the hit/miss mechanics.

## Assignment
Call the same prompt twice through a `dict`-backed cache:
- 1st call → miss, store result.
- 2nd call (identical prompt) → hit, **no new API/model call**.
- Print `CACHE_HIT`.

## Files
- `python/main.py` — stub with the cache dict and `get()` already wired; fill in the final print.
- `hint.md` — `dict cache keyed by prompt`.
- `solution/python/main.py` — reference implementation.

## Verify
```bash
codam-labs --mock verify production/02_cache
```
Expected stdout: `CACHE_HIT`.

## Troubleshooting
- **Cache never hits** — you're probably creating a new dict per call instead of a module/session-
  level one; the cache must persist across the two lookups.
- **"Hit" but wrong content** — double-check your key includes enough context; keying only on the
  first N characters of a prompt will collide two different questions into one cached answer.
- **Cache grows unbounded** — fine for this toy exercise, but in production add a max size or TTL
  (see `functools.lru_cache(maxsize=...)` or a Redis key with `EX`) so memory doesn't leak.
- **Stale answers after a prompt-template change** — if you change the *system* prompt but keep
  caching by user-prompt only, you'll silently serve answers generated under the old template.

## Docs
- [Python `functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache) — the stdlib version of what you're building by hand here.
- [Redis `EX`/`TTL` docs](https://redis.io/docs/latest/commands/expire/) — how real systems expire cache entries.
- [Mistral pricing](https://mistral.ai/products/la-plateforme#pricing) — why caching matters at scale (cost per token).
