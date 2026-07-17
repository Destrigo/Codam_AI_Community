# Ollama Health Check

## Theory
[Ollama](https://ollama.com) serves open models locally.
Check the daemon with GET {CODAM_LABS_OLLAMA_BASE}/api/version.

`python
base = os.environ.get("CODAM_LABS_OLLAMA_BASE", "http://localhost:11434").rstrip("/")
`

--mock points this at the local labs mock (no Ollama install needed).

## Assignment
Call the version endpoint. Print OLLAMA_OK: + version string from JSON.

## Verify
`ash
codam-labs --mock verify ollama/01_check_version
`
