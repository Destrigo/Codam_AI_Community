# Hint — 08_streaming

**Python**
1. Add `"stream": true` to the payload
2. `urllib` is not ideal for streaming — use `http.client` or read in chunks with `response`
3. Split by `\n`, ignore empty lines
4. For each line starting with `data: `, if it is not `[DONE]`, parse JSON and read `choices[0].delta.content`

**C++**
1. `CURLOPT_WRITEFUNCTION` will receive multiple chunks
2. Accumulate in a buffer, process complete `data: ...` lines
