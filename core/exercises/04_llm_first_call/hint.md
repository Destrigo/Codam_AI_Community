# Hint — 04_llm_first_call

1. Read `MISTRAL_API_BASE` (default `https://api.mistral.ai/v1`) and `MISTRAL_API_KEY`
2. Full URL: `{base}/chat/completions`
3. Body: `{"model": "...", "messages": [{"role": "user", "content": "hello"}]}`
4. Headers: `Authorization: Bearer ...` and `Content-Type: application/json`
5. Extract: `response["choices"][0]["message"]["content"]`

Create a reusable `chat_completion(messages)` function — you will need it in later exercises.
