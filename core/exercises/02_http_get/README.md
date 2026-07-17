# 02 — HTTP GET and JSON

## Theory

Modern APIs — including every LLM API you'll use in this course — talk over **HTTP** and exchange **JSON**. This exercise is the smallest possible version of that pattern, with no auth and no LLM in the way, so you can focus purely on the request/response mechanics.

### HTTP GET

- The method for **reading** a resource without changing anything on the server (idempotent).
- The response carries a **status code**: `200` OK, `404` not found, `500` server error, and so on.
- The response **body** holds the actual data — here, a JSON document.

### JSON, quickly

JavaScript Object Notation — plain text, key-value pairs, nestable:

```json
{"id": 1, "title": "delectus aut autem", "completed": false}
```

Python's `json.loads()` turns that text into a `dict`; `data["title"]` gets you the value.

### The flow you'll repeat all course long

1. Build the URL (from an env var, with a fallback).
2. Send the GET request.
3. Check that it succeeded.
4. Parse the response body as JSON.
5. Pull out the one field you actually need.

### Where the URL comes from

```python
url = os.environ.get(
    "CODAM_LABS_TODO_URL",
    "https://jsonplaceholder.typicode.com/todos/1",
)
```

`--mock` sets `CODAM_LABS_TODO_URL` to point at a local server on `127.0.0.1` that returns the exact same JSON shape as the real [JSONPlaceholder](https://jsonplaceholder.typicode.com/) todo — so your code doesn't need to know or care whether it's talking to the internet or to `codam-labs`'s built-in mock.

### Why this comes before the LLM exercises

Exercise `04` calls `POST /v1/chat/completions` — same request → JSON response → extract-a-field shape, just with a POST body and an `Authorization` header on top. Get comfortable with GET first.

---

## Assignment

Send a GET request to the todo URL above and print the todo's `title` field, and nothing else — one line, no quotes, no surrounding text.

Expected output:

```
delectus aut autem
```

## Files to modify

- `python/main.py` — use `urllib.request` (stdlib, no extra dependency)
- `cpp/main.cpp` — use libcurl + nlohmann/json

## Verify

```bash
codam-labs --mock verify 02_http_get
```

Prefer `--mock` here: it's instant and works with no internet. If you want to hit the real API instead:

```bash
codam-labs verify 02_http_get
```

## Troubleshooting

- **Hangs or times out on a school/office network** — some networks block `jsonplaceholder.typicode.com`. Switch to `--mock`; the assignment output is identical either way.
- **`KeyError: 'title'`** — you're indexing the wrong shape. The todo object has `userId`, `id`, `title`, `completed` — no nesting, so `data["title"]` is correct as-is.
- **Output has extra text around the title** — verify does a substring check on stdout, but any stray `print()` calls (debug prints, `print(data)` left in by accident) will pollute the output and can break the exact match downstream exercises rely on. Print only the title.
- **`TypeError: the JSON object must be str, bytes or bytearray, not ...`** — `response.read()` returns `bytes`; decode it (`.decode("utf-8")`) before `json.loads`, or pass the bytes straight to `json.loads` (both work in Python 3.6+, but be consistent with the rest of the course's style).
- **Confusing GET params with a body** — GET requests carry data in the URL/query string, not in a JSON body. There's nothing to send here besides the URL itself.

## Docs & further reading

- [MDN — HTTP request methods: GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET)
- [Python docs — `urllib.request`](https://docs.python.org/3/library/urllib.request.html)
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) (the live fallback API used by this exercise)
