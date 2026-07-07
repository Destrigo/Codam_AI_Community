"""Expected output checks for all exercises."""

from __future__ import annotations

# slug -> list of substrings that must appear in stdout
OUTPUT_CHECKS: dict[str, list[str]] = {
    # core
    "01_env_vars": ["APP_NAME=codamlings"],
    "02_http_get": ["delectus aut autem"],
    "03_http_post": ["ECHO_OK:codam"],
    "04_llm_first_call": ["MOCK_RESPONSE"],
    "05_system_user_prompts": ["HELLO"],
    "06_conversation_history": ["HISTORY_OK:4"],
    "07_output_control": ["TOKEN_LIMIT_OK"],
    "08_streaming": ["MOCK_RESPONSE"],
    "09_timeout_retry": ["RETRY_OK"],
    "10_dirty_json": ["PARSED:name=codam", "PARSED:score=42"],
    # prompt_engineering
    "prompt_engineering/01_clear_vs_ambiguous": ["SPECIFIC_OK"],
    "prompt_engineering/02_few_shot": ["FEW_SHOT_OK"],
    "prompt_engineering/03_json_format": ["JSON_LABEL_OK"],
    "prompt_engineering/04_chain_of_thought": ["COT_OK"],
    "prompt_engineering/05_role_prompt": ["ROLE_OK"],
    "prompt_engineering/06_prompt_template": ["TEMPLATE_OK:codam"],
    # structured_output
    "structured_output/01_extract_json": ["EXTRACT_OK:positive"],
    "structured_output/02_validate_schema": ["SCHEMA_OK"],
    "structured_output/03_retry_invalid": ["RETRY_JSON_OK"],
    "structured_output/04_classify": ["CLASS:bug"],
    "structured_output/05_extract_entities": ["ENTITY:name=Marco"],
    # embeddings
    "embeddings/01_generate_embedding": ["EMBED_DIM:3"],
    "embeddings/02_cosine_similarity": ["SIMILARITY:1.0"],
    "embeddings/03_top1_retrieval": ["TOP1:doc_a"],
    "embeddings/04_batch_compare": ["BATCH_OK"],
    "embeddings/05_embed_source": ["EMBED_SOURCE:mock"],
    # rag
    "rag/01_chunk_fixed": ["CHUNKS:3"],
    "rag/02_chunk_paragraph": ["CHUNKS:2"],
    "rag/03_build_index": ["INDEX_SIZE:3"],
    "rag/04_top_k": ["TOPK:2"],
    "rag/05_rag_pipeline": ["RAG_ANSWER:42"],
    "rag/06_citations": ["CITED:chunk_1"],
    "rag/07_context_overflow": ["TRUNCATED_OK"],
    # tools
    "tools/01_tool_schema": ["SCHEMA_OK"],
    "tools/02_tool_select": ["TOOL_CALL:calculator"],
    "tools/03_tool_execute": ["TOOL_RESULT:42"],
    "tools/04_calculator": ["CALC:42"],
    "tools/05_fetch_url": ["FETCH_OK:delectus aut autem"],
    "tools/06_multi_tool": ["ROUTER:search"],
    # agents
    "agents/01_agent_loop": ["AGENT_DONE:3"],
    "agents/02_max_steps": ["MAX_STEPS_OK"],
    "agents/03_planner": ["PLAN:3"],
    "agents/04_scratchpad": ["SCRATCH:note"],
    "agents/05_two_tools": ["AGENT_TOOLS_OK"],
    "agents/06_human_confirm": ["CONFIRM_OK"],
    # local_llm
    "local_llm/01_local_call": ["LOCAL_OK"],
    "local_llm/02_model_select": ["MODEL:mistral-small-latest"],
    "local_llm/03_cloud_vs_local": ["COMPARE_OK"],
    "local_llm/04_local_embeddings": ["LOCAL_EMBED_OK"],
    # production
    "production/01_rate_limit": ["RATE_OK"],
    "production/02_cache": ["CACHE_HIT"],
    "production/03_redacted_log": ["LOG_REDACTED"],
    "production/04_guardrail": ["BLOCKED:injection"],
    "production/05_fallback": ["FALLBACK_OK"],
    "production/06_output_test": ["TEST_PASS"],
    # advanced_patterns
    "advanced_patterns/01_map_reduce": ["MAP_REDUCE_OK"],
    "advanced_patterns/02_router": ["ROUTE:rag"],
    "advanced_patterns/03_self_consistency": ["VOTE:2"],
    "advanced_patterns/04_critique_revise": ["REVISED_OK"],
    "advanced_patterns/05_eval_set": ["EVAL:4/5"],
}

# Exercises that never start the mock server
NO_MOCK_SLUGS = {
    "01_env_vars", "02_http_get", "03_http_post",
    "prompt_engineering/06_prompt_template",
    "structured_output/01_extract_json", "structured_output/02_validate_schema",
    "embeddings/02_cosine_similarity", "embeddings/03_top1_retrieval", "embeddings/04_batch_compare",
    "rag/01_chunk_fixed", "rag/02_chunk_paragraph", "rag/03_build_index", "rag/04_top_k", "rag/07_context_overflow",
    "tools/01_tool_schema", "tools/03_tool_execute", "tools/04_calculator", "tools/05_fetch_url",
    "agents/01_agent_loop", "agents/02_max_steps", "agents/03_planner", "agents/04_scratchpad", "agents/06_human_confirm",
    "local_llm/02_model_select", "local_llm/03_cloud_vs_local",
    "production/02_cache", "production/03_redacted_log", "production/04_guardrail", "production/05_fallback", "production/06_output_test",
    "advanced_patterns/01_map_reduce", "advanced_patterns/02_router", "advanced_patterns/03_self_consistency", "advanced_patterns/05_eval_set",
}

EXACT_OUTPUT = {
    "05_system_user_prompts": "HELLO",
}
