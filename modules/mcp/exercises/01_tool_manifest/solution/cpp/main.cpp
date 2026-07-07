#include <nlohmann/json.hpp>
#include <iostream>

int main() {
    nlohmann::json manifest = {{"tools", nlohmann::json::array({{{"name", "search"}}, {{"name", "calculator"}}})}};
    auto tools = manifest.at("tools");
    for (const auto& t : tools) {
        if (t.at("name").get<std::string>() == "search") {
            std::cout << "MANIFEST_OK:" << tools.size() << "\n";
            return 0;
        }
    }
    return 1;
}
