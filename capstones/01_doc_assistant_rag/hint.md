# Hints — Capstone 01 Doc Assistant

Reveal one at a time.

## Milestone 1
<details>
<summary>Hint 1.1 — Walking files</summary>

Use `pathlib.Path(docs).rglob("*")` and filter `.suffix in {".md", ".txt"}`.
</details>

<details>
<summary>Hint 1.2 — Chunk IDs</summary>

Use `f"{path.stem}#{i}"` so citations are human-readable.
</details>

## Milestone 2
<details>
<summary>Hint 2.1 — Persist index</summary>

```json
{"chunks": [{"id": "hr_remote_policy#0", "text": "...", "embedding": [...]}]}
```
</details>

## Milestone 3
<details>
<summary>Hint 3.1 — Cosine similarity</summary>

Reuse `embeddings/02_cosine_similarity` logic. Embed the question, compare to all chunk vectors.
</details>

## Milestone 4
<details>
<summary>Hint 4.1 — Prompt template</summary>

```
System: Answer only using the context below. Cite chunk IDs in CITED line.
Context:
[chunk_id] text
...
User: {question}
```
</details>

## Milestone 5
<details>
<summary>Hint 5.1 — Low confidence</summary>

If `max(similarity scores) < 0.5`, skip LLM call and return refusal template.
</details>
