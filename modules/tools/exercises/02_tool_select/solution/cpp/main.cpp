#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "calculate 6*7"}},
    });
    nlohmann::json tools = nlohmann::json::array({
        {{"type", "function"}, {"function", {{"name", "calculator"}}}},
    });
    std::cout << codam::chat_completion(messages, -1, {{"tools", tools}}) << "\n";
    return 0;
}
