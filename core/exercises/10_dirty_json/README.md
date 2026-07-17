# 10 — Extracting JSON from Dirty Responses

## Theory

LLMs don't always return pure JSON, even when you explicitly ask for it. They're trained on natural text, and it shows — they love wrapping structured output in explanations and markdown:

~~~
Here is the result:
```json
{"name": "codam", "score": 42}
```
Hope this helps!
~~~

Call `json.loads()` on that **entire string** and it fails immediately — `json.decoder.JSONDecodeError`, because the parser hits `Here is the result:` before it ever sees a `{`.

### Why it happens

- Models are trained on natural text, not JSON files — "helpful assistant" behavior leaks in even when you don't want it.
- Even with an instruction like *"respond only in JSON"*, they'll sometimes still wrap the answer in a ` ```json ` fence out of habit.
- The fence itself is a UX nicety for a human reading a chat window — and an obstacle for anything trying to parse the output programmatically.

### Defensive parsing strategies

1. **Find delimiters** — extract between ` ```json ` and the closing ` ``` `, or fall back to the first `{` and the last `}` in the text.
2. **Regex** for known wrapping patterns.
3. **JSON mode / structured output** from the API, when the provider supports it — this prevents the problem at the source instead of patching around it.
4. **Retry with correction** — if parsing fails, send the broken output back to the model and ask it to fix the JSON.

### Why this is a production concern, not just a course exercise

Whenever an agent needs to hand structured data to code — tool call arguments, extracted entities, filters for a database query — defensive parsing like this is mandatory. It's one of the most common places a working prototype breaks the first time it meets real, messy model output.

---

## Assignment

1. Ask the model (user prompt): `"Return JSON in markdown"`
2. From the raw response text, **extract** the JSON that's embedded inside the markdown code block.
3. Parse it and print exactly two lines:

```
PARSED:name=codam
PARSED:score=42
```

## Files to modify

- `python/main.py` — implement `chat_completion` (reuse from `04`) and `extract_json_block(text)`

## Verify

```bash
codam-labs --mock verify 10_dirty_json
```

## Troubleshooting

- **Calling `json.loads()` on the full response** — the text includes `"Here is the result:"` and the ` ```json ` fence itself; none of that is valid JSON on its own. You must extract the `{...}` substring first, *then* parse it.
- **Greedy regex spanning too much (or too little)** — a pattern like `` r"```(?:json)?\s*(\{.*\})\s*```" `` without `re.DOTALL` won't match across newlines at all; with `.* ` (greedy) instead of `.*?` (non-greedy) plus `re.DOTALL`, a response with multiple code blocks could capture from the first `{` to the *last* `}`, swallowing unrelated text in between. Use `re.DOTALL` and a non-greedy `.*?`.
- **Assuming there's always a ` ```json ` fence** — some responses use a plain ` ``` ` fence with no language tag, or no fence at all. Fall back to "first `{`, last `}` in the whole text" when the regex doesn't match, rather than crashing.
- **String-hacking the response instead of extracting it properly** — replacing quote characters or manually trimming characters off the ends might happen to work for this one mock response, but breaks the moment the model phrases things slightly differently. Extract the JSON block cleanly, then let `json.loads` do the actual parsing.
- **`KeyError` on `'name'` or `'score'`** — if your extraction grabbed the wrong substring (e.g. including the fence itself, or an incomplete object), `json.loads` might raise, or succeed on the wrong dict shape entirely. Print the extracted string while debugging to see exactly what you're handing to `json.loads`.

## Docs & further reading

- [Python docs — `json` module](https://docs.python.org/3/library/json.html)
- [Python docs — `re` module, `DOTALL` flag](https://docs.python.org/3/library/re.html#re.DOTALL)
- [Mistral — JSON mode / structured outputs](https://docs.mistral.ai/capabilities/structured-output/json_mode/) (the production-grade alternative to regex-extraction)
