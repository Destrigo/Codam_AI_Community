# Ollama Health Check

## Theory
[Ollama](https://ollama.com) serves open models locally at `http://localhost:11434`.
Check the daemon with `GET /api/version`.

## Assignment
Call the version endpoint. Print `OLLAMA_OK:` + version string from JSON.
