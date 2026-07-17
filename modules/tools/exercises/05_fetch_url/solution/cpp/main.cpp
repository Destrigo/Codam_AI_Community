#include <httplib.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <string>

static std::string todo_url() {
    const char* env = std::getenv("CODAM_LABS_TODO_URL");
    return env ? std::string(env) : "https://jsonplaceholder.typicode.com/todos/1";
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
    auto [host, path] = parse_url(todo_url());
    httplib::Client cli(host);
    cli.set_connection_timeout(15, 0);
    auto res = cli.Get(path);
    if (!res || res->status != 200) return 1;
    std::string title = nlohmann::json::parse(res->body).at("title").get<std::string>();
    std::cout << "FETCH_OK:" << title << "\n";
    return 0;
}
