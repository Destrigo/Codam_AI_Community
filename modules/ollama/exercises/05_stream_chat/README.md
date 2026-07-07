# Ollama Streaming Chat

## Theory
With `stream: true`, Ollama returns **newline-delimited JSON** chunks until `done: true`.

## Assignment
Stream chat with user message `ollama stream hello`. Concatenate `message.content` chunks and print the full text.
