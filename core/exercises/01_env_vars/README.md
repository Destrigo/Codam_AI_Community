# 01 — Environment Variables

## Theory

**Environment variables** are key-value pairs that the operating system (or parent process) passes to your program at startup. They do not live in the source code: they live *outside* the application.

### Why they matter in AI

- **API keys** (`MISTRAL_API_KEY`, `ANTHROPIC_API_KEY`) must never be committed to the repo
- **Configurable endpoints** (`MISTRAL_API_BASE`) let you point to Mistral, Azure, Ollama, local mocks
- **12-Factor App**: config that changes between environments (dev/staging/prod) belongs in the environment, not in files

### How it works

```bash
export APP_NAME=codamlings   # Linux/macOS
set APP_NAME=codamlings      # Windows CMD
$env:APP_NAME="codamlings"   # PowerShell
```

The program reads them with `os.environ` (Python) or `std::getenv` (C++).

### Best practices

1. Provide a `.env.example` with *empty* keys or placeholders
2. Add `.env` to `.gitignore`
3. If a required variable is missing, print a clear message and exit

---

## Assignment

Read the environment variable `APP_NAME`.

- If it is set, print: `APP_NAME=<value>`
- If it is missing, print: `APP_NAME=MISSING`

The verify command sets `APP_NAME=codamlings` automatically.

## Files to modify

- `python/main.py`
- `cpp/main.cpp`

## Verify

```bash
codamlings verify 01_env_vars
```
