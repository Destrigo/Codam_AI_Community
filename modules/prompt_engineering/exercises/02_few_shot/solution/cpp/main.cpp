#include "codam_llm.hpp"
#include <iostream>
#include <string>

int main() {
    std::string prompt = "Example 1: hi -> friendly\nExample 2: bye -> friendly\nClassify: hello";
    nlohmann::json messages = nlohmann::json::array({{{"role", "user"}, {"content", prompt}}});
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
