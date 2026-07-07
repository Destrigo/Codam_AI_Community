#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "retry invalid json"}},
    });
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
