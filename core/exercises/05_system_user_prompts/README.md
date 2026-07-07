# 05 — System Prompt and User Prompt

## Theory

In chat APIs, messages have a **role** that indicates who is speaking:

| Role | Who | Purpose |
|------|-----|---------|
| `system` | Global instructions | Defines behavior, tone, constraints |
| `user` | The human user | The question or task |
| `assistant` | The model | Previous responses (history) |

### System prompt

It is not visible to the end user of the app, but it **conditions every response**. Examples:

- *"Always respond in English"*
- *"You are an assistant that responds only in UPPERCASE"*
- *"Do not invent data not present in the context"* (useful for RAG)

### User prompt

The concrete request of the moment: *"Summarize this text"*, *"hello"*.

### Message order

Typically:

```
system → user → assistant → user → assistant → ...
```

The system prompt goes **first**. Changing it changes behavior without modifying the user question.

### Why it matters

The system prompt is where you put **policy**, **output format**, and **guardrails**. It is the most important distinction in basic prompt engineering.

---

## Assignment

Send a chat with:

- **system**: `"Always respond in UPPERCASE"`
- **user**: `"hello"`

Print only the assistant response.

Expected output (with mock): `HELLO`

## Verify

```bash
codamlings verify 05_system_user_prompts
```
