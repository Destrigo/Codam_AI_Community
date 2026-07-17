# MCP — Model Context Protocol

[MCP](https://modelcontextprotocol.io/) standardizes how an LLM application talks to external
tools and data: a client asks a server "what can you do?", then calls a tool or reads a
resource by URI. This module builds that mental model one HTTP call at a time — the mock
server in `--mock` mode speaks a **simplified, HTTP/JSON shim** over the same ideas (manifest,
`tools/list`, `tools/call`, resources, session init), not the real stdio/JSON-RPC transport
used by the official [`mcp` Python SDK](https://modelcontextprotocol.io/docs/concepts/architecture).
That's intentional: get the concepts right here before adding the SDK's transport plumbing.

| # | Exercise | Topic |
|---|----------|-------|
| 01 | tool_manifest | Static JSON manifest (no network) |
| 02 | list_tools | Discover tools — `GET /tools` |
| 03 | call_tool | Invoke a tool — `POST /call` |
| 04 | resource_read | Read a resource URI — `GET /resources/{id}` |
| 05 | client_session | Initialize a session — `POST /initialize` |
| 06 | bridge_llm | Let an LLM decide which MCP tool to use |

## How the exercises connect

01 has no server at all — it's a warm-up on the *shape* of a manifest. 02–05 all talk to the
**same** mock MCP server, at four different endpoints, so once you get the env-var + JSON
pattern working in 02, 03–05 are mostly "same recipe, new path." 06 is the payoff: it swaps
the MCP mock for the Mistral mock and asks the model to react to an MCP-flavored prompt —
this is the "LLM picks a tool" pattern real agents use, minus the actual tool execution.

## Setup

Exercises 02–05 need a running mock (or, for advanced students, a real MCP-compatible HTTP
service) reachable through **`CODAM_LABS_MCP_BASE`**:

```python
base = os.environ.get("CODAM_LABS_MCP_BASE", "http://127.0.0.1:8765/mcp").rstrip("/")
```

`--mock` starts a throwaway HTTP server on an OS-assigned port and injects
`CODAM_LABS_MCP_BASE` for you — **the port is different every run.** The literal fallback
`127.0.0.1:8765` above only exists so the script doesn't crash if you forget `--mock`; never
hardcode that host:port as the thing you actually call.

```bash
codam-labs --mock --module mcp verify all
# single exercise:
codam-labs --mock verify mcp/03_call_tool
```

06 additionally needs `MISTRAL_API_KEY` in the repo-root `.env` (or run it with `--mock` too,
which fakes the Mistral endpoint instead of calling the real API).

## Troubleshooting

- **`ConnectionRefusedError` / `[Errno 111]`** — you ran `codam-labs verify ...` without
  `--mock` and there's no MCP server on the fallback `127.0.0.1:8765`. Add `--mock`, or point
  `CODAM_LABS_MCP_BASE` at a real MCP-style endpoint you control.
- **Works once, then fails on the next run** — you cached the port from a previous `--mock`
  run (e.g. exported `CODAM_LABS_MCP_BASE` in your shell profile). Each `--mock` invocation
  spins up a *new* server on a *new* port; always read the env var fresh, never persist it.
- **`KeyError: 'tools'` / `'result'` / `'content'` / `'session_id'`** — you're reading the
  wrong field for that endpoint. Each of 02–05 has its own response shape (`tools`, `result`,
  `content`, `session_id` respectively) — check that exercise's README, they are not
  interchangeable.
- **06 prints `MOCK_RESPONSE:...` instead of `MCP_BRIDGE_OK`** — the mock only recognizes the
  literal phrase `mcp bridge` in the user message; rewording the prompt breaks the match.
- **`401`/`403` on 06 in live mode** — `MISTRAL_API_KEY` missing or invalid; unset it and use
  `--mock` while iterating, then switch to live once the logic works.

Prerequisites: `core/`, `modules/tools`
