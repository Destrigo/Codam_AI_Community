# Self-Consistency

## Theory
A single sample from a model can land on a wrong reasoning path even when the model *can* reach
the right answer. Self-consistency asks the same question multiple times (at nonzero temperature,
so answers can actually differ), then takes the **majority vote** across samples — trading extra
API calls for higher answer reliability.

**Worked example — a word problem sampled 3 times:**

```text
Sample 1 → "42"
Sample 2 → "42"
Sample 3 → "17"   (model took a wrong reasoning path this time)

Votes: {"42": 2, "17": 1}  →  majority = "42", with 2 supporting votes
```

This is the technique from Wang et al.'s *"Self-Consistency Improves Chain of Thought Reasoning"*
(2022) — sample-and-vote instead of trusting one greedy decode.

## Assignment
Given samples `["a", "a", "b"]`, count votes and print `VOTE:2` (the winning answer's vote count).

## Files
- `python/main.py` — stub with `votes = Counter(["a", "a", "b"])` predefined.
- `hint.md` — `Counter most common`.
- `solution/python/main.py` — reference: `Counter.most_common(1)[0][1]`.

## Verify
```bash
codam-labs --mock verify advanced_patterns/03_self_consistency
```
Expected stdout: `VOTE:2`.

## Troubleshooting
- **Printing the wrong tuple element** — `most_common(1)[0]` is `("a", 2)`; the exercise wants the
  **count** (`2`), i.e. index `[1]`, not the answer itself.
- **Temperature 0 defeats the point** — if every sample is generated deterministically, all 3
  samples will be identical and voting adds cost with zero reliability benefit; self-consistency
  needs actual sampling diversity (temperature > 0).
- **Ties** — with an even sample count (e.g. `[a, a, b, b]`), `most_common()` returns *a* winner
  but there's no real majority; decide (and document) a tie-break rule rather than silently
  picking whichever `Counter` happens to order first.
- **Cost blindness** — self-consistency literally multiplies your API cost by the sample count;
  it's a reliability/cost trade, not a free upgrade — reserve it for answers where being wrong is
  expensive.

## Docs
- [Wang et al., 2022 — "Self-Consistency Improves Chain of Thought Reasoning in Language Models"](https://arxiv.org/abs/2203.11171)
- [Python `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
