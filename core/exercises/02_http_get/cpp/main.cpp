#include <httplib.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <string>

int main() {
    httplib::Client cli("jsonplaceholder.typicode.com");
    cli.set_connection_timeout(15, 0);
    auto res = cli.Get("/todos/1");
    if (!res || res->status != 200) {
        return 1;
    }
    auto data = nlohmann::json::parse(res->body);
    std::cout << data.at("title").get<std::string>() << "\n";
    return 0;
}
