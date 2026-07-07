"""Capstone 02 — Ops Agent. See README.md."""

from __future__ import annotations

import argparse
import sys


def cmd_tool(name: str, **kwargs) -> int:
  # TODO: Milestone 1
  print(f"TOOL_TODO:{name}")
  return 1


def cmd_run(data: str, task: str) -> int:
  # TODO: Milestones 2–5
  print("AGENT_DONE:0")
  return 1


def cmd_eval() -> int:
  print("EVAL:0/3")
  return 1


def main() -> None:
  parser = argparse.ArgumentParser(description="Ops Agent capstone")
  sub = parser.add_subparsers(dest="command", required=True)

  p_tool = sub.add_parser("tool", help="Run a single tool")
  p_tool.add_argument("name", choices=["search_docs", "calculator", "write_report"])
  p_tool.add_argument("--query", default="")
  p_tool.add_argument("--expr", default="")

  p_run = sub.add_parser("run", help="Run agent on a task")
  p_run.add_argument("--data", default="./data")
  p_run.add_argument("--task", required=True)

  sub.add_parser("eval", help="Run eval tasks")

  args = parser.parse_args()
  if args.command == "tool":
    sys.exit(cmd_tool(args.name, query=args.query, expr=args.expr))
  if args.command == "run":
    sys.exit(cmd_run(args.data, args.task))
  if args.command == "eval":
    sys.exit(cmd_eval())


if __name__ == "__main__":
  main()
