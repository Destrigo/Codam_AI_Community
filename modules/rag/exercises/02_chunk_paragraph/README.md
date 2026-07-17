# Paragraph Chunking

## Theory

Fixed-size chunking (previous exercise) is blind to structure — it will happily cut a
sentence in half. **Paragraph chunking** respects an author's own boundaries: split on
blank lines (`\n\n`) so each chunk stays a coherent unit of meaning instead of an
arbitrary character window. This is a form of *semantic chunking* — trading a little
consistency in chunk size for much better retrieval quality, since a retrieved chunk is
more likely to contain a complete thought rather than half of one plus half of the next.

## Assignment

Given the two-paragraph string:

```
para one

para two
```

split it on the blank line separator and print the number of resulting chunks.

**Expected output:**

```
CHUNKS:2
```

## Files to modify

- `python/main.py` — Python track
- `cpp/main.cpp` — C++ track

## Verify

```bash
codam-labs --mock verify rag/02_chunk_paragraph
```

No LLM call is involved, so `--mock` and live mode produce the same result — run with
`--mock` for a fast, offline check.

## Troubleshooting

- **Getting `CHUNKS:1`?** You probably split on a single `\n` instead of the double
  newline `\n\n` that actually separates paragraphs, so the whole string stayed intact
  and `.split()` found nothing to break on.
- **Getting more chunks than expected on real text?** Files with trailing blank lines
  or `\r\n` line endings can produce empty-string chunks after `.split("\n\n")` —
  filter out `""` entries (e.g. `[c for c in chunks if c.strip()]`) before counting.
- **Windows-edited text files:** if you paste this exercise's example into a file saved
  with CRLF endings, `\n\n` won't match `\r\n\r\n`. Normalize with
  `text.replace("\r\n", "\n")` first if you extend this beyond the hardcoded example.

## Further reading

- [LangChain — Split by character (text splitters)](https://python.langchain.com/docs/how_to/character_text_splitter/)
- [LlamaIndex — Node Parsers & chunking](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/)
