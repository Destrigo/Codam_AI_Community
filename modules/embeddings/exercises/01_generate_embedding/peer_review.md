# Peer Review — Generate Embedding

Use this checklist **instead of reading `solution/`**. Pair with a classmate.

## Before review
- [ ] Your code runs: `codam-labs run 01_generate_embedding --lang python`
- [ ] You tried `codam-labs hint` (not `--solution`)
- [ ] Submit: `codam-labs review submit 01_generate_embedding --lang python`

## Reviewer checklist
- [ ] Code runs without errors on reviewer's machine
- [ ] Output matches the assignment in README.md
- [ ] No API keys hardcoded in source files
- [ ] Error handling present where required
- [ ] Code is readable (names, structure, no dead code)
- [ ] LLM calls use `MISTRAL_API_KEY` from environment

## Questions for the author
1. What was the hardest part?
2. What would you improve with more time?

## Approve
When all boxes are checked:
```bash
codam-labs review approve 01_generate_embedding --lang python --reviewer YOUR_NAME
```

This marks the exercise complete (alternative to `codam-labs verify`).
