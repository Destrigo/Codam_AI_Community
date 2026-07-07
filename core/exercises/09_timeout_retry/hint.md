# Hint — 09_timeout_retry

1. URL: `{MISTRAL_API_BASE}/fail_twice` — not `/chat/completions`
2. Loop `for attempt in range(3)`
3. On `urllib.error.HTTPError` with code 503, continue the loop
4. On 200, print `RETRY_OK` and exit
5. Optional: `time.sleep(2 ** attempt)` between attempts
