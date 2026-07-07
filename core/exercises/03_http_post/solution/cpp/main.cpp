#include <httplib.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <string>

int main() {
    httplib::Client cli("httpbin.org");
    cli.set_connection_timeout(15, 0);
    nlohmann::json payload = {{"name", "codam"}};
    auto res = cli.Post("/post", payload.dump(), "application/json");
    if (!res || res->status != 200) {
        return 1;
    }
    auto data = nlohmann::json::parse(res->body);
    std::string name = data.at("json").at("name").get<std::string>();
    std::cout << "ECHO_OK:" << name << "\n";
    return 0;
}
