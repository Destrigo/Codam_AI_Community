#include <iostream>
#include <regex>
#include <string>

int main() {
    std::string code = R"(api_key = "sk-test123456789")";
    if (std::regex_search(code, std::regex(R"(sk-[A-Za-z0-9_-]+)"))) {
        std::cout << "SECRET_SCAN_OK\n";
    }
    return 0;
}
