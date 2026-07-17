# List Ollama Models

## Theory
Installed models are listed via GET {CODAM_LABS_OLLAMA_BASE}/api/tags (field models).

Use CODAM_LABS_OLLAMA_BASE (set by --mock).

## Assignment
Fetch tags. Print MODELS_OK: + number of models.

## Verify
`ash
codam-labs --mock verify ollama/02_list_models
`
