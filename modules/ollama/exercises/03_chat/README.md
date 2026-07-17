# Ollama Chat

## Theory
Chat uses POST {CODAM_LABS_OLLAMA_BASE}/api/chat with model, messages, and stream: false.

Use CODAM_LABS_OLLAMA_BASE (set by --mock).

## Assignment
Send user message ollama chat hello to model llama3.2. Print assistant message.content.

## Verify
`ash
codam-labs --mock verify ollama/03_chat
`
