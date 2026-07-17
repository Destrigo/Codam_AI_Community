# Ollama Stream Chat

## Theory
Streaming chat returns NDJSON chunks from POST {CODAM_LABS_OLLAMA_BASE}/api/chat with stream: true.

Use CODAM_LABS_OLLAMA_BASE (set by --mock).

## Assignment
Stream chat with user message ollama stream hello. Concatenate message.content chunks and print the full text.

## Verify
`ash
codam-labs --mock verify ollama/05_stream_chat
`
