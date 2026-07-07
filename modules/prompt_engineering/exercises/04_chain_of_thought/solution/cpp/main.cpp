#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "What is 2+2? Think step by step."}},
    });
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
