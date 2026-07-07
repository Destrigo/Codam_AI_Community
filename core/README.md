# Core — Foundations for everyone

Required path before stand-alone modules (`rag`, `agents`, `prompt_engineering`, …).

## What you'll learn

1. **Secure setup** — environment variables, no secrets in code
2. **HTTP & JSON** — talk to any REST API
3. **LLM basics** — chat completions, roles, history
4. **Output control** — temperature, token limits, streaming
5. **Robustness** — retry, timeout, defensive parsing

## Getting started

```bash
cd private/codam_AI_community
pip install -e .

# Python (default)
codam-labs list
codam-labs watch

# C++
codam-labs watch --lang cpp
```

## Exercises

| # | Slug | Topic |
|---|------|-------|
| 01 | `01_env_vars` | Environment variables |
| 02 | `02_http_get` | HTTP GET + JSON |
| 03 | `03_http_post` | HTTP POST |
| 04 | `04_llm_first_call` | First LLM call |
| 05 | `05_system_user_prompts` | System vs user prompt |
| 06 | `06_conversation_history` | Conversation history |
| 07 | `07_output_control` | Temperature and max_tokens |
| 08 | `08_streaming` | SSE streaming |
| 09 | `09_timeout_retry` | Timeout and retry |
| 10 | `10_dirty_json` | Extract JSON from messy text |

## C++ requirements

- CMake ≥ 3.16
- C++17 compiler (MSVC, GCC, Clang)
- Internet connection **only on first build** (downloads `json` + `httplib` headers)

No extra system dependencies: HTTP/JSON libraries are header-only in `shared/cpp/vendor/`.

## Mock vs live

`codam-labs verify` uses a **local mock server** for LLM exercises — works offline.

All LLM exercises use **[Mistral](https://mistral.ai)** via its OpenAI-compatible API (`https://api.mistral.ai/v1`, model `mistral-small-latest`).

`codam-labs run --mock` runs against the mock. Without `--mock`, LLM exercises use `MISTRAL_API_BASE`, `MISTRAL_API_KEY`, and `MISTRAL_MODEL` from your environment.
