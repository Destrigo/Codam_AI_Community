#include <nlohmann/json.hpp>
#include <iostream>
#include <string>

int main() {
    std::string raw = R"(Result: {"label":"positive"})";
    size_t start = raw.find('{');
    size_t end = raw.rfind('}');
    auto data = nlohmann::json::parse(raw.substr(start, end - start + 1));
    std::cout << "EXTRACT_OK:" << data.at("label").get<std::string>() << "\n";
    return 0;
}
