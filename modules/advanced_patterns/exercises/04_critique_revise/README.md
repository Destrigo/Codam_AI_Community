# Critique and Revise

## Theory
A model's first draft is often good but not great. Rather than accepting it as final, ask the
model to critique its own output, then produce a revised version informed by that critique. This
is a lightweight version of the Reflexion pattern — two LLM calls instead of one, in exchange for
noticeably higher-quality final output on tasks like writing, code review, or structured
extraction.

**Worked example — drafting a customer apology email:**

```text
Draft:    "Sorry about the bug, we fixed it."
Critique: "Too terse, doesn't acknowledge impact, no next steps."
Revised:  "We're sorry for the disruption this caused — the issue is now fixed,
           and we've added monitoring to catch it earlier next time."
```

In this exercise, the mock server shortcuts the two-step exchange: any request whose message
contains the phrase `"critique revise"` is treated as already having gone through that loop, and
the mock replies with `REVISED_OK` directly — so you can verify the *plumbing* (a real
`POST /chat/completions` call with a real response parse) without needing two live round-trips.

## Assignment
`POST {MISTRAL_API_BASE}/chat/completions` with a user message containing `"critique revise"`,
parse `choices[0].message.content` from the JSON response, and print it (`REVISED_OK`).

## Files
- `python/main.py` — blank stub (`# TODO: implement`) — this one you build from scratch.
- `hint.md` — `Two-step prompt or mock keyword`.
- `solution/python/main.py` — reference: builds the payload, POSTs, prints the parsed content.

## Verify
```bash
codam-labs --mock verify advanced_patterns/04_critique_revise
```
Expected stdout: `REVISED_OK`.

## Troubleshooting
- **Using GET instead of POST** — chat completions is a `POST` with a JSON body; a bare `GET`
  against `/chat/completions` returns 404 on the mock (see `mock_server.py`'s `do_GET`).
- **Wrong content-type header** — omitting `Content-Type: application/json` can cause the mock
  (or the real API) to fail parsing your body.
- **Keyword casing** — the mock lowercases the user message before checking for `"critique
  revise"`; your prompt text casing doesn't matter, but the phrase itself must appear verbatim
  (as substring) somewhere in the user message.
- **Parsing the wrong JSON path** — the response shape is
  `{"choices": [{"message": {"content": "..."}}]}`; a common mistake is indexing
  `response["content"]` directly instead of `response["choices"][0]["message"]["content"]`.
- **Missing/invalid `MISTRAL_API_KEY` without `--mock`** — live calls to the real endpoint need a
  key from the `.env` at the repo root; `--mock` bypasses this entirely.

## Docs
- [Mistral: Chat Completions API](https://docs.mistral.ai/api/#tag/chat)
- ["Reflexion: Language Agents with Verbal Reinforcement Learning" (Shinn et al., 2023)](https://arxiv.org/abs/2303.11366)
- [Python `urllib.request.Request` (POST bodies)](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request)
