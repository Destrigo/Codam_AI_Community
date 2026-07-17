# 03 — HTTP POST

## Theory

**POST** sends data to the server — it is the method used by LLM APIs to send prompts and receive responses.

### GET vs POST

| GET | POST |
|-----|------|
| Reads resources | Creates / sends data |
| Parameters in URL | Body in the request |
| Idempotent | May have side effects |

### Content-Type

When you send JSON, the `Content-Type: application/json` header tells the server how to interpret the body.

### Echo endpoint

You POST JSON to an **echo** service that returns your body back. Useful for verifying the POST without authentication.

**URL (important):**

```text
os.environ["CODAM_LABS_ECHO_URL"]   # set automatically when you use --mock
# fallback if unset: https://httpbin.org/post
```

Prefer **`--mock`** for this exercise. Public `httpbin.org` is often rate-limited or returns **503**; that is an infrastructure issue, not your code.

The response contains a `json` field with the body you sent (not the string field `data`):

```json
{
  "json": {"name": "codam"},
  "data": "{\"name\": \"codam\"}"
}
```

Use `response["json"]["name"]` → print `ECHO_OK:codam`.  
Do **not** parse `data` (that is a raw string and leads to awkward double-`json.loads`).

### Connection to AI

Every call to `/v1/chat/completions` is a POST with a JSON body:

```json
{
  "model": "mistral-small-latest",
  "messages": [{"role": "user", "content": "hello"}]
}
```

---

## Assignment

Send a POST request to the echo URL above with JSON body:

```json
{"name": "codam"}
```

Header: `Content-Type: application/json`

Print: `ECHO_OK:codam` (extract `json.name` from the response).

## Verify

```bash
codam-labs --mock verify 03_http_post
```

If you insist on live `httpbin.org` and get `503` / HTML errors, switch back to `--mock`.
