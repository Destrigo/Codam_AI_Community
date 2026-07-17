# Secret Scanner

## Theory

Leaked API keys are one of the most common real-world security incidents in AI projects —
see the [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
for why secrets belong in environment variables (like this repo's root `.env`), never in
source. This exercise builds the simplest possible version of the tool that catches the
mistake before it ships: a regex that recognizes the shape of a Mistral-style secret key
(`sk-...`) inside a string.

## Assignment

Scan the sample string `api_key = "sk-test123456789"` for a secret-key pattern matching
`sk-[A-Za-z0-9_-]+`. If found, print `SECRET_SCAN_OK`.

## Verify

```bash
codam-labs --mock verify security/03_secret_scan
```

Expected: `SECRET_SCAN_OK`

## Troubleshooting

- **Prints nothing** — `re.search` returns `None` on no match, which is falsy; make sure
  your `if` checks the `Match` object (or wraps it in `bool(...)`) rather than assuming the
  call itself raises or always succeeds.
- **Regex too strict / too greedy** — `sk-[A-Za-z0-9_-]+` requires at least one character
  after `sk-`; forgetting the `+` (or using `*`) changes whether `"sk-"` alone would match.
  This repo's actual Mistral keys and the `MISTRAL_API_KEY` env var follow this same `sk-`
  prefix convention — this toy pattern is a simplified stand-in for it.
- **Don't confuse this with 06_red_team's guard clause** — this exercise scans *static code
  text* for accidentally committed secrets (a linting-style check you'd run over source
  files or diffs), not user input at request time. There's no prompt, no LLM call, and no
  blocking behavior here — just pattern matching over a string.
