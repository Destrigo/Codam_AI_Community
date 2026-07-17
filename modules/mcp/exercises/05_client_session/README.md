# MCP Client Session

## Theory

MCP is a **stateful** protocol — before calling tools or reading resources for real, a
client and server negotiate a session and protocol version during initialization
([Architecture overview → Lifecycle management](https://modelcontextprotocol.io/docs/learn/architecture)).
The mock simplifies that handshake to `POST {CODAM_LABS_MCP_BASE}/initialize`, returning a
`session_id` and `protocol` version.

Use `CODAM_LABS_MCP_BASE` from the environment (set by `--mock`).

## Assignment

`POST` an empty JSON object `{}` to `/initialize`. Print `SESSION_OK:` followed by the
`session_id` from the response.

```python
req = urllib.request.Request(f"{base}/initialize", data=b"{}", method="POST")
```

## Verify

```bash
codam-labs --mock verify mcp/05_client_session
```

Expected: `SESSION_OK:mock-session-1`

## Troubleshooting

- **`400 Bad Request`** — the body must be *valid JSON*, even if empty — send `b"{}"`, not
  `b""`. An empty byte string fails `json.loads` server-side.
- **`KeyError: 'session_id'`** — this response also carries a `protocol` field (e.g.
  `"2024-11-05"`); don't confuse the two. You want `session_id`, not `protocol`.
- **Session id looks different each run in mock mode** — it shouldn't: the mock always
  returns the fixed string `mock-session-1` so tests are deterministic. If you see something
  else, you're likely hitting a stale server from a previous `--mock` run on a cached port —
  re-run the full `codam-labs --mock verify ...` command rather than reusing an old env var.
- **Real MCP servers won't accept this shape** — a live client also sends
  `protocolVersion`, `capabilities`, and `clientInfo` in the initialize request per the spec.
  This exercise's empty `{}` body is a simplification for the mock only.
