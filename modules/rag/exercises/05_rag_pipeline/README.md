# RAG Pipeline

## Theory

This is where the module's earlier pieces (chunk → index → top-k) connect to an
actual model call. The **RAG pattern** is: retrieve relevant chunks, *augment* the
prompt by inserting them as context, then let the model *generate* an answer grounded
in that context instead of its own (possibly stale or hallucinated) knowledge. The
key engineering detail is prompt construction — the retrieved text has to actually
land inside the `user` (or `system`) message content sent to the API, not just live in
a variable your code never uses.

## Assignment

Simulate retrieval of the context `"The answer is 42"`, build a prompt that includes
both this context and the phrase **`rag pipeline`**, and send it to the chat
completions endpoint at `MISTRAL_API_BASE`. Print the assistant's response.

**Expected output:**

```
RAG_ANSWER:42
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify rag/05_rag_pipeline
```

This exercise calls an LLM, so prefer `--mock` in class (no API key, no internet). For
a live sanity check with your own key:

```bash
codam-labs verify rag/05_rag_pipeline
```

## Troubleshooting

- **Getting `MOCK_RESPONSE:...` instead of `RAG_ANSWER:42`?** The offline mock server
  pattern-matches on the literal substring `"rag pipeline"` (case-insensitive) inside
  your **user** message content. If your prompt paraphrases it away (e.g. "answer using
  retrieved context"), the mock falls through to its generic default response.
- **Timeout or connection refused?** Check that you read the base URL from
  `MISTRAL_API_BASE` (set automatically to a local mock port by `--mock`) rather than
  hardcoding `https://api.mistral.ai/v1` — hardcoding breaks offline verification.
- **`KeyError: 'choices'`?** Make sure you POST to `{base}/chat/completions` with a
  JSON body containing `model` and `messages`; a malformed request gets a 404 mock
  response with an `error` key instead of `choices`.
- **Live mode returns something unrelated to 42?** That's expected and fine — live
  mode only checks the response is non-empty (`_non_empty` validator), not the literal
  number, since a real model paraphrases instead of echoing the mock's fixed string.

## Further reading

- [Mistral AI — Chat Completion API reference](https://docs.mistral.ai/api/#tag/chat)
- [LangChain — RAG tutorial (retrieve + augment + generate)](https://python.langchain.com/docs/tutorials/rag/)
