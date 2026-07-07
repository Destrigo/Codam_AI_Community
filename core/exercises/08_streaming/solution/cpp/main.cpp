#include "codam_llm.hpp"
#include <iostream>

int main() {
    nlohmann::json messages = nlohmann::json::array({{{"role", "user"}, {"content", "hello"}}});
    std::cout << codam::chat_stream(messages);
    return 0;
}
