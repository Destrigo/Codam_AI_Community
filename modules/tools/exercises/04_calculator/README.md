# Calculator Tool

## Theory

LLMs are great at language and terrible, reliably, at arithmetic — ask one to multiply
two six-digit numbers and you'll get a plausible-looking wrong answer more often than
not. **Deterministic tools** fix this: hand the actual math to a real calculator
function instead of trusting the model's next-token guess. The catch is *how* you
evaluate an expression string safely — Python's built-in `eval()` will happily run
arbitrary code (`eval("__import__('os').system('rm -rf /')")` is a valid "expression"),
so a real tool needs a restricted evaluator, not raw `eval`.

## Assignment

Safely evaluate the expression `6 * 7` and print the result.

**Expected output:**

```
CALC:42
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify tools/04_calculator
```

No LLM call — pure local logic, `--mock` and live mode are equivalent here.

## Troubleshooting

- **Tempted to just use `eval("6*7")`?** It'll pass this specific check, but it's
  exactly the security anti-pattern this exercise exists to make you think about — a
  tool wired to arbitrary strings from user input via an LLM is a code-execution
  vulnerability if left as raw `eval`.
- **Tried `ast.literal_eval("6*7")` and got a `ValueError`?** That's expected —
  `literal_eval` only parses *literals* (numbers, strings, lists), not arithmetic
  operators, so `"6*7"` isn't valid input to it even though `"42"` would be. A safer
  calculator needs `ast.parse` plus a whitelist of allowed node types
  (`ast.BinOp`, `ast.Num`/`ast.Constant`, `ast.operator` subclasses) walked manually, or
  a small arithmetic-only parser.
- **Division-by-zero or malformed expressions:** whatever evaluator you build, guard
  against `ZeroDivisionError` and `SyntaxError` and return a clear error string instead
  of crashing — the model may pass along user-supplied expressions verbatim.

## Further reading

- [Python docs — `ast` module (safe expression parsing)](https://docs.python.org/3/library/ast.html)
- [Python docs — `eval()` security caveats](https://docs.python.org/3/library/functions.html#eval)
