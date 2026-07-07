# 10 — Extracting JSON from Dirty Responses

## Theory

LLMs do not always return pure JSON. They often add surrounding text:

~~~
Here is the result:
```json
{"name": "codam", "score": 42}
```
Hope this helps!
~~~

If you call `json.loads()` on the entire string, it **fails**.

### Why it happens

- Models are trained on natural text, not just JSON
- Even with "respond only in JSON", they sometimes add markdown
- ```json fences are useful for humans, problematic for parsers

### Defensive parsing strategies

1. **Find delimiters**: extract between `{` and `}` or between ` ```json ` and ` ``` `
2. **Regex** for known patterns
3. **JSON mode** / **structured output** from the API (when available) — prevents the problem at the source
4. **Retry with correction**: if parsing fails, ask the model to fix it

### For RAG and agents

When an agent must pass structured data to code (tool args, filters, entities), defensive parsing is **mandatory**. It is one of the places where prototypes break in production.

---

## Assignment

1. Ask the LLM (user prompt): `"Return JSON in markdown"`
2. From the response, **extract** the JSON from the markdown block
3. Parse it and print two lines:
   - `PARSED:name=codam`
   - `PARSED:score=42`

## Verify

```bash
codamlings verify 10_dirty_json
```
