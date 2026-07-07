# Hint — 03_http_post

**Python**
1. `json.dumps({"name": "codam"}).encode()` for the body
2. `urllib.request.Request(url, data=body, method="POST")`
3. `request.add_header("Content-Type", "application/json")`
4. In the response: `data["json"]["name"]`

**C++**
1. `curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str())`
2. Header list: `Content-Type: application/json`
3. Parse the response and read `["json"]["name"]`
