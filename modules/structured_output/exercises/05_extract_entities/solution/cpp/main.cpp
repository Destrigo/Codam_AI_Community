#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "extract entities from: Marco signed on Monday"}},
    });
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
