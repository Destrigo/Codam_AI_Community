#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({{{"role", "user"}, {"content", "hello"}}});
    std::cout << codam::chat_completion(messages, 5) << "\n";
    return 0;
}
