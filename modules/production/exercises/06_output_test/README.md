# Output Testing

## Theory
LLM output isn't deterministic by default, which makes it tempting to skip testing it entirely.
But you can still assert **structural** properties — a required marker, a JSON shape, a forbidden
word — even when the exact wording varies. This is what lets an LLM-backed feature live safely in
a CI pipeline (see `.github/workflows/ci.yml` in this repo for the real thing).

**Worked example — a support-bot smoke test in CI:**

```text
Output:  "MOCK_RESPONSE:hello"
Assert:  re.search(r"MOCK_RESPONSE", output)   # passes regardless of wording after the marker
```

A test like this catches the failure mode that matters most in practice: the model (or your
prompt change) stops returning the shape downstream code depends on — not "did it phrase this
exactly like last time."

## Assignment
Assert a regex against a mock response and print `TEST_PASS`.

## Files
- `python/main.py` — stub with `out = "MOCK_RESPONSE:hello"` already set.
- `hint.md` — `re.search expected pattern`.
- `solution/python/main.py` — reference: `re.search(r"MOCK_RESPONSE", out)`.

## Verify
```bash
codam-labs --mock verify production/06_output_test
```
Expected stdout: `TEST_PASS`.

## Troubleshooting
- **Regex escaping** — if you test against real model output that includes special regex
  characters (`.`, `(`, `$`), remember to `re.escape()` any literal substring you're searching for.
- **Testing exact strings against live output** — assert *structure* (`re.search`, JSON schema)
  against a live model, not exact string equality; wording will drift between calls even at the
  same temperature.
- **False "pass" from a too-loose pattern** — `re.search(r".*", out)` always passes and tests
  nothing; make sure the pattern actually encodes the property you care about.
- **Flaky CI** — if this kind of test runs against the *real* API in CI it will be flaky and slow;
  that's why `codam-labs --mock verify` exists — pin the mock's deterministic output and assert
  against that.

## Docs
- [Python `re` module](https://docs.python.org/3/library/re.html)
- [pytest: asserting with regex](https://docs.pytest.org/en/stable/how-to/assert.html)
- Repo CI reference: `.github/workflows/ci.yml`
