# Peer Review — Clear vs Ambiguous Prompt

Use this checklist **instead of reading `solution/`**. Pair with a classmate.

## Before review
- [ ] Your code runs: `codamlings run 01_clear_vs_ambiguous --lang python`
- [ ] You tried `codamlings hint` (not `--solution`)
- [ ] Submit: `codamlings review submit 01_clear_vs_ambiguous --lang python`

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
codamlings review approve 01_clear_vs_ambiguous --lang python --reviewer YOUR_NAME
```

This marks the exercise complete (alternative to `codamlings verify`).
