# MCP Read Resource

## Theory

Tools *do* things; resources are the read-only counterpart — passive context like files,
policies, or schemas, fetched by URI via `resources/read`
([Understanding MCP servers → Resources](https://modelcontextprotocol.io/docs/learn/server-concepts)).
The mock exposes that as `GET {CODAM_LABS_MCP_BASE}/resources/{id}`, returning
`{"content": ...}`.

Use `CODAM_LABS_MCP_BASE` from the environment (set by `--mock`).

## Assignment

Read the resource with id `policy`. Print the response's `content` field — the line will
contain `RESOURCE_OK`.

## Verify

```bash
codam-labs --mock verify mcp/04_resource_read
```

Expected: output containing `RESOURCE_OK`

## Troubleshooting

- **`KeyError: 'content'`** — this endpoint's payload key is `content`, distinct from
  `tools` (02) and `result` (03). Each MCP-mock endpoint in this module has its own response
  shape — re-check the key rather than copying a previous exercise's parsing line.
- **404 on a different resource id** — the mock matches any path containing
  `/resources/`, so `policy`, `foo`, or any other id all return the same generic
  `RESOURCE_OK: policy v1` string in mock mode. A real MCP server would 404 on an unknown
  URI — don't assume the mock's leniency reflects production behavior.
- **Forgot this is `GET`, not `POST`** — unlike 03's tool call, reading a resource has no
  body; sending one with `POST` will hit the wrong route or a `404`.
- **Printing the whole JSON instead of `content`** — the expected output is the *string*
  `data["content"]`, not the raw `data` dict — printing the dict will still technically
  contain the substring `RESOURCE_OK` but makes the output harder to read and diverges from
  what the assignment asks for.
