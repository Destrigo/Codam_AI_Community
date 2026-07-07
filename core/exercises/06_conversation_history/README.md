# 06 — Conversation History

## Theory

LLMs **have no memory** between different API calls. Each request is stateless: the model only sees what you send in `messages`.

### Context window

The `messages` array is the **conversation memory**. To maintain a multi-turn dialogue, you must resend the entire history:

```json
[
  {"role": "user", "content": "My name is Marco"},
  {"role": "assistant", "content": "Nice to meet you, Marco!"},
  {"role": "user", "content": "What is my name?"}
]
```

Without the previous messages, the model would not know to answer *"Marco"*.

### Limits

Every model has a **context window** (e.g. 128k tokens). Too many messages = truncation or error. In production, old messages are summarized or trimmed.

### Implications for agents and RAG

- **Agent**: each loop step adds messages (tool call, result, reflection)
- **RAG**: retrieved context is injected as a `user` or `system` message before the question

Understanding history is a prerequisite for any serious conversational application.

---

## Assignment

Send **4 messages** in a single call:

1. `user`: `"First"`
2. `assistant`: `"Received first"`
3. `user`: `"Second"`
4. `user`: `"How many user messages are in the history?"`

Print the assistant response.

With the mock, the output is: `HISTORY_OK:4` (4 total messages in the request).

## Verify

```bash
codam-labs verify 06_conversation_history
```
