# Retry on Invalid JSON

## Theory

LLMs occasionally produce malformed JSON — a trailing comma, an unescaped quote, truncated output because it hit a token limit mid-object. Rather than failing the whole pipeline on the first bad parse, a common and effective pattern is: **try, catch the parse failure, retry the call** (optionally with a corrective follow-up message like *"That wasn't valid JSON, please resend as JSON only"*), up to a small retry cap.

```python
for attempt in range(3):
    response = call_model(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        prompt = f"{prompt}\nYour last reply was not valid JSON. Try again."
continue_or_raise()
```

This exercise focuses on the *calling* half of that pattern — sending a request and getting a response back — which you'd then wrap in the retry-on-failure loop shown above. Capping retries (e.g. at 3) matters: without a limit, a persistently broken prompt or a model that's fundamentally unable to satisfy your schema will retry forever, burning API calls and latency.

## Assignment

Call the chat completions endpoint with the message `retry invalid json`.

- Print the raw response returned by the mock/API.

Expected stdout (mock mode) contains:

```text
RETRY_JSON_OK
```

## Files to modify

- `python/main.py` — send the request with content `"retry invalid json"` and print the response.
- `cpp/main.cpp` — build the equivalent HTTP POST and print the response body/content.

## Verify

```bash
codam-labs --mock verify structured_output/03_retry_invalid
```

## Troubleshooting

- **Implementing an actual retry loop when the mock doesn't need one**: for *this specific exercise*, the mock endpoint returns `RETRY_JSON_OK` on the first call as long as the message content matches — you don't need real retry-loop logic to pass the check, though building one is good practice and won't break anything.
- **Wrong message content**: the payload's `content` field must be exactly `retry invalid json` (lowercase) — the mock server matches on this string to decide what to respond with.
- **Not printing anything**: same failure mode as other exercises in this module — fetching the response but forgetting `print()` produces empty stdout and a failed check.
- **Confusing this with `02_validate_schema`**: this exercise is about the network round-trip and message content, not about validating fields on a local dict — don't copy that exercise's assertion logic in here.

## Docs

- [Mistral API — Chat Completions](https://docs.mistral.ai/api/#tag/chat)
- [Mistral JSON mode guide](https://docs.mistral.ai/capabilities/structured-output/json_mode/) — reduces (but doesn't eliminate) the need for retries
- [Python `json.JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError) — the exception you'd catch in a real retry loop
