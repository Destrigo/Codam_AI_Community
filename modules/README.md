# Stand-alone modules

Complete `core/` first, then pick any module independently.

| Module | Exercises | Topic |
|--------|-----------|-------|
| `prompt_engineering` | 6 | Prompts, few-shot, CoT, roles |
| `structured_output` | 5 | JSON parsing, validation, retry |
| `embeddings` | 5 | Vectors, similarity, retrieval |
| `rag` | 7 | Chunking, index, RAG pipeline |
| `tools` | 6 | Function calling, tool execution |
| `agents` | 6 | Agent loops, planning, HITL |
| `local_llm` | 4 | Local/offline inference |
| `production` | 6 | Cache, guardrails, testing |
| `advanced_patterns` | 5 | Map-reduce, routing, eval |

```bash
codamlings list --module rag
codamlings verify all --module prompt_engineering
codamlings watch --module agents
```

**Total: 10 core + 50 module = 60 exercises**
