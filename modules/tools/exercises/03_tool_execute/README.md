# Execute Tool

## Theory

A tool *call* from the model is just a request — nothing actually happens until your
code runs the corresponding function and feeds the result back. The real loop is:
model decides to call `calculator` → your code executes it locally → you append the
tool's output to the conversation (as a `tool` role message) → you call the model again
so it can turn the raw result into a natural-language answer. This exercise isolates
just the execution step: simulating what the tool itself computes, before wiring it
back into a conversation.

## Assignment

Simulate the `calculator` tool executing the expression `6 * 7` locally and print the
result.

**Expected output:**

```
TOOL_RESULT:42
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify tools/03_tool_execute
```

No API call in this exercise — it's local execution logic, so `--mock` and live mode
check the exact same output.

## Troubleshooting

- **`TOOL_RESULT:0` or missing output?** Make sure the multiplication actually runs
  (`6 * 7`) and gets interpolated into the f-string — a common typo is printing the
  *expression string* `"6*7"` instead of the *computed value* `42`.
- **Off-by-format error, e.g. `TOOL_RESULT:42.0`?** If you compute with floats (`6.0 *
  7`) the substring check `"TOOL_RESULT:42"` still technically matches since `"42.0"`
  contains `"42"` as a prefix — but keep results as `int` where the math is exact, to
  avoid surprises in later exercises that do exact-match comparisons.
- **Conflating this with `04_calculator`?** This exercise hardcodes the result to
  illustrate the *execute-and-report* step in the tool loop; `04_calculator` is where
  you build a real (safe) expression evaluator instead of a hardcoded `6*7`.

## Further reading

- [Mistral AI — Function calling guide (tool execution loop)](https://docs.mistral.ai/capabilities/function_calling/)
- [OpenAI — Function calling: appending tool results to messages](https://platform.openai.com/docs/guides/function-calling#handling-function-calls)
