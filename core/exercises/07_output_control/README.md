# 07 — Temperature and max_tokens

## Theory

Beyond `model` and `messages`, you control **how** the model generates text.

### temperature (0.0 – 2.0)

- **Low (0.0–0.3)**: more deterministic, repeatable responses — ideal for JSON, classification, code
- **High (0.7–1.0)**: more creativity and variability — ideal for brainstorming, copywriting

### max_tokens

Maximum limit of tokens **generated** in the response (not in the prompt). Useful for:

- Controlling costs
- Forcing short responses
- Avoiding responses that exhaust the budget

### top_p, frequency_penalty, …

Other optional parameters. For now, temperature and max_tokens are enough.

### Cost/latency trade-off

More generated tokens = more time and more cost. In production, `max_tokens` is set based on the use case.

---

## Assignment

Call chat completions with:

- `messages`: `[{"role": "user", "content": "hello"}]`
- `max_tokens`: `5`

Print the assistant response.

With the mock: `TOKEN_LIMIT_OK`

## Verify

```bash
codamlings verify 07_output_control
```
