# Hint — 02_http_get

**Python**
1. `urllib.request.urlopen(url)` opens the connection
2. `json.loads(response.read())` parses the body
3. Access with `data["title"]`

**C++**
1. `curl_easy_init()` / `curl_easy_perform()`
2. `CURLOPT_WRITEFUNCTION` callback to accumulate the response in a string
3. `nlohmann::json::parse(body)["title"]`
