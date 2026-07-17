# Classification with a Constrained Label Set

## Theory

Open-ended generation is the wrong tool when you need a decision your code can branch on. If you ask "what kind of issue is this?" you might get *"This appears to be a software defect related to a crash"* — technically correct, but your `if` statement can't switch on a paragraph. Classification tasks need the model constrained to a **fixed, known set of labels**.

```text
Prompt:  "classify category (one of: bug, feature, question): app crashes on launch"
Response: "bug"
```

Naming the exact allowed set inside the prompt (`bug`, `feature`, `question`) sharply reduces the chance of the model inventing a near-miss label like `"defect"` or `"issue"` that your code doesn't recognize. This is the prompting-only version of classification; stricter systems constrain it further with `response_format` JSON schemas or logit-biasing so the label set is *enforced*, not just *requested* — but naming the categories explicitly is the first and cheapest step.

## Assignment

Send a prompt containing `classify category` for the input `app crashes`.

- Print the response.

Expected stdout (mock mode) contains:

```text
CLASS:bug
```

## Files to modify

- `python/main.py` — build a message containing `classify category` and the text to classify, send it, print the response.
- `cpp/main.cpp` — build the equivalent request/print logic.

## Verify

```bash
codam-labs --mock verify structured_output/04_classify
```

## Troubleshooting

- **Missing the trigger phrase**: the mock grader matches on the literal substring `classify category` appearing in your prompt — `"categorize this"` or `"what category"` won't trigger the expected mock response.
- **Not including the item to classify**: the prompt needs both the instruction (`classify category`) and the actual text being classified (`app crashes`) in the same message — omitting the input text means there's nothing to classify.
- **Expecting the *content* to determine the label**: in mock mode, the response is canned based on matching the trigger phrase, not on genuine reasoning about "app crashes" being a bug — don't overthink swapping in different example text, it won't change the mock's canned label.
- **Printing before receiving the response**: make sure the print statement is after the request completes and reads the parsed `message.content`, not the raw HTTP response object.

## Docs

- [Mistral API — Chat Completions](https://docs.mistral.ai/api/#tag/chat)
- [Mistral structured outputs / constrained generation](https://docs.mistral.ai/capabilities/structured-output/)
- [Prompting Guide — Classification](https://www.promptingguide.ai/applications/classification) — patterns for reliable label-set classification
