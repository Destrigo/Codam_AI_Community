# JSON-Only Output

## Theory

When your code needs to `json.loads()` a model's response, prose is the enemy. A model asked "what's the sentiment?" might answer *"I'd say this leans positive, though there's a hint of sarcasm."* — perfectly reasonable for a human, unparseable for a program.

Explicitly instructing the model to respond with JSON only (and nothing else) collapses that ambiguity:

```text
Bad:  "What's the sentiment of: great day"
Good: "What's the sentiment of: great day. Respond with json only,
       no extra text: {\"sentiment\": \"...\"}"
```

Telling the model the exact shape you expect (even sketching the keys) makes it far more likely to emit clean, parseable JSON as the *entire* response rather than JSON embedded in a sentence. This is a cheaper, model-agnostic alternative to structured output modes (like Mistral's `response_format: {"type": "json_object"}`) — useful when you don't have access to that parameter, or want to understand what it's doing under the hood before relying on it.

## Assignment

Implement `ask_json_only()`:

- The prompt sent to the model must contain the literal phrase `json only`.
- Print the raw response to stdout.

Expected stdout (mock mode) contains:

```text
JSON_LABEL_OK
```

## Files to modify

- `python/main.py` — implement `ask_json_only() -> str` and call it in `main()`.
- `cpp/main.cpp` — build the equivalent request with the `json only` instruction.

## Verify

```bash
codam-labs --mock verify prompt_engineering/03_json_format
```

## Troubleshooting

- **Paraphrasing the instruction**: writing "respond only in JSON format" is good practice but won't satisfy this specific check — the grader looks for the exact substring `json only` in your prompt (case-sensitive lowercase). Include it verbatim, e.g. *"...respond with json only."*
- **Confusing this with `response_format`**: Mistral's API supports a `response_format` parameter for guaranteed JSON mode, but this exercise is about the *prompting* technique, not the API parameter — don't skip the instruction text just because you set that field.
- **Forgetting the request still returns a string**: even with `json only` in your prompt, the mock/real response comes back as a normal string in `message.content`. This exercise only asks you to print it — you are not required to `json.loads()` it here (that's exercise `structured_output/01_extract_json`).

## Docs

- [Mistral API — JSON mode / `response_format`](https://docs.mistral.ai/capabilities/structured-output/json_mode/)
- [Mistral chat completions reference](https://docs.mistral.ai/api/#tag/chat)
- [OpenAI structured outputs guide](https://platform.openai.com/docs/guides/structured-outputs) (same underlying philosophy of constraining output shape)
