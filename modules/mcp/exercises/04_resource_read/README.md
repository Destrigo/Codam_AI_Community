# MCP Read Resource

## Theory
MCP **resources** are readable URIs. GET {CODAM_LABS_MCP_BASE}/resources/{id}.

Use env CODAM_LABS_MCP_BASE (set by --mock).

## Assignment
Read resource policy. Print line containing RESOURCE_OK.

## Verify
`ash
codam-labs --mock verify mcp/04_resource_read
`
