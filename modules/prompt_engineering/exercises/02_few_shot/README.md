# Few-Shot Prompting

## Theory

Zero-shot prompting asks the model to do a task cold. Few-shot prompting shows it 2-3 worked examples first, then asks it to continue the pattern. The model doesn't "learn" in the training sense — it's pattern-matching within the context window — but this dramatically improves consistency for tasks with a specific output style or edge cases that are hard to describe in words.

```text
Example 1: "This is amazing!" -> positive
Example 2: "Worst purchase ever." -> negative
Classify: "It's okay, does the job."
```

Notice the examples establish both the **input format** and the **output format** (a lowercase single word after `->`). The model imitates that shape rather than inventing its own. Few-shot is most valuable when:

- The desired output format is unusual (custom labels, specific punctuation, terse answers).
- The task has tricky edge cases better shown than explained.
- Zero-shot attempts have been inconsistent across similar inputs.

The tradeoff is prompt length — each example costs tokens, so keep them short and representative.

## Assignment

Build a prompt that demonstrates the few-shot pattern before asking the real question:

- The user message sent to the model must literally contain the substrings `Example 1:` and `Example 2:`.
- Both examples must appear **before** the real classification request in the message.
- Print the assistant's response to stdout.

Expected stdout (mock mode) contains:

```text
FEW_SHOT_OK
```

## Files to modify

- `python/main.py` — build the multi-line prompt string with two examples, then send it.
- `cpp/main.cpp` — construct the equivalent prompt and request.

## Verify

```bash
codam-labs --mock verify prompt_engineering/02_few_shot
```

## Troubleshooting

- **Wrong label casing**: the grader checks the literal strings `Example 1:` and `Example 2:` (capital E, colon, no extra space) — `example 1` or `Example1:` won't match.
- **Examples after the question**: some students append examples as an afterthought at the end. The technique only works if the examples come *before* the item you want classified, so the model has already seen the pattern by the time it reaches your real question.
- **Too many examples**: this exercise only requires two — adding a third isn't wrong, but don't accidentally omit `Example 1:` while renumbering.
- **Using `\n` incorrectly in f-strings**: if you build the prompt with string concatenation, double-check there's an actual newline character between examples, not a literal `\n` inside single quotes without an `f` or raw prefix mismatch.

## Docs

- [Mistral prompting capabilities — few-shot section](https://docs.mistral.ai/guides/prompting_capabilities/)
- [Brown et al., "Language Models are Few-Shot Learners" (GPT-3 paper)](https://arxiv.org/abs/2005.14165) — the paper that coined the term
- [Prompting Guide — Few-Shot Prompting](https://www.promptingguide.ai/techniques/fewshot)
