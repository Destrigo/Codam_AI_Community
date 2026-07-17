# PII Redaction

## Theory

[OWASP LLM02:2025 — Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
covers the risk of personal data (emails, phone numbers, credentials) leaking through logs,
prompts, or model output. The standard mitigation is redaction before storage or transmission
— replace the sensitive substring with a placeholder tag so downstream systems (and log
viewers) never see the real value. This exercise implements the smallest useful version:
email redaction with a regex.

## Assignment

Given the string `"contact marco@example.com please"`, replace the email address with the
literal tag `[EMAIL]`. Print `PII_REDACTED` if the tag appears in the result, otherwise
`LEAK`.

## Verify

```bash
codam-labs --mock verify security/05_pii_redact
```

Expected: `PII_REDACTED`

## Troubleshooting

- **Prints `LEAK`** — your regex didn't match the sample email, or you replaced with a
  different tag string (`[REDACTED]`, `***`, etc.) instead of the exact literal `[EMAIL]`
  the check looks for.
- **Regex only matches simple addresses** — a pattern like `[\w.-]+@[\w.-]+` is enough for
  `marco@example.com` but won't handle `+` in the local part (`marco+test@example.com`) or
  multi-level subdomains reliably. That's fine for this exercise; don't over-engineer it, but
  don't assume it's production-grade PII detection either — see `production/03_redacted_log`
  for where this same idea gets applied to real log lines.
- **Redacting mutates the wrong thing** — `redact_pii` should return a *new* string; if you
  redact in place on a variable you also print elsewhere, you may end up printing `[EMAIL]`
  where you meant to show the original text for debugging, or vice versa.
