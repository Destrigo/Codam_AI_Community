"""Capstone 03 — LLM Gateway CLI (reference solution)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from codamlings.config import load_dotenv_if_present, require_mistral_key

load_dotenv_if_present()

# Import sibling gateway module
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gateway import Gateway  # noqa: E402


def cmd_eval(gw: Gateway) -> int:
    eval_path = Path(__file__).resolve().parent.parent.parent / "eval" / "prompts.json"
    items = json.loads(eval_path.read_text(encoding="utf-8"))
    passed = 0
    for item in items:
        system = item.get("system", "")
        out = gw.complete(item["prompt"], system=system)
        must = item.get("must_contain", [])
        if not must:
            passed += 1
            continue
        if all(m.lower() in out.lower() for m in must):
            passed += 1
    total = len(items)
    print(f"EVAL:{passed}/{total}")
    return 0 if passed >= int(total * 0.9) else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Gateway capstone")
    sub = parser.add_subparsers(dest="command", required=True)

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("--prompt", required=True)
    p_complete.add_argument("--system", default="")

    sub.add_parser("eval")
    sub.add_parser("stats")

    args = parser.parse_args()
    require_mistral_key()
    gw = Gateway()

    if args.command == "complete":
        out = gw.complete(args.prompt, system=args.system)
        print(f"GATEWAY_OK:{out}")
        sys.exit(0)
    if args.command == "eval":
        sys.exit(cmd_eval(gw))
    if args.command == "stats":
        s = gw.stats()
        print(
            f"STATS:calls={s['calls']}:cache_hits={s['cache_hits']}:"
            f"retries={s['retries']}:fallbacks={s['fallbacks']}"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
