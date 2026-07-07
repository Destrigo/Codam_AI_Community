#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "First"}},
        {{"role", "assistant"}, {"content", "Received first"}},
        {{"role", "user"}, {"content", "Second"}},
        {{"role", "user"}, {"content", "How many user messages are in the history?"}},
    });
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
