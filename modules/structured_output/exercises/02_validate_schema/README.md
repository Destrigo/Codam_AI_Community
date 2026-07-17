# Validate Schema

## Theory

Parsing JSON successfully doesn't mean the JSON is *usable*. `json.loads('{"name": "codam"}')` parses fine even if your downstream code also needs a `score` field that isn't there — and you won't find out until something crashes three function calls later with a confusing `KeyError`.

Schema validation closes that gap by checking, immediately after parsing and *before* using the data, that every field you depend on actually exists (and, in stricter versions, has the right type):

```python
data = {"name": "codam", "score": 1}
required = ("name", "score")
assert all(field in data for field in required)
```

This is the minimal form of validation. Production systems typically escalate to a schema library (Pydantic, `jsonschema`, or Mistral/OpenAI's native structured-output schemas) that checks types, ranges, and nested structure in one call rather than hand-rolled `in` checks — but the core principle is identical: **fail fast, at the boundary, with a clear error**, rather than letting malformed data silently propagate.

## Assignment

Given the object `{"name": "codam", "score": 1}`:

- Verify both `"name"` and `"score"` are present as keys.
- Print `SCHEMA_OK` if validation passes.

Expected stdout:

```text
SCHEMA_OK
```

## Files to modify

- `python/main.py` — implement the presence check (e.g. `assert` or an `if`/raise) for both required fields.
- `cpp/main.cpp` — implement the equivalent key-presence check against a `std::map`/JSON value.

## Verify

```bash
codam-labs --mock verify structured_output/02_validate_schema
```

No network call is involved — the object is defined locally in the exercise — so mock mode is a no-op here but is kept for command consistency across the module.

## Troubleshooting

- **Checking value truthiness instead of key presence**: `if data["score"]:` fails for a legitimately valid `score` of `0`, since `0` is falsy in Python. Use `"score" in data` to check *presence*, not `if data["score"]`.
- **`KeyError` before your validation runs**: if you write `data["score"]` directly without an `in` check first, a missing key raises before you get a chance to report a clean validation failure — always check `in` first, access second.
- **Only checking one of the two fields**: the assignment requires both `"name"` and `"score"` — a partial check (`"name" in data`) alone will pass this specific mock input but misses the point of the exercise; use `all(...)` or chained `and`.
- **Printing `SCHEMA_OK` unconditionally**: don't print the success message before the validation check runs — if you're using `assert`, let it raise (crash) rather than printing success regardless of the outcome.

## Docs

- [Python docs — `dict` membership testing (`in`)](https://docs.python.org/3/reference/expressions.html#membership-test-operations)
- [Pydantic — data validation using Python type hints](https://docs.pydantic.dev/latest/) (the production-grade version of this pattern)
- [Mistral structured outputs guide](https://docs.mistral.ai/capabilities/structured-output/) — schema-constrained generation at the API level
