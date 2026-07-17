"""Minimal Mistral-compatible mock server for offline verification."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class _MockHandler(BaseHTTPRequestHandler):
    fail_count = 0
    fail_until = 2

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b"{}"
        return json.loads(body.decode("utf-8") or "{}")

    def _send_json(self, payload: dict, status: int = 200) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _handle_fail_twice(self) -> None:
        _MockHandler.fail_count += 1
        if _MockHandler.fail_count <= _MockHandler.fail_until:
            self._send_json({"error": "temporary"}, status=503)
            return
        self._send_json({"status": "ok"})

    def _chat_content(self, req: dict, user: str, system: str, messages: list) -> str:
        tools = req.get("tools") or []
        ul = user.lower()
        sl = system.lower()

        if "uppercase" in sl:
            return user.upper() if user else "HELLO"
        if "json" in ul and "markdown" in ul:
            return 'Here is the result:\n```json\n{"name": "codam", "score": 42}\n```'
        if "history" in ul or len(messages) >= 4:
            return f"HISTORY_OK:{len(messages)}"
        if req.get("max_tokens") is not None and req.get("max_tokens") <= 5:
            return "TOKEN_LIMIT_OK"
        if "example 1:" in ul:
            return "FEW_SHOT_OK"
        if "json only" in ul:
            return '{"label":"positive"} JSON_LABEL_OK'
        if "think step by step" in ul:
            return "COT_OK: 4"
        if "code reviewer" in sl:
            return "ROLE_OK: looks fine"
        if "positive or negative" in ul:
            return "SPECIFIC_OK: positive"
        if "retry invalid json" in ul:
            return '{"ok":true} RETRY_JSON_OK'
        if "classify category" in ul:
            return "CLASS:bug"
        if "extract entities" in ul:
            return "ENTITY:name=Marco"
        if "rag pipeline" in ul:
            return "RAG_ANSWER:42"
        if "cite chunk" in ul:
            return "CITED:chunk_1"
        if tools and "search docs" in ul:
            return "ROUTER:search"
        if tools and "calculate" in ul:
            return "TOOL_CALL:calculator"
        if "agent two tools" in ul:
            return "AGENT_TOOLS_OK"
        if "local llm" in ul:
            return "LOCAL_OK"
        if "critique revise" in ul:
            return "REVISED_OK"
        if "mcp bridge" in ul:
            return "MCP_BRIDGE_OK"
        if "ollama chat" in ul:
            return "OLLAMA_CHAT_OK"
        if "ollama stream" in ul:
            return "OLLAMA_STREAM_OK"
        return f"MOCK_RESPONSE:{user or 'hello'}"

    def do_GET(self) -> None:
        if self.path.endswith("/fail_twice"):
            self._handle_fail_twice()
            return
        if "/mcp/tools" in self.path:
            self._send_json({"tools": [{"name": "search"}, {"name": "calculator"}]})
            return
        if "/mcp/resources/" in self.path:
            self._send_json({"content": "RESOURCE_OK: policy v1"})
            return
        if self.path.endswith("/api/version"):
            self._send_json({"version": "0.5.7-mock"})
            return
        if self.path.endswith("/api/tags"):
            self._send_json({
                "models": [
                    {"name": "llama3.2:latest"},
                    {"name": "nomic-embed-text:latest"},
                ],
            })
            return
        # jsonplaceholder-compatible todo (02_http_get, tools/05_fetch_url)
        if self.path.rstrip("/").endswith("/todos/1") or self.path.endswith("/todo"):
            self._send_json({
                "userId": 1,
                "id": 1,
                "title": "delectus aut autem",
                "completed": False,
            })
            return
        self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        if self.path.endswith("/fail_twice"):
            self._handle_fail_twice()
            return

        if self.path.endswith("/api/embeddings"):
            self._send_json({"embedding": [0.1, 0.2, 0.3]})
            return

        if self.path.endswith("/v1/embeddings") or self.path == "/embeddings":
            self._send_json({
                "data": [{"embedding": [0.1, 0.2, 0.3], "index": 0}],
                "model": "mistral-embed",
            })
            return

        if self.path.endswith("/fail_twice"):
            self._handle_fail_twice()
            return

        if self.path.endswith("/echo"):
            req = self._read_json()
            self._send_json({"json": req})
            return

        if "/mcp/call" in self.path:
            self._send_json({"result": "MCP_CALL_OK:search"})
            return

        if "/mcp/initialize" in self.path:
            self._send_json({"session_id": "mock-session-1", "protocol": "2024-11-05"})
            return

        if self.path.endswith("/api/chat"):
            req = self._read_json()
            messages = req.get("messages", [])
            user = next((m["content"] for m in messages if m.get("role") == "user"), "")
            content = self._chat_content(req, user, "", messages)
            if req.get("stream"):
                self.send_response(200)
                self.send_header("Content-Type", "application/x-ndjson")
                self.end_headers()
                for word in content.split():
                    chunk = {"message": {"role": "assistant", "content": word + " "}, "done": False}
                    self.wfile.write((json.dumps(chunk) + "\n").encode("utf-8"))
                self.wfile.write((json.dumps({"done": True}) + "\n").encode("utf-8"))
                return
            self._send_json({
                "model": req.get("model", "llama3.2"),
                "message": {"role": "assistant", "content": content},
                "done": True,
            })
            return

        if not self.path.endswith("/chat/completions"):
            self._send_json({"error": "not found"}, status=404)
            return

        req = self._read_json()
        messages = req.get("messages", [])
        stream = bool(req.get("stream"))
        system = next((m["content"] for m in messages if m.get("role") == "system"), "")
        user = next((m["content"] for m in messages if m.get("role") == "user"), "")
        content = self._chat_content(req, user, system, messages)

        if stream:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            for chunk in content.split():
                payload = {"choices": [{"delta": {"content": chunk + " "}, "index": 0}]}
                self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode("utf-8"))
            self.wfile.write(b"data: [DONE]\n\n")
            return

        self._send_json({
            "choices": [{"message": {"role": "assistant", "content": content.strip()}, "index": 0}],
            "model": req.get("model", "mock-model"),
        })


def start_mock_server(port: int = 0) -> ThreadingHTTPServer:
    _MockHandler.fail_count = 0
    server = ThreadingHTTPServer(("127.0.0.1", port), _MockHandler)
    server.allow_reuse_address = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def mock_api_base(server: ThreadingHTTPServer) -> str:
    host, port = server.server_address[:2]
    return f"http://{host}:{port}/v1"
