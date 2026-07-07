"""Output validation for mock vs live Mistral runs."""

from __future__ import annotations

import json
import re
from collections.abc import Callable

# Exercises that do not call the Mistral API
NO_MISTRAL_SLUGS = {
    "01_env_vars", "02_http_get", "03_http_post",
    "prompt_engineering/06_prompt_template",
    "structured_output/01_extract_json", "structured_output/02_validate_schema",
    "embeddings/02_cosine_similarity", "embeddings/03_top1_retrieval", "embeddings/04_batch_compare",
    "rag/01_chunk_fixed", "rag/02_chunk_paragraph", "rag/03_build_index", "rag/04_top_k", "rag/07_context_overflow",
    "tools/01_tool_schema", "tools/03_tool_execute", "tools/04_calculator", "tools/05_fetch_url",
    "agents/01_agent_loop", "agents/02_max_steps", "agents/03_planner", "agents/04_scratchpad", "agents/06_human_confirm",
    "local_llm/02_model_select", "local_llm/03_cloud_vs_local",
    "production/02_cache", "production/03_redacted_log", "production/04_guardrail",
    "production/05_fallback", "production/06_output_test",
    "advanced_patterns/01_map_reduce", "advanced_patterns/02_router",
    "advanced_patterns/03_self_consistency", "advanced_patterns/05_eval_set",
    "mcp/01_tool_manifest", "mcp/02_list_tools", "mcp/03_call_tool", "mcp/04_resource_read",
    "mcp/05_client_session",
    "security/01_detect_injection", "security/02_sanitize_input", "security/03_secret_scan",
    "security/04_prompt_boundary", "security/05_pii_redact", "security/06_red_team",
    "ollama/01_check_version", "ollama/02_list_models", "ollama/04_model_env",
}

# slug -> substrings required in stdout (mock mode)
MOCK_CHECKS: dict[str, list[str]] = {
    "01_env_vars": ["APP_NAME=codam-ai-labs"],
    "02_http_get": ["delectus aut autem"],
    "03_http_post": ["ECHO_OK:codam"],
    "04_llm_first_call": ["MOCK_RESPONSE"],
    "05_system_user_prompts": ["HELLO"],
    "06_conversation_history": ["HISTORY_OK:4"],
    "07_output_control": ["TOKEN_LIMIT_OK"],
    "08_streaming": ["MOCK_RESPONSE"],
    "09_timeout_retry": ["RETRY_OK"],
    "10_dirty_json": ["PARSED:name=codam", "PARSED:score=42"],
    "prompt_engineering/01_clear_vs_ambiguous": ["SPECIFIC_OK"],
    "prompt_engineering/02_few_shot": ["FEW_SHOT_OK"],
    "prompt_engineering/03_json_format": ["JSON_LABEL_OK"],
    "prompt_engineering/04_chain_of_thought": ["COT_OK"],
    "prompt_engineering/05_role_prompt": ["ROLE_OK"],
    "prompt_engineering/06_prompt_template": ["TEMPLATE_OK:codam"],
    "structured_output/01_extract_json": ["EXTRACT_OK:positive"],
    "structured_output/02_validate_schema": ["SCHEMA_OK"],
    "structured_output/03_retry_invalid": ["RETRY_JSON_OK"],
    "structured_output/04_classify": ["CLASS:bug"],
    "structured_output/05_extract_entities": ["ENTITY:name=Marco"],
    "embeddings/01_generate_embedding": ["EMBED_DIM:3"],
    "embeddings/02_cosine_similarity": ["SIMILARITY:1.0"],
    "embeddings/03_top1_retrieval": ["TOP1:doc_a"],
    "embeddings/04_batch_compare": ["BATCH_OK"],
    "embeddings/05_embed_source": ["EMBED_SOURCE:mock"],
    "rag/01_chunk_fixed": ["CHUNKS:3"],
    "rag/02_chunk_paragraph": ["CHUNKS:2"],
    "rag/03_build_index": ["INDEX_SIZE:3"],
    "rag/04_top_k": ["TOPK:2"],
    "rag/05_rag_pipeline": ["RAG_ANSWER:42"],
    "rag/06_citations": ["CITED:chunk_1"],
    "rag/07_context_overflow": ["TRUNCATED_OK"],
    "tools/01_tool_schema": ["SCHEMA_OK"],
    "tools/02_tool_select": ["TOOL_CALL:calculator"],
    "tools/03_tool_execute": ["TOOL_RESULT:42"],
    "tools/04_calculator": ["CALC:42"],
    "tools/05_fetch_url": ["FETCH_OK:delectus aut autem"],
    "tools/06_multi_tool": ["ROUTER:search"],
    "agents/01_agent_loop": ["AGENT_DONE:3"],
    "agents/02_max_steps": ["MAX_STEPS_OK"],
    "agents/03_planner": ["PLAN:3"],
    "agents/04_scratchpad": ["SCRATCH:note"],
    "agents/05_two_tools": ["AGENT_TOOLS_OK"],
    "agents/06_human_confirm": ["CONFIRM_OK"],
    "local_llm/01_local_call": ["LOCAL_OK"],
    "local_llm/02_model_select": ["MODEL:mistral-small-latest"],
    "local_llm/03_cloud_vs_local": ["COMPARE_OK"],
    "local_llm/04_local_embeddings": ["LOCAL_EMBED_OK"],
    "production/01_rate_limit": ["RATE_OK"],
    "production/02_cache": ["CACHE_HIT"],
    "production/03_redacted_log": ["LOG_REDACTED"],
    "production/04_guardrail": ["BLOCKED:injection"],
    "production/05_fallback": ["FALLBACK_OK"],
    "production/06_output_test": ["TEST_PASS"],
    "advanced_patterns/01_map_reduce": ["MAP_REDUCE_OK"],
    "advanced_patterns/02_router": ["ROUTE:rag"],
    "advanced_patterns/03_self_consistency": ["VOTE:2"],
    "advanced_patterns/04_critique_revise": ["REVISED_OK"],
    "advanced_patterns/05_eval_set": ["EVAL:4/5"],
    "mcp/01_tool_manifest": ["MANIFEST_OK:2"],
    "mcp/02_list_tools": ["TOOLS_OK:2"],
    "mcp/03_call_tool": ["MCP_CALL_OK"],
    "mcp/04_resource_read": ["RESOURCE_OK"],
    "mcp/05_client_session": ["SESSION_OK:mock-session-1"],
    "mcp/06_bridge_llm": ["MCP_BRIDGE_OK"],
    "security/01_detect_injection": ["INJECTION_DETECTED"],
    "security/02_sanitize_input": ["SANITIZED_OK:hello"],
    "security/03_secret_scan": ["SECRET_SCAN_OK"],
    "security/04_prompt_boundary": ["BOUNDARY_OK:2"],
    "security/05_pii_redact": ["PII_REDACTED"],
    "security/06_red_team": ["REDTEAM_BLOCKED"],
    "ollama/01_check_version": ["OLLAMA_OK:0.5.7-mock"],
    "ollama/02_list_models": ["MODELS_OK:2"],
    "ollama/03_chat": ["OLLAMA_CHAT_OK"],
    "ollama/04_model_env": ["MODEL_OK:llama3.2"],
    "ollama/05_stream_chat": ["OLLAMA_STREAM_OK"],
    "ollama/06_embeddings": ["EMBED_DIM:3"],
}


