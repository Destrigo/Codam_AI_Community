# Prompt Templates

## Theory

Once you have more than one or two prompts in a codebase, hardcoding text inline everywhere becomes a maintenance headache — every wording tweak means hunting through source files. A **prompt template** is just a string with placeholders, kept as a named constant, filled in with real values at call time:

```python
GREETING_TEMPLATE = "Hello {name}"
GREETING_TEMPLATE.format(name="codam")   # -> "Hello codam"
```

This is the same idea as templating in web frameworks (Jinja, Handlebars) applied to prompts. Benefits:

- **DRY**: one source of truth for the wording; fix a typo once.
- **Testable**: you can unit-test template rendering without hitting an API.
- **Composable**: templates can be built from smaller templates (system template + task template + few-shot block).

This exercise is intentionally **local-only** — no network call, no API key needed. It's the simplest possible template: one placeholder, one substitution. Real systems scale this up to templates with many variables, conditional sections, and loaded-from-file templates (e.g. Jinja2, or Mistral's chat template format for local models).

## Assignment

Define a template constant `"Hello {name}"` and render it with `name = "codam"`.

- Print exactly: `TEMPLATE_OK:codam`

Expected stdout:

```text
TEMPLATE_OK:codam
```

## Files to modify

- `python/main.py` — define the template, format it with `name="codam"`, print `f"TEMPLATE_OK:{name}"` (or format the full rendered string directly).
- `cpp/main.cpp` — build the equivalent string and print it.

## Verify

Since this exercise makes no network call, `--mock` isn't required — but it's harmless to keep the flag for consistency with the rest of the module:

```bash
codam-labs verify prompt_engineering/06_prompt_template
# or, equivalently:
codam-labs --mock verify prompt_engineering/06_prompt_template
```

## Troubleshooting

- **Extra whitespace or punctuation**: the expected output is the exact string `TEMPLATE_OK:codam` — no trailing space, no period, no `TEMPLATE_OK: codam` with a space after the colon.
- **Printing the template literally**: don't print `"Hello {name}"` unformatted — the placeholder must actually be substituted (`Hello codam`), and then that fact reported as `TEMPLATE_OK:codam`, not the greeting itself, per the expected output.
- **Overcomplicating it**: no API call, no `os.environ` lookups needed here — reaching for `urllib.request` in this file is a sign you've mixed this exercise up with the others in the module.
- **f-string vs `.format()` confusion**: both work fine; just make sure the variable name inside the braces matches the variable you defined (`{name}` requires a variable literally named `name` when using `str.format(**locals())`-style calls, or matched keyword when using `.format(name=...)`).

## Docs

- [Python docs — `str.format()`](https://docs.python.org/3/library/stdtext.html#str.format)
- [Python docs — f-strings (formatted string literals)](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
- [Mistral chat templates (Jinja2-based) for local/self-hosted models](https://docs.mistral.ai/guides/tokenization/)
