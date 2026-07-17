# Codam AI Labs — Assignment lookup

Quick reference for all **78 exercises**: slug → assignment → verify output.

Verify with: `codam-labs --mock verify <slug>`

## Core (10)

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `01_env_vars` | Read the environment variable `APP_NAME`. - If it is set, print: `APP_NAME=<value>` - If it is missing, print: `APP_NAME=MISSING` The ver... | `APP_NAME=codam-ai-labs` |
| `02_http_get` | GET `CODAM_LABS_TODO_URL` (mock) / jsonplaceholder fallback. Print the todo `title`. Prefer `--mock`. | `delectus aut autem` |
| `03_http_post` | POST JSON `{"name":"codam"}` to `CODAM_LABS_ECHO_URL` (mock) / httpbin fallback. Print `ECHO_OK:codam` from `json.name`. Prefer `--mock`. | `ECHO_OK:codam` |
| `04_llm_first_call` | Call the chat completions API with: - `model`: `"mistral-small-latest"` (or any string with the mock) - `messages`: a single user message... | `MOCK_RESPONSE` |
| `05_system_user_prompts` | Send a chat with: - **system**: `"Always respond in UPPERCASE"` - **user**: `"hello"` Print only the assistant response. Expected output ... | `HELLO` |
| `06_conversation_history` | Send **4 messages** in a single call: 1. `user`: `"First"` 2. `assistant`: `"Received first"` 3. `user`: `"Second"` 4. `user`: `"How many... | `HISTORY_OK:4` |
| `07_output_control` | Call chat completions with: - `messages`: `[{"role": "user", "content": "hello"}]` - `max_tokens`: `5` Print the assistant response. With... | `TOKEN_LIMIT_OK` |
| `08_streaming` | Call chat completions in **stream mode** with user `"hello"`. Print the content chunks **concatenated** without extra newlines between th... | `MOCK_RESPONSE` |
| `09_timeout_retry` | Implement a function that calls `GET {MISTRAL_API_BASE}/fail_twice` (mock endpoint). - Maximum **3 attempts** - If the first attempts fai... | `RETRY_OK` |
| `10_dirty_json` | 1. Ask the LLM (user prompt): `"Return JSON in markdown"` 2. From the response, **extract** the JSON from the markdown block 3. Parse it ... | `PARSED:name=codam`, `PARSED:score=42` |

## Prompt Engineering

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `prompt_engineering/01_clear_vs_ambiguous` | Build a `classify_sentiment(text)` function that calls Mistral with a **specific** prompt (must mention `positive` or `negative` and the ... | `SPECIFIC_OK` |
| `prompt_engineering/02_few_shot` | Send a prompt containing `Example 1:` and `Example 2:` before the real question. Print the response (contains `FEW_SHOT_OK`). | `FEW_SHOT_OK` |
| `prompt_engineering/03_json_format` | Prompt must include `json only`. Print response containing `JSON_LABEL_OK`. | `JSON_LABEL_OK` |
| `prompt_engineering/04_chain_of_thought` | Include `think step by step` in the prompt. Print response with `COT_OK`. | `COT_OK` |
| `prompt_engineering/05_role_prompt` | Use system role `code reviewer`. Response contains `ROLE_OK`. | `ROLE_OK` |
| `prompt_engineering/06_prompt_template` | Use template `Hello {name}` with name=codam. Print `TEMPLATE_OK:codam`. | `TEMPLATE_OK:codam` |

## Structured Output

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `structured_output/01_extract_json` | Parse `{{"label":"positive"}}` from mock response. Print `EXTRACT_OK:positive`. | `EXTRACT_OK:positive` |
| `structured_output/02_validate_schema` | Given `{{"name":"codam","score":1}}` require both fields. Print `SCHEMA_OK`. | `SCHEMA_OK` |
| `structured_output/03_retry_invalid` | Call mock with `retry invalid json`. Print `RETRY_JSON_OK`. | `RETRY_JSON_OK` |
| `structured_output/04_classify` | Prompt with `classify category`. Print `CLASS:bug`. | `CLASS:bug` |
| `structured_output/05_extract_entities` | Prompt `extract entities`. Print `ENTITY:name=Marco`. | `ENTITY:name=Marco` |

## Embeddings

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `embeddings/01_generate_embedding` | POST `/embeddings` with input `hello`. Print `EMBED_DIM:3`. | `EMBED_DIM:3` |
| `embeddings/02_cosine_similarity` | Compute cosine of `[1,0,0]` and `[1,0,0]`. Print `SIMILARITY:1.0`. | `SIMILARITY:1.0` |
| `embeddings/03_top1_retrieval` | Given query `[1,0]` and docs `a:[1,0]`, `b:[0,1]`. Print `TOP1:doc_a`. | `TOP1:doc_a` |
| `embeddings/04_batch_compare` | 3 docs, print `BATCH_OK`. | `BATCH_OK` |
| `embeddings/05_embed_source` | Call embeddings endpoint. Print `EMBED_SOURCE:mock`. | `EMBED_SOURCE:mock` |

## Rag

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `rag/01_chunk_fixed` | Chunk `abcdefghij` size 4. Print `CHUNKS:3`. | `CHUNKS:3` |
| `rag/02_chunk_paragraph` | Two paragraphs. Print `CHUNKS:2`. | `CHUNKS:2` |
| `rag/03_build_index` | Index 3 chunks. Print `INDEX_SIZE:3`. | `INDEX_SIZE:3` |
| `rag/04_top_k` | Print `TOPK:2`. | `TOPK:2` |
| `rag/05_rag_pipeline` | Call mock with `rag pipeline`. Print `RAG_ANSWER:42`. | `RAG_ANSWER:42` |
| `rag/06_citations` | Prompt `cite chunk`. Print `CITED:chunk_1`. | `CITED:chunk_1` |
| `rag/07_context_overflow` | Truncate 5 chunks to 2. Print `TRUNCATED_OK`. | `TRUNCATED_OK` |

## Tools

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `tools/01_tool_schema` | Define tool `calculator` with param `expression`. Print `SCHEMA_OK`. | `SCHEMA_OK` |
| `tools/02_tool_select` | Send tools in API request. Print `TOOL_CALL:calculator`. | `TOOL_CALL:calculator` |
| `tools/03_tool_execute` | Print `TOOL_RESULT:42`. | `TOOL_RESULT:42` |
| `tools/04_calculator` | Safe eval `6*7`. Print `CALC:42`. | `CALC:42` |
| `tools/05_fetch_url` | GET jsonplaceholder todo 1 title. Print `FETCH_OK:delectus aut autem`. | `FETCH_OK:delectus aut autem` |
| `tools/06_multi_tool` | Route search query. Print `ROUTER:search`. | `ROUTER:search` |

## Agents

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `agents/01_agent_loop` | Simulate 3 steps. Print `AGENT_DONE:3`. | `AGENT_DONE:3` |
| `agents/02_max_steps` | Stop at 5 steps. Print `MAX_STEPS_OK`. | `MAX_STEPS_OK` |
| `agents/03_planner` | Split into 3 subtasks. Print `PLAN:3`. | `PLAN:3` |
| `agents/04_scratchpad` | Write note, print `SCRATCH:note`. | `SCRATCH:note` |
| `agents/05_two_tools` | Call mock `agent two tools`. Print `AGENT_TOOLS_OK`. | `AGENT_TOOLS_OK` |
| `agents/06_human_confirm` | Gate action with confirm flag. Print `CONFIRM_OK`. | `CONFIRM_OK` |

## Local Llm

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `local_llm/01_local_call` | Call mock as local endpoint. Print `LOCAL_OK`. | `LOCAL_OK` |
| `local_llm/02_model_select` | Print `MODEL:mistral-small-latest`. | `MODEL:mistral-small-latest` |
| `local_llm/03_cloud_vs_local` | Print `COMPARE_OK`. | `COMPARE_OK` |
| `local_llm/04_local_embeddings` | Call /embeddings. Print `LOCAL_EMBED_OK`. | `LOCAL_EMBED_OK` |

## Production

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `production/01_rate_limit` | Retry /fail_twice pattern. Print `RATE_OK`. | `RATE_OK` |
| `production/02_cache` | Second identical call hits cache. Print `CACHE_HIT`. | `CACHE_HIT` |
| `production/03_redacted_log` | Log with key redacted. Print `LOG_REDACTED`. | `LOG_REDACTED` |
| `production/04_guardrail` | Detect `ignore instructions`. Print `BLOCKED:injection`. | `BLOCKED:injection` |
| `production/05_fallback` | Print `FALLBACK_OK`. | `FALLBACK_OK` |
| `production/06_output_test` | Assert regex on output. Print `TEST_PASS`. | `TEST_PASS` |

## Advanced Patterns

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `advanced_patterns/01_map_reduce` | 2 chunks summarized. Print `MAP_REDUCE_OK`. | `MAP_REDUCE_OK` |
| `advanced_patterns/02_router` | Route factual query to RAG. Print `ROUTE:rag`. | `ROUTE:rag` |
| `advanced_patterns/03_self_consistency` | 3 samples, majority wins. Print `VOTE:2`. | `VOTE:2` |
| `advanced_patterns/04_critique_revise` | Call mock `critique revise`. Print `REVISED_OK`. | `REVISED_OK` |
| `advanced_patterns/05_eval_set` | 4/5 pass. Print `EVAL:4/5`. | `EVAL:4/5` |

## Mcp

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `mcp/01_tool_manifest` | Validate manifest below. Print `MANIFEST_OK:2` if tool `search` exists. | `MANIFEST_OK:2` |
| `mcp/02_list_tools` | Call the MCP mock endpoint. Print `TOOLS_OK:` + number of tools. | `TOOLS_OK:2` |
| `mcp/03_call_tool` | Call tool `search` with `{query: "docs"}`. Print response containing `MCP_CALL_OK`. | `MCP_CALL_OK` |
| `mcp/04_resource_read` | Read resource `policy`. Print line containing `RESOURCE_OK`. | `RESOURCE_OK` |
| `mcp/05_client_session` | Initialize session. Print `SESSION_OK:` + session id from response. | `SESSION_OK:mock-session-1` |
| `mcp/06_bridge_llm` | Call Mistral with user message `mcp bridge select tool search`. Print assistant content (contains `MCP_BRIDGE_OK`). | `MCP_BRIDGE_OK` |

## Security

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `security/01_detect_injection` | If input contains `ignore instructions`, print `INJECTION_DETECTED`. Else `SAFE`. | `INJECTION_DETECTED` |
| `security/02_sanitize_input` | Remove `system:` and `ignore instructions` from user string. Print `SANITIZED_OK:` + cleaned text. | `SANITIZED_OK:hello` |
| `security/03_secret_scan` | Scan sample code string. Print `SECRET_SCAN_OK` if a secret pattern is found. | `SECRET_SCAN_OK` |
| `security/04_prompt_boundary` | Build messages array with system + user roles. Print `BOUNDARY_OK:` + number of messages. | `BOUNDARY_OK:2` |
| `security/05_pii_redact` | Redact email in text. Print `PII_REDACTED` if `[EMAIL]` present in output. | `PII_REDACTED` |
| `security/06_red_team` | If prompt contains `ignore instructions`, print `REDTEAM_BLOCKED` without calling API. | `REDTEAM_BLOCKED` |

## Ollama

| Slug | Assignment | Verify expects |
|------|------------|----------------|
| `ollama/01_check_version` | Call the version endpoint. Print `OLLAMA_OK:` + version string from JSON. | `OLLAMA_OK:0.5.7-mock` |
| `ollama/02_list_models` | Fetch tags. Print `MODELS_OK:` + number of models. | `MODELS_OK:2` |
| `ollama/03_chat` | Send user message `ollama chat hello` to model `llama3.2`. Print assistant `message.content`. | `OLLAMA_CHAT_OK` |
| `ollama/04_model_env` | Read `OLLAMA_MODEL` (default `llama3.2`). Print `MODEL_OK:` + model name. | `MODEL_OK:llama3.2` |
| `ollama/05_stream_chat` | Stream chat with user message `ollama stream hello`. Concatenate `message.content` chunks and print the full text. | `OLLAMA_STREAM_OK` |
| `ollama/06_embeddings` | Embed prompt `codam ollama embed`. Print `EMBED_DIM:` + length of `embedding` array. | `EMBED_DIM:3` |
