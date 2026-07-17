# Clear vs Ambiguous Prompts

## Theory

The single biggest lever you have over an LLM's output quality is *how precisely you ask*. An ambiguous prompt leaves the model to guess at your intent, and it will guess — confidently, and often wrong.

Compare these two prompts:

```text
Ambiguous:  "What do you think about this?"
Specific:   "Classify the sentiment of this review as positive or negative,
             and explain your reasoning in one sentence: 'The battery died
             after two hours.'"
```

The ambiguous version doesn't even say *what* "this" is, or what kind of judgment you want back. The specific version pins down three things: the **task** (classify sentiment), the **output constraint** (positive/negative), and the **input** (the actual review text). That's the difference between a coin-flip answer and a reliable one.

A good rule of thumb: if two different people reading your prompt could reasonably expect two different answers, the prompt is ambiguous.

## Assignment

Implement `classify_sentiment(text)` in `python/main.py` (or the equivalent function in `cpp/main.cpp`). It must call the Mistral chat completions endpoint with a prompt that is unambiguous about the task:

- The prompt text sent to the model must mention **both** `positive` and `negative` as the allowed labels.
- The prompt must include the actual `text` being classified (not a placeholder).
- Print the raw assistant response to stdout.

Expected stdout (mock mode) contains:

```text
SPECIFIC_OK
```

## Files to modify

- `python/main.py` — implement `classify_sentiment(text: str) -> str` and call it from `main()`.
- `cpp/main.cpp` — implement the equivalent request/print logic.

## Verify

```bash
codam-labs --mock verify prompt_engineering/01_clear_vs_ambiguous
```

Mock mode short-circuits the real Mistral API and returns a canned response so you can validate prompt *shape* (labels + input text present) without spending API credits.

## Troubleshooting

- **Missing labels**: if your prompt only says "classify this text" without naming `positive`/`negative` explicitly, the check fails even if the model happens to answer correctly — the grader looks at what you *asked*, not just what came back.
- **Hardcoded example text**: don't hardcode the review text separately from the `text` parameter — the prompt must interpolate the actual argument passed to your function, otherwise calling it with different input silently classifies the wrong thing.
- **Empty `MISTRAL_API_KEY` in real mode**: fine for `--mock`, but if you run without `--mock` against the live API you'll get a 401. Stick to mock while iterating.
- **Forgetting to print**: the grader reads stdout — returning the string from `classify_sentiment` without a `print()` in `main()` produces empty output.

## Docs

- [Mistral API reference — Chat Completions](https://docs.mistral.ai/api/#tag/chat)
- [Mistral prompting capabilities guide](https://docs.mistral.ai/guides/prompting_capabilities/)
- [OpenAI's "Write clear instructions" guide](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions) (the same clarity principles apply across providers)
