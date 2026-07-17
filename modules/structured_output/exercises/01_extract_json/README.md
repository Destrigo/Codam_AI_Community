# Extract JSON from Prose

## Theory

Even when you ask nicely, LLMs frequently wrap JSON in explanatory text: *"Sure! Here's the result: {"label": "positive"} Let me know if you need anything else."* If your code does a naive `json.loads(response)` on that, it crashes on the leading `Sure! Here's the result:` before the parser ever sees a `{`.

The pragmatic fix — before reaching for a full JSON-mode API parameter — is to locate the outermost braces yourself and slice out just the JSON substring:

```python
raw = 'Result: {"label":"positive"}'
start, end = raw.find("{"), raw.rfind("}") + 1
data = json.loads(raw[start:end])   # {'label': 'positive'}
```

`find("{")` grabs the *first* opening brace and `rfind("}")` grabs the *last* closing brace — this correctly spans nested objects (`{"a": {"b": 1}}`) as long as there's exactly one top-level JSON object in the text. It breaks down if the model emits two separate JSON objects in one response, which is why production systems often add a regex fallback or ask the model for JSON-only output (see `prompt_engineering/03_json_format`) to reduce how often this rescue logic is needed at all.

## Assignment

Given the mock raw string `Result: {"label":"positive"}`:

- Extract the JSON substring and parse it with `json.loads`.
- Read the `label` field from the parsed object.
- Print `EXTRACT_OK:positive` (i.e. `EXTRACT_OK:` followed by the extracted label value).

Expected stdout:

```text
EXTRACT_OK:positive
```

## Files to modify

- `python/main.py` — implement the brace-slicing + `json.loads` logic in `main()`.
- `cpp/main.cpp` — implement equivalent substring extraction and JSON parsing (e.g. manual brace scan, or a lightweight JSON parse of the sliced substring).

## Verify

```bash
codam-labs --mock verify structured_output/01_extract_json
```

This exercise is pure string/JSON logic — no network call — so `--mock` mainly exists for consistency with the grader's expectations across the module; there's no live-mode variant to fall back to here.

## Troubleshooting

- **Using `find("}")` instead of `rfind("}")`**: if the label's value itself could ever contain a `}` character (not in this exact input, but in general), `find` grabs the *first* closing brace and truncates the JSON early. Always pair `find("{")` with `rfind("}")`.
- **Off-by-one on the slice end**: `raw.rfind("}")` returns the *index* of `}`, not one past it — forgetting the `+ 1` when slicing (`raw[start:end]`) drops the final `}` and breaks `json.loads`.
- **Assuming the whole string is JSON**: don't skip straight to `json.loads(raw)` — the literal prefix `Result: ` in the mock input guarantees that fails, which is the whole point of the exercise.
- **KeyError on `label`**: double check you're parsing into a `dict` and indexing `data["label"]`, not accidentally treating `data` as a list or string.

## Docs

- [Python `json` module docs](https://docs.python.org/3/library/json.html)
- [Mistral JSON mode guide](https://docs.mistral.ai/capabilities/structured-output/json_mode/) — the alternative to brace-scraping: ask the API to guarantee valid JSON output
- [`str.find` / `str.rfind` — Python docs](https://docs.python.org/3/library/stdtypes.html#str.find)
