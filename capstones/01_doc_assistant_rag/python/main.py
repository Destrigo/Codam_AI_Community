"""Capstone 01 — Doc Assistant (mini-RAG). See README.md."""

from __future__ import annotations

import argparse
import sys


def cmd_index(docs: str) -> int:
  # TODO: Milestone 1–2 — chunk + embed
  print("INDEX_OK:docs=0:chunks=0")
  return 1


def cmd_ask(docs: str, question: str) -> int:
  # TODO: Milestone 3–4 — retrieve + generate
  print("ANSWER: TODO")
  print("CITED: TODO")
  print("CONFIDENCE: low")
  return 1


def cmd_eval(docs: str) -> int:
  # TODO: Milestone 5
  print("EVAL:0/5")
  return 1


def main() -> None:
  parser = argparse.ArgumentParser(description="Doc Assistant — mini-RAG capstone")
  sub = parser.add_subparsers(dest="command", required=True)

  p_index = sub.add_parser("index", help="Build chunk + embedding index")
  p_index.add_argument("--docs", default="./data")

  p_ask = sub.add_parser("ask", help="Ask a question")
  p_ask.add_argument("--docs", default="./data")
  p_ask.add_argument("--question", required=True)

  p_eval = sub.add_parser("eval", help="Run gold question eval set")
  p_eval.add_argument("--docs", default="./data")

  args = parser.parse_args()
  if args.command == "index":
    sys.exit(cmd_index(args.docs))
  if args.command == "ask":
    sys.exit(cmd_ask(args.docs, args.question))
  if args.command == "eval":
    sys.exit(cmd_eval(args.docs))


if __name__ == "__main__":
  main()
