"""Capstone 03 — LLM Gateway. See README.md."""

from __future__ import annotations

import argparse
import sys


class Gateway:
  """TODO: implement milestones in gateway.py (or here)."""

  def complete(self, prompt: str, *, system: str = "") -> str:
    raise NotImplementedError

  def stats(self) -> dict:
    return {"calls": 0, "cache_hits": 0, "retries": 0, "fallbacks": 0}


def main() -> None:
  parser = argparse.ArgumentParser(description="LLM Gateway capstone")
  sub = parser.add_subparsers(dest="command", required=True)

  p_complete = sub.add_parser("complete", help="Single completion")
  p_complete.add_argument("--prompt", required=True)
  p_complete.add_argument("--system", default="")

  sub.add_parser("eval", help="Run eval suite")
  sub.add_parser("stats", help="Show gateway stats")

  args = parser.parse_args()
  gw = Gateway()

  if args.command == "complete":
    # TODO
    print("GATEWAY_OK:TODO")
    sys.exit(1)
  if args.command == "eval":
    print("EVAL:0/10")
    sys.exit(1)
  if args.command == "stats":
    s = gw.stats()
    print(f"STATS:calls={s['calls']}:cache_hits={s['cache_hits']}:retries={s['retries']}:fallbacks={s['fallbacks']}")
    sys.exit(0)


if __name__ == "__main__":
  main()
