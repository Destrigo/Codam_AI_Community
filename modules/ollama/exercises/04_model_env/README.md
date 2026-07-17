# Ollama Model From Env

## Theory

In production you rarely hardcode the model name inside source. Operators change
`llama3.2` → `mistral` (or a fine-tune) without a redeploy by setting an environment
variable. This exercise is intentionally **offline**: no HTTP, no Ollama daemon — only
`os.environ.get` / `std::getenv`, the same pattern as `core/01_env_vars` but for model
selection.

Note the name carefully: the variable is **`OLLAMA_MODEL`**, not `CODAM_LABS_OLLAMA_BASE`
(that one is the daemon URL used by 01/02/03/05/06). Two different concerns, two different
names.

## Assignment

Read `OLLAMA_MODEL` from the environment. If it is unset, default to `llama3.2`.
Print exactly:

```text
MODEL_OK:<model-name>
```

## Files to modify

- `python/main.py`
- `cpp/main.cpp`

## Verify

```bash
codam-labs --mock verify ollama/04_model_env
```

Expected: `MODEL_OK:llama3.2` (verify sets / defaults that value).

## Troubleshooting

- **`MODEL_OK:` with nothing after the colon** — you printed `None`/empty because you used
  `os.environ["OLLAMA_MODEL"]` and the key was missing, or you forgot the default second
  argument to `.get`. Use `os.environ.get("OLLAMA_MODEL", "llama3.2")`.
- **Changing `OLLAMA_MODEL` does not change exercises 03/05** — those solutions hardcode
  `"llama3.2"` on purpose so *this* exercise has a unique lesson. That is not a bug in 04.
- **You added an HTTP call "just in case"** — not required here. Extra network code makes
  live runs fail with `ConnectionRefusedError` even though the assignment never asked for it.
- **Wrong env name `CODAM_LABS_OLLAMA_MODEL`** — that variable does not exist in this repo.
  The check looks for the printed `MODEL_OK:` line, but your mental model will be wrong for
  later live Ollama work if you invent prefixes.

## Docs

- [Python `os.environ`](https://docs.python.org/3/library/os.html#os.environ)
- [Ollama — modelfile / model names](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
  (useful once you move past the default `llama3.2` string)
