# MCP List Tools

## Theory
Clients discover tools via HTTP GET {CODAM_LABS_MCP_BASE}/tools.

CODAM_LABS_MCP_BASE is set automatically by --mock. Do **not** hardcode 127.0.0.1:8765 — the mock port is dynamic.

## Assignment
Call the MCP tools endpoint. Print TOOLS_OK: + number of tools.

## Verify
`ash
codam-labs --mock verify mcp/02_list_tools
`
