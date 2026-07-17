# Hint — 03_http_post

**Use the env URL** (mock-friendly):

```python
url = os.environ.get("CODAM_LABS_ECHO_URL", "https://httpbin.org/post")
```

**Python**
1. `json.dumps({"name": "codam"}).encode()` for the body
2. `urllib.request.Request(url, data=body, method="POST")`
3. `request.add_header("Content-Type", "application/json")`
4. In the response: `data["json"]["name"]` — **not** `data["data"]`
5. Print `ECHO_OK:{name}`

**C++**
1. Read `CODAM_LABS_ECHO_URL` (fallback `https://httpbin.org/post`)
2. `curl` / httplib POST with `Content-Type: application/json`
3. Parse and read `["json"]["name"]`

**Debugging**
- `503` / HTML from httpbin → run with `--mock` (local echo). Your logic can still be correct.
- Double `json.loads` usually means you read the `data` string field instead of `json`.
