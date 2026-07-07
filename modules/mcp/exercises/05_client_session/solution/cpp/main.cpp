#include <httplib.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <string>

static std::string mcp_base() {
    const char* env = std::getenv("CODAM_LABS_MCP_BASE");
    return env ? std::string(env) : "http://127.0.0.1:8765/mcp";
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
    return {u.substr(start, path - start), u.substr(path)};
}

int main() {
    auto [host, prefix] = parse_url(mcp_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(15, 0);
    auto res = cli.Post(prefix + "/initialize", "{}", "application/json");
    if (!res || res->status != 200) return 1;
    auto session = nlohmann::json::parse(res->body).at("session_id").get<std::string>();
    std::cout << "SESSION_OK:" << session << "\n";
    return 0;
}
