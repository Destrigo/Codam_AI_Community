# Tool Selection

## Theory

Defining a schema (previous exercise) is only half the story — the model has to decide
*whether and which* tool to call, based on the user's intent. That decision only
happens if you actually send the `tools` array in the request; a model given no tools
can never call one, no matter how clearly the user asks. This exercise is about the
request side of tool calling: attaching your tool definitions to the API call so the
model has something to choose from.

## Assignment

Send a chat request containing a `tools` array (including a `calculator` tool) and a
user message asking to **calculate** something. Print the assistant's response.

**Expected output:**

```
TOOL_CALL:calculator
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify tools/02_tool_select
```

Calls an LLM — prefer `--mock` for offline/CI. Live check with your own key:

```bash
codam-labs verify tools/02_tool_select
```

## Troubleshooting

- **Getting a generic `MOCK_RESPONSE:...` instead of `TOOL_CALL:calculator`?** The
  offline mock only returns the tool-call marker when **both** conditions hold: the
  request's `tools` list is non-empty **and** the user message contains the substring
  `"calculate"` (case-insensitive). Missing either one falls through to the default
  response.
- **Sent `tools` but forgot the trigger word?** A user message like `"what's 6 times
  7"` won't match — the mock looks for the literal word `"calculate"`, not semantic
  intent (it's a mock, not a real model). Use a phrase like `"calculate 6*7"`.
- **Live mode gives an actual tool_call object, not a string?** In live mode the real
  Mistral API may return `message.tool_calls` instead of plain text `content` — the
  live validator here just checks the response is non-empty, but production code
  should branch on `finish_reason == "tool_calls"` and read `tool_calls[0].function`
  rather than assuming plain text.

## Further reading

- [Mistral AI — Function calling guide](https://docs.mistral.ai/capabilities/function_calling/)
- [OpenAI Cookbook — How to call functions with chat models](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models)
