# 02 — HTTP GET and JSON

## Theory

Modern APIs — including LLM APIs — communicate over **HTTP** and exchange **JSON** data.

### HTTP GET

- Method for **reading** resources
- The response has a **status code**: `200` OK, `404` not found, `500` server error
- The response body contains the data (often JSON)

### JSON

JavaScript Object Notation — a text-based key-value format:

```json
{"id": 1, "title": "delectus aut autem", "completed": false}
```

### Typical flow

1. Build the URL (from env, see below)
2. Send a GET request
3. Check the status code
4. Parse the JSON
5. Extract the field you need

### URL (important)

```python
url = os.environ.get(
    "CODAM_LABS_TODO_URL",
    "https://jsonplaceholder.typicode.com/todos/1",
)
```

`--mock` sets `CODAM_LABS_TODO_URL` to a local fake todo (no internet). Prefer mock if typicode is slow or blocked.

### Why before the LLM

Before calling an LLM you learn the same pattern: HTTP request → JSON response → extract field. LLM APIs use POST, but parsing the response is identical.

---

## Assignment

Send a GET request to the todo URL above.

Print the todo's `title` field (one line, title text only).

Expected output: `delectus aut autem`

## Files to modify

- `python/main.py` — use `urllib.request` (stdlib)
- `cpp/main.cpp` — use libcurl + nlohmann/json

## Verify

```bash
codam-labs --mock verify 02_http_get
```
