# 06 — Conversation History

## Theory

LLMs have **no memory** between separate API calls. Each request is stateless — the model only ever sees what's inside the `messages` array you send it, right now, this call. There's no session, no server-side "remember what we talked about."

### The `messages` array *is* the memory

To hold a multi-turn conversation, you resend the **entire history** on every call:

```json
[
  {"role": "user", "content": "My name is Marco"},
  {"role": "assistant", "content": "Nice to meet you, Marco!"},
  {"role": "user", "content": "What is my name?"}
]
```

Without the first two messages in that list, the model has no way to answer `"Marco"` on the third turn — it isn't lying or forgetting, it genuinely was never told.

### Context window limits

Every model has a **context window** (e.g. 128k tokens). Send too many messages and you'll hit truncation or an outright error. Production systems summarize or drop old messages to stay under the limit — for this exercise, with only 4 messages, that's not yet a concern.

### Why this matters for agents and RAG later in the course

- **Agents**: every loop iteration appends messages — the tool call, its result, the model's reflection. History grows fast.
- **RAG**: retrieved context gets injected as an extra `user` or `system` message *before* the actual question, then the whole thing is sent together.

Understanding "history = resend everything" is a prerequisite for both.

---

## Assignment

Send exactly **4 messages** in a single API call, in this order:

1. `user`: `"First"`
2. `assistant`: `"Received first"`
3. `user`: `"Second"`
4. `user`: `"How many user messages are in the history?"`

Print the assistant's response.

With `--mock`, the server counts `len(messages)` in the request and replies with:

```
HISTORY_OK:4
```

## Files to modify

- `python/main.py` — build the 4-message list, call `chat_completion`

## Verify

```bash
codam-labs --mock verify 06_conversation_history
```

## Troubleshooting

- **Sending only the last message** — if you only pass `[{"role": "user", "content": "How many..."}]` and drop the rest, `len(messages)` is `1`, not `4`, and the mock replies `HISTORY_OK:1`. The whole point is resending everything.
- **Wrong count because of an extra message** — adding an unrequested `system` message makes the total 5, not 4. Stick to exactly the 4 messages listed, in that order.
- **`assistant` message written as `user`** — message 2 (`"Received first"`) must have `role: "assistant"`, simulating a prior model reply. Getting the role wrong doesn't break this particular mock check (which only counts messages), but it breaks the *meaning* of the conversation and will bite you with a real model.
- **Copy-pasting exercise `05`'s two-message pattern and stopping there** — this exercise specifically needs 4 messages; don't stop at system+user.
- **`chat_completion` not reused/implemented** — if you skipped exercise `04`/`05` or didn't carry the function over, you'll hit `NotImplementedError` before the history logic even runs.

## Docs & further reading

- [Mistral — Context window / token limits](https://docs.mistral.ai/getting-started/models/)
- [OpenAI — Managing conversation state](https://platform.openai.com/docs/guides/text-generation) (same "resend the whole array" model shared across providers)
