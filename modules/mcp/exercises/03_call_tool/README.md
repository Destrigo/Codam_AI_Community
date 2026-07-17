# MCP Call Tool

## Theory
Invoke a tool with POST {CODAM_LABS_MCP_BASE}/call and JSON body {name, arguments}.

Use env CODAM_LABS_MCP_BASE (set by --mock). Do not hardcode the mock host/port.

## Assignment
Call tool search with {query: "docs"}. Print response containing MCP_CALL_OK.

## Verify
`ash
codam-labs --mock verify mcp/03_call_tool
`
