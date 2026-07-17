# Prompt Boundary

## Theory

Many injection attacks succeed simply because developer instructions and user data get
concatenated into one blob of text with no structural separation. The
[OWASP Prompt Injection Prevention Cheat Sheet's "Structured Prompts with Clear Separation"](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
guidance is exactly why chat APIs (Mistral, Ollama, and the mock server used throughout this
repo) accept a `messages` array with explicit `role` fields instead of one flat string —
`system` is the trusted instruction channel, `user` is untrusted data, and the API boundary
between them is enforced by the transport, not by hoping the model "remembers" who said what.

## Assignment

Build a `messages` list with exactly two entries: a `system` message ("You are a helpful
assistant.") and a `user` message ("Summarize this policy."). Print `BOUNDARY_OK:` followed
by the number of messages.

## Verify

```bash
codam-labs --mock verify security/04_prompt_boundary
```

Expected: `BOUNDARY_OK:2`

## Troubleshooting

- **Off-by-one count** — `BOUNDARY_OK:2` means exactly two dicts in the list; adding a third
  message (e.g. duplicating one role) or collapsing both into one dict with concatenated
  text defeats the point of the exercise, even if the count happens to still print `2`.
- **Wrong key names** — each entry needs a `role` key (`"system"` / `"user"`) and a
  `content` key, matching the shape every chat endpoint in this repo expects (Mistral,
  Ollama's `/api/chat`, and the MCP-adjacent mock). `type`/`text` or other naming won't be
  wrong for *this* exercise's local check, but it will break real requests you build on top
  of this pattern later.
- **This exercise never sends the messages anywhere** — it's a pure data-structure exercise;
  don't add an HTTP call to "test it for real" — that's `core/05_system_user_prompts`, which
  builds on this exact same boundary but actually calls the model.
