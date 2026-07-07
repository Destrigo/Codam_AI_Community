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

### httpbin.org/post

A test service that **echoes** the request it receives. Useful for verifying your POST is correct without authentication.

The response contains a `json` field with the body you sent.

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

Send a POST request to `https://httpbin.org/post` with JSON body:

```json
{"name": "codam"}
```

Header: `Content-Type: application/json`

Print: `ECHO_OK:codam` (extract `json.name` from the response).

## Verify

```bash
codamlings verify 03_http_post
```
