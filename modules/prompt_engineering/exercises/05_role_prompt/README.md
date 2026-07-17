# Role Prompting (System Messages)

## Theory

Chat-tuned models accept a `system` message alongside `user` messages. The system message sets persona, tone, and constraints that apply for the whole conversation — it's processed differently from a user turn and tends to have a stronger, more persistent influence on style and framing.

```json
[
  {"role": "system", "content": "You are a senior code reviewer. Be terse and point out bugs first."},
  {"role": "user", "content": "Review: print(1)"}
]
```

Without the system role, you'd have to repeat "act as a code reviewer, be terse, focus on bugs" inside every single user message. With it, that framing is set once and the model applies it consistently across turns. Common roles you'll see in production systems: `"You are a customer support agent for {product}"`, `"You are a strict JSON API, never output prose"`, `"You are a Socratic tutor who never gives direct answers"`.

Role prompting shapes *how* the model answers; it doesn't grant it new capabilities — a "security expert" system prompt won't make the model actually run a scanner, it just biases the response style and priorities.

## Assignment

Implement `with_role()`:

- The messages array sent to the model must have a **first** message with `role: "system"`.
- That system message's content must mention `code reviewer`.
- Print the response.

Expected stdout (mock mode) contains:

```text
ROLE_OK
```

## Files to modify

- `python/main.py` — implement `with_role() -> str`, building a messages list with system + user roles.
- `cpp/main.cpp` — build the equivalent two-message payload.

## Verify

```bash
codam-labs --mock verify prompt_engineering/05_role_prompt
```

## Troubleshooting

- **System message not first**: some APIs tolerate a system message anywhere in the list, but convention (and this grader) expects it as `messages[0]`. Putting it after the user message defeats its purpose and may fail the check.
- **Using `"role": "assistant"` by mistake**: assistant is for prior model turns in multi-turn history, not for setting persona — double-check you wrote `"system"`.
- **Vague role text**: `"You are helpful"` doesn't mention `code reviewer` and won't satisfy the check — the system content string needs that phrase present.
- **Sending only one message**: forgetting the `user` message means there's nothing for the reviewer persona to actually review; the exercise expects both messages in the array.

## Docs

- [Mistral API — Chat Completions (messages/roles)](https://docs.mistral.ai/api/#tag/chat)
- [Mistral prompting capabilities guide](https://docs.mistral.ai/guides/prompting_capabilities/)
- [OpenAI guide — giving the model a persona](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions)
