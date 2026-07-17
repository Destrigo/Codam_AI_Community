# MCP Client Session

## Theory
Sessions start with POST {CODAM_LABS_MCP_BASE}/initialize returning protocol version + session id.

Use env CODAM_LABS_MCP_BASE (set by --mock).

## Assignment
Initialize session. Print SESSION_OK: + session id from response.

## Verify
`ash
codam-labs --mock verify mcp/05_client_session
`
