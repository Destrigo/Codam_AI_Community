#include "codam_llm.hpp"
#include <iostream>
#include <regex>

nlohmann::json extract_json_block(const std::string& text) {
    std::regex fence(R"(```(?:json)?\s*(\{[\s\S]*?\})\s*```)");
    std::smatch match;
    if (std::regex_search(text, match, fence)) {
        return nlohmann::json::parse(match[1].str());
    }
    auto start = text.find('{');
    auto end = text.rfind('}');
    return nlohmann::json::parse(text.substr(start, end - start + 1));
}

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "Return JSON in markdown"}},
    });
    std::string response = codam::chat_completion(messages);
    auto data = extract_json_block(response);
    std::cout << "PARSED:name=" << data.at("name").get<std::string>() << "\n";
    std::cout << "PARSED:score=" << data.at("score").get<int>() << "\n";
    return 0;
}
