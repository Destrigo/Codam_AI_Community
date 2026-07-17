# 03 — HTTP POST

## Theory

**POST** sends data *to* the server — it's the method every LLM API uses to deliver your prompt and get a completion back. GET asks "give me X"; POST says "here's a payload, do something with it and tell me what happened."

### GET vs POST

| GET | POST |
|-----|------|
| Reads resources | Sends / creates data |
| Parameters live in the URL | Body carries the payload |
| Idempotent (safe to repeat) | May have side effects |

### `Content-Type` matters

When you send JSON, the `Content-Type: application/json` header tells the server how to interpret the body. Skip it and some servers will treat your bytes as plain text or form data instead of JSON — the request might "succeed" but be parsed wrong.

### The echo endpoint

You POST JSON to an **echo** service that hands your own body back to you. No auth, no model, no cost — it exists purely to verify that your POST mechanics are correct before exercise `04` adds a real LLM on the other end.

**URL (read this carefully):**

```python
url = os.environ.get("CODAM_LABS_ECHO_URL", "https://httpbin.org/post")
```

`--mock` sets `CODAM_LABS_ECHO_URL` for you, pointing at a local echo server. **Prefer `--mock` for this exercise** — the public `httpbin.org` is frequently rate-limited or returns `503`, which is an infrastructure problem, not a bug in your code.

### Two different fields, don't mix them up

The echo response wraps your body in two ways:

```json
{
  "json": {"name": "codam"},
  "data": "{\"name\": \"codam\"}"
}
```

- `response["json"]` is your body **already parsed** into a dict — this is what you want.
- `response["data"]` is the **raw string** you sent — parsing this again means a second, unnecessary `json.loads()` and is easy to get wrong.

Use `response["json"]["name"]` and print `ECHO_OK:codam`.

### Where this connects to the LLM exercises

Every call to `/v1/chat/completions` from exercise `04` onward is a POST with a JSON body:

```json
{
  "model": "mistral-small-latest",
  "messages": [{"role": "user", "content": "hello"}]
}
```

Same `Request(url, data=body, method="POST")` + `Content-Type` header pattern you build here.

---

## Assignment

POST this JSON body to the echo URL above:

```json
{"name": "codam"}
```

with header `Content-Type: application/json`. From the response, extract `json.name` and print:

```
ECHO_OK:codam
```

## Files to modify

- `python/main.py` — use `urllib.request` (stdlib)
- `cpp/main.cpp` — use libcurl + nlohmann/json

## Verify

```bash
codam-labs --mock verify 03_http_post
```

If you insist on live `httpbin.org` and hit `503` or an HTML error page, that confirms the exercise's whole point — switch back to `--mock`.

## Troubleshooting

- **Reading `data["data"]` instead of `data["json"]`** — the `data` field is a raw string; you'd need a second `json.loads()` and it's fragile. Always go through `data["json"]["name"]`.
- **`503 Service Unavailable` / HTML instead of JSON** — you're hitting the live `httpbin.org` fallback and it's rate-limiting or down. This is expected sometimes; rerun with `--mock`.
- **Missing `Content-Type` header** — some servers silently misinterpret the body without it. Always call `request.add_header("Content-Type", "application/json")` before opening the request.
- **`TypeError: POST data should be bytes`** — `urllib.request.Request` wants `bytes` for `data`, not a `str` or `dict`. Encode with `json.dumps(payload).encode("utf-8")`.
- **Printing the whole `json` dict** — `print(f"ECHO_OK:{data['json']}")` prints `ECHO_OK:{'name': 'codam'}`, not `ECHO_OK:codam`. Extract the `name` field specifically: `data["json"]["name"]`.

## Docs & further reading

- [MDN — HTTP request methods: POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST)
- [httpbin.org](https://httpbin.org/) — the live echo service used as a fallback here
- [MDN — Content-Type header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type)
