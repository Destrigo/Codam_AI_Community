#include <httplib.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <string>

static std::string echo_url() {
    const char* env = std::getenv("CODAM_LABS_ECHO_URL");
    return env ? std::string(env) : "https://httpbin.org/post";
}

static std::pair<std::string, std::string> parse_url(const std::string& url) {
    size_t scheme = url.find("://");
    size_t start = scheme == std::string::npos ? 0 : scheme + 3;
    size_t path = url.find('/', start);
    if (path == std::string::npos) {
        return {url.substr(start), "/"};
    }
    return {url.substr(start, path - start), url.substr(path)};
}

int main() {
    auto [host, path] = parse_url(echo_url());
    httplib::Client cli(host);
    cli.set_connection_timeout(15, 0);
    nlohmann::json payload = {{"name", "codam"}};
    auto res = cli.Post(path, payload.dump(), "application/json");
    if (!res || res->status != 200) {
        return 1;
    }
    auto data = nlohmann::json::parse(res->body);
    std::string name = data.at("json").at("name").get<std::string>();
    std::cout << "ECHO_OK:" << name << "\n";
    return 0;
}
