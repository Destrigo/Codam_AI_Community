# Redacted Logging

## Theory
Logs get shipped to third-party tools (Datadog, Sentry, a shared Slack channel) far more casually
than production databases. If you log the raw request/response of an LLM call, any API key,
customer PII, or secret embedded in that text ends up sitting in plaintext somewhere you don't
fully control.

**Worked example — a support ticket enrichment job:**

```text
Raw:      "Authenticate with key=sk-secret and summarize this ticket"
Logged:   "Authenticate with key=[REDACTED] and summarize this ticket"
```

The redaction has to happen **before** the string reaches your logger/telemetry sink — not after.
Once it's written to a log aggregator, you can't safely unwrite it.

## Assignment
Write a `redact()` function that replaces a known secret pattern (`sk-secret`) with `[REDACTED]`
before logging, then print `LOG_REDACTED`.

## Files
- `python/main.py` — stub; `redact()` needs the substitution, `main()` needs the final print.
- `hint.md` — `Replace sk-... with [REDACTED]`.
- `solution/python/main.py` — reference: literal string replace for the exercise's fixed pattern.

## Verify
```bash
codam-labs --mock verify production/03_redacted_log
```
Expected stdout: `LOG_REDACTED`.

## Troubleshooting
- **Redaction misses real keys** — this exercise uses a literal match (`sk-secret`) for
  simplicity; real Mistral keys don't have a fixed suffix, so production code needs a regex like
  `r"sk-[A-Za-z0-9]{20,}"`, not a literal string.
- **Over-redaction** — a regex that's too broad (e.g. matching any `key=...`) can eat legitimate
  log content. Scope the pattern tightly to known secret shapes.
- **Redacting after the fact** — if you log first and redact in a separate pass, the unredacted
  version may already be indexed/cached by your logging pipeline before the redaction runs.
- **Case sensitivity** — `SK-SECRET` vs `sk-secret`; decide once whether matching is
  case-insensitive and apply it consistently across every log call site.

## Docs
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — what never belongs in a log line.
- [Python `re.sub`](https://docs.python.org/3/library/re.html#re.sub) — for real (non-literal) secret patterns.
- [Datadog Sensitive Data Scanner](https://docs.datadoghq.com/sensitive_data_scanner/) — how a real observability pipeline redacts logs at ingest.
