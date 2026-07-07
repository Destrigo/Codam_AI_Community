# 09 — Timeout and Retry

## Theory

External APIs fail: unstable network, rate limits (429), temporary errors (503). A production-ready client **does not give up on the first error**.

### Timeout

Wait limit for a response. Without a timeout, the program can hang indefinitely.

- Python `urllib`: `timeout=30` parameter
- libcurl: `CURLOPT_TIMEOUT`

### Retry with backoff

Common strategy:

1. Attempt 1 → fails (503)
2. Wait 1 second
3. Attempt 2 → fails
4. Wait 2 seconds
5. Attempt 3 → success

**Exponential backoff**: double the wait between attempts to avoid hammering the server.

### What NOT to retry

- 400 errors (bad request) — the payload is wrong, retrying will not help
- 401 errors (auth) — invalid key

Only retry **transient** errors: 429, 500, 502, 503, network timeouts.

### In AI

OpenAI rate limits are very common. Retry + backoff is mandatory in any serious pipeline.

---

## Assignment

Implement a function that calls `GET {MISTRAL_API_BASE}/fail_twice` (mock endpoint).

- Maximum **3 attempts**
- If the first attempts fail (503), retry
- On success print: `RETRY_OK`

The mock fails 2 times then responds with 200.

## Verify

```bash
codam-labs verify 09_timeout_retry
```
