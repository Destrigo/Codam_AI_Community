"""Add Ollama module (6 exercises) with Python solutions."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ROOT / "modules"

CPP_CMAKE = """cmake_minimum_required(VERSION 3.16)
project({project})
include(${{CMAKE_CURRENT_SOURCE_DIR}}/../../../../../shared/cpp/cmake/Exercise.cmake)
add_codam_exercise(main main.cpp)
"""

STUB_CPP = '#include <iostream>\n\nint main() {\n    // TODO: see README.md\n    return 1;\n}\n'

PEER = """# Peer Review — {title}

- [ ] `codamlings run {slug} --lang python`
- [ ] Ollama running locally (`ollama serve`) or use `--mock` for offline verify
- [ ] No API keys in source — configure `OLLAMA_*` in repo root `.env`

## Approve
`codamlings review approve {slug} --lang python --reviewer YOUR_NAME`
"""


def write_ex(module: str, ex_id: str, readme: str, hint: str, sol: str, stub: str) -> None:
    folder = MODULES / module / "exercises" / ex_id
    folder.mkdir(parents=True, exist_ok=True)
    title = readme.splitlines()[0].lstrip("# ").strip()
    (folder / "README.md").write_text(readme.strip() + "\n", encoding="utf-8")
    (folder / "hint.md").write_text(hint.strip() + "\n", encoding="utf-8")
    (folder / "peer_review.md").write_text(
        PEER.format(title=title, slug=f"{module}/{ex_id}"), encoding="utf-8"
    )
    (folder / "python").mkdir(parents=True, exist_ok=True)
    (folder / "python" / "main.py").write_text(stub.strip() + "\n", encoding="utf-8")
    (folder / "solution" / "python").mkdir(parents=True, exist_ok=True)
    (folder / "solution" / "python" / "main.py").write_text(sol.strip() + "\n", encoding="utf-8")
    (folder / "cpp").mkdir(parents=True, exist_ok=True)
    (folder / "cpp" / "CMakeLists.txt").write_text(
        CPP_CMAKE.format(project=f"ex_{module}_{ex_id}"), encoding="utf-8"
    )
    (folder / "cpp" / "main.cpp").write_text(STUB_CPP, encoding="utf-8")
    (folder / "solution" / "cpp").mkdir(parents=True, exist_ok=True)
    (folder / "solution" / "cpp" / "main.cpp").write_text(
        '#include <iostream>\n\nint main() { std::cout << "TODO\\n"; return 1; }\n', encoding="utf-8"
    )


OLLAMA_BASE = 'os.environ.get("CODAMLINGS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")'

write_ex(
    "ollama",
    "01_check_version",
    """# Ollama Health Check

