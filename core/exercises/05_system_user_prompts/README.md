# 05 — System Prompt and User Prompt

## Theory

In chat APIs, every message carries a **role** that says who's speaking:

| Role | Who | Purpose |
|------|-----|---------|
| `system` | Global instructions | Defines behavior, tone, constraints |
| `user` | The human | The actual question or task |
| `assistant` | The model | Previous responses (conversation history, exercise `06`) |

### The system prompt

Never shown to the end user of an app, but it **conditions every response** the model gives. Typical examples:

- *"Always respond in English."*
- *"You are an assistant that responds only in UPPERCASE."* (today's example)
- *"Do not invent facts not present in the provided context."* (the guardrail every RAG system relies on)

### The user prompt

The concrete ask of the moment: `"Summarize this text"`, `"hello"`. It changes every turn; the system prompt usually doesn't.

### Message order

```
system → user → assistant → user → assistant → ...
```

The system prompt always goes **first** in the array. This lets you change the *policy* without touching the *question* — swap the system message and the same user input produces a differently-behaved assistant.

### Why this is the most important distinction in basic prompt engineering

Confusing "what the app wants" (system) with "what the user is asking" (user) is the single most common beginner bug. It's also a security boundary: in production, untrusted user input should never be able to overwrite your system instructions (see `modules/security` later in the course).

---

## Assignment

Send a chat completion with exactly two messages:

- `system`: `"Always respond in UPPERCASE"`
- `user`: `"hello"`

Print **only** the assistant's response — nothing else, no labels, no trailing text.

Expected output (with `--mock`), and it must be the *entire* stdout, not just a substring:

```
HELLO
```

The mock uppercases whatever you sent as the user message — it does not hardcode `"HELLO"`. Don't uppercase the string yourself in Python; the model (or here, the mock standing in for it) has to do it by following your system prompt.

## Files to modify

- `python/main.py` — reuse or re-implement `chat_completion` from exercise `04`, then build the two-message array

## Verify

```bash
codam-labs --mock verify 05_system_user_prompts
```

## Troubleshooting

- **Uppercasing the string in Python yourself** — `print(user_text.upper())` "passes" only if you also happen to call the API correctly, but it defeats the exercise: the system prompt must do the work, not your code.
- **Output isn't exactly `HELLO`** — unlike some other exercises, this check requires stdout to equal `HELLO` exactly (after trimming whitespace), not just contain it. A leftover `print("Response:", content)` or an extra newline from `print(content + "\n")` will fail even though the content itself is correct.
- **System message placed after the user message** — the array order should be `system` first, `user` second. Some mocks may tolerate the wrong order, but real providers and the exercise's convention expect system first.
- **`chat_completion` still raising `NotImplementedError`** — copy the working implementation from exercise `04` rather than starting from scratch.
- **Wording the system prompt differently than specified** — "Respond in caps" or "always use capital letters" might not trigger the same behavior from a real model (or this mock, which checks for the literal word `"uppercase"`). Use the exact instruction text from the assignment.

## Docs & further reading

- [Mistral — Prompting capabilities & system prompts](https://docs.mistral.ai/guides/prompting_capabilities/)
- [OpenAI — Role-based prompting concepts](https://platform.openai.com/docs/guides/text-generation) (same `system`/`user`/`assistant` model most providers share)
