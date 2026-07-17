# Citations

## Theory

A RAG answer that sounds confident but doesn't say *where it came from* is hard to
trust or debug. Asking the model to **cite chunk ids** alongside its answer (e.g.
`[chunk_1]`) gives users a way to verify claims and gives you a way to catch
hallucinations — if the model cites a chunk id that wasn't actually retrieved, that's a
strong signal something went wrong upstream. This only works if the citation format is
specified explicitly in the prompt; models don't cite sources unless told to and shown
the ids to reference.

## Assignment

Send a prompt instructing the model to **cite `chunk_1`** in its answer, and print the
response.

**Expected output:**

```
CITED:chunk_1
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify rag/06_citations
```

Calls an LLM — use `--mock` for offline/CI runs. Live check with your own key:

```bash
codam-labs verify rag/06_citations
```

## Troubleshooting

- **Response doesn't contain `CITED:chunk_1`?** The mock keys off the literal substring
  `"cite chunk"` (case-insensitive) in your user message. `"please cite the source
  chunk"` won't match — use the exact phrase from the assignment, e.g.
  `"cite chunk_1 in answer"`.
- **Confusing this with `05_rag_pipeline`?** Both exercises call the same
  `/chat/completions` endpoint — the *only* thing that changes the mock's behavior is
  which trigger phrase is present in the prompt (`"rag pipeline"` vs `"cite chunk"`).
  If you copy-pasted the previous exercise's prompt, you'll get `RAG_ANSWER:42` here
  instead.
- **Real citations look inconsistent in live mode?** That's realistic — real models
  need explicit formatting instructions (e.g. "cite using `[chunk_id]` after each
  claim") and sometimes still drift; this exercise's live check only requires a
  non-empty response, not a specific citation format.

## Further reading

- [Mistral AI — Chat Completion API reference](https://docs.mistral.ai/api/#tag/chat)
- [Anthropic — Citations / grounding responses in sources](https://www.anthropic.com/news/introducing-citations-api)
