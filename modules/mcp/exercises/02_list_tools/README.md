# MCP List Tools

## Theory

Real MCP clients discover tools by calling `tools/list` on the server
([Understanding MCP servers → Tools](https://modelcontextprotocol.io/docs/learn/server-concepts)).
This exercise's mock exposes that same idea over plain HTTP: a `GET` to `{CODAM_LABS_MCP_BASE}/tools`
returns `{"tools": [...]}`.

`CODAM_LABS_MCP_BASE` is set automatically by `--mock` — **the port is different every run.**
Never hardcode `127.0.0.1:8765`; always read the env var.

```python
base = os.environ.get("CODAM_LABS_MCP_BASE", "http://127.0.0.1:8765/mcp").rstrip("/")
```

## Assignment

`GET {base}/tools`. Parse the JSON body and print `TOOLS_OK:` followed by the number of
tools in the `tools` array.

## Verify

```bash
codam-labs --mock verify mcp/02_list_tools
```

Expected: `TOOLS_OK:2`

## Troubleshooting

- **`urllib.error.URLError` / connection refused** — you ran the script directly without
  `--mock`, so `CODAM_LABS_MCP_BASE` isn't set and the fallback URL points at nothing. Run
  through `codam-labs --mock verify mcp/02_list_tools`, or export the var yourself if you're
  testing against a real MCP-style endpoint.
- **`KeyError: 'tools'`** — the mock's `GET /tools` response is `{"tools": [...]}`, not
  `{"result": [...]}` (that shape is used by 03's `POST /call`, not this endpoint).
- **`TOOLS_OK:0` when you expected `2`** — you counted `len(data)` (the whole response dict,
  which has 1 key) instead of `len(data["tools"])` (the array itself).
- **Trailing slash mismatch** — build the URL as `f"{base}/tools"`; if `base` already ends in
  `/`, `.rstrip("/")` on it first avoids an accidental `//tools`.
