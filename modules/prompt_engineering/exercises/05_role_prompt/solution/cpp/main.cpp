#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "system"}, {"content", "You are a code reviewer"}},
        {{"role", "user"}, {"content", "Review: print(1)"}},
    });
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
