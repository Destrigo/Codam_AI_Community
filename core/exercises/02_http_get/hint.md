# Hint — 02_http_get

**URL**

```python
url = os.environ.get(
    "CODAM_LABS_TODO_URL",
    "https://jsonplaceholder.typicode.com/todos/1",
)
```

Prefer `codam-labs --mock verify 02_http_get` so you do not depend on typicode.

**Python**
1. `urllib.request.urlopen(url)` opens the connection
2. `json.loads(response.read())` parses the body
3. Access with `data["title"]`

**C++**
1. Read `CODAM_LABS_TODO_URL` (or the typicode fallback)
2. GET, parse JSON, print `title`
