# Chain-of-Thought Prompting

## Theory

LLMs generate tokens left to right, one at a time, without an internal scratchpad — unless you give them one in the output itself. For arithmetic, logic, and multi-step reasoning, asking the model to "show its work" before giving a final answer measurably improves accuracy, because each intermediate step becomes context that constrains the next token.

```text
Without CoT:  "What is 17 * 24?"          -> model may just guess a number
With CoT:     "What is 17 * 24? Think step by step."
              -> "17 * 24 = 17 * 20 + 17 * 4 = 340 + 68 = 408"
```

The phrase "think step by step" (or "let's work through this") is a lightweight trigger for this behavior — it costs nothing extra to add and often turns a wrong one-shot guess into a correct, auditable derivation. It's most valuable for:

- Arithmetic and multi-step word problems.
- Logic puzzles with several dependent constraints.
- Any task where an intermediate mistake would otherwise be invisible.

It's less useful (and wastes tokens) for simple factual lookups or single-step classification.

## Assignment

Implement `cot(question)`:

- The prompt sent to the model must include the phrase `think step by step` (case doesn't need to match exactly, but the words must appear).
- Print the response.

Expected stdout (mock mode) contains:

```text
COT_OK
```

## Files to modify

- `python/main.py` — implement `cot(question: str) -> str`, appending the CoT trigger phrase to the question.
- `cpp/main.cpp` — build the equivalent prompt.

## Verify

```bash
codam-labs --mock verify prompt_engineering/04_chain_of_thought
```

## Troubleshooting

- **Trigger phrase placed oddly**: `"Think step by step. What is 2+2?"` and `"What is 2+2? Think step by step."` both work — the check just scans the full prompt string, not position. But make sure the phrase isn't split across two separate API calls (it must be in the single message you send).
- **Typo in the phrase**: "step-by-step" (hyphenated) or "thinking step by step" may not match a strict substring check depending on the grader — stick to the literal wording `think step by step` to be safe.
- **Confusing this with the model's actual reasoning**: this exercise checks that you *asked* for step-by-step reasoning, not that the response contains visible steps — in mock mode the response is canned regardless of how well the real model would reason.

## Docs

- [Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"](https://arxiv.org/abs/2201.11903) — the original CoT paper
- [Prompting Guide — Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
- [Mistral prompting capabilities guide](https://docs.mistral.ai/guides/prompting_capabilities/)
