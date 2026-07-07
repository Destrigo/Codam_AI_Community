#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "system"}, {"content", "Always respond in UPPERCASE"}},
        {{"role", "user"}, {"content", "hello"}},
    });
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
