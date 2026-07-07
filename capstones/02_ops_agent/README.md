# Capstone 02 — Ops Agent (mini-agent)

## Brief (fictional client)

**Nordic SaaS Ltd** runs internal ops from markdown playbooks and spreadsheets. Analysts waste hours copying numbers into weekly reports.

**Your job:** build a terminal agent with three tools that completes multi-step tasks: search docs → calculate → write a structured report file.

---

## Theory

An **agent** is not a chatbot. It runs a loop:

```
while not done and steps < max:
    observe (user task + tool results so far)
    think  (LLM decides next action)
    act    (call a tool)
```

You combine:

- **Tool schemas** (`tools/01_tool_schema`)
- **Tool selection** (`tools/02_tool_select`, `06_multi_tool`)
- **Agent loop** (`agents/01_agent_loop`, `02_max_steps`)
- **Scratchpad** (`agents/04_scratchpad`)
- **Human confirm** (`agents/06_human_confirm`)
- **Structured output** (`structured_output/02_validate_schema`)

---

## Prerequisites

- `core/` (all 10)
- `modules/tools` (all 6)
- `modules/agents` (all 6)
- `modules/structured_output` (01, 02, 04)

---

## Assignment

Build `ops_agent` CLI:

```bash
python python/main.py run --data ./data --task "Find the Q1 discount cap and calculate 15% of 12000"

# Expected flow (stderr logs):
# STEP:1 ACTION:search_docs QUERY:discount cap
# STEP:2 ACTION:calculator EXPR:12000*0.15
# STEP:3 ACTION:write_report (pending confirm)
# CONFIRM? write report to ./out/report.json [y/N]
# AGENT_DONE:3
# REPORT_OK:./out/report.json
```

### Tools (you must implement)

| Tool | Name | Input | Output |
|------|------|-------|--------|
| Search | `search_docs` | `query: string` | Top matching paragraph from `data/*.md` |
| Math | `calculator` | `expression: string` | Numeric result (safe eval: digits, +−*/, parentheses only) |
| Write | `write_report` | `title, summary, figures` | Writes JSON to `out/report.json` |

Pass tool definitions to Mistral in the `tools` field of chat completions.

### Functional requirements

| # | Requirement |
|---|-------------|
| A1 | Max 8 steps; print `MAX_STEPS_OK` if stopped by limit without finishing |
| A2 | Scratchpad: append each tool result to an internal string sent back to LLM |
| A3 | `write_report` requires stdin confirmation `y` before writing |
| A4 | Final report validates against `schemas/report.schema.json` |
| A5 | Print `AGENT_DONE:<n>` where n = number of tool calls executed |

### Out of scope

- Arbitrary shell execution
- Network fetch (use local `data/` only)
- Parallel tool calls

---

## Milestones

### Milestone 1 — Tool implementations

Each tool works standalone:

```bash
python python/main.py tool search_docs --query "discount"
# SEARCH_OK:file=sales_discount_rules.md:line=...

python python/main.py tool calculator --expr "12000*0.15"
# CALC_OK:1800
```

---

### Milestone 2 — Single tool selection

LLM picks the right tool for a one-step task:

```
TOOL_SELECT_OK:calculator
```

---

### Milestone 3 — Agent loop (2+ tools)

Complete `eval/tasks.json` task `t01` (search + calculate) without human confirm on write.

```
AGENT_DONE:2
```

---

### Milestone 4 — Full pipeline with confirm

Task `t02` writes report after user confirms.

```
AGENT_DONE:3
REPORT_OK:./out/report.json
```

---

### Milestone 5 — Structured report + eval

All tasks in `eval/tasks.json` pass schema validation. Print `EVAL:3/3`.

---

## Project structure

```
02_ops_agent/
├── README.md
├── peer_review.md
├── hint.md
├── data/
│   ├── sales_discount_rules.md
│   └── engineering_oncall.md
├── eval/
│   └── tasks.json
├── schemas/
│   ├── tools.schema.json
│   └── report.schema.json
├── python/
│   └── main.py
└── cpp/
    └── main.cpp
```

---

## Evaluation rubric

| Criterion | Weight |
|-----------|--------|
| Tools work correctly in isolation | 20% |
| Agent selects correct tools | 25% |
| Multi-step tasks complete | 25% |
| Human confirm before write | 15% |
| Valid JSON report output | 15% |

---

## Time estimate

**16–22 hours** total.

---

## Safety note

The `calculator` tool must **not** use `eval()` on arbitrary Python. Whitelist characters: `0-9+-*/().` and reject everything else.
