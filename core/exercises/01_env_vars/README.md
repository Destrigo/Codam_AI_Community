# 01 — Environment Variables

## Theory

**Environment variables** are key-value pairs that the operating system (or parent process) hands to your program at startup. They live *outside* your source code — nobody can `git clone` your API key by accident if it never appears in a file.

### Why they matter in AI work specifically

- **API keys** (`MISTRAL_API_KEY`, `ANTHROPIC_API_KEY`, …) must never be committed to a repo. Every exercise from `04` onward reads `MISTRAL_API_KEY` this way.
- **Configurable endpoints** (`MISTRAL_API_BASE`) let the *same* code point at Mistral's cloud, an Azure deployment, a local Ollama server, or `codam-labs`'s offline mock — without touching a line of code.
- **12-Factor App**: config that changes between environments (dev / staging / prod / CI) belongs in the environment, not hardcoded in files.

### Setting a variable, per shell

```bash
export APP_NAME=codam-ai-labs   # bash / zsh (Linux, macOS)
set APP_NAME=codam-ai-labs      # Windows CMD
$env:APP_NAME="codam-ai-labs"   # Windows PowerShell
```

Your program reads it back with `os.environ` (Python) or `std::getenv` (C++). It has no idea *how* the variable got there — export, `.env` file, CI secret, Docker `-e` flag, it's all the same by the time your process starts.

### The "missing" case is not an edge case, it's the point

A robust program never assumes a variable exists. `os.environ["KEY"]` raises `KeyError` and crashes; `os.environ.get("KEY")` returns `None` and lets you decide what happens next. This exercise forces you to handle both branches explicitly.

### Best practices

1. Ship a `.env.example` with placeholder values, never real secrets.
2. Add `.env` to `.gitignore` (already done in this repo).
3. If a required variable is missing, fail with a clear message instead of a cryptic stack trace.

---

## Assignment

Read the environment variable `APP_NAME` and print exactly one line:

- If it is set: `APP_NAME=<value>` (e.g. `APP_NAME=codam-ai-labs`)
- If it is missing: `APP_NAME=MISSING`

`codam-labs verify` sets `APP_NAME=codam-ai-labs` for you before running your code — you don't need to export anything yourself to pass verify. If you want to test the "missing" branch manually, run your script directly (without going through `codam-labs run`) in a shell where `APP_NAME` was never set.

## Files to modify

- `python/main.py` — implement `main()` using `os.environ`
- `cpp/main.cpp` — implement using `std::getenv`

## Verify

```bash
codam-labs verify 01_env_vars
```

No `--mock` needed — this exercise never touches the network. Expected stdout contains:

```
APP_NAME=codam-ai-labs
```

## Troubleshooting

- **`KeyError: 'APP_NAME'` crash** — you used `os.environ["APP_NAME"]` directly instead of `.get()`. The bracket form raises when the key is absent; `.get()` returns `None` so you can print `MISSING`.
- **Verify passes even though your "missing" logic is untested** — `codam-labs verify` always injects `APP_NAME`, so a bug in your `MISSING` branch won't show up there. Test it manually by running the script in a fresh shell with the variable unset.
- **Silently masking the missing case** — `os.environ.get("APP_NAME", "codam-ai-labs")` supplies a *default*, which means your program can never actually print `APP_NAME=MISSING`. Use `os.environ.get("APP_NAME")` (no default, returns `None`) and branch on that.
- **Extra whitespace or f-string typo** — `print(f"APP_NAME= {value}")` (stray space after `=`) or `print("APP_NAME:" + value)` won't match the expected substring check. Match the format exactly: `APP_NAME=<value>`.
- **C++: dereferencing a null pointer** — `std::getenv` returns `nullptr` when the variable is absent. Constructing a `std::string` directly from that pointer is undefined behavior; check for `nullptr` first.

## Docs & further reading

- [The Twelve-Factor App — Config](https://12factor.net/config)
- [Python docs — `os.environ`](https://docs.python.org/3/library/os.html#os.environ)
- [cppreference — `std::getenv`](https://en.cppreference.com/w/cpp/utility/program/getenv)