def _non_empty(out: str) -> bool:
    return len(out.strip()) > 0


def _has_json_object(out: str) -> bool:
    try:
        start, end = out.find("{"), out.rfind("}")
        if start == -1 or end <= start:
            return False
        json.loads(out[start : end + 1])
        return True
    except json.JSONDecodeError:
        return False


def _embed_dim_ok(out: str) -> bool:
    m = re.search(r"EMBED_DIM:(\d+)", out)
    return bool(m and int(m.group(1)) > 0)


def _uppercase_ok(out: str) -> bool:
    text = out.strip()
    return bool(text) and text == text.upper()


def _parsed_json_fields(out: str) -> bool:
    return "PARSED:name=" in out and "PARSED:score=" in out


# Live mode: semantic checks (real Mistral API)
LIVE_VALIDATORS: dict[str, Callable[[str], bool]] = {
    "04_llm_first_call": _non_empty,
    "05_system_user_prompts": _uppercase_ok,
    "06_conversation_history": _non_empty,
    "07_output_control": _non_empty,
    "08_streaming": _non_empty,
    "09_timeout_retry": lambda o: "RETRY_OK" in o,
    "10_dirty_json": _parsed_json_fields,
    "prompt_engineering/01_clear_vs_ambiguous": _non_empty,
    "prompt_engineering/02_few_shot": _non_empty,
    "prompt_engineering/03_json_format": _has_json_object,
    "prompt_engineering/04_chain_of_thought": _non_empty,
    "prompt_engineering/05_role_prompt": _non_empty,
    "structured_output/03_retry_invalid": _has_json_object,
    "structured_output/04_classify": _non_empty,
    "structured_output/05_extract_entities": _non_empty,
    "embeddings/01_generate_embedding": _embed_dim_ok,
    "embeddings/05_embed_source": lambda o: "EMBED_SOURCE:" in o,
    "rag/05_rag_pipeline": _non_empty,
    "rag/06_citations": _non_empty,
    "tools/02_tool_select": _non_empty,
    "tools/06_multi_tool": _non_empty,
    "agents/05_two_tools": _non_empty,
    "local_llm/01_local_call": _non_empty,
    "local_llm/04_local_embeddings": _non_empty,
    "production/01_rate_limit": lambda o: "RETRY_OK" in o or "RATE_OK" in o,
    "advanced_patterns/04_critique_revise": _non_empty,
    "mcp/06_bridge_llm": _non_empty,
    "ollama/03_chat": _non_empty,
    "ollama/05_stream_chat": _non_empty,
    "ollama/06_embeddings": _embed_dim_ok,
}


def requires_mistral(slug: str) -> bool:
    return slug not in NO_MISTRAL_SLUGS


def check_output(slug: str, stdout: str, stderr: str, *, use_mock: bool) -> tuple[bool, str]:
    out = stdout.strip()
    if use_mock:
        expected = MOCK_CHECKS.get(slug, [])
        missing = [item for item in expected if item not in out]
        if missing:
            return False, f"Missing expected output: {missing}\n--- stdout ---\n{out}"
        if slug == "05_system_user_prompts" and out != "HELLO":
            return False, f"Expected HELLO, got {out!r}"
        return True, "OK"

    # Live: exact checks for local exercises
    if slug in NO_MISTRAL_SLUGS:
        expected = MOCK_CHECKS.get(slug, [])
        missing = [item for item in expected if item not in out]
        if missing:
            return False, f"Missing expected output: {missing}\n--- stdout ---\n{out}"
        return True, "OK"

    validator = LIVE_VALIDATORS.get(slug, _non_empty)
    if validator(out):
        return True, "OK"
    return False, f"Live validation failed.\n--- stdout ---\n{out}\n--- stderr ---\n{stderr.strip()}"
