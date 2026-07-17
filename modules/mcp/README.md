# MCP — Model Context Protocol

Expose and consume tools/resources via MCP-style HTTP (mock server in verify).

| # | Exercise | Topic |
|---|----------|-------|
| 01 | tool_manifest | JSON manifest |
| 02 | list_tools | Discover tools |
| 03 | call_tool | Invoke tool |
| 04 | resource_read | Read resource URI |
| 05 | client_session | Initialize session |
| 06 | bridge_llm | LLM + MCP bridge |

## Important

Exercises 02–05 talk to **`CODAM_LABS_MCP_BASE`** (set by `--mock`). Do not hardcode `127.0.0.1:8765` — the mock port is dynamic.

```bash
codam-labs --mock --module mcp verify all
```

Prerequisites: `core/`, `modules/tools`
