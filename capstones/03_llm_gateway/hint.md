# Hints — Capstone 03 LLM Gateway

## Milestone 1
<details>
<summary>Hint 1.1 — Thin wrapper</summary>

Start with a single `httplib` or `urllib` POST to `/chat/completions` — same as `core/04`.
</details>

## Milestone 2
<details>
<summary>Hint 2.1 — Retry loop</summary>

Copy pattern from `core/09_timeout_retry` / `production/01_rate_limit`. Sleep `2**attempt` seconds.
</details>

## Milestone 3
<details>
<summary>Hint 3.1 — Cache key</summary>

```python
import hashlib, json
key = hashlib.sha256(json.dumps({"system": system, "prompt": prompt}, sort_keys=True).encode()).hexdigest()
```
</details>

## Milestone 4
<details>
<summary>Hint 4.1 — Guardrail before HTTP</summary>

Check injection phrases **before** cache lookup — never cache blocked prompts as valid responses.
</details>

## Milestone 5
<details>
<summary>Hint 5.1 — Eval runner</summary>

For each entry in `prompts.json`: `out = gateway.complete(prompt)`; pass if all `must_contain` substrings in `out`.
</details>
