# MCP Call Tool

## Theory

Once a client knows a tool exists (exercise 02), it invokes it with `tools/call`
([Understanding MCP servers → Tools](https://modelcontextprotocol.io/docs/learn/server-concepts)).
The mock represents that as `POST {CODAM_LABS_MCP_BASE}/call` with a JSON body of
`{"name": ..., "arguments": {...}}`, returning `{"result": ...}`.

Use `CODAM_LABS_MCP_BASE` from the environment (set by `--mock`) — don't hardcode the mock
host/port, it changes every run.

## Assignment

Call the `search` tool with `{"query": "docs"}` as arguments. Print the response's `result`
field — it will contain `MCP_CALL_OK`.

```python
body = json.dumps({"name": "search", "arguments": {"query": "docs"}}).encode()
```

## Verify

```bash
codam-labs --mock verify mcp/03_call_tool
```

Expected: output containing `MCP_CALL_OK`

## Troubleshooting

- **`405 Method Not Allowed` / server ignores the body** — this endpoint only accepts `POST`.
  A `GET` with query params (the pattern from 02) will not reach the handler that returns
  `result`.
- **`urllib.error.HTTPError: 400`** — you sent a raw string instead of a JSON-encoded body,
  or forgot the `Content-Type: application/json` header. `urllib.request.Request(..., data=body,
  method="POST")` needs the header added explicitly via `req.add_header(...)`.
- **`KeyError: 'result'`** — the call response wraps its payload under `result`, a different
  key than `tools` (02) or `content` (04). Don't reuse the parsing line from a sibling
  exercise without checking the key name.
- **The mock doesn't validate your `name`/`arguments`** — unlike a real MCP server, this mock
  always returns `MCP_CALL_OK:search` for any `/call` request. That's fine for passing
  verification, but don't take it as proof your payload shape is correct for a live server —
  double-check against the spec, not just against green output here.
