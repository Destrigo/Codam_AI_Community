# Ollama Embeddings

## Theory
POST {CODAM_LABS_OLLAMA_BASE}/api/embeddings returns an embedding array.

Use CODAM_LABS_OLLAMA_BASE (set by --mock).

## Assignment
Embed prompt codam ollama embed. Print EMBED_DIM: + length of embedding array.

## Verify
`ash
codam-labs --mock verify ollama/06_embeddings
`
