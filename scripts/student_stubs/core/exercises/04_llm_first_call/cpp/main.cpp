#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <string>

static size_t write_callback(char* ptr, size_t size, size_t nmemb, void* userdata) {
    auto* buffer = static_cast<std::string*>(userdata);
    buffer->append(ptr, size * nmemb);
    return size * nmemb;
}

std::string chat_completion(const nlohmann::json& messages) {
    // TODO: implement
    return {};
}

int main() {
    nlohmann::json messages = nlohmann::json::array({
        {{"role", "user"}, {"content", "hello"}},
    });
    std::cout << chat_completion(messages) << "\n";
    return 0;
}
