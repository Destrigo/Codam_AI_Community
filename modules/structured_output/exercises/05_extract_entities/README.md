# Entity Extraction

## Theory

Entity extraction pulls specific, named pieces of information (people, dates, places, amounts) out of free text — turning *"Marco signed on Monday"* into structured facts your code can use: `name = Marco`, `day = Monday`. This is one of the oldest NLP tasks, traditionally done with dedicated NER (Named Entity Recognition) models; LLMs now do it competitively just by being asked, with the huge advantage of understanding *context* and *instructions* rather than only recognizing entity types they were explicitly trained on.

```text
Prompt:   "extract entities from: Marco signed on Monday.
            Respond as key=value pairs, one per line."
Response: "name=Marco
            day=Monday"
```

The `key=value` output convention (rather than free prose) is what makes the extraction *usable* — your code can split on `=` and `\n` to build a dict, instead of regex-hunting through a sentence. This is a lighter-weight cousin of full JSON extraction (see `structured_output/01_extract_json`): appropriate when you only need a handful of flat fields and don't want the overhead of a JSON schema.

## Assignment

Send a prompt containing `extract entities` for the input `Marco signed on Monday`.

- Print the response.

Expected stdout (mock mode) contains:

```text
ENTITY:name=Marco
```

## Files to modify

- `python/main.py` — build a message containing `extract entities` and the source sentence, send it, print the response.
- `cpp/main.cpp` — build the equivalent request/print logic.

## Verify

```bash
codam-labs --mock verify structured_output/05_extract_entities
```

## Troubleshooting

- **Missing the trigger phrase**: the mock server matches on `extract entities` appearing in the prompt content — rewording it to `"pull out the entities"` won't trigger the canned `ENTITY:name=Marco` response.
- **Omitting the source sentence**: the prompt needs the actual text `Marco signed on Monday` (or equivalent per the mock's expectations) — sending only the instruction with no source text to extract from doesn't make sense and may not match the mock.
- **Expecting multiple entities in stdout**: the expected check only verifies `ENTITY:name=Marco` is present — if your real prompt also asks for a `day=` field, that's fine and realistic, but don't assume the grader checks for it here.
- **Confusing `key=value` format with JSON**: don't wrap the expected output in `{}` — this exercise's expected format is a plain `key=value` string, not a JSON object (contrast with `01_extract_json`).

## Docs

- [Mistral API — Chat Completions](https://docs.mistral.ai/api/#tag/chat)
- [Wikipedia — Named-entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition) — background on the classical version of this task
- [Prompting Guide — Information Extraction](https://www.promptingguide.ai/applications/) (extraction techniques section)
