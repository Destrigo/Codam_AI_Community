# 07 — Temperature and max_tokens

## Theory

Beyond `model` and `messages`, the API exposes parameters that control **how** text gets generated, not just what's being asked.

### `temperature` (typically 0.0 – 2.0)

- **Low (0.0–0.3)**: near-deterministic, repeatable output — the right choice for JSON extraction, classification, code generation.
- **High (0.7–1.0+)**: more variety and "creativity" — good for brainstorming, copywriting, anything where diversity beats precision.

### `max_tokens`

A hard ceiling on how many tokens the model is allowed to **generate** in its response (it does not limit the size of your prompt). It's the knob you reach for to:

- control cost (you pay per generated token),
- force short, punchy answers,
- avoid a runaway response burning through your budget.

### Other knobs you'll meet later

`top_p`, `frequency_penalty`, `presence_penalty`, etc. exist too, but `temperature` and `max_tokens` cover the two decisions you'll make most often: *how random* and *how long*.

### The cost/latency trade-off

More generated tokens = more time waiting and more money spent. In production, `max_tokens` is tuned per use case — a one-word classification doesn't need the same budget as a paragraph summary.

---

## Assignment

Call chat completions with:

- `messages`: `[{"role": "user", "content": "hello"}]`
- `max_tokens`: `5`

Print the assistant's response.

With `--mock`, the server checks that `max_tokens` is present and `<= 5`, and replies:

```
TOKEN_LIMIT_OK
```

## Files to modify

- `python/main.py` — extend `chat_completion` to accept and forward `max_tokens`

## Verify

```bash
codam-labs --mock verify 07_output_control
```

## Troubleshooting

- **Forgetting to add `max_tokens` to the JSON payload** — having the parameter as a Python function argument isn't enough; it must end up as a key in the `payload` dict you `json.dumps()` and send. If the mock never sees `max_tokens`, it won't reply `TOKEN_LIMIT_OK`.
- **Sending it as a string** — `payload["max_tokens"] = "5"` sends a JSON string, not a number. The mock's check (`req.get("max_tokens") <= 5`) expects a numeric comparison and will error or misbehave on a string.
- **Value greater than 5** — the assignment specifically asks for `max_tokens=5`. Anything higher fails the mock's `<= 5` check even though it's a "valid" parameter in general.
- **Confusing `max_tokens` with `temperature`** — they control different things (length vs. randomness). This exercise only needs `max_tokens`; you don't need to touch `temperature` at all.
- **Breaking the exercise `04` function signature** — if `chat_completion(messages)` doesn't accept an optional `max_tokens` parameter, calling `chat_completion(messages, max_tokens=5)` raises `TypeError: unexpected keyword argument`. Update the signature, don't just add a global.

## Docs & further reading

- [Mistral API reference — Chat Completions parameters](https://docs.mistral.ai/api/#tag/chat) (`temperature`, `max_tokens`, and friends)
- [Hugging Face — How LLMs generate text (sampling, temperature)](https://huggingface.co/blog/how-to-generate)
