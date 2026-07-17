# Eval Set

## Theory
Once a prompt is in production, every "small tweak" is a risk: it might fix the case you were
looking at while quietly breaking three others. An eval set is a fixed collection of gold
question/expected-answer (or expected-property) pairs that you re-run after every prompt change,
so regressions show up as a number dropping instead of a support ticket three weeks later.

**Worked example — a policy-Q&A bot's eval set:**

| # | Question | Expected property | Pass? |
|---|----------|--------------------|-------|
| 1 | "What's the refund window?" | mentions "30 days" | ✅ |
| 2 | "Do you ship internationally?" | mentions "yes" or a country list | ✅ |
| 3 | "What's your refund window?" (typo variant) | mentions "30 days" | ✅ |
| 4 | "Can I cancel anytime?" | mentions "cancel" | ✅ |
| 5 | "What's the CEO's phone number?" | refuses / says it doesn't know | ❌ (regression: leaked a guess) |

4 out of 5 passing (`EVAL:4/5`) is a **signal to investigate**, not a rounding error — every
failing case should map to a specific, nameable bug.

## Assignment
Given `gold = [True, True, True, True, False]`, count passing checks and print `EVAL:4/5`.

## Files
- `python/main.py` — stub with `gold` predefined.
- `hint.md` — `Count passing assertions`.
- `solution/python/main.py` — reference: `sum(gold)` over the boolean list.

## Verify
```bash
codam-labs --mock verify advanced_patterns/05_eval_set
```
Expected stdout: `EVAL:4/5`.

## Troubleshooting
- **Off-by-one in the ratio** — the denominator is the *total number of cases* (5), not the number
  of passes; `EVAL:4/4` (dropping the failing case from the denominator) hides the regression
  instead of reporting it.
- **Boolean vs truthy confusion** — `sum(gold)` works because `True == 1` in Python; if your gold
  list ever contains non-bool "pass" markers (e.g. strings), `sum()` will raise instead of count.
- **Eval set too small to mean anything** — 5 cases is illustrative; a real eval set for a
  production prompt needs enough cases per behavior (edge cases, adversarial inputs, common
  paths) that a 1-case flip is statistically meaningful, not noise.
- **Not versioning the eval set with the prompt** — if you change the prompt and the eval set in
  the same commit without separating them, you can't tell whether a score change came from the
  prompt or from quietly relaxed gold answers.

## Docs
- [OpenAI Evals framework](https://github.com/openai/evals) — a real open-source eval harness with the same core idea.
- [promptfoo docs](https://www.promptfoo.dev/docs/intro/) — eval-set tooling built specifically for prompt regression testing.
