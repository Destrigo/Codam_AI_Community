#include <httplib.h>
#include <nlohmann/json.hpp>
#include <iostream>

int main() {
    httplib::Client cli("jsonplaceholder.typicode.com");
    cli.set_connection_timeout(15, 0);
    auto res = cli.Get("/todos/1");
    if (!res || res->status != 200) return 1;
    std::string title = nlohmann::json::parse(res->body).at("title").get<std::string>();
    std::cout << "FETCH_OK:" << title << "\n";
    return 0;
}
