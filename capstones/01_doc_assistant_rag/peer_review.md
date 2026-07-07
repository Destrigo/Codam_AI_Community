# Peer Review — Capstone 01 Doc Assistant

Pair with a classmate. **Do not share full source** until after review.

## Before review
- [ ] `index` works on provided `data/`
- [ ] `ask` returns ANSWER + CITED + CONFIDENCE
- [ ] `eval` prints at least `EVAL:4/5`
- [ ] No API keys in source or logs

## Reviewer checklist — Milestone coverage
- [ ] Chunking strategy documented in README or code comment
- [ ] Embeddings stored with stable chunk IDs (`filename#chunk_N`)
- [ ] Top-k retrieval uses cosine similarity (not keyword-only)
- [ ] Citations reference real chunk IDs from retrieval
- [ ] Off-topic question returns low confidence / refusal
- [ ] stderr logs redact `sk-` patterns

## Demo script (reviewer runs)
```bash
python python/main.py index --docs ./data
python python/main.py ask --docs ./data --question "How many remote days per week?"
python python/main.py ask --docs ./data --question "What is the CEO salary?"
python python/main.py eval --docs ./data
```

## Questions for the author
1. Why did you choose your chunk size / strategy?
2. What similarity threshold did you pick and why?
3. What would break first with 10,000 documents?

## Approve
Instructor or peer signs off in workshop sheet. Capstone complete when all boxes checked + demo succeeds on reviewer's machine.
