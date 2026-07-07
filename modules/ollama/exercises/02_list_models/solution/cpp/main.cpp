#include <httplib.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>

static std::string ollama_base() {
    const char* env = std::getenv("CODAM_LABS_OLLAMA_BASE");
    return env ? std::string(env) : "http://localhost:11434";
}

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

int main() {
    auto [host, prefix] = parse_url(ollama_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(15, 0);
    auto res = cli.Get(prefix + "/api/tags");
    if (!res || res->status != 200) return 1;
    auto models = nlohmann::json::parse(res->body).at("models");
    std::cout << "MODELS_OK:" << models.size() << "\n";
    return 0;
}
