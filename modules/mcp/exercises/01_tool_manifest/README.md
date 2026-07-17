# MCP Tool Manifest

## Theory

Before a client can call anything, an MCP server has to say what it offers. Each tool in that
manifest is a small schema: a `name`, a human-readable `description`, and an `inputSchema`
(JSON Schema) describing its arguments — see
[Understanding MCP servers → Tools](https://modelcontextprotocol.io/docs/learn/server-concepts)
for the full shape real servers use. This exercise strips that down to the bare minimum:
just the `name` field, so you can focus on *reading* a manifest before you ever *send* one
over the network. There's no HTTP call here — 02 picks up the networked version.

## Assignment

`MANIFEST` below is a hardcoded dict with a `tools` list. Check whether a tool named
`search` exists in it. If it does, print `MANIFEST_OK:` followed by the number of tools.

```python
MANIFEST = {"tools": [{"name": "search"}, {"name": "calculator"}]}
```

## Verify

```bash
codam-labs --mock verify mcp/01_tool_manifest
```

Expected: `MANIFEST_OK:2`

## Troubleshooting

- **Nothing prints at all** — the starter pattern only prints *inside* the `if "search" in
  names:` branch. If your name check is wrong (typo, wrong key, checking `tool["name"]` vs.
  the whole dict), the script exits silently with no error and no output — that's the bug to
  watch for here, not a crash.
- **`KeyError: 'name'`** — you iterated over `MANIFEST["tools"]` correctly but tried to index
  a tool dict with the wrong key; the field is `name`, not `tool_name` or `id`.
- **Printed count looks wrong** — count `len(tools)` (the whole list), not
  `len(names)` after filtering — you want the manifest size, not how many matched `"search"`.
