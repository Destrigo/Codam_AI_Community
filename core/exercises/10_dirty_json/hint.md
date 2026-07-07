# Hint — 10_dirty_json

1. Call `chat_completion` with user `"Return JSON in markdown"`
2. Look for ` ```json ` in the response (or generic ` ``` `)
3. Extract the text between the fences
4. `json.loads()` on the extracted text
5. Print `PARSED:name=...` and `PARSED:score=...`

Alternative without markdown fence: find the first `{` and the last `}`.