## Theory
[Ollama](https://ollama.com) serves open models locally at `http://localhost:11434`.
Check the daemon with `GET /api/version`.

## Assignment
Call the version endpoint. Print `OLLAMA_OK:` + version string from JSON.""",
    "Use `CODAMLINGS_OLLAMA_BASE` from env (set in mock verify). `urllib.request.urlopen`.",
    f"""import json, os, urllib.request

def main() -> None:
    base = {OLLAMA_BASE}
    with urllib.request.urlopen(f"{{base}}/api/version", timeout=10) as r:
        data = json.loads(r.read())
    print(f"OLLAMA_OK:{{data['version']}}")

if __name__ == "__main__":
    main()
""",
    '"""TODO: Ollama version check."""\n\ndef main() -> None:\n    pass\n\nif __name__ == "__main__":\n    main()\n',
)

write_ex(
    "ollama",
    "02_list_models",
    """# List Ollama Models

## Theory
Installed models are listed via `GET /api/tags` (response field `models`).

## Assignment
Fetch tags. Print `MODELS_OK:` + number of models.""",
    "Parse JSON array `models`. Count entries.",
    f"""import json, os, urllib.request

def main() -> None:
    base = {OLLAMA_BASE}
    with urllib.request.urlopen(f"{{base}}/api/tags", timeout=10) as r:
        data = json.loads(r.read())
    print(f"MODELS_OK:{{len(data['models'])}}")

if __name__ == "__main__":
    main()
""",
    '"""TODO: list Ollama models."""\n\ndef main() -> None:\n    pass\n\nif __name__ == "__main__":\n    main()\n',
)

write_ex(
    "ollama",
    "03_chat",
    """# Ollama Chat

## Theory
Chat uses `POST /api/chat` with `model`, `messages`, and `stream: false`.

## Assignment
Send user message `ollama chat hello` to model `llama3.2`. Print assistant `message.content`.""",
    "Ollama response shape: `message.content` (not OpenAI `choices`).",
    f"""import json, os, urllib.request

def main() -> None:
    base = {OLLAMA_BASE}
    payload = {{
        "model": "llama3.2",
        "messages": [{{"role": "user", "content": "ollama chat hello"}}],
        "stream": False,
    }}
    req = urllib.request.Request(
        f"{{base}}/api/chat",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={{"Content-Type": "application/json"}},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    print(data["message"]["content"])

if __name__ == "__main__":
    main()
""",
    '"""TODO: Ollama chat."""\n\ndef main() -> None:\n    pass\n\nif __name__ == "__main__":\n    main()\n',
)

write_ex(
    "ollama",
    "04_model_env",
    """# Ollama Model from Environment

## Theory
Point exercises at different local models via `.env` (`OLLAMA_MODEL`) without code changes.

## Assignment
Read `OLLAMA_MODEL` (default `llama3.2`). Print `MODEL_OK:` + model name.""",
    "Same pattern as `MISTRAL_MODEL` — one `.env` for all exercises.",
    """import os

def main() -> None:
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    print(f"MODEL_OK:{model}")

if __name__ == "__main__":
    main()
""",
    '"""TODO: Ollama model env."""\n\ndef main() -> None:\n    pass\n\nif __name__ == "__main__":\n    main()\n',
)

write_ex(
    "ollama",
    "05_stream_chat",
    """# Ollama Streaming Chat

## Theory
With `stream: true`, Ollama returns **newline-delimited JSON** chunks until `done: true`.

## Assignment
Stream chat with user message `ollama stream hello`. Concatenate `message.content` chunks and print the full text.""",
    "Read line by line; `json.loads` each line; skip empty lines.",
    f"""import json, os, urllib.request

def main() -> None:
    base = {OLLAMA_BASE}
    payload = {{
        "model": "llama3.2",
        "messages": [{{"role": "user", "content": "ollama stream hello"}}],
        "stream": True,
    }}
    req = urllib.request.Request(
        f"{{base}}/api/chat",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={{"Content-Type": "application/json"}},
    )
    parts: list[str] = []
    with urllib.request.urlopen(req, timeout=60) as r:
        for line in r:
            line = line.decode("utf-8").strip()
            if not line:
                continue
            chunk = json.loads(line)
            msg = chunk.get("message") or {{}}
            if content := msg.get("content"):
                parts.append(content)
    print("".join(parts))

if __name__ == "__main__":
    main()
""",
    '"""TODO: Ollama streaming."""\n\ndef main() -> None:\n    pass\n\nif __name__ == "__main__":\n    main()\n',
)

write_ex(
    "ollama",
    "06_embeddings",
    """# Ollama Embeddings

## Theory
Ollama exposes `POST /api/embeddings` with `model` and `prompt` (keeps vectors on-prem).

## Assignment
Embed prompt `codam ollama embed`. Print `EMBED_DIM:` + length of `embedding` array.""",
    "Use a model like `nomic-embed-text` if installed; mock verify works without a real model.",
    f"""import json, os, urllib.request

def main() -> None:
    base = {OLLAMA_BASE}
    payload = {{"model": "nomic-embed-text", "prompt": "codam ollama embed"}}
    req = urllib.request.Request(
        f"{{base}}/api/embeddings",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={{"Content-Type": "application/json"}},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    print(f"EMBED_DIM:{{len(data['embedding'])}}")

if __name__ == "__main__":
    main()
""",
    '"""TODO: Ollama embeddings."""\n\ndef main() -> None:\n    pass\n\nif __name__ == "__main__":\n    main()\n',
)

(MODULES / "ollama" / "README.md").write_text(
    """# Ollama — local LLM runtime

Run open models on your machine with the [Ollama HTTP API](https://github.com/ollama/ollama/blob/main/docs/api.md).

| # | Exercise | Topic |
|---|----------|-------|
| 01 | check_version | Daemon health |
| 02 | list_models | Installed models |
| 03 | chat | `/api/chat` completion |
| 04 | model_env | `OLLAMA_MODEL` in `.env` |
| 05 | stream_chat | NDJSON streaming |
| 06 | embeddings | Local embeddings |

## Setup

```bash
# Install: https://ollama.com/download
ollama serve
ollama pull llama3.2
ollama pull nomic-embed-text   # optional, for exercise 06
```

Add to repo root `.env`:

```bash
OLLAMA_BASE=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

`codamlings verify --mock` uses a built-in mock — no Ollama install required for CI.

Prerequisites: `core/`, `modules/local_llm`
""",
    encoding="utf-8",
)

if __name__ == "__main__":
    print("Ollama module written.")
