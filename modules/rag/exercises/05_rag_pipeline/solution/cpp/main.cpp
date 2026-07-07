#include "codam_llm.hpp"
#include <iostream>
#include <string>

int main() {
    std::string ctx = "The answer is 42";
    std::string content = "rag pipeline context: " + ctx;
    nlohmann::json messages = nlohmann::json::array({{{"role", "user"}, {"content", content}}});
    std::cout << codam::chat_completion(messages) << "\n";
    return 0;
}
