# Hints — Capstone 02 Ops Agent

## Milestone 1
<details>
<summary>Hint 1.1 — search_docs</summary>

Linear scan over `data/*.md` is fine. Score lines by keyword overlap or embed query + lines (overkill for capstone).
</details>

<details>
<summary>Hint 1.2 — Safe calculator</summary>

```python
import re
if not re.fullmatch(r"[\d+\-*/().\s]+", expr):
    raise ValueError("unsafe")
```
</details>

## Milestone 2
<details>
<summary>Hint 2.1 — Tool schema for Mistral</summary>

```json
{"type": "function", "function": {"name": "search_docs", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}
```
</details>

## Milestone 3
<details>
<summary>Hint 3.1 — Agent loop</summary>

```python
messages = [{"role": "user", "content": task}]
for step in range(max_steps):
    response = chat_with_tools(messages, tools)
    if no_tool_call: break
    result = execute_tool(...)
    messages.append(tool_result_message)
```
</details>

## Milestone 4
<details>
<summary>Hint 4.1 — Human confirm</summary>

Only gate `write_report`. Search and calculate can run autonomously.
</details>
