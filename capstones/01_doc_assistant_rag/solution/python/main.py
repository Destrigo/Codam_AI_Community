"""Capstone 01 — Doc Assistant (reference solution)."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

from codam_ai_labs.config import load_dotenv_if_present, require_mistral_key
from codam_ai_labs.llm_client import chat_text, embed_text, is_mock_mode

load_dotenv_if_present()

SIM_THRESHOLD = 0.35
CHUNK_SIZE = 400
INDEX_NAME = ".index/chunks.json"


def _index_path(docs: Path) -> Path:
    return docs / INDEX_NAME


def _chunk_text(text: str, size: int = CHUNK_SIZE) -> list[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _keyword_score(query: str, text: str) -> float:
    words = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2]
    if not words:
        return 0.0
    body = text.lower()
    return sum(1 for w in words if w in body) / len(words)


def build_index(docs_dir: Path) -> tuple[int, int]:
    require_mistral_key()
    chunks: list[dict] = []
    doc_count = 0
    for path in sorted(docs_dir.rglob("*")):
        if path.suffix.lower() not in {".md", ".txt"} or path.is_dir():
            continue
        if ".index" in path.parts:
            continue
        doc_count += 1
        text = path.read_text(encoding="utf-8")
        for i, piece in enumerate(_chunk_text(text)):
            chunk_id = f"{path.stem}#{i}"
            embedding = [] if is_mock_mode() else embed_text(piece)
            chunks.append({"id": chunk_id, "text": piece, "embedding": embedding, "file": path.stem})

    index_path = _index_path(docs_dir)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps({"chunks": chunks}, indent=2), encoding="utf-8")
    return doc_count, len(chunks)


def load_index(docs_dir: Path) -> list[dict]:
    path = _index_path(docs_dir)
    if not path.exists():
        raise FileNotFoundError(f"Index not found. Run: index --docs {docs_dir}")
    return json.loads(path.read_text(encoding="utf-8"))["chunks"]


def retrieve(chunks: list[dict], question: str, k: int = 3) -> list[tuple[float, dict]]:
    if is_mock_mode():
        scored = [(_keyword_score(question, c["text"]), c) for c in chunks]
    else:
        q_emb = embed_text(question)
        scored = [(_cosine(q_emb, c["embedding"]), c) for c in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]


def ask(docs_dir: Path, question: str) -> int:
    require_mistral_key()
    chunks = load_index(docs_dir)
    top = retrieve(chunks, question)
    best_score = top[0][0] if top else 0.0

    if best_score < SIM_THRESHOLD:
        print("ANSWER: I don't have enough information.")
        print("CITED:")
        print("CONFIDENCE: low")
        return 0

    best_id = top[0][1]["id"]
    context = "\n\n".join(f"[{c['id']}] {c['text']}" for _, c in top)
    system = "Answer only from context. Be concise."
    user = f"Context:\n{context}\n\nQuestion: {question}"
    answer = chat_text(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        max_tokens=300,
    )
    print(f"ANSWER: {answer}")
    print(f"CITED:{best_id}")
    print("CONFIDENCE: high")
    return 0


def eval_set(docs_dir: Path) -> int:
    capstone_root = Path(__file__).resolve().parent.parent.parent
    gold_path = capstone_root / "eval" / "gold_questions.json"
    items = json.loads(gold_path.read_text(encoding="utf-8"))
    chunks = load_index(docs_dir)
    passed = 0

    for item in items:
        q = item["question"]
        top = retrieve(chunks, q)
        best_score = top[0][0] if top else 0.0
        best = top[0][1] if top else None
        prefix = item.get("expected_cite_prefix")

        if item.get("should_refuse"):
            if best_score < SIM_THRESHOLD:
                passed += 1
            continue

        if not prefix or not best:
            continue
        if prefix not in best["file"] and prefix not in best["id"]:
            continue
        must = [m for m in item.get("must_contain", []) if m]
        if not must or all(m.lower() in best["text"].lower() for m in must):
            passed += 1

    total = len(items)
    print(f"EVAL:{passed}/{total}")
    return 0 if passed >= 4 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Doc Assistant — mini-RAG capstone")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index")
    p_index.add_argument("--docs", default="./data")

    p_ask = sub.add_parser("ask")
    p_ask.add_argument("--docs", default="./data")
    p_ask.add_argument("--question", required=True)

    p_eval = sub.add_parser("eval")
    p_eval.add_argument("--docs", default="./data")

    args = parser.parse_args()
    if args.command == "index":
        n_docs, n_chunks = build_index(Path(args.docs))
        print(f"INDEX_OK:docs={n_docs}:chunks={n_chunks}")
        if not is_mock_mode() and n_chunks:
            dim = len(load_index(Path(args.docs))[0]["embedding"])
            print(f"EMBED_INDEX_OK:chunks={n_chunks}:dim={dim}")
        sys.exit(0)
    if args.command == "ask":
        sys.exit(ask(Path(args.docs), args.question))
    if args.command == "eval":
        sys.exit(eval_set(Path(args.docs)))


if __name__ == "__main__":
    main()
