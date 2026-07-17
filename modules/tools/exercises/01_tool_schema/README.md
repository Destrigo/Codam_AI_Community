# Tool Schema

## Theory

Function calling lets an LLM request that *your* code run something instead of trying
to compute or fabricate the answer itself. Before the model can call anything, it needs
a **schema**: a structured description of the tool's name, purpose, and parameters
(name, type, whether required) — typically JSON, matching the shape OpenAI and Mistral
both expect for `tools=[...]` in a chat completions request. Get the schema wrong (bad
types, missing required fields) and the model either refuses to call the tool or sends
malformed arguments your code can't parse.

## Assignment

Define a tool named **`calculator`** with a single parameter named **`expression`**,
then confirm the schema is well-formed.

**Expected output:**

```
SCHEMA_OK
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify tools/01_tool_schema
```

This exercise doesn't call an LLM at all — it's about the *shape* of the schema dict
itself, so `--mock` and live mode are identical.

## Troubleshooting

- **Printing the dict instead of `SCHEMA_OK`?** The verifier checks stdout for the
  literal marker string — print `"SCHEMA_OK"` after your assertions pass, not the raw
  schema object.
- **`AssertionError` on `tool["name"]`?** Double-check the key nesting — a common
  mistake is nesting `name` under `function` (as the real Mistral/OpenAI wire format
  does: `{"type": "function", "function": {"name": ...}}`) when this exercise expects a
  flatter `{"name": ..., "parameters": {...}}` shape. Match whichever structure your
  `main.py` stub actually asserts against.
- **Parameter type mismatch:** `parameters` here is a simple `{"expression": "string"}`
  mapping for teaching purposes — real API schemas use full JSON Schema
  (`{"type": "object", "properties": {"expression": {"type": "string"}}, "required":
  [...]}`). Exercise `02_tool_select` is where that fuller schema actually gets sent
  over the wire.

## Further reading

- [Mistral AI — Function calling guide](https://docs.mistral.ai/capabilities/function_calling/)
- [OpenAI — Function calling / tools reference](https://platform.openai.com/docs/guides/function-calling)
