"""Capstone 02 — Ops Agent (reference solution)."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

from codam_ai_labs.config import load_dotenv_if_present, require_mistral_key
from codam_ai_labs.llm_client import chat_text, is_mock_mode

load_dotenv_if_present()

MAX_STEPS = 8
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "Search local markdown docs",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate math expression",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_report",
            "description": "Write JSON report to out/report.json",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                },
                "required": ["title", "summary"],
            },
        },
    },
]


def search_docs(data_dir: Path, query: str) -> str:
    best_file, best_line, best_score = "", "", 0
    for path in sorted(data_dir.glob("*.md")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            score = sum(1 for w in query.lower().split() if w in line.lower())
            if score > best_score:
                best_score, best_file, best_line = score, path.name, line.strip()
    print(f"SEARCH_OK:file={best_file}:line={best_line}", file=sys.stderr)
    return f"{best_file}: {best_line}"


def calculator(expression: str) -> str:
    if not re.fullmatch(r"[\d+\-*/().\s]+", expression):
        raise ValueError("unsafe expression")
    result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
    print(f"CALC_OK:{result}", file=sys.stderr)
    return str(result)


def write_report(title: str, summary: str, figures: dict | None = None) -> str:
    auto = os.environ.get("CODAM_LABS_AUTO_CONFIRM", "").lower() in {"1", "true", "yes"}
    if not auto:
        ans = input("CONFIRM? write report to ./out/report.json [y/N] ").strip().lower()
        if ans != "y":
            return "CANCELLED"
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    report = {
        "title": title,
        "summary": summary,
        "figures": figures or {},
        "sources": [],
    }
    path = out_dir / "report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"REPORT_OK:{path}", file=sys.stderr)
    return str(path)


def run_tool(data_dir: Path, name: str, args: dict) -> str:
    if name == "search_docs":
        return search_docs(data_dir, args.get("query", ""))
    if name == "calculator":
        return calculator(args.get("expression", "0"))
    if name == "write_report":
        return write_report(args.get("title", "Report"), args.get("summary", ""))
    raise ValueError(f"unknown tool: {name}")


def _mock_plan(task: str, step: int, history: str) -> dict:
    t = task.lower()
    h = history.lower()
    if "report" in t:
        if "search_docs" not in h:
            return {"tool": "search_docs", "args": {"query": "P1 on-call"}}
        if "write_report" not in h:
            return {
                "tool": "write_report",
                "args": {"title": "OnCall Summary", "summary": history or "on-call findings"},
            }
    if "discount" in t and "search_docs" not in h:
        return {"tool": "search_docs", "args": {"query": "discount cap"}}
    if "12000" in t and "calculator" not in h:
        return {"tool": "calculator", "args": {"expression": "12000*0.15"}}
    if "50000" in t and "calculator" not in h:
        return {"tool": "calculator", "args": {"expression": "50000*0.20"}}
    return {"done": True}


def _plan_next(task: str, history: list[str]) -> dict:
    if is_mock_mode():
        return _mock_plan(task, len(history), " ".join(history))

    system = (
        "You are an ops agent. Use one tool per step. "
        'Reply ONLY JSON: {"tool":"search_docs|calculator|write_report","args":{...}} '
        'or {"done":true} when finished.'
    )
    user = f"Task: {task}\nHistory:\n" + "\n".join(history)
    raw = chat_text([{"role": "system", "content": system}, {"role": "user", "content": user}])
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start : end + 1])


def agent_run(data_dir: Path, task: str) -> int:
    require_mistral_key()
    history: list[str] = []
    tools_used = 0

    for step in range(1, MAX_STEPS + 1):
        plan = _plan_next(task, history)
        if plan.get("done"):
            break
        tool = plan.get("tool")
        args = plan.get("args", {})
        if not tool:
            break
        print(f"STEP:{step} ACTION:{tool}", file=sys.stderr)
        result = run_tool(data_dir, tool, args)
        history.append(f"{tool} -> {result}")
        tools_used += 1
        if tool == "write_report":
            break

    if tools_used >= MAX_STEPS:
        print("MAX_STEPS_OK")
        return 0
    print(f"AGENT_DONE:{tools_used}")
    return 0


def cmd_tool(data_dir: Path, name: str, query: str, expr: str) -> int:
    if name == "search_docs":
        search_docs(data_dir, query)
        return 0
    if name == "calculator":
        calculator(expr)
        return 0
    if name == "write_report":
        os.environ.setdefault("CODAM_LABS_AUTO_CONFIRM", "1")
        write_report("Test", "summary")
        return 0
    return 1


def cmd_eval(data_dir: Path) -> int:
    capstone_root = Path(__file__).resolve().parent.parent.parent
    tasks_path = capstone_root / "eval" / "tasks.json"
    tasks = json.loads(tasks_path.read_text(encoding="utf-8"))
    passed = 0
    os.environ["CODAM_LABS_AUTO_CONFIRM"] = "1"
    report_path = Path("out/report.json")
    for task in tasks:
        if report_path.exists():
            report_path.unlink()
        if agent_run(data_dir, task["task"]) != 0:
            continue
        if task.get("expects_report") and not report_path.exists():
            continue
        passed += 1
    print(f"EVAL:{passed}/{len(tasks)}")
    return 0 if passed == len(tasks) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Ops Agent capstone")
    sub = parser.add_subparsers(dest="command", required=True)

    p_tool = sub.add_parser("tool")
    p_tool.add_argument("name", choices=["search_docs", "calculator", "write_report"])
    p_tool.add_argument("--query", default="")
    p_tool.add_argument("--expr", default="")
    p_tool.add_argument("--data", default="./data")

    p_run = sub.add_parser("run")
    p_run.add_argument("--data", default="./data")
    p_run.add_argument("--task", required=True)

    p_eval = sub.add_parser("eval")
    p_eval.add_argument("--data", default="./data")

    args = parser.parse_args()
    data_dir = Path(getattr(args, "data", "./data"))

    if args.command == "tool":
        sys.exit(cmd_tool(data_dir, args.name, args.query, args.expr))
    if args.command == "run":
        sys.exit(agent_run(data_dir, args.task))
    if args.command == "eval":
        sys.exit(cmd_eval(data_dir))


if __name__ == "__main__":
    main()
