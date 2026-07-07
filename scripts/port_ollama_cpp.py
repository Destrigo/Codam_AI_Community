"""Port Ollama module solutions to C++."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PARSE_URL = r'''
static std::pair<std::string, std::string> parse_url(const std::string& url) {
    std::string u = url;
    while (!u.empty() && u.back() == '/') u.pop_back();
    size_t scheme = u.find("://");
    size_t start = scheme == std::string::npos ? 0 : scheme + 3;
    size_t path = u.find('/', start);
    if (path == std::string::npos) {
        return {u.substr(start), ""};
    }
    return {u.substr(start), u.substr(path)};
}
'''

OLLAMA_BASE = r'''
static std::string ollama_base() {
    const char* env = std::getenv("CODAM_LABS_OLLAMA_BASE");
    return env ? std::string(env) : "http://localhost:11434";
}
'''

INCLUDES = """#include <httplib.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
"""


def http_cpp(main: str) -> str:
    return INCLUDES + OLLAMA_BASE + PARSE_URL + main


CPP: dict[str, str] = {
    "ollama/01_check_version": http_cpp("""
int main() {
    auto [host, prefix] = parse_url(ollama_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(15, 0);
    auto res = cli.Get(prefix + "/api/version");
    if (!res || res->status != 200) return 1;
    auto version = nlohmann::json::parse(res->body).at("version").get<std::string>();
    std::cout << "OLLAMA_OK:" << version << "\\n";
    return 0;
}
"""),
    "ollama/02_list_models": http_cpp("""
int main() {
    auto [host, prefix] = parse_url(ollama_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(15, 0);
    auto res = cli.Get(prefix + "/api/tags");
    if (!res || res->status != 200) return 1;
    auto models = nlohmann::json::parse(res->body).at("models");
    std::cout << "MODELS_OK:" << models.size() << "\\n";
    return 0;
}
"""),
    "ollama/03_chat": http_cpp("""
int main() {
    auto [host, prefix] = parse_url(ollama_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(60, 0);
    nlohmann::json payload = nlohmann::json::parse(
        R"({"model":"llama3.2","messages":[{"role":"user","content":"ollama chat hello"}],"stream":false})");
    auto res = cli.Post(prefix + "/api/chat", payload.dump(), "application/json");
    if (!res || res->status != 200) return 1;
    std::cout << nlohmann::json::parse(res->body).at("message").at("content").get<std::string>() << "\\n";
    return 0;
}
"""),
    "ollama/04_model_env": '''#include "codam_config.hpp"
#include <iostream>

int main() {
    std::string model = codam::getenv_or("OLLAMA_MODEL", "llama3.2");
    std::cout << "MODEL_OK:" << model << "\\n";
    return 0;
}
''',
    "ollama/05_stream_chat": http_cpp("""
int main() {
    auto [host, prefix] = parse_url(ollama_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(60, 0);
    nlohmann::json payload = nlohmann::json::parse(
        R"({"model":"llama3.2","messages":[{"role":"user","content":"ollama stream hello"}],"stream":true})");
    auto res = cli.Post(prefix + "/api/chat", payload.dump(), "application/json");
    if (!res || res->status != 200) return 1;
    std::string out;
    std::istringstream stream(res->body);
    std::string line;
    while (std::getline(stream, line)) {
        if (line.empty()) continue;
        auto chunk = nlohmann::json::parse(line);
        if (chunk.contains("message") && chunk["message"].contains("content")) {
            out += chunk["message"]["content"].get<std::string>();
        }
    }
    std::cout << out << "\\n";
    return 0;
}
"""),
    "ollama/06_embeddings": http_cpp("""
int main() {
    auto [host, prefix] = parse_url(ollama_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(60, 0);
    nlohmann::json payload = {{"model", "nomic-embed-text"}, {"prompt", "codam ollama embed"}};
    auto res = cli.Post(prefix + "/api/embeddings", payload.dump(), "application/json");
    if (!res || res->status != 200) return 1;
    auto embedding = nlohmann::json::parse(res->body).at("embedding");
    std::cout << "EMBED_DIM:" << embedding.size() << "\\n";
    return 0;
}
"""),
}


def main() -> None:
    for slug, code in CPP.items():
        module, name = slug.split("/", 1)
        path = ROOT / "modules" / module / "exercises" / name / "solution" / "cpp" / "main.cpp"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code.strip() + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Done: {len(CPP)} C++ solutions.")


if __name__ == "__main__":
    main()
