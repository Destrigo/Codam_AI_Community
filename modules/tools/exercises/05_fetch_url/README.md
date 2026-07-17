# Fetch URL Tool

## Theory
Tools can fetch external data the model cannot know.

## Assignment
GET the todo URL and print `FETCH_OK:` + title.

```python
url = os.environ.get(
    "CODAM_LABS_TODO_URL",
    "https://jsonplaceholder.typicode.com/todos/1",
)
```

Expected: `FETCH_OK:delectus aut autem`

## Verify

```bash
codam-labs --mock verify tools/05_fetch_url
```
