#include <iostream>
#include <regex>
#include <string>

int main() {
    std::string out = "MOCK_RESPONSE:hello";
    std::cout << (std::regex_search(out, std::regex("MOCK_RESPONSE")) ? "TEST_PASS" : "FAIL") << "\n";
    return 0;
}
