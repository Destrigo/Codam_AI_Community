# Codam AI Labs — Student Onboarding Guide

Welcome! **Codam AI Labs** is a hands-on, [Rustlings](https://github.com/rust-lang/rustlings)-style
course to learn how to build real AI/LLM applications in **Python** and **C++**.

You fix small, focused exercises one at a time. Each one teaches a single concept —
from your first HTTP call to full RAG pipelines, agents, MCP, security, and local models.

- **78 exercises** (10 core + 68 across 12 modules)
- **3 capstones** and **3 business cases**
- Every exercise ships with theory, hints, a stub to complete, and a reference solution
- Runs **live** against your own Mistral key by default, or **offline** with `--mock`

---

## 1. Prerequisites

| You want to do | You need |
|----------------|----------|
| Python track (recommended start) | **Python 3.10+** |
| C++ track | **CMake 3.16+** and a C++17 compiler (MSVC on Windows, gcc/clang on macOS/Linux) |
| Live exercises | A personal **Mistral API key** ([console.mistral.ai](https://console.mistral.ai)) |
| The `ollama` module (live) | [Ollama](https://ollama.com/download) installed and running |
| Nothing but the logic | Just use `--mock` — no key, no internet |

No administrator privileges are required. Works on **Windows, macOS, and Linux**.

> Not sure? Start with **Python + `--mock`**. You can add your key and C++ later.

---

## 2. First-time setup

### 2.1 Clone and install

```bash
git clone git@github.com:Destrigo/Codam_AI_Community.git
cd Codam_AI_Community
pip install -e .
```

This installs the `codam-labs` command.

**If `codam-labs` is not found** (common on Windows if the Scripts folder isn't on your PATH),
use the module form everywhere instead:

```bash
python -m codam_ai_labs list
```

Everywhere this guide says `codam-labs ...`, `python -m codam_ai_labs ...` works too.

### 2.2 Configure your key (one `.env` for everything)

Copy the template and edit it:

```bash
cp .env.example .env
```

Open `.env` and set **your own** key:

```bash
MISTRAL_API_KEY=your-personal-key-here
MISTRAL_API_BASE=https://api.mistral.ai/v1
MISTRAL_MODEL=mistral-small-latest

APP_NAME=codam-ai-labs

# Only needed for the ollama module (local, no cloud key):
OLLAMA_BASE=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**Rules of the game:**
- There is **one `.env`** at the repo root — it powers every exercise.
- **Each student uses their own key.** Never share keys, never commit `.env` (it's git-ignored).
- If you don't have a key yet, you can still do most of the course with `--mock`.

### 2.3 Smoke test

```bash
codam-labs verify 01_env_vars --mock
```

You should see `PASS 01_env_vars`. If so, you're ready.

---

## 3. Your daily loop

The core workflow is: **see the task → edit code → verify → repeat.**

```bash
codam-labs                 # shows your next incomplete exercise + its README
codam-labs list            # your progress across everything
codam-labs run <slug>      # run your current code and see the output
codam-labs verify <slug>   # check your output against the exercise rubric
```

The fastest way to work is **watch mode** — it re-runs verify every time you save:

```bash
codam-labs watch
```

Leave it running in one terminal, edit `python/main.py` in your editor, and watch it
turn green when you get it right. When it passes, it automatically moves to the next one.

### Where do I write my code?

Each exercise is a folder like `core/exercises/01_env_vars/`:

```
01_env_vars/
├── README.md          ← theory + assignment (read this first)
├── hint.md            ← progressive hints
├── peer_review.md     ← checklist for peer review
├── python/main.py     ← YOU edit this (Python track)
├── cpp/main.cpp       ← YOU edit this (C++ track)
└── solution/          ← reference (try NOT to peek)
```

You only edit the file under `python/` or `cpp/`. Leave `solution/` alone until you're done.

---

## 4. Live vs mock — what's the difference?

| | Live (default) | `--mock` |
|---|----------------|----------|
| Command | `codam-labs verify 04_llm_first_call` | `codam-labs verify 04_llm_first_call --mock` |
| Uses | Your real Mistral/Ollama | A local fake server on `127.0.0.1` |
| Needs a key? | Yes | No |
| Needs internet? | Yes | No |
| Model replies | Real, varied | Fixed, deterministic |
| Good for | Learning how models really behave | Testing your code logic offline / on a plane / no key |

**Use live** to see real model behavior. **Use `--mock`** when you have no key/network,
or to quickly check that your HTTP calls and parsing are correct.

Some exercises never call an API at all (regex, sanitization, chunking) — they behave the
same in both modes.

---

## 5. Getting unstuck (in order)

1. **Re-read the `README.md`** of the exercise — the exact expected output is described there.
2. **Read the hint:**
   ```bash
   codam-labs hint <slug>
   ```
   This shows `hint.md` and the peer-review checklist — not the solution.
3. **Check the actual vs expected output.** `verify` tells you what string it was looking for.
4. **Ask a classmate** and do a peer review (see below).
5. **Last resort — the solution:**
   ```bash
   codam-labs hint <slug> --solution
   ```
   Use this sparingly. You learn far more by struggling a little first.

---

## 6. Marking an exercise done

There are **two** ways to complete an exercise:

**A) Automated verify** — your output matches the rubric:
```bash
codam-labs verify <slug>
```

**B) Peer review** — a classmate checks your work:
```bash
codam-labs review submit <slug> --author YOUR_NAME     # you submit
codam-labs review rubric <slug>                        # reviewer reads the checklist
codam-labs review approve <slug> --reviewer PEER_NAME  # reviewer approves
```

Peer review is a real skill — treat the checklist seriously (code runs, output correct,
no hardcoded keys, readable code).

---

## 7. Choosing a language

Add `--lang cpp` to any command to work in C++ instead of Python:

```bash
codam-labs run <slug> --lang cpp
codam-labs verify <slug> --lang cpp
codam-labs watch --lang cpp
```

Both tracks share the exact same READMEs, checks, and mock/live behavior. The C++ track
uses CMake and header-only dependencies (downloaded automatically on first build).

---

## 8. Suggested learning path

```
core (10)
  → prompt_engineering (6) → structured_output (5)
  → embeddings (5) → rag (7)
  → tools (6) → agents (6) → mcp (6)
  → local_llm (4) → ollama (6)
  → production (6) → security (6) | advanced_patterns (5)
  → capstones (3) → business_cases (3)
```

- Do **`core/` first** — everything builds on it.
- After core, modules are **stand-alone** — pick what interests you.
- `local_llm`/`ollama`, `production`/`security`, and `advanced_patterns` are parallel tracks.
- Save **capstones** and **business cases** for after you've finished the relevant modules.

Browse modules any time:

```bash
codam-labs list --module all
codam-labs list --module rag
```

---

## 9. The `ollama` module (optional, fully local)

This module runs open models **on your own machine** — no cloud, no key.

```bash
# 1. Install Ollama: https://ollama.com/download
# 2. Start the daemon:
ollama serve
# 3. Pull the models used by the exercises:
ollama pull llama3.2
ollama pull nomic-embed-text   # only for the embeddings exercise
```

Then:

```bash
codam-labs verify all --module ollama          # live, against your local Ollama
codam-labs verify all --module ollama --mock   # offline, no Ollama needed
```

---

## 10. Capstones & business cases

Once you've cleared the relevant modules:

```bash
codam-labs capstone list
codam-labs capstone run <name> -- <args>       # e.g. the RAG assistant, ops agent, gateway

codam-labs business list
codam-labs business run <name>                 # workshop-style ingestion pipelines
```

These are larger, integrated projects (mini-RAG, mini-agent, LLM gateway, and real-world
data-ingestion scenarios). Reference solutions are provided in Python.

---

## 11. Command cheat sheet

| Command | What it does |
|---------|--------------|
| `codam-labs` | Show next incomplete exercise + README |
| `codam-labs list` | Progress overview |
| `codam-labs list --module <name>` | List a module's exercises |
| `codam-labs run <slug>` | Run your code |
| `codam-labs verify <slug>` | Verify against rubric (live) |
| `codam-labs verify <slug> --mock` | Verify offline |
| `codam-labs verify all --module <name>` | Verify a whole module |
| `codam-labs watch` | Re-verify on every save |
| `codam-labs hint <slug>` | Show hints + peer-review checklist |
| `codam-labs hint <slug> --solution` | Show the reference solution |
| `codam-labs review submit/rubric/approve <slug>` | Peer-review workflow |
| `codam-labs capstone list / run` | Capstone projects |
| `codam-labs business list / run` | Business-case pipelines |
| `--lang cpp` | Switch any command to the C++ track |
| `--mock` | Run offline against the local mock server |

---

## 12. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `codam-labs: command not found` | Use `python -m codam_ai_labs ...`, or add your Python Scripts dir to PATH |
| `MISTRAL_API_KEY is required` | Set your key in `.env`, or add `--mock` to run offline |
| Live verify fails but `--mock` passes | Network/firewall/proxy issue, or invalid key — check connectivity first |
| C++ build fails: `cmake not found` | Install CMake 3.16+ and a C++17 compiler |
| First C++ build is slow | It's downloading header-only deps once; later builds are fast |
| Ollama exercise fails (live) | Make sure `ollama serve` is running and the model is pulled, or use `--mock` |
| Verify says "missing expected output" | Re-read the README — it lists the exact string your program must print |

---

## 13. Golden rules

1. **One `.env`, your own key, never committed.**
2. **Read the README first**, then code, then verify.
3. **Struggle a bit before looking at `--solution`.**
4. **Use `--mock` freely** when you have no key or network.
5. **Peer review** is part of the learning — give and receive it honestly.

Have fun, and ship something real. 🚀
