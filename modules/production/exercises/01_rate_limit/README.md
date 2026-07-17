# Rate Limiting

## Theory
Back off when API returns 429/503.

## Assignment
Retry the mock `/fail_twice` pattern on `{MISTRAL_API_BASE}/fail_twice`. Print `RATE_OK`.

That path exists **only** with `--mock` (not on the real Mistral API).

## Verify

```bash
codam-labs --mock verify production/01_rate_limit
```
